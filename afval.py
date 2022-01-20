#!/usr/bin/env python3
# Haal eerstvolgende ophaaldag op
# Genereer ICAL met deze dagen.
# By Apie 25-01-2020
# MIT

import requests
from icalendar import Event, Calendar
from datetime import timedelta, datetime
from os import path
from sys import argv
import pytz
import dateparser

from settings import postcode, huisnummer, apikey

timezone = "Europe/Amsterdam"


def lees_json():
    url = f"https://api.mijnafvalwijzer.nl/webservices/appsinput/?apikey={apikey}&method=postcodecheck&postcode={postcode}&street=&huisnummer={huisnummer}&toevoeging=&platform=phone&langs=nl&mobiletype=android&version=58&app_name=afvalwijzer"
    response = requests.get(url)
    response.raise_for_status()
    pickupdates = response.json()["data"]["ophaaldagen"]["data"]
    return map(
        lambda d: (
            dateparser.parse(
                d["date"],
                settings={"TIMEZONE": timezone, "RETURN_AS_TIMEZONE_AWARE": True},
            ),
            d["type"],
        ),
        pickupdates,
    )


def schrijf_ical(afvalkal):
    cal = Calendar()
    cal.add("prodid", f"-//Afvalkalender//Voor {postcode} {huisnummer}//")
    cal.add("version", "2.0")

    now = datetime.now(pytz.timezone(timezone))
    for date, waste_type in sorted(afvalkal):
        event = Event()
        event.add("summary", f"Afvalkalender {waste_type.capitalize()}")
        event.add("dtstart", date + timedelta(seconds=60 * 60 * 7))  # 07:00
        event.add("dtend", date + timedelta(seconds=60 * 60 * 9))  # 09:00
        event.add("dtstamp", now)
        cal.add_component(event)

    with open(
        path.join(path.dirname(path.realpath(argv[0])), "afvalkalender.ics"), "wb"
    ) as f:
        f.write(cal.to_ical())


if __name__ == "__main__":
    schrijf_ical(lees_json())
