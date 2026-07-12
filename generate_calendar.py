from datetime import datetime

fixtures = [
    {
        "date": "2026-07-04 19:10",
        "opponent": "France",
        "venue": "Christchurch"
    },
    {
        "date": "2026-07-11 19:10",
        "opponent": "Italy",
        "venue": "Wellington"
    }
]

calendar = [
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    "PRODID:-//All Blacks Calendar//EN",
    "CALSCALE:GREGORIAN",
    "X-WR-CALNAME:All Blacks Tests"
]

for match in fixtures:
    dt = datetime.strptime(match["date"], "%Y-%m-%d %H:%M")
    start = dt.strftime("%Y%m%dT%H%M00")
    
    calendar.extend([
        "BEGIN:VEVENT",
        f"UID:{start}-{match['opponent'].replace(' ','')}@allblacks-calendar",
        f"DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}",
        f"DTSTART:{start}",
        f"SUMMARY:All Blacks v {match['opponent']}",
        f"LOCATION:{match['venue']}",
        "END:VEVENT"
    ])

calendar.append("END:VCALENDAR")

with open("allblacks.ics", "w") as f:
    f.write("\n".join(calendar))

print("All Blacks calendar generated")
