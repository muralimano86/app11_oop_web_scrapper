import requests
import selectorlib
import smtplib, ssl
import os
import sqlite3
import time

URL = "https://programmer100.pythonanywhere.com/tours/"


class Event:
    def scrape(self, url):
        response = requests.get(url)
        source = response.text
        return source

    def extract(self, source):
        extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
        value = extractor.extract(source)["tours"]
        return value


class Email:
    def send(self, message):
        host = "smtp.gmail.com"
        port = 465

        username = "muralimano86@gmail.com"
        password = os.getenv("GMAILPASSWORD")

        receiver = "muralimano86@gmail.com"
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(host, port, context=context) as server:
            server.login(username, password)
            server.sendmail(username, receiver, msg=message)

        print("Email was sent:")


class Database():
    def __init__(self, database_path):
        self.connection = sqlite3.connect(database_path)

    def store(self, rows):
        row = extracted.split(",")
        row = [item.strip() for item in row]

        cursor = self.connection.cursor()
        cursor.execute("insert into events values(?, ?, ?)", row)
        self.connection.commit()

    def read(self, extracted):
        row = extracted.split(",")
        row = [item.strip() for item in row]
        band, city, date = row

        cursor = self.connection.cursor()
        cursor.execute("Select * from events where band = ? and city = ? and date = ?",
                       (band, city, date))
        rows = cursor.fetchall()
        return rows


if __name__ == "__main__":
    while True:
        event = Event()
        scrapped = event.scrape(URL)
        extracted = event.extract(scrapped)
        print(extracted)

        if extracted not in "No upcoming tours":
            database = Database(database_path="data.db")
            in_db = database.read(extracted)
            if not in_db:
                database.store(extracted)
                email = Email()
                email.send(message="Hey, new event was found!")

        time.sleep(2)
