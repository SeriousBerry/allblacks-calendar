import requests
from icalendar import Calendar, Event
import pytz
from datetime import datetime

SOURCE_URL = "https://www.google.com/calendar/ical/ct240d39oc9kq21cq3bn70jii8%40group.calendar.google.com/public/basic.ics"

SYDNEY = pytz.timezone("Australia/Sydney")

response = requests.get(SOURCE_URL)
response.raise_for_status()

source_calendar = Calendar.from_ical(response.text)

output = Calendar()
output.add("prodid", "-//All Blacks Calendar//EN")
output.add("version", "2.0")
output.add("X-WR-CALNAME", "All Blacks Fixtures")

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

    event.add("uid", component.get("uid"))
    event.add("summary", summary)

    if component.get("dtstart"):
        event.add("dtstart", component.get("dtstart").dt)

    if component.get("dtend"):
        event.add("dtend", component.get("dtend").dt)

    if component.get("location"):
        event.add("location", component.get("location"))

    if component.get("description"):
        event.add("description", component.get("description"))

    output.add_component(event)
    count += 1

with open("allblacks.ics", "wb") as f:
    f.write(output.to_ical())

print(f"Created All Blacks calendar with {count} events")
