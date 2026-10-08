#!/usr/bin/env python3
# Vygeneruje tasks.json - zdroj pravdy pre kalendar Kamiony.
# Pravidla:
#  - povinne bloky len PO az PI
#  - sobota: len volitelne doplnkove ulohy, v nazve "(volitelne)" -> v texte "(voliteľné)"
#  - nedela: nikdy
#  - ziadne bloky v dnoch s Baska / Orava / Bratislava
#  - respektovat jeho existujuce udalosti (Byt 8-18, Mackulin Zilina od 10:00)
import datetime as dt, json, sys
D = dt.date

# ---- jeho existujuce zavazky (z Apple Kalendara, kalendare Praca/Sukromny) ----
# cele dni bez prace na kamionoch (Orava s Baskou)
VOLNO = {D(2026,10,15), D(2026,10,16), D(2026,10,17), D(2026,10,18)}
# obsadene casti dna: datum -> [(od, do), ...]
OBSADENE = {
    D(2026,10,12): [("08:00","18:00")],   # Byt, Masarykova
    D(2026,10,13): [("10:00","23:59")],   # Mackulin Zilina
    D(2026,10,14): [("08:00","18:00")],   # Byt
    D(2026,10,15): [("08:00","18:00")],   # Byt + Orava
}
SVIATKY = {D(2026,11,17), D(2026,12,24), D(2026,12,25), D(2026,12,26),
           D(2027,1,1), D(2027,1,6)}

# ---- texty ----
FIRMY = ("BOJKUN, Protrans SK, IMP Transport, Target Group, Autodoprava Kočiš, "
         "NESATRANS, TRIPARK, Osif Peter, PM EXPRES")
PITCH = ("Hlavná veta: Umyjem vaše autá priamo u vás za pevnú cenu za kus, takže vaši "
         "ľudia môžu robiť svoju prácu namiesto umývania.")
OBH = ("Pri obhliadke zisti: voda (prípojka, tlak), tlakový stroj a typ koncovky, "
       "odlučovač ropných látok, osvetlenie, kedy sú autá v depe, koľko áut a akého typu.")
SKUSKA = ("Skúška zadarmo (2 až 3 vozidlá).\n"
 "- Vezmi: aktívnu penu, odmasťovač, čistič diskov, penový nadstavec, kefy, rebrík, mikrovlákna, vedrá, ochranné pomôcky.\n"
 "- Pred začatím: fotky každého auta zo všetkých strán (aj existujúce poškodenia!).\n"
 "- Stopni čas na každom aute zvlášť.\n"
 "- Riedenie peny: postrekovač 1:100 leto / 1:50 zima, penový nadstavec 1:5 leto / 1:3 zima, oplach 120 až 150 bar.\n"
 "- Po umytí fotky po, podpis dispečera.\n- Prestávka 15 min v polovici.")
UMY = ("Pravidelné umývanie u zákazníkov.\n"
 "- Presný čas si dohodni so zákazníkom: kamióny bývajú v depe v piatok poobede alebo skoro ráno.\n"
 "- Deň vopred skontroluj zoznam vozidiel, chémiu a palivo.\n"
 "- Fotky pred a po, zápis ŠPZ a času.\n- Podpis dispečera na zozname.\n"
 "- Prestávka 15 min v polovici, pi vodu.\n- Doma: zapíš počet áut a spotrebu chémie.")
PREHLAD = ("Týždenný prehľad a administratíva.\n- Čo vyšlo, čo nie.\n"
 "- Čísla: počet návštev, skúšok, umytých áut, tržby, náklady.\n"
 "- Doplň tabuľku firiem, odpíš na e-maily, odlož doklady.\n"
 "- Poznač, čo presunúť na budúci týždeň.")
PLAN = ("Plán týždňa (30 min).\n- Pozri úlohy týždňa v pláne.\n"
 "- Dohodni telefonicky termíny návštev a skúšok.\n- Skontroluj zásoby chémie a palivo.")
