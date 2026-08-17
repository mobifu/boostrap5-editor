# Bootstrap 5 & 3 Low-Code Editor

Ein Desktop-Editor auf Python- & CustomTkinter-Basis zur einfachen Erstellung von Bootstrap-HTML-Inhalten für Onlineshops und Webseiten.

## Sicherheitsarchitektur & Features

- **Projektverschlüsselung**: Projekte (`.enc`) werden mit **AES-256-GCM** verschlüsselt. Die Schlüsselableitung erfolgt über PBKDF2HMAC (SHA-256, 600.000 Iterationen) und kryptografisch sichere Salzes/Nonces via `secrets`. Vollständige Abwärtskompatibilität zu bestehenden Fernet-Dateien ist integriert.
- **XSS & Injection-Schutz**: URL-Sanitizer neutralisiert schadhafte URI-Schemata (`javascript:`, `vbscript:`, `data:text/html`) in Buttons, Bildern und Navigationsleisten. CSS-Klassen und HTML-Attribute werden gefiltert.
- **Sichere Pfadverwaltung**: Alle internen Dateizugriffe und Vorschau-Generierungen nutzen deterministische `pathlib.Path`-Pfade.
- **Supply-Chain-Sicherheit**: Trennung in `requirements.txt` (Produktion) und `requirements-dev.txt` (Build & Tests) mit fest definierten Versionsgrenzen.

## Build & CI/CD Automation

Der Build-Prozess wird über `build_exe.py` sowie über **GitHub Actions** gesteuert und beinhaltet automatisierte Qualitäts- und Sicherheitsprüfungen (Ruff, Pytest, Bandit):

```powershell
# Lokaler Standard-Build (PyInstaller mit _internal Ordnerstruktur & schnellem Start)
python build_exe.py

# Nuitka-Build (Optional für C-Code Kompilierung)
python build_exe.py --nuitka
```

### Automatische Releases & Code-Signing (CI/CD)

Sobald ein Git-Tag (z. B. `v1.0.0`) gepusht wird, baut die GitHub Action `.github/workflows/release.yml` automatisch das Release:
- Führt alle Unit-Tests und Security-Audits aus.
- Kompiliert die Windows-Executable (`BootstrapEditor.exe`).
- Signiert die Binärdatei (sofern `WINDOWS_CERT_BASE64` in den Repository Secrets hinterlegt ist).
- Publiziert das fertige ZIP-Archiv und die Executable direkt in den **GitHub Releases**.

---

## Roadmap / Todo

- [ ] **Windows-Installer (.exe / Setup-Wizard)**:
  - Umwandlung der Anwendung in eine echte, installierbare Windows-Setup-Datei (z. B. via Inno Setup oder NSIS), um die Abhängigkeit von einzelnen Zip/Portable-Verzeichnissen zu lösen und eine saubere Windows-Installation (Startmenü-Eintrag, Deinstallationsroutine) anzubieten.
