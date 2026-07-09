import os
import sys

import pandas as pd
import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture
def df_osoby() -> pd.DataFrame:
    """DataFrame z danymi pięciu osób — używany przez wszystkie testy.

    Args:
        Brak.

    Returns:
        pd.DataFrame: tabela z kolumnami "imie", "miasto", "wiek", "wynagrodzenie";
            5 wierszy: Warszawa×3 (Anna/20/3000, Zofia/40/5000, Ewa/35/4500)
            i Krakow×2 (Piotr/30/4000, Marek/25/3500).
    """
    return pd.DataFrame({
        "imie": ["Anna", "Piotr", "Zofia", "Marek", "Ewa"],
        "miasto": ["Warszawa", "Krakow", "Warszawa", "Krakow", "Warszawa"],
        "wiek": [20, 30, 40, 25, 35],
        "wynagrodzenie": [3000, 4000, 5000, 3500, 4500]
    })