VOL = "\n\nToto je doplnková úloha. Ak si s Baškou alebo si unavený, pokojne ju vynechaj alebo presuň."

ev = []
def a(d, s, e, t, desc):
    ev.append({"date": d.isoformat(), "start": s, "end": e, "title": t, "desc": desc})

def po_pi(mon): return [mon + dt.timedelta(i) for i in range(5)]

# ================= OKTÓBER =================
# T1: piatok 9.10 + sobota 10.10
a(D(2026,10,9), "10:00","12:00","Nácvik predajného rozhovoru",
  f"{PITCH}\n- Nauč sa 3 argumenty: platený čas vodiča (smernica 2002/15/ES), žiadny odklon na umyváreň, čisté auto ako vizitka.\n"
  "- Odpovede na námietky: Máme to vyriešené -> skúška zadarmo. Je to drahé -> porovnaj s cenou umyvárne (súprava 34 až 38 € bez DPH) plus čas vodiča.\n"
  "- Nacvič nahlas aspoň 5x, nahraj sa na mobil.")
a(D(2026,10,9), "12:15","13:45","Jednostranová ponuka s cenníkom",
  "Vytvor 1 stranu na vytlačenie (Canva alebo Word).\n- Kto si, čo ponúkaš, ako to funguje (u nich, na ich umývacom mieste).\n"
  "- Cenník: dodávka 10 €, ťahač 12 €, súprava 18 až 22 €, interiér +10 až 15 €, ložná plocha +8 až 12 €.\n"
  "- Skúška 2 až 3 vozidiel zadarmo.\n- Telefón, e-mail. Vytlač 15 ks.")
a(D(2026,10,9), "14:30","16:00","Dokončiť mapovanie a tabuľku firiem",
  f"Dokonči firmy skupiny A, na ktoré nezostal čas: {FIRMY}.\n"
  "- Pre každú: areál, umývacie miesto a odlučovač áno/nie, počet kamiónov a dodávok, kontakt na dispečera.\n"
  "- Kontakty z webu firmy, finstat.sk, orsr.sk. Zapisuj do tabuľky v iCloud Drive/Kamiony.")
a(D(2026,10,10),"09:00","12:00","Obhliadka areálov autom (voliteľné)",
  "Prejdi okolo 3 až 4 najbližších areálov zo zoznamu.\n- Pozri z cesty umývacie miesto, koľko áut stojí.\n"
  "- Nevstupuj bez dovolenia, len pozoruj.\n- Doplň do tabuľky." + VOL)

# T2: 12.-16.10 - Byt po/st/st, Mackulin ut, Orava od st 15.10
a(D(2026,10,12),"18:30","20:00","Plán týždňa a VZN mesta Michalovce",
  PLAN + "\n\nVečerný blok, lebo cez deň máš Byt.\n"
  "Na michalovce.sk nájdi VZN o odpadových vodách a verejnom poriadku.\n"
  "- Zapíš, čo platí pre umývanie na súkromnom areáli s odlučovačom.\n- Priprav otázky na úrad.")
a(D(2026,10,13),"08:00","09:30","Telefonáty: úrad, účtovníčka, poisťovne",
  "Ráno pred odchodom do Žiliny.\n- Okresný úrad Michalovce, odbor starostlivosti o životné prostredie (štátna vodná správa): dohodni stretnutie.\n"
  "- Nájdi 2 až 3 účtovníčky v MI, dohodni konzultáciu.\n"
  "- Zavolaj 3 poisťovne: poistenie zodpovednosti za škodu, ktoré výslovne kryje škody na vozidlách zákazníka.")
a(D(2026,10,14),"18:30","20:00","Poisťovne: žiadosti o ponuku e-mailom",
  "Večerný blok, lebo cez deň máš Byt.\nPošli e-mailom žiadosť o ponuku 3 poisťovniam.\n"
  "- Činnosť: mobilné umývanie nákladných vozidiel u zákazníka.\n"
  "- Krytie: škody na cudzích vozidlách (prevzaté veci), limit, spoluúčasť, ročná cena.")
