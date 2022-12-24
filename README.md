# Informatie

De applicatie is geschreven in Python en daarop de web-framework Flask. Voor de front-end gebruiken we bootstrap, het is eenvoudig te gebruiken als front-end library. Als database maken we gebruik van [SQLite](https://www.sqlite.org/index.html) dit is een relationeel databasebeheersystem. 

Om de redacteurs te helpen met verbeteren van de kwaliteit van de inhoud wil men een tool maken. Dit tool, eenwebapplicatie, zou aan de hand van bekende patronen vraag items moeten tonen waarzaken aan verbeterd moeten worden. Een soort “vragen hospitaal”.

Voorbeelden

Pagina 1

Pagina 2

etc..

# Vereisten

De gebruikers van dit platform zullen de redacteurs van de databank worden. We willen heneen platform bieden dat op basis van een aantal bekende patronen vraag items toont meteen probleem en de redacteur de mogelijkheid geeft deze te verbeteren of te exporteren.

De applicatie zou normaliter direct op de database in prikken, maar die is heel groot. Test-correct heeft voor ons een demo dataset met vragen en een beperkt aantal kolommenvoorbereid (zonder antwoorden en metadata) die de nu bekende problemen illustreren.

- [x] De interface en styling moet aansluiten bij test-correct huisstijl
- [x] Geautoriseerde gebruikers moeten kunnen inloggen 
- [x] Dashboard overzicht met de datatabellen van test-correct overzicht
- [x] Redacteur wilt na het lezen van een vraag een opzoeklijst naar de juiste item kunnen kiezen, wijzigen en opslaan
- [x] Vragen waarin HTML onzichtbare codes meegeeft zoals "break line" en "&nbsp" en deze kunnen wijzigen
- [x] De gehele vraag moet zichtbaar zijn. auteur en leerdoel als <b>tekst</b> niet als <b>id</b>
- [x] De redacteur moet de vraag direct kunnen verbeteren.
- [x] Bij een vraag zou je een "terug naar lijst" knop willen zien, en na het bijwerken terug springen naar deze lijst
- [x] vraag als “uitzondering” te markeren. Uitzonderingen hoeven niet meer getoond te worden in de overzichtslijst
- [ ] Gebruikers met "beheer permissies" kunnen de gebruikersnamen en wachtwoorden instellen (<b>should-have</b>)
- [ ] Maak een hyperlink van een vraag die als ID op het scherm ?vraag={{ id }}”. te zien krijgt
- [ ] Sommige kolommen hebben lege waardes waar dat niet mag, en ook waardes die leeg moeten zijn
- [ ] Sommige kolommen moeten converteerbaar zijn naar een datatype, maar hebben waardes waarbij dat niet kan
- [ ] CSV-export van alle probleemgevallen dus kies een tabel, column, en dan alle cases met het "<b>ID veld</b>"


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

python main.py
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
