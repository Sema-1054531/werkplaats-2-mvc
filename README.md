# Informatie

Een CRUD app maken voor TEST-CORRECT (Het Vragen-hospitaal) 

De app is geschreven in Python en daarop de web-framework Flask. De front-end is gebouwd met Bootstrap en scss, het is gemakkelijk te gebruiken html en css ook javascript als front-end library te gebruiken. Als database maken we gebruik van [SQLite](https://www.sqlite.org/index.html) 

Voorbeelden

Pagina 1

Pagina 2

etc..

# Vereisten

~~Gebruiker moet kunnen registreren~~
- [x] De styling moet aansluiten bij de test-correct huisstijl
- [x] Geautoriseerde gebruikers moeten kunnen inloggen
- [x] Dashboard overzicht menu waarin de overige problemen worden beschreven
- [ ] Redacteur wil na het lezen van de vraag een opzoeklijst en deze kunnen wijzigen
- [ ] Vragen waarin HTML onzichtbare codes meegeeft zoals "br" en "&nbsp" en deze wijzigen
- [ ] De gehele vraag moet zichtbaar zijn. auteur en leerdoel als <b>tekst</b> niet als <b>id</b>
- [ ] Als een vraag wordt getoond, zet de waarde van het ID op het scherm en maak daar een hyperlink van 
https://www.test-correct.nl/?vraag={{ id }}
- [ ] Bij een vraag zou je een "terug naar lijst" knop willen zien 
- [ ] En na het bijwerken van een vraag zou je ook hier terug naar deze lijst springen
- [ ] Gebruikers met "beheer permissies" kan gebruikersnamen en wachtwoorden instellen (<b>should-have</b>)
- [ ] 

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
