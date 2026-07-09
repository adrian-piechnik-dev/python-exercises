import sys
import os
from pathlib import Path

import pandas as pd
import pytest
from openpyxl import Workbook

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture
def plik_xlsx(tmp_path: Path) -> Path:
    """Tymczasowy plik Excela z nagłówkami i trzema wierszami danych sprzedaży.

    Args:
        tmp_path: wstrzykiwany przez pytest katalog tymczasowy (czysty dla każdego testu).

    Returns:
        Path: ścieżka do pliku .xlsx z nagłówkami ["miasto", "sprzedaz"]
            i wierszami: Warszawa/100, Krakow/200, Warszawa/300.
    """
    # TODO: utwórz wb = Workbook() i pobierz ws = wb.active
    # TODO: dodaj nagłówki: ws.append(["miasto", "sprzedaz"])
    # TODO: dodaj trzy wiersze danych przez ws.append:
    #       ["Warszawa", 100], ["Krakow", 200], ["Warszawa", 300]
    # TODO: utwórz p = tmp_path / "dane.xlsx" i zapisz: wb.save(str(p))
    # TODO: return p
    wb = Workbook()
    ws = wb.active
    ws.append(["Warszawa", 100], ["Krakow", 200], ["Warszawa", 300])
    p = tmp_path / "dane.xlsx"
    wb.save(str(p))
    return p


@pytest.fixture
def df_sprzedaz() -> pd.DataFrame:
    """DataFrame z danymi sprzedaży w trzech wierszach — do zadań 11-12.

    Args:
        Brak.

    Returns:
        pd.DataFrame: tabela z kolumnami "miasto" i "sprzedaz";
            wiersze: Warszawa/100, Krakow/200, Warszawa/300.
    """
    # TODO: return pd.DataFrame({
    #           "miasto": ["Warszawa", "Krakow", "Warszawa"],
    #           "sprzedaz": [100, 200, 300],
    #       })
    return pd.DataFrame({
        "miasto": ["Warszawa", "Krakow", "Warszawa"],
        "sprzedaz": [100, 200, 300],
    })
