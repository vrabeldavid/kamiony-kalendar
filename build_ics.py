#!/usr/bin/env python3
# tasks.json -> .ics  (stabilne UID, aby sa odber aktualizoval a nerobili sa duplikaty)
import datetime as dt, json, sys, uuid, os

NS = uuid.UUID("6f1b0c2e-9a44-5b31-a1d2-7e5c9f0b3a88")
src, out = sys.argv[1], sys.argv[2]
ev = json.load(open(src))

def esc(s):
    return (s.replace("\\", "\\\\").replace(";", "\\;")
             .replace(",", "\\,").replace("\n", "\\n"))

def fold(line):
    b = line.encode(); parts = []
    while len(b) > 75:
        cut = 75 if not parts else 74
        while (b[cut] & 0xC0) == 0x80: cut -= 1
        parts.append(b[:cut]); b = b[cut:]
    parts.append(b)
    return "\r\n ".join(p.decode() for p in parts)

stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
seq = int(os.environ.get("SEQ", "0"))

L = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Kamiony//Plan//SK",
     "CALSCALE:GREGORIAN", "METHOD:PUBLISH",
     "X-WR-CALNAME:Kamióny", "X-WR-TIMEZONE:Europe/Bratislava",
     "X-WR-CALDESC:Rozbeh mobilného umývania kamiónov. Pracovné bloky PO až PI\\, sobota len voliteľné\\, nedeľa voľno.",
     "REFRESH-INTERVAL;VALUE=DURATION:PT1H", "X-PUBLISHED-TTL:PT1H",
     "BEGIN:VTIMEZONE", "TZID:Europe/Bratislava",
     "BEGIN:DAYLIGHT", "TZOFFSETFROM:+0100", "TZOFFSETTO:+0200", "TZNAME:CEST",
     "DTSTART:19700329T020000", "RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU", "END:DAYLIGHT",
     "BEGIN:STANDARD", "TZOFFSETFROM:+0200", "TZOFFSETTO:+0100", "TZNAME:CET",
     "DTSTART:19701025T030000", "RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU", "END:STANDARD",
     "END:VTIMEZONE"]

for r in sorted(ev, key=lambda x: (x["date"], x["start"])):
    d = r["date"].replace("-", "")
    f = lambda t: d + "T" + t.replace(":", "") + "00"
    uid = uuid.uuid5(NS, r["id"])
    L += ["BEGIN:VEVENT", f"UID:{uid}@kamiony", f"DTSTAMP:{stamp}",
          f"SEQUENCE:{seq}", f"LAST-MODIFIED:{stamp}",
          f"DTSTART;TZID=Europe/Bratislava:{f(r['start'])}",
          f"DTEND;TZID=Europe/Bratislava:{f(r['end'])}",
          "SUMMARY:" + esc(("✓ " if r.get("done") else "") + r["title"]),
          "DESCRIPTION:" + esc(r["desc"]),
          "BEGIN:VALARM", "ACTION:DISPLAY", "DESCRIPTION:" + esc(r["title"]),
          "TRIGGER:-PT30M", "END:VALARM", "END:VEVENT"]
L.append("END:VCALENDAR")
open(out, "w", newline="").write("\r\n".join(fold(x) for x in L) + "\r\n")
print(f"{len(ev)} udalostí -> {out}")
