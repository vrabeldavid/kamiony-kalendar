"""Export selected tasks.json blocks into a standalone .ics for import into an existing Apple calendar.
Usage: python3 -I export_ics.py tasks.json out.ics id1 id2 ...  (or 'from:YYYY-MM-DD' to export all blocks from that date)
UIDs differ from the Kamióny subscription so the two never collide."""
import json, sys, uuid, datetime

src, out, *sel = sys.argv[1:]
t = json.load(open(src))
if sel and sel[0].startswith('from:'):
    start = sel[0][5:]
    bl = [b for b in t if b['date'] >= start]
else:
    bl = [b for b in t if b['id'] in sel]
NS = uuid.UUID('6f1c1b0e-6b4a-4c7e-9a43-7d2f0a1e5b21')
BS = chr(92)


def esc(s):
    return s.replace(BS, BS + BS).replace(';', BS + ';').replace(',', BS + ',').replace('\n', BS + 'n')


def fold(line):
    b = line.encode('utf-8')
    out = []
    while len(b) > 74:
        cut = 74
        while (b[cut] & 0xC0) == 0x80:
            cut -= 1
        out.append(b[:cut].decode())
        b = b' ' + b[cut:]
    out.append(b.decode())
    return '\r\n'.join(out)


now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
L = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Vydrhnute//plan//SK', 'CALSCALE:GREGORIAN', 'METHOD:PUBLISH',
     'BEGIN:VTIMEZONE', 'TZID:Europe/Bratislava', 'BEGIN:STANDARD', 'DTSTART:19701025T030000',
     'RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU', 'TZOFFSETFROM:+0200', 'TZOFFSETTO:+0100', 'TZNAME:CET', 'END:STANDARD',
     'BEGIN:DAYLIGHT', 'DTSTART:19700329T020000', 'RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU', 'TZOFFSETFROM:+0100',
     'TZOFFSETTO:+0200', 'TZNAME:CEST', 'END:DAYLIGHT', 'END:VTIMEZONE']
for b in sorted(bl, key=lambda b: (b['date'], b['start'])):
    d = b['date'].replace('-', '')
    title = ('✓ ' if b.get('done') else '') + b['title']
    L += ['BEGIN:VEVENT', f"UID:{uuid.uuid5(NS, 'vydrhnute-sk-' + b['id'])}@vydrhnute", f'DTSTAMP:{now}',
          f"DTSTART;TZID=Europe/Bratislava:{d}T{b['start'].replace(':', '')}00",
          f"DTEND;TZID=Europe/Bratislava:{d}T{b['end'].replace(':', '')}00",
          fold('SUMMARY:' + esc(title)), fold('DESCRIPTION:' + esc(b['desc'])), 'END:VEVENT']
L.append('END:VCALENDAR')
open(out, 'w', newline='').write('\r\n'.join(L) + '\r\n')
print(len(bl), 'udalostí ->', out)