# 15.-18.10 Orava - nic

# T3: 19.-23.10
m = po_pi(D(2026,10,19))
a(m[0],"09:00","09:30","Plán týždňa",PLAN)
a(m[0],"09:30","11:00","Telefonáty a dohadovanie návštev",
  "Zavolaj firmám zo skupiny A a dohodni krátke stretnutie (10 min) na utorok až štvrtok.")
a(m[0],"13:00","14:30","Okresný úrad Michalovce",
  "Otázky:\n- Potrebujem povolenie, ak umývam na umývacom mieste zákazníka s odlučovačom?\n"
  "- Kto zodpovedá za odpadovú vodu, ja alebo prevádzkovateľ miesta?\n- Čo ak firma nemá odlučovač?\n"
  "- Aká chémia je povolená (Kärcher RM 812 / RM 81 do odlučovača)?\nZapíš meno úradníka a odpovede.")
a(m[1],"09:30","11:30","Návšteva firmy 1 a 2",
  f"Osobne u dispečera alebo majiteľa. Neprichádzaj pred 9:00.\n- Otázka: Kto a kde vám dnes umýva autá?\n- {PITCH}\n- {OBH}\n"
  "- Nechaj ponuku. Pri záujme dohodni skúšku na začiatok novembra.")
a(m[1],"13:00","14:30","Návšteva firmy 3", f"{PITCH}\n{OBH}\n- Zapíš výsledok do tabuľky.")
a(m[2],"09:30","11:30","Návšteva firmy 4 a 5", f"{PITCH}\n{OBH}")
a(m[2],"13:00","14:30","Konzultácia s účtovníčkou",
  "Otázky:\n- Pod aký predmet živnosti patrí umývanie vozidiel?\n- Paušálne výdavky alebo skutočné?\n"
  "- Odvody: sociálne prvý rok, zdravotné ako denný študent vs. externý.\n"
  "- DPH hranica a čo ak zákazník chce faktúru s DPH.\n- Koľko stojí jej služba mesačne.")
a(m[3],"09:30","11:30","Návšteva firmy 6 a 7", f"{PITCH}\n{OBH}")
a(m[3],"13:00","14:30","Obhliadka umývacieho miesta",
  f"U firmy so záujmom.\n{OBH}\n- Odfoť umývacie miesto a koncovku stroja (kvôli penovému nadstavcu).")
a(m[4],"09:00","11:30","Vzor zmluvy",
  "Priprav vzor zmluvy o poskytovaní služieb:\n- Rozsah (čo sa umýva), cenník za kus.\n"
  "- Kto dodáva vodu a stroj (zákazník) a kto chémiu a náradie (ty).\n- Odpadová voda do odlučovača zákazníka.\n"
  "- Zodpovednosť za škody, odkaz na poistenie.\n- Fakturácia mesačne, splatnosť 14 dní.\n"
  "- Výpovedná lehota 1 mesiac.\n- Bezpečnosť práce v areáli.\nDaj si ju skontrolovať.")
a(m[4],"13:00","14:00","Týždenný prehľad",PREHLAD)
a(D(2026,10,24),"09:00","10:30","Fotky a jednoduchá prezentácia (voliteľné)",
  "Priprav si jednoduchú vizitku a stránku na Facebooku alebo Instagrame.\n"
  "- Názov, telefón, čo robíš, kde pôsobíš.\n- 3 až 5 fotiek, aj keď zatiaľ len z obhliadok." + VOL)

# T4: 26.-30.10
m = po_pi(D(2026,10,26))
a(m[0],"09:00","09:30","Plán týždňa",PLAN)
a(m[0],"09:30","11:30","Posledné návštevy firiem", f"Cieľ: 3 firmy so súhlasom na skúšku.\n{PITCH}")
a(m[1],"09:00","10:30","Ohlásenie živnosti",
  "Priprav ohlásenie živnosti cez slovensko.sk (občiansky s čipom) alebo na jednotnom kontaktnom mieste Okresného úradu MI.\n"
  "- Predmet podnikania podľa rady účtovníčky.\n- Podaj hneď, ako je isté, že peniaze prídu. Živnosť musíš mať pred prvou platenou prácou.")
