import datetime
import os
import zipfile


def create_backup():
    source_dir = os.path.dirname(os.path.abspath(__file__))
    backup_base_dir = r"C:\E\python\boostrap5-editor-sicherung"

    # Sicherstellen, dass das Zielverzeichnis existiert
    if not os.path.exists(backup_base_dir):
        os.makedirs(backup_base_dir)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(
        backup_base_dir, f"boostrap_editor_backup_{timestamp}.zip"
    )

    # Ordner und Dateien, die ignoriert werden sollen
    exclude_dirs = {
        "venv",
        "venv_win",
        "__pycache__",
        ".pytest_cache_local",
        ".git",
        ".gemini",
    }
    exclude_exts = {".pyc"}

    print(f"Starte Sicherung nach {backup_file} ...")

    with zipfile.ZipFile(backup_file, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            # Ignoriere bestimmte Ordner
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            for file in files:
                # Ignoriere temporäre DB-Dateien und pyc
                if file.startswith("tmp") and (
                    file.endswith(".db") or file.endswith(".db.salt")
                ):
                    continue
                if any(file.endswith(ext) for ext in exclude_exts):
                    continue
                if file == os.path.basename(
                    __file__
                ):  # Sich selbst kann man sichern, aber wir nehmen es mit
                    pass

                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source_dir)
                zipf.write(file_path, arcname)

    print("Sicherung erfolgreich abgeschlossen!")


if __name__ == "__main__":
    create_backup()
