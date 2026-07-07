import sys
import os
import pytest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture
def plik_txt(tmp_path: Path) -> Path:
    """Tymczasowy plik z trzema liniami tekstu do testow czytania.

    Args:
        tmp_path: wstrzykiwany przez pytest katalog tymczasowy (czysty dla kazdego testu).

    Returns:
        Path: sciezka do pliku z trescia "ala ma kota\\npies i kot\\nkot spi\\n".
    """
    p = tmp_path / "dane.txt"
    p.write_text("ala ma kota\npies i kot\nkot spi\n", encoding="utf-8")
    return p


@pytest.fixture
def plik_pusty(tmp_path: Path) -> Path:
    """Tymczasowy istniejacy, pusty plik tekstowy do testow brzegowych.

    Args:
        tmp_path: wstrzykiwany przez pytest katalog tymczasowy.

    Returns:
        Path: sciezka do pustego pliku.
    """
    p = tmp_path / "pusty.txt"
    p.write_text("", encoding="utf-8")
    return p