a(m[1],"13:00","14:30","Doplnková návšteva firmy", f"Ak ešte nemáš 3 skúšky.\n{PITCH}")
a(m[2],"09:00","11:00","Poistenie, fakturácia, účet",
  "- Vyber poistenie (krytie škôd na vozidlách zákazníka!), začiatok najneskôr k prvej skúške.\n"
  "- Vyber fakturačnú aplikáciu (SuperFaktúra, iDoklad), nastav šablónu.\n- Založ osobitný bankový účet na podnikanie.")
a(m[3],"09:00","10:30","Objednať vizitky, tabule, tričko",
  "- Vizitky 100 ks.\n- Magnetické tabule na Octaviu s názvom a telefónom.\n"
  "- Pracovné tričko alebo mikina s nápisom.\n- Dodanie zvyčajne do týždňa. Rozpočet 60 až 150 €.")
a(m[4],"09:00","10:30","Potvrdiť termíny skúšok",
  "Zavolaj 3 firmám a potvrď presný deň a hodinu skúšky.\n- Spýtaj sa, ktoré 2 až 3 autá budú k dispozícii.\n- Pošli SMS alebo e-mail s potvrdením.")
a(m[4],"13:00","14:00","Týždenný prehľad",PREHLAD)
a(D(2026,10,31),"09:00","10:00","Kontrola tabuľky firiem (voliteľné)",
  "Prejdi tabuľku, doplň chýbajúce kontakty a stavy. Označ firmy, ktoré treba ešte raz osloviť." + VOL)

# T5: 2.-6.11
m = po_pi(D(2026,11,2))
a(m[0],"09:00","09:30","Plán týždňa",PLAN)
a(m[0],"09:30","11:30","Nákup chémie a náradia",
  "Keď prídu peniaze, objednaj (minimum okolo 760 €):\n"
  "- Aktívna pena Tenzi Truck Clean 20 l, odmasťovač Kärcher RM 81 20 l, čistič diskov a skiel.\n"
  "- Penový nadstavec podľa koncovky zákazníka, teleskopické kefy, kefa na disky.\n"
  "- Rebrík alebo plošina, mikrovlákna, vedrá.\n- Gumáky, nepremokavé oblečenie, rukavice, okuliare.\n"
  "Aktivuj poistenie. Ak peniaze ešte nie sú, posuň skúšky o pár dní.")
a(m[1],"10:00","12:00","Príprava výbavy",
  "- Skontroluj, čo prišlo.\n- Priprav box s chémiou a náradím do auta alebo prívesu.\n"
  "- Napíš si checklist, čo brať na každý výjazd.\n- Odmeraj si riedenie chémie.")
a(m[2],"08:00","12:00","Skúška u firmy 1",SKUSKA)
a(m[3],"09:00","10:30","Ponuka pre firmu 1",
  "- Spracuj fotky pred a po.\n- Zapíš namerané časy.\n- Pošli ponuku s cenou za kus a fotkami do 2 dní od skúšky.\n"
  "- Zavolaj dispečerovi, či boli spokojní.")
a(m[3],"13:00","14:00","Administratíva",
  "- Zapíš náklady na nákup, bločky a faktúry odlož pre účtovníčku.\n- Skontroluj, či je živnosť zapísaná (zrsr.sk).")
a(m[4],"08:00","12:00","Skúška u firmy 2",SKUSKA)
a(m[4],"13:00","14:00","Týždenný prehľad",PREHLAD)
a(D(2026,11,7),"09:00","10:00","Údržba a kontrola výbavy (voliteľné)",
  "Umy a usuš kefy a mikrovlákna, skontroluj zásoby chémie, doplň, čo chýba." + VOL)

