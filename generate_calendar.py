import requests
from icalendar import Calendar, Event
from datetime import datetime, timezone
import uuid
import re

SOURCE_URL = "https://www.google.com/calendar/ical/ct240d39oc9kq21cq3bn70jii8%40group.calendar.google.com/public/basic.ics"

response = requests.get(SOURCE_URL)
response.raise_for_status()

source_calendar = Calendar.from_ical(response.text)

output = Calendar()
output.add("prodid", "-//All Blacks Calendar//EN")
output.add("version", "2.0")
output.add("X-WR-CALNAME", "All Blacks Fixtures")
output.add("CALSCALE", "GREGORIAN")

count = 0

# Keep matches from 1 January 2025 onwards
cutoff_date = datetime(2025, 1, 1, tzinfo=timezone.utc)

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

    # Only New Zealand senior men's fixtures
    if "New Zealand" not in summary:
        continue

    # Exclude women's rugby and other New Zealand teams
    if any(term in event_text for term in excluded_terms):
        continue

    # Get event start date
    start = component.get("dtstart")

    if not start:
        continue

    event_date = start.dt

    # Keep only events from 1 January 2025 onwards
    if isinstance(event_date, datetime):

        if event_date.tzinfo is None:
            event_date = event_date.replace(tzinfo=timezone.utc)

        if event_date < cutoff_date:
            continue

    else:

        if event_date < cutoff_date.date():
            continue

    # Clean the event title
    clean_summary = summary

    # Remove prefixes such as NC:, C:, and NZ:
    for prefix in ["NC:", "C:", "NZ:"]:
        clean_summary = clean_summary.replace(prefix, "").strip()

    # Remove scores from completed matches
    # Example:
    # New Zealand 🇳🇿 40 v 21 ☘️ Ireland
    # becomes:
    # New Zealand 🇳🇿 v ☘️ Ireland
    clean_summary = re.sub(
        r"\s+\d+\s+v\s+\d+\s+",
        " v ",
        clean_summary
    )

    event = Event()

    # Use a stable UID so Google Calendar recognises the same match
    original_uid = str(component.get("uid", ""))
    event.add("uid", original_uid + "@allblacks-calendar")

    event.add("summary", clean_summary)

    if component.get("dtstart"):
        event.add("dtstart", component.get("dtstart").dt)

    if component.get("dtend"):
        event.add("dtend", component.get("dtend").dt)

    if location:
        event.add("location", location)

    event.add("description", "All Blacks fixture")

    output.add_component(event)

    count += 1


with open("allblacks.ics", "wb") as f:
    f.write(output.to_ical())


print(f"Created All Blacks calendar with {count} events")
