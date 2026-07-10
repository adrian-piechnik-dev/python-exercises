import os
import sys
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
    wb = Workbook()
    ws = wb.active
    ws.append(["miasto", "sprzedaz"])
    ws.append(["Warszawa", 100])
    ws.append(["Krakow", 200])
    ws.append(["Warszawa", 300])
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
    return pd.DataFrame({
        "miasto": ["Warszawa", "Krakow", "Warszawa"],
        "sprzedaz": [100, 200, 300],
    })