# T6: 9.-13.11
m = po_pi(D(2026,11,9))
a(m[0],"09:00","09:30","Plán týždňa",PLAN)
a(m[0],"09:30","11:00","Ponuka pre firmu 2","Fotky, namerané časy, ponuka s cenou za kus do 2 dní od skúšky.")
a(m[1],"08:00","12:00","Skúška u firmy 3",SKUSKA)
a(m[2],"09:00","11:00","Úprava cenníka",
  "Vzorec: cena za kus = hodinová sadzba (20 €) × čas + chémia + doprava.\n- Dosaď namerané časy zo skúšok.\n"
  "- Minimálne 5 vozidiel na výjazd alebo paušál za výjazd okolo 15 €.\n- Extrémne znečistené +30 %.")
a(m[3],"09:30","11:00","Stretnutie: zmluva s firmou 1",
  "- Vezmi 2 vytlačené zmluvy.\n- Dohodni pravidelný deň umývania, zoznam vozidiel, kontakt na dispečera.\n- Podpis.")
a(m[3],"13:00","14:30","Ponuka pre firmu 3","Ponuka po skúške, aktualizuj tabuľku firiem.")
a(m[4],"08:00","12:00","Umývanie: prvý platený výjazd",
  UMY + "\nAk ešte nemáš zmluvu, použi čas na follow-up telefonáty.")
a(m[4],"13:00","14:00","Týždenný prehľad",PREHLAD)
a(D(2026,11,14),"09:00","10:00","Fotky pred a po: archív (voliteľné)",
  "Roztrieď fotky z umývania do priečinkov podľa firmy a dátumu. Vyber najlepšie dvojice pred/po pre ponuky a investora." + VOL)

# T7: 16.-20.11 (17.11 sviatok)
m = po_pi(D(2026,11,16))
a(m[0],"09:00","09:30","Plán týždňa",PLAN + "\nUtorok 17. 11. je sviatok, voľno.")
a(m[0],"09:30","11:00","Follow-up firmy 2 a 3",
  "Zavolaj, ako sa rozhodli. Pri súhlase dohodni stretnutie na podpis zmluvy.")
a(m[2],"09:30","11:00","Stretnutie: zmluva s firmou 2","Vezmi zmluvy, dohodni pravidelný deň a zoznam vozidiel.")
a(m[3],"09:00","10:30","Náklady na jedno auto",
  "Spočítaj skutočné náklady: chémia na auto, palivo na výjazd, čas.\nPorovnaj s cenníkom a uprav, ak treba.")
a(m[4],"08:00","12:00","Umývanie",UMY)
a(m[4],"13:00","14:00","Týždenný prehľad",PREHLAD)
a(D(2026,11,21),"09:00","10:00","Čítanie: chémia a technika (voliteľné)",
  "Prečítaj si technické listy k chémii, ktorú používaš, a pozri 2 až 3 videá o umývaní kamiónov. Zapíš, čo vyskúšaš." + VOL)

# T8: 23.-27.11
m = po_pi(D(2026,11,23))
a(m[0],"09:00","09:30","Plán týždňa",PLAN)
a(m[0],"09:30","11:30","Nové firmy do 40 km",
  "Nájdi firmy v Trebišove, Sobranciach a Humennom (dopravcovia, stavebné firmy, kuriéri, autobusy).\n"
  "Doplň do tabuľky, dohodni návštevy na utorok a stredu.")
a(m[1],"09:00","12:00","Návštevy: Trebišov a Sobrance", f"{PITCH}\n{OBH}")
a(m[2],"09:00","12:00","Návštevy: Humenné", f"{PITCH}\n{OBH}")
a(m[3],"09:00","10:30","Prevádzkovateľ elektrobusov v MI",
  "Zisti, kto bude prevádzkovať 9 nových elektrických autobusov mestskej dopravy (web mesta, vestník verejného obstarávania).\n"
  "Priprav pre neho ponuku na čistý interiér a exteriér.")
