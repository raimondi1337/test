import csv
from datetime import datetime
import re
import json

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

db = {}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query_string = self.path.split("?", 1)[-1]
        query_parameters = parse_qs(query_string)

        if "datetime" in query_parameters:
            datetime_string = query_parameters["datetime"][0]

            try:
                parsed_datetime = datetime.strptime(
                    datetime_string, "%Y-%m-%d %H:%M:%S"
                )

                response_message = get_open_restaurants(parsed_datetime)
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                json_data = json.dumps(response_message, indent=2)
                self.wfile.write(json_data.encode("utf-8"))
            except ValueError:
                response_message = "Invalid datetime format"
                status_code = 400

                self.send_response(status_code)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(response_message.encode())
        else:
            self.send_response(400)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Missing datetime parameter")


def is_open_at_timestamp(restaurant, timestamp):
    day = timestamp.strftime("%a").lower()
    if day == "tue":
        day = "tues"
    print(day)

    if day in restaurant["hours"]:
        open_time = datetime.strptime(
            restaurant["hours"][day]["open"], "%I:%M %p"
        ).replace(year=timestamp.year, month=timestamp.month, day=timestamp.day)
        close_time = datetime.strptime(
            restaurant["hours"][day]["close"], "%I:%M %p"
        ).replace(year=timestamp.year, month=timestamp.month, day=timestamp.day)
        print(open_time, timestamp, close_time)
        return open_time <= timestamp <= close_time

    return False


def get_open_restaurants(timestamp):
    return [
        restaurant["name"]
        for restaurant in db
        if is_open_at_timestamp(restaurant, timestamp)
    ]


def expand_days(start, end):
    output = []
    weekdays = [
        "mon",
        "tues",
        "wed",
        "thu",
        "fri",
        "sat",
        "sun",
    ]
    weekdays = weekdays[weekdays.index(start) :] + weekdays[: weekdays.index(end)]
    return ",".join(weekdays[: weekdays.index(end) + 1])


def replace_days(match):
    start = match.group(1)
    end = match.group(2)
    return expand_days(start, end)


def ingest_data():
    with open("./data.csv", "r") as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        output = []

        # get evertyhing before the hours numerals
        # get groups on either side of a hyphen
        # replace hyphen groups with csv
        # get everything that comes after the first time
        days_pattern = re.compile(r"^(.*?)(?=\d)")
        hyphen_days_pattern = re.compile(r"\b([A-Za-z]+)\s*-\s*([A-Za-z]+)\b")
        sub_time_pattern = re.compile(r"(?<!:)\b(\d+)\b(?!:)")
        times_pattern = re.compile(r"\d.*m")

        for row in csv_reader:
            restaurant = {"name": row[0], "hours": {}}
            if "/" in row[1]:
                row[1] = row[1].lower().split("/")
            else:
                row[1] = [row[1].lower()]

            for item in row[1]:
                match_days = days_pattern.search(item).group().strip(" ,")
                match_times = times_pattern.search(item).group().strip(" ,")
                days = re.sub(hyphen_days_pattern, replace_days, match_days)
                match_times = re.sub(sub_time_pattern, r"\1:00", match_times)
                match_times = match_times.split(" - ")
                for d in days.split(","):
                    restaurant["hours"][d] = {
                        "open": match_times[0],
                        "close": match_times[1],
                    }
            output.append(restaurant)
    return output


def run(server_class=HTTPServer, handler_class=Handler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}")
    httpd.serve_forever()


if __name__ == "__main__":
    db = ingest_data()
    run()
