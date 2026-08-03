# Bootstrap 5 & 3 Low-Code Editor

Ein Desktop-Editor auf Python- & CustomTkinter-Basis zur einfachen Erstellung von Bootstrap-HTML-Inhalten für Onlineshops und Webseiten.

## Build & Release Process

Der Build-Prozess wird über `build_exe.py` gesteuert und beinhaltet automatisierte Qualitäts- und Sicherheitsprüfungen (Ruff, Pytest, Bandit).

```powershell
# Standard-Build (PyInstaller mit _internal Ordnerstruktur & schnellem Start)
python build_exe.py

# Nuitka-Build (Optional für C-Code Kompilierung)
python build_exe.py --nuitka
```

---

## Roadmap / Todo

- [ ] **Windows-Installer (.exe / Setup-Wizard)**:
  - Umwandlung der Anwendung in eine echte, installierbare Windows-Setup-Datei (z. B. via Inno Setup oder NSIS), um die Abhängigkeit von einzelnen Zip/Portable-Verzeichnissen zu lösen und eine saubere Windows-Installation (Startmenü-Eintrag, Deinstallationsroutine) anzubieten.
