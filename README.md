# Informatie

Een CRUD app maken voor TEST-CORRECT (Het Vragen-hospitaal) 

De app is geschreven in Python en daarop de web-framework Flask. De front-end is gebouwd met Bootstrap en scss, het is gemakkelijk te gebruiken html en css ook javascript als front-end library te gebruiken. Als database maken we gebruik van [SQLite](https://www.sqlite.org/index.html) 

Voorbeelden

Pagina 1

Pagina 2

etc..

# Vereisten

~~Gebruiker moet kunnen registreren~~
- [ ] De interface en styling moet aansluiten bij test-correct huisstijl
- [x] Geautoriseerde gebruikers moeten kunnen inloggen
- [x] Dashboard overzicht menu waar gebruikers een keuze voor één van de eerder beschreven problemen kunnen maken
- [ ] Er zijn vragen die geen of een ongeldig leerdoel hebben
- [ ] Vragen waarin HTML onzichtbare codes meegeeft zoals "break line" en "&nbsp" en deze kunnen wijzigen
- [ ] De gehele vraag moet zichtbaar zijn. auteur en leerdoel als <b>tekst</b> niet als <b>id</b>
- [ ] Als een vraag wordt getoond, zet de waarde van het ID op het scherm en maak daar een hyperlink van
- [ ] Bij een vraag zou je een "terug naar lijst" knop willen zien, en na het bijwerken terug springen naar deze lijst
- [ ] gebruikers en hun wachtwoorden te kunnen instellen allen met "beheer permissies" (<b>should-have</b>)
- [ ] Sommige kolommen hebben lege waardes waar dat niet mag, er staan waardes in een kolom die leeg zou moeten zijn
- [ ] Sommige kolommen moeten converteerbaar zijn naar een datatype, maar hebben waardes waarbij dat niet kan
- [ ] Redacteuren willen alle rijen zien waarvan een kolom tussen bepaalde waardes valt


# werkplaats2_starter
Starter repository voor Werkplaats 2. Deze repository bevat een Flask applicatie met een aantal van de componenten die we ook nodig hebben om de werkplaats opdracht uit te voeren: 
- Een database
- Templates
- De Flask server
- HTML & Style sheets

# Installatie en setup
Om Flask te kunnen starten zul je eerst de Flask packages moeten installeren. Wil je latere problemen met versies voorkomen, dan raden we je aan een virtual environment te maken en daar de modules in te 
installeren:  

```
pip install virtualenv

virtualenv venv

.\venv\sripts\activate

pip install -r requirements.txt

```
Om de demo applicatie te starten: 
``` 

.\venv\sripts\activate

python app.py
```

# Gebruikte software
- Python
- Flask
- Bootstrap
- Html
- Css

# Credits

Nadir, Martijn, Romius, Thijs, Sema

Overige links hieronder license, copyright etc.
