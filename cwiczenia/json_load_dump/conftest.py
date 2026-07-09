import sys
import os
import json
from pathlib import Path

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture
def plik_json_slownik(tmp_path: Path) -> Path:
    """Tymczasowy plik JSON zawierający jeden słownik z danymi osoby.

    Args:
        tmp_path: wstrzykiwany przez pytest katalog tymczasowy (czysty dla każdego testu).

    Returns:
        Path: ścieżka do pliku JSON z {"imie": "Anna", "wiek": 30, "miasto": "Warszawa"}.
    """
    p = tmp_path / "osoby.json"
    p.write_text(json.dumps({"imie": "Anna", "wiek": 30, "miasto": "Warszawa"}), encoding="utf-8")
    return p


@pytest.fixture
def plik_json_lista(tmp_path: Path) -> Path:
    """Tymczasowy plik JSON zawierający listę trzech słowników z danymi osób.

    Args:
        tmp_path: wstrzykiwany przez pytest katalog tymczasowy (czysty dla każdego testu).

    Returns:
        Path: ścieżka do pliku JSON z listą [Anna/Warszawa, Piotr/Krakow, Zofia/Warszawa].
    """
    p = tmp_path / "osoby.json"
    lista = [
        {"imie": "Anna", "wiek": 30, "miasto": "Warszawa"},
        {"imie": "Piotr", "wiek": 25, "miasto": "Krakow"},
        {"imie": "Zofia", "wiek": 35, "miasto": "Warszawa"},
    ]
    p.write_text(json.dumps(lista), encoding="utf-8")
    return p