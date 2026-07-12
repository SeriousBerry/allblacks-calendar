from datetime import datetime

calendar = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//All Blacks Calendar//EN
CALSCALE:GREGORIAN

BEGIN:VEVENT
UID:test@example.com
DTSTAMP:20260712T000000Z
DTSTART:20260718T090000Z
DTEND:20260718T110000Z
SUMMARY:All Blacks Automated Test
LOCATION:New Zealand
END:VEVENT

END:VCALENDAR
"""

with open("allblacks.ics", "w") as f:
    f.write(calendar)

print("Calendar updated")
