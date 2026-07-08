import sys
import os
import pytest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture
def plik_csv(tmp_path: Path) -> Path:
    """Tymczasowy plik CSV z nagłówkiem i trzema wierszami danych.

    Args:
        tmp_path: wstrzykiwany przez pytest katalog tymczasowy (czysty dla każdego testu).

    Returns:
        Path: ścieżka do pliku CSV z nagłówkiem imie,wiek,miasto i 3 wierszami danych.
    """
    p = tmp_path / "dane.csv"
    p.write_text(
        "imie,wiek,miasto\nAnna,30,Warszawa\nPiotr,25,Krakow\nZofia,35,"
        "Gdansk\n", encoding="utf-8"
    )
    return p


@pytest.fixture
def plik_pusty_csv(tmp_path: Path) -> Path:
    """Tymczasowy plik CSV zawierający wyłącznie nagłówek, bez wierszy danych.

    Args:
        tmp_path: wstrzykiwany przez pytest katalog tymczasowy.

    Returns:
        Path: ścieżka do pliku CSV z samym nagłówkiem imie,wiek,miasto.
    """
    p = tmp_path / "pusty.csv"
    p.write_text("imie,wiek,miasto\n", encoding="utf-8")
    return p
