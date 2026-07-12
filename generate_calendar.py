import requests
from icalendar import Calendar, Event
from datetime import datetime, timezone

SOURCE_URL = "https://www.google.com/calendar/ical/ct240d39oc9kq21cq3bn70jii8%40group.calendar.google.com/public/basic.ics"

response = requests.get(SOURCE_URL)
response.raise_for_status()

source_calendar = Calendar.from_ical(response.text)

output = Calendar()
output.add("prodid", "-//All Blacks Calendar//EN")
output.add("version", "2.0")
output.add("X-WR-CALNAME", "All Blacks Fixtures")

count = 0

excluded_terms = [
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

    # Exclude other NZ teams
    if any(term in event_text for term in excluded_terms):
        continue

    # Remove past events
    start = component.get("dtstart")

    if not start:
        continue

    event_date = start.dt

    if isinstance(event_date, datetime):
        if event_date < datetime.now(timezone.utc):
            continue

    # Clean title
    clean_summary = summary

    for prefix in ["NC:", "C:", "NZ:"]:
        clean_summary = clean_summary.replace(prefix, "").strip()

    event = Event()

    event.add("uid", component.get("uid"))
    event.add("summary", clean_summary)

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
