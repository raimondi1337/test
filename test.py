from urllib.request import urlopen
from urllib.parse import quote
import json

import unittest
from datetime import datetime


class TestTimestamp(unittest.TestCase):
    base_url = "http://localhost:8000/"

    def test_wednesday_morning(self):
        time = "2024-02-14 09:00:00"
        expected = ["Tupelo Honey"]

        url = self.base_url + "?datetime=" + quote(time)
        response = json.loads(urlopen(url).read().decode("utf-8"))
        self.assertEqual(response, expected)

    # def test_tuesday_noon(self):
    #     time = "2024-02-13 12:00:00"
    #     # expected = ["Tupelo Honey"]

    #     url = self.base_url + "?datetime=" + quote(time)
    #     response = json.loads(urlopen(url).read().decode("utf-8"))
    #     print(response)
    #     # self.assertEqual(response, expected)

    # def test_sunday_noon(self):
    #     time = "2024-02-12 12:00:00"
    #     # expected = ["Tupelo Honey"]

    #     url = self.base_url + "?datetime=" + quote(time)
    #     response = json.loads(urlopen(url).read().decode("utf-8"))
    #     print(response)
    #     # self.assertEqual(response, expected)

    # def test_friday_night(self):
    #     time = "2024-02-16 21:00:00"
    #     # expected = ["Tupelo Honey"]

    #     url = self.base_url + "?datetime=" + quote(time)
    #     response = json.loads(urlopen(url).read().decode("utf-8"))
    #     print(response)
    #     # self.assertEqual(response, expected)


if __name__ == "__main__":
    unittest.main()
