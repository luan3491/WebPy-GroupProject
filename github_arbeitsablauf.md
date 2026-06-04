# GitHub-Arbeitsablauf für unser Gruppenprojekt

Diese kurze Anleitung erklärt, wie wir ab jetzt am Projekt arbeiten.
Der `main`-Branch ist geschützt. Das bedeutet: **Nicht direkt auf `main` arbeiten oder pushen.** Änderungen sollen über einen eigenen Branch und einen Pull Request in `main` kommen.

---

## 1. Projekt einmal herunterladen

Wenn du das Projekt noch nicht auf deinem PC hast:

```bash
git clone https://github.com/luan3491/WebPy-GroupProject.git
cd NAME_DES_PROJEKTORDNERS
```

Den Link bekommt man auf GitHub über **Code → HTTPS**.

---

## 2. Vor jeder Arbeit den aktuellen Stand holen

Bevor du anfängst, immer zuerst den aktuellen Stand von `main` holen:

```bash
git checkout main
git pull
```

So vermeidet man, auf einem alten Stand zu arbeiten.

---

## 3. Eigenen Branch erstellen

Für jede Aufgabe oder Änderung wird ein eigener Branch erstellt:

```bash
git checkout -b name-der-aenderung
```

Beispiele:

```bash
git checkout -b login-fix
git checkout -b kommentar-modell
git checkout -b styling-homepage
```

Der Branch-Name sollte kurz beschreiben, woran du arbeitest.

---

## 4. Dateien bearbeiten und speichern

Jetzt kannst du normal im Projekt arbeiten.

Danach prüfst du, welche Dateien geändert wurden:

```bash
git status
```

---

## 5. Änderungen committen

Geänderte Dateien vormerken:

```bash
git add .
```

Dann einen Commit erstellen:

```bash
git commit -m "Kurze Beschreibung der Änderung"
```

Beispiele:

```bash
git commit -m "Add comment model"
git commit -m "Fix home page redirect"
git commit -m "Update gitignore"
```

---

## 6. Branch zu GitHub hochladen

```bash
git push -u origin name-der-aenderung
```

Beispiel:

```bash
git push -u origin login-fix
```

---

## 7. Pull Request erstellen

Nach dem Push zeigt GitHub meistens direkt einen Button an:

**Compare & pull request**

Dort:

1. Kurzen Titel eintragen
2. Kurz beschreiben, was geändert wurde
3. Pull Request erstellen

Wichtig: Der Pull Request soll von deinem Branch nach `main` gehen.

---

## 8. Andere Person schaut drüber

Mindestens eine andere Person aus der Gruppe soll den Pull Request anschauen.

Wenn alles passt, gibt sie eine Approval-Freigabe.

Erst danach wird der Pull Request in `main` gemerged.

---

## 9. Nach dem Merge lokalen Stand aktualisieren

Nachdem der Pull Request gemerged wurde:

```bash
git checkout main
git pull
```

Danach kannst du für die nächste Aufgabe wieder einen neuen Branch erstellen.

---

## Wichtigste Regeln

- Nicht direkt auf `main` arbeiten.
- Für jede Aufgabe einen eigenen Branch erstellen.
- Vor dem Arbeiten immer `git pull` auf `main` machen.
- Änderungen mit verständlicher Commit-Nachricht committen.
- Danach Branch pushen und Pull Request erstellen.
- Mindestens eine andere Person schaut den Pull Request an.
- Erst nach Approval in `main` mergen.

---

## Häufige Probleme

### Ich bin auf dem falschen Branch

Prüfen mit:

```bash
git branch
```

Der Branch mit `*` davor ist aktuell aktiv.

Wechseln zu `main`:

```bash
git checkout main
```

---

### Ich habe vergessen vorher `git pull` zu machen

Dann zuerst speichern/committen, danach:

```bash
git checkout main
git pull
```

Falls Konflikte entstehen, kurz in der Gruppe fragen und nicht einfach irgendwas löschen.

---

### Ich möchte wissen, was Git gerade sieht

```bash
git status
```

Das ist fast immer der erste Befehl, wenn man unsicher ist.