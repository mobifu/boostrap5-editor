import os
import base64
import json
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.exceptions import InvalidKey


def _derive_key(password: str, salt: bytes) -> bytes:
    """
    Leitet einen sicheren Schlüssel aus dem Passwort ab (PBKDF2HMAC).
    Fernet erfordert einen URL-safe Base64-codierten 32-Byte Key.
    Erfüllt OWASP Empfehlung mit 600.000 Iterationen.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600000,
    )
    key = kdf.derive(password.encode("utf-8"))
    return base64.urlsafe_b64encode(key)


def encrypt_project(data_dict: dict, password: str) -> bytes:
    """
    Konvertiert das Projekt-Dictionary in JSON und verschlüsselt es.
    Der generierte Salt wird an den Anfang der Ausgabe gehängt (16 Bytes).
    """
    salt = os.urandom(16)
    key = _derive_key(password, salt)
    fernet = Fernet(key)

    json_data = json.dumps(data_dict).encode("utf-8")
    encrypted_data = fernet.encrypt(json_data)

    # Packe Salt und Daten zusammen: SALT (16 bytes) + ENCRYPTED_DATA
    return salt + encrypted_data


def decrypt_project(encrypted_content: bytes, password: str) -> dict:
    """
    Liest den Salt, leitet den Schlüssel ab und entschlüsselt das Projekt.
    """
    if len(encrypted_content) < 16:
        raise ValueError("Die Datei ist zu klein, um gültig zu sein.")

    salt = encrypted_content[:16]
    actual_encrypted_data = encrypted_content[16:]

    key = _derive_key(password, salt)
    fernet = Fernet(key)

    try:
        decrypted_data = fernet.decrypt(actual_encrypted_data)
        return json.loads(decrypted_data.decode("utf-8"))
    except InvalidKey:
        raise ValueError("Falsches Passwort oder beschädigte Datei.")
    except json.JSONDecodeError:
        raise ValueError("Entschlüsselte Daten sind kein gültiges JSON-Format.")
    except Exception:
        raise ValueError(
            "Fehler bei der Entschlüsselung. Bitte Passwort und Datei prüfen."
        )
