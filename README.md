# Common Commands

<<<<<<< Updated upstream
Nachdem man models.py anpasst sollten folgende Befehle ausgeführt werden.
 
=======
### Virtual Enviroment erstellen und benutzen

```
python -m venv .venv
.venv\Scripts\activate
```

### Fehlende Pakete installieren

Requirements.txt benutzen, um fehlende pip packages zu installieren

```
pip install -r requirements.txt
```

### Migrations

Nachdem man models.py anpasst sollten folgende Befehle ausgeführt werden.

>>>>>>> Stashed changes
```
python manage.py makemigrations
python manage.py migrate
```

<<<<<<< Updated upstream

Zum Starten des Servers
=======
### SuperUser/Admin Account erstellen

```
python manage.py createsuperuser
```

### Starten des Servers

>>>>>>> Stashed changes
```
python manage.py runserver
```

<<<<<<< Updated upstream
Zum Erweitern der Applikation
=======
### Zum Erweitern der Applikation

>>>>>>> Stashed changes
```
python manage.py startapp app_name
```

<<<<<<< Updated upstream
Requirements.txt generieren - installierte pip packages dokumentieren
```
pip freeze > requirements.txt
```

Requirements.txt benutzen, um fehlende pip packages zu installieren
```
pip install -r requirements.txt
```
=======
### Paketliste generieren

Requirements.txt generieren - installierte pip packages dokumentieren

```
pip freeze > requirements.txt
```
>>>>>>> Stashed changes
