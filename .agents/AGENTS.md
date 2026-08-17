# Agent Instructions

## General Workflow
- Sprache: Antworten und Code-Kommentare ausschließlich auf Deutsch.
- Stil: Maximal prägnant, fokus auf Code/Lösung, keine einleitenden Floskeln oder Meta-Erklärungen.
- Testing: Zu neuen/geänderten Funktionen automatisch `pytest`-Unittests erstellen und ausführen.
- Dokumentation: Bei Funktionsänderungen oder neuen Features immer die `README.md` direkt aktualisieren.

## Security & Coding Standards
- Secrets: Niemals Credentials/Keys hardcoden; ausschließlich `.env`/Umgebungsvariablen nutzen und in `.gitignore` ausschließen.
- Krypto: Sensible Daten/API-Keys mit AES-256-GCM verschlüsseln; Zufallswerte via `secrets`-Modul generieren (kein `random`).
- Input & Injection: Keine dynamischen SQL/Command-Strings; parametrisierte Queries nutzen; kein `shell=True` in `subprocess`.
- File & Data: Pfade strikt via `pathlib.Path.resolve()` absichern (Path Traversal); kein `pickle` oder unsicheres `yaml.load()`.
- Net & Testing: Niemals `verify=False` bei HTTP-Requests; alle Validierungs- und Krypto-Routinen mit Tests absichern.