a(m[4],"08:00","12:00","Umývanie",UMY)
a(m[4],"13:00","14:00","Týždenný prehľad",PREHLAD)
a(D(2026,11,28),"09:00","10:00","Hľadanie nových firiem online (voliteľné)",
  "Pozri finstat.sk a mapy: dopravcovia a firmy s vozovým parkom do 40 km od Michaloviec. Doplň 5 nových do tabuľky." + VOL)

# T9: 30.11-4.12
m = po_pi(D(2026,11,30))
a(m[0],"09:00","10:30","Prvá mesačná faktúra",
  "- Vystav faktúru každému zákazníkovi za november so zoznamom vozidiel (ŠPZ, dátum, cena).\n"
  "- Splatnosť 14 dní.\n- Pošli e-mailom, kópiu odlož pre účtovníčku.")
a(m[0],"10:45","11:15","Plán týždňa",PLAN)
a(m[1],"09:30","10:30","Požiadať o odporúčanie",
  "Spýtaj sa spokojného zákazníka, či pozná inú firmu, ktorej by ťa odporučil. Ideálne poprosiť o telefonát alebo kontakt.")
a(m[2],"09:00","11:00","Mesačná bilancia",
  "Tržby, náklady (chémia, palivo, poistenie), hodiny, zisk na hodinu.\nZapíš do tabuľky, budú sa hodiť pre investora.")
a(m[3],"09:30","11:30","Návštevy nových firiem",PITCH)
a(m[4],"08:00","12:00","Umývanie",UMY)
a(m[4],"13:00","14:00","Týždenný prehľad",PREHLAD)
a(D(2026,12,5),"09:00","10:00","Údržba výbavy a zásoby (voliteľné)",
  "Skontroluj kefy, hadice a nadstavce, doplň chémiu na ďalší mesiac." + VOL)

# T10-T11: 7.-11.12 a 14.-18.12
for mon, sob in [(D(2026,12,7), D(2026,12,12)), (D(2026,12,14), D(2026,12,19))]:
    m = po_pi(mon)
    a(m[0],"09:00","09:30","Plán týždňa",PLAN)
    a(m[0],"09:30","11:00","Telefonáty: nové firmy z odporúčaní","Dohodni skúšky u 2 nových firiem.")
    a(m[2],"08:00","12:00","Skúška u novej firmy",SKUSKA)
    a(m[3],"09:00","10:30","Ponuka a follow-up",
      "Ponuka po skúške do 2 dní. Ponúkni aj umývanie pred Vianocami, dopravcovia sú vyťažení.")
    a(m[4],"08:00","12:00","Umývanie",UMY)
    a(m[4],"13:00","14:00","Čísla a fotky pre investora",
      "Zbieraj: zmluvy, počet umytých áut, tržby, najlepšie fotky pred a po, reakcie zákazníkov.")
a(D(2026,12,12),"09:00","10:00","Referencie od zákazníkov (voliteľné)",
  "Poproś dispečerov o krátku vetu, ako sú spokojní. Zapíš si ju aj s menom firmy, pôjde do podkladov pre investora." + VOL)
a(D(2026,12,19),"09:00","10:00","Príprava na vianočnú špičku (voliteľné)",
  "Skontroluj zásoby chémie a stav výbavy pred týždňom 21. 12. Dohodni si, ktoré autá sa umyjú 22. 12." + VOL)

# Vianočný týždeň 21.-23.12 (24.-26.12 sviatky)
a(D(2026,12,21),"09:00","09:30","Plán týždňa (sviatky)",
  "Tento týždeň len stáli zákazníci. 24. až 26. 12. voľno.")
a(D(2026,12,22),"08:00","12:00","Umývanie pred Vianocami",UMY)
a(D(2026,12,23),"09:00","10:00","Vianočné poďakovanie zákazníkom",
  "Pošli krátku SMS alebo e-mail s poďakovaním a želaním. Udrží ťa to v hlave u dispečerov.")

