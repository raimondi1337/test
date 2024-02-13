FROM python:3.9
WORKDIR /app
ADD . /app
EXPOSE 8000
ENV NAME World
CMD ["python3", "liine.py"]
# docker run -p 8000:8000 liine-test