import pytest

from security import decrypt_project, encrypt_project


def test_encrypt_decrypt_success():
    data = {"title": "Test Project", "elements": [1, 2, 3]}
    password = "SecretPassword123!"

    encrypted = encrypt_project(data, password)
    assert isinstance(encrypted, bytes)
    assert len(encrypted) > 16

    decrypted = decrypt_project(encrypted, password)
    assert decrypted == data


def test_decrypt_invalid_password():
    data = {"title": "Test Project"}
    encrypted = encrypt_project(data, "CorrectPassword")

    with pytest.raises(ValueError, match="Falsches Passwort oder beschädigte Datei."):
        decrypt_project(encrypted, "WrongPassword")


def test_decrypt_too_short_content():
    with pytest.raises(ValueError, match="Die Datei ist zu klein, um gültig zu sein."):
        decrypt_project(b"short", "password")


def test_decrypt_corrupted_json(monkeypatch):
    data = {"test": 123}
    encrypted = encrypt_project(data, "pass")

    # Mock fernet decrypt to return non-json bytes
    monkeypatch.setattr(
        "cryptography.fernet.Fernet.decrypt", lambda self, data: b"invalid json bytes"
    )

    with pytest.raises(
        ValueError, match="Entschlüsselte Daten sind kein gültiges JSON-Format."
    ):
        decrypt_project(encrypted, "pass")