# Týždeň 28.-31.12 (1.1 sviatok)
a(D(2026,12,28),"09:00","09:30","Plán týždňa",PLAN)
a(D(2026,12,29),"08:00","12:00","Umývanie",UMY)
a(D(2026,12,30),"09:00","10:30","Faktúra za december","Faktúry za december so zoznamami vozidiel. Pošli e-mailom.")
a(D(2026,12,31),"10:00","11:30","Ročné podklady a ciele na január",
  "- Všetky doklady pre účtovníčku do jednej zložky.\n- Pozri sa späť na plán, čo vyšlo.\n"
  "- Cieľ na január: tretí pravidelný zákazník, udržať existujúcich počas skúšok.")
a(D(2027,1,2),"10:00","11:00","Ciele na rok 2027 (voliteľné)",
  "Napíš si 3 ciele na rok: počet zákazníkov, mesačné tržby, technika. Krátko, na jednu stranu." + VOL)

# JANUÁR (skúškové obdobie CEVRO)
a(D(2027,1,4),"09:00","10:00","Termíny skúšok CEVRO do kalendára",
  "Zapíš si termíny skúšok a umývanie plánuj mimo nich.\nPočas skúškového len stáli zákazníci, nové firmy neotváraj.")
a(D(2027,1,4),"10:15","11:00","Plán týždňa",PLAN)
a(D(2027,1,7),"09:30","11:00","Tretí zákazník: follow-up",
  "Zavolaj firmám po decembrových skúškach. Cieľ: tretia zmluva do 31. 1.")
a(D(2027,1,8),"08:00","12:00","Umývanie",UMY)
a(D(2027,1,9),"09:00","10:00","Údržba výbavy (voliteľné)",
  "Zimná kontrola: hadice, nadstavce, riedenie chémie 1:50 a 1:3 na zimu." + VOL)
for mon, sob in [(D(2027,1,11), D(2027,1,16)), (D(2027,1,18), D(2027,1,23)), (D(2027,1,25), D(2027,1,30))]:
    m = po_pi(mon)
    a(m[0],"09:00","09:30","Plán týždňa",PLAN + "\nSkúškové obdobie: len stáli zákazníci.")
    a(m[4],"08:00","12:00","Umývanie",UMY)
a(D(2027,1,20),"09:30","11:00","Tretí zákazník: podpis zmluvy",
  "Ak firma súhlasí, podpis zmluvy, pravidelný termín, zoznam vozidiel.")
a(D(2027,1,27),"09:00","10:30","Rozhodnutie: externé štúdium",
  "Pred rozhodnutím sa spýtaj účtovníčky a zdravotnej poisťovne:\n"
  "- Ako denný študent do 26 rokov máš pravdepodobne zdravotné poistenie platené štátom.\n"
  "- Ako externý si ho zrejme platíš sám ako SZČO.\nSpočítaj, či sa to oplatí.")
a(D(2027,1,28),"09:00","10:30","Faktúra za január a bilancia",
  "Faktúry za január. Mesačná bilancia: tržby, náklady, hodiny, zisk na hodinu.")
a(D(2027,1,16),"09:00","10:00","Fotky a referencie (voliteľné)",
  "Doplň fotoalbum pred a po, zapíš nové referencie od dispečerov." + VOL)
a(D(2027,1,23),"09:00","10:00","Hľadanie nových firiem (voliteľné)",
  "Priprav si zoznam 5 firiem na oslovenie vo februári, po skúškovom období." + VOL)
a(D(2027,1,30),"09:00","10:00","Údržba výbavy (voliteľné)",
  "Kontrola a doplnenie chémie, príprava na február." + VOL)

# FEBRUÁR
for mon in [D(2027,2,1), D(2027,2,8), D(2027,2,15), D(2027,2,22)]:
    m = po_pi(mon)
    a(m[0],"09:00","09:30","Plán týždňa",PLAN)
    a(m[4],"08:00","12:00","Umývanie",UMY)
