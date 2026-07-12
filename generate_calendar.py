import requests
from icalendar import Calendar, Event
from datetime import datetime, timezone
import uuid

SOURCE_URL = "https://www.google.com/calendar/ical/ct240d39oc9kq21cq3bn70jii8%40group.calendar.google.com/public/basic.ics"

response = requests.get(SOURCE_URL)
response.raise_for_status()

source_calendar = Calendar.from_ical(response.text)

output = Calendar()
output.add("prodid", "-//All Blacks Calendar//EN")
output.add("version", "2.0")
output.add("X-WR-CALNAME", "All Blacks Fixtures")
output.add("X-WR-TIMEZONE", "Australia/Sydney")
output.add("CALSCALE", "GREGORIAN")

count = 0

excluded_terms = [
    "♀",
    "Women",
    "Women's",
    "Women’s",
    "Black Ferns",
    "Maori",
    "Māori",
    "All Blacks XV",
    "U20",
    "Under 20",
    "Sevens",
]

for component in source_calendar.walk():

    if component.name != "VEVENT":
        continue

    summary = str(component.get("summary", ""))
    description = str(component.get("description", ""))
    location = str(component.get("location", ""))

    event_text = summary + " " + description + " " + location

    if "New Zealand" not in summary:
        continue

    if any(term in event_text for term in excluded_terms):
        continue

    start = component.get("dtstart")

    if not start:
        continue

    event_date = start.dt

    # Remove past events
    if isinstance(event_date, datetime):
        if event_date.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
            continue
    else:
        if event_date < datetime.now().date():
            continue

    clean_summary = summary
    for prefix in ["NC:", "C:", "NZ:"]:
        clean_summary = clean_summary.replace(prefix, "").strip()

    event = Event()

    # Generate a fresh UID Google can track
    event.add("uid", str(uuid.uuid4()) + "@allblacks-calendar")

    event.add("summary", clean_summary)

    event.add("dtstart", component.get("dtstart").dt)

    if component.get("dtend"):
        event.add("dtend", component.get("dtend").dt)

    if location:
        event.add("location", location)

    event.add(
        "description",
        "All Blacks fixture"
    )

    output.add_component(event)

    count += 1


with open("allblacks.ics", "wb") as f:
    f.write(output.to_ical())


print(f"Created All Blacks calendar with {count} events")
