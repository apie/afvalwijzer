#!/usr/bin/env python3
#Haal eerstvolgende ophaaldag op
#Genereer ICAL met deze dagen.
#By Apie 25-01-2020
#MIT

import requests
from bs4 import BeautifulSoup
from icalendar import Event, Calendar
from datetime import timedelta, datetime
from os import path
from sys import argv
import pytz
import dateparser

from settings import postcode, huisnummer

timezone = 'Europe/Amsterdam'


def lees_website():
    response = requests.get(f'https://www.mijnafvalwijzer.nl/nl/{postcode}/{huisnummer}/')
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'lxml')
    afvalkal = []
    for t in ("pmd", "gft", "papier", "restafval"):
        for e in soup.find_all(class_=t):
            date_str, waste_type = e.text.strip().split('\n')
            if date_str.lower() == t:
                continue  # Not a date
            date = dateparser.parse(date_str, settings={'TIMEZONE': timezone, 'RETURN_AS_TIMEZONE_AWARE': True})
            afvalkal.append((date, waste_type))

    return afvalkal


def schrijf_ical(afvalkal):
    cal = Calendar()
    cal.add('prodid', f'-//Afvalkalender//Voor {postcode} {huisnummer}//')
    cal.add('version', '2.0')
  
    now = datetime.now(pytz.timezone(timezone))
    for date, waste_type in sorted(afvalkal):
        event = Event()
        event.add('summary', f'Afvalkalender {waste_type}')
        event.add('dtstart', date+timedelta(seconds=60*60*7)) # 07:00
        event.add('dtend',   date+timedelta(seconds=60*60*9)) # 09:00
        event.add('dtstamp', now) 
        cal.add_component(event)

    with open(path.join(path.dirname(path.realpath(argv[0])),'afvalkalender.ics'), 'wb') as f:
        f.write(cal.to_ical())


if __name__ == "__main__":
    schrijf_ical(lees_website())