a(D(2027,2,3),"09:00","11:30","Podklady pre investora (1/2)",
  "Jedna strana:\n- Čo robíš a pre koho, zmluvy so zákazníkmi.\n"
  "- Mesačné tržby december a január, náklady, zisk.\n- Fotky pred a po.")
a(D(2027,2,10),"09:00","11:30","Podklady pre investora (2/2)",
  "- Čo kúpiť: úsporná mobilná výbava 10 až 15 tis. € (použitý Kärcher HDS 1000 De a vozík alebo staršia dodávka).\n"
  "- Koľko nových zákazníkov to umožní (firmy bez umývacieho miesta).\n"
  "- Čo ponúkaš investorovi: podiel alebo pôžička.\nNacvič prezentáciu nahlas.")
a(D(2027,2,11),"09:00","10:00","SBA mikropôžička: overiť",
  "Na sba.sk over aktuálne podmienky mikropôžičky (výška, úrok, ručiteľ, odklad istiny) ako náhradný variant.")
a(D(2027,2,16),"09:00","09:30","Dohodnúť stretnutie s investorom",
  "Zavolaj investorovi a dohodni stretnutie na budúci týždeň.")
a(D(2027,2,24),"10:00","11:30","Stretnutie s investorom",
  "Vezmi jednostranový plán, zmluvy, čísla a fotky.\nUpresni termín podľa dohody s investorom.")
a(D(2027,2,26),"13:00","14:30","Faktúra za február a bilancia","Faktúry za február, mesačná bilancia.")
a(D(2027,2,6),"09:00","10:00","Nácvik prezentácie pre investora (voliteľné)",
  "Povedz nahlas, čo robíš, koľko zarábaš a čo potrebuješ. Do 3 minút. Nahraj sa na mobil." + VOL)
a(D(2027,2,13),"09:00","10:00","Fotoalbum pred a po (voliteľné)",
  "Vyber 10 najlepších dvojíc fotiek pred a po pre investora." + VOL)
a(D(2027,2,20),"09:00","10:00","Nácvik prezentácie (voliteľné)",
  "Druhý nácvik, tentoraz s číslami naspamäť." + VOL)

# ---- kontroly ----
def t2m(x):
    h, mi = x.split(":"); return int(h)*60+int(mi)

ev.sort(key=lambda r: (r["date"], r["start"]))
byday = {}
for i, r in enumerate(ev):
    d = dt.date.fromisoformat(r["date"])
    r["id"] = f"k{i+1:03d}"
    assert d.weekday() != 6, ("nedeľa", r)
    assert d not in SVIATKY, ("sviatok", r)
    assert d not in VOLNO, ("Baška/Orava", r)
    assert t2m(r["start"]) < t2m(r["end"]), ("čas", r)
    if d.weekday() == 5:
        assert "(voliteľné)" in r["title"], ("sobota musí byť voliteľná", r)
    else:
        assert "(voliteľné)" not in r["title"], ("voliteľné len v sobotu", r)
    for s, e in OBSADENE.get(d, []):
        assert t2m(r["end"]) <= t2m(s) or t2m(r["start"]) >= t2m(e), ("kolízia s Byt/Mackulin", r)
    byday.setdefault(d, []).append(r)

for d, rows in byday.items():
    for x, y in zip(rows, rows[1:]):
        assert t2m(x["end"]) <= t2m(y["start"]), ("prekryv blokov", x, y)
    tot = sum(t2m(r["end"]) - t2m(r["start"]) for r in rows)
    assert tot <= 9*60, ("priveľa práce v jeden deň", d, tot)

json.dump(ev, open(sys.argv[1], "w"), ensure_ascii=False, indent=1)
sob = sum(1 for r in ev if dt.date.fromisoformat(r["date"]).weekday() == 5)
print(f"blokov: {len(ev)}, z toho sobotných voliteľných: {sob}, dní: {len(byday)}")
