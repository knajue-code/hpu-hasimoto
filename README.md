# HPU & Hashimoto Mentoring

Aktueller Entwicklungsstand. Veröffentlichung der Website erst nach ausdrücklicher Freigabe.

## Inhalt

- `dist/`: fertige statische Website einschließlich Bildern, Schriften, CSS und JavaScript.
- `source/`: ursprüngliche Seiten sowie Inhalts- und Dateinachweise.
- `scripts/`: Inhaltsgenerator und Prüfung.

Das Angebot kombiniert zwei persönliche Sessions à 90 Minuten mit acht Videomodulen und Selbstlernmaterialien. Gesamtpreis: 997 €. Die Buchungsbuttons auf der Mentoring-Seite öffnen den neuen Ablefy-Checkout in einem neuen Tab.

## Vorschau

```sh
python3 -m http.server 8765 --bind 127.0.0.1 --directory dist
```

Anschließend http://127.0.0.1:8765/ öffnen.

## Neuaufbau

```sh
python3 -m pip install -r requirements.txt
python3 scripts/build.py
python3 scripts/verify.py
```

CSS, JavaScript und das Mentoring-Mockup werden direkt in `dist/` gepflegt und beim Neuaufbau nicht überschrieben. Diesen Ordner nicht als temporären Build-Ordner löschen.

## Vor Veröffentlichung

- Freigabe einholen; Hosting wurde nicht eingerichtet.
- `noindex,nofollow` ist für die Vorschau gesetzt.
- Das bereitgestellte Mockup enthält auf einem kleinen Bildschirm noch „Balance Code“.
- Die alte lokale Checkout-Seite enthält die frühere Ablefy-Einbettung. Die aktuellen Buchungsbuttons umgehen diese und verlinken direkt auf das neue Angebot.
- Checkout und Newsletter benötigen eine Internetverbindung. Keine Bestellung oder Anmeldung wurde abgeschickt.
- Rechtstexte wurden aus der bisherigen Website übernommen.
