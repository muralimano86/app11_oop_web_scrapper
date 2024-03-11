import requests
import selectorlib
import smtplib, ssl
import os
import sqlite3
import time

URL = "https://programmer100.pythonanywhere.com/tours/"


connection = sqlite3.connect("data.db")

def scrape(url):
    response = requests.get(url)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def send_email(message):
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


def store(rows):
    row = extracted.split(",")
    row = [item.strip() for item in row]

    cursor = connection.cursor()
    cursor.execute("insert into events values(?, ?, ?)", row)
    connection.commit()


def read(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    band, city, date = row

    cursor = connection.cursor()
    cursor.execute("Select * from events where band = ? and city = ? and date = ?",
                   (band, city, date))
    rows = cursor.fetchall()
    return rows


if __name__ == "__main__":
    while True:
        scrapped = scrape(URL)
        extracted = extract(scrapped)
        print(extracted)

        if extracted not in "No upcoming tours":
            in_db = read(extracted)
            if not in_db:
                store(extracted)
                send_email(message="Hey, new event was found!")

        time.sleep(2)
