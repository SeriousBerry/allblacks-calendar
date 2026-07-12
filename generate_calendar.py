import requests
from icalendar import Calendar, Event
from datetime import datetime
import pytz

SOURCE_URL = "PUT_MIKE_RIVERSDALE_URL_HERE"

SYDNEY = pytz.timezone("Australia/Sydney")

response = requests.get(SOURCE_URL)
response.raise_for_status()

source_calendar = Calendar.from_ical(response.text)

output = Calendar()
output.add("prodid", "-//All Blacks Calendar//EN")
output.add("version", "2.0")
output.add("X-WR-CALNAME", "All Blacks Tests")

count = 0

for component in source_calendar.walk():
    if component.name != "VEVENT":
        continue

    summary = str(component.get("summary", ""))

    # Keep only All Blacks matches
    if (
        "All Blacks" not in summary
        and "New Zealand" not in summary
    ):
        continue

    event = Event()

    for field in [
        "summary",
        "dtstart",
        "dtend",
        "description",
        "location",
        "uid",
    ]:
        if component.get(field):
            event.add(field, component.get(field))

    output.add_component(event)
    count += 1

with open("allblacks.ics", "wb") as f:
    f.write(output.to_ical())

print(f"Created calendar with {count} All Blacks events")
