# Kamióny – kalendár na odber

Harmonogram rozbehu mobilného umývania kamiónov (Michalovce).

Odber v Apple Kalendári: **Súbor → Nový odber kalendára** a vlož

```
webcal://raw.githubusercontent.com/vrabeldavid/kamiony-kalendar/main/kamiony.ics
```

- `tasks.json` – zoznam blokov (zdroj pravdy)
- `build_ics.py` – z `tasks.json` vyrobí `kamiony.ics` (stabilné UID, aby sa odber aktualizoval bez duplikátov)
- `plan.py` – pôvodné vygenerovanie plánu s kontrolami pravidiel
