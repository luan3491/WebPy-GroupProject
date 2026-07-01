# Common Commands

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

```
python manage.py makemigrations
python manage.py migrate
```

### SuperUser/Admin Account erstellen

```
python manage.py createsuperuser
```

### Starten des Servers

```
python manage.py runserver
```

### Zum Erweitern der Applikation

```
python manage.py startapp app_name
```

### Paketliste generieren

Requirements.txt generieren - installierte pip packages dokumentieren

```
pip freeze > requirements.txt
```

### Demo Daten generieren

python manage.py seed_demo_data
