# Informatie

Een CRUD app maken voor TEST-CORRECT (Het Vragen-hospitaal) 

De app is geschreven in Python en daarop de web-framework Flask. Voor de front-end gebruiken we bootstrap, het is eenvoudig te gebruiken als front-end library. Als database maken we gebruik van [SQLite](https://www.sqlite.org/index.html) dit is een relationeel databasebeheersystem. 

Voorbeelden

Pagina 1

Pagina 2

etc..

# Vereisten

~~Gebruiker moet kunnen registreren~~
- [ ] De interface en styling moet aansluiten bij test-correct huisstijl
- [x] Geautoriseerde gebruikers moeten kunnen inloggen
- [x] Dashboard overzicht menu waar de gebruiker de keuze kan maken voor de eerder benoemde problemen
- [ ] Redacteur wilt na het lezen van een vraag een opzoeklijst naar de juiste item kunnen kiezen, wijzigen en opslaan
- [ ] Vragen waarin HTML onzichtbare codes meegeeft zoals "break line" en "&nbsp" en deze kunnen wijzigen
- [ ] De gehele vraag moet zichtbaar zijn. auteur en leerdoel als <b>tekst</b> niet als <b>id</b>
- [ ] Als een vraag wordt getoond, zet de waarde van het ID op het scherm en maak daar een hyperlink van
- [ ] Bij een vraag zou je een "terug naar lijst" knop willen zien, en na het bijwerken terug springen naar deze lijst
- [ ] Sommige kolommen hebben lege waardes waar dat niet mag, en ook waardes die leeg moeten zijn
- [ ] Sommige kolommen moeten converteerbaar zijn naar een datatype, maar hebben waardes waarbij dat niet kan
- [ ] Redacteuren willen alle rijen zien waarvan een kolom tussen bepaalde waardes valt
- [ ] CSV-export van alle probleemgevallen dus kies een tabel, column, en dan alle cases met het "<b>ID veld</b>"
- [ ] Gebruikers met "beheer permissies" kunnen de gebruikersnamen en wachtwoorden instellen (<b>should-have</b>)


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
