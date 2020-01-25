# Afvalwijzer
Generate ICAL for the waste collection days listed on [https://www.mijnafvalwijzer.nl/]()


###### Getting started:
1. Install the requirements from `requirements.txt` by running `pip install -r requirements.txt`.
2. Create a file `settings.py` and put two lines in it:
```
postcode=<your postcode>
huisnummer=<your house number>
```
2. Run `python3 afval.py`
3. The script generates a file `afvalkalender.ics`. Use it in your calendar application.
