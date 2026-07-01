# Common Commands

Nachdem man models.py anpasst sollten folgende Befehle ausgeführt werden.
 
```
python manage.py makemigrations
python manage.py migrate
```


Zum Starten des Servers
```
python manage.py runserver
```

Zum Erweitern der Applikation
```
python manage.py startapp app_name
```

Requirements.txt generieren - installierte pip packages dokumentieren
```
pip freeze > requirements.txt
```

Requirements.txt benutzen, um fehlende pip packages zu installieren
```
pip install -r requirements.txt
```