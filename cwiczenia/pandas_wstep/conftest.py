import os
import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture
def df_osoby() -> pd.DataFrame:
    """DataFrame z danymi trzech osób — używany przez większość testów.

    Args:
        Brak.

    Returns:
        pd.DataFrame: tabela z kolumnami "imie", "wiek", "miasto";
            3 wiersze: Anna/20/Warszawa, Piotr/30/Krakow, Zofia/40/Warszawa.
    """
    return pd.DataFrame({
        "imie": ["Anna", "Piotr", "Zofia"],
        "wiek": [20, 30, 40],
        "miasto": ["Warszawa", "Krakow", "Warszawa"],
    })


@pytest.fixture
def csv_osoby(tmp_path: Path) -> Path:
    """Tymczasowy plik CSV z danymi trzech osób (te same dane co df_osoby).

    Args:
        tmp_path: wstrzykiwany przez pytest katalog tymczasowy.

    Returns:
        Path: ścieżka do gotowego pliku CSV z nagłówkiem imie,wiek,miasto.
    """
    p = tmp_path / "osoby.csv"
    df = pd.DataFrame({
        "imie": ["Anna", "Piotr", "Zofia"],
        "wiek": [20, 30, 40],
        "miasto": ["Warszawa", "Krakow", "Warszawa"],
    })
    df.to_csv(str(p), index=False)
    return p


@pytest.fixture
def excel_osoby(tmp_path: Path) -> Path:
    """Tymczasowy plik Excel (.xlsx) z danymi trzech osób (te same dane co df_osoby).

    Args:
        tmp_path: wstrzykiwany przez pytest katalog tymczasowy.

    Returns:
        Path: ścieżka do gotowego pliku .xlsx z nagłówkiem imie,wiek,miasto.
    """
    p = tmp_path / "osoby.xlsx"
    df = pd.DataFrame({
        "imie": ["Anna", "Piotr", "Zofia"],
        "wiek": [20, 30, 40],
        "miasto": ["Warszawa", "Krakow", "Warszawa"],
    })
    df.to_excel(str(p), index=False)
    return p
