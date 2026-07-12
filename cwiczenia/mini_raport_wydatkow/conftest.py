# UWAGA (reguły mini-projektu M1): ten conftest dostajesz GOTOWY, bez TODO.
# Dane testowe są żmudne do wpisywania i niczego nie uczą — twoja praca
# to logika w mini_raport_wydatkow.py i asserty w testach.
# Przeczytaj jednak te fixture uważnie: musisz znać dane, żeby testować.

import os
import sys
from pathlib import Path

import pandas as pd
import pytest
from openpyxl import Workbook

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture
def wydatki_csv(tmp_path: Path) -> Path:
    """Poprawny plik CSV z 7 wydatkami w trzech kategoriach.

    Args:
        tmp_path: wstrzykiwany przez pytest katalog tymczasowy.

    Returns:
        Path: ścieżka do pliku CSV z kolumnami data, kategoria, opis, kwota;
            sumy kategorii: jedzenie 261.0, transport 290.0, rozrywka 188.0;
            suma całkowita 739.0.
    """
    zawartosc = (
        "data,kategoria,opis,kwota\n"
        "2026-06-01,jedzenie,zakupy spozywcze,120.50\n"
        "2026-06-03,transport,bilet miesieczny,110.00\n"
        "2026-06-05,jedzenie,obiad na miescie,45.00\n"
        "2026-06-08,rozrywka,kino,38.00\n"
        "2026-06-12,jedzenie,zakupy spozywcze,95.50\n"
        "2026-06-15,transport,paliwo,180.00\n"
        "2026-06-20,rozrywka,koncert,150.00\n"
    )
    sciezka = tmp_path / "wydatki.csv"
    sciezka.write_text(zawartosc, encoding="utf-8")
    return sciezka


@pytest.fixture
def brudne_wiersze() -> list[dict[str, str]]:
    """Lista wierszy wydatków z błędami — do testów walidacji (zadanie 02).

    Args:
        Brak.

    Returns:
        list[dict[str, str]]: 5 wierszy; poprawne są tylko "kawa" (18.00)
            i "paliwo" (150.00); odpadają kwoty "abc", pusta i ujemna.
    """
    return [
        {"data": "2026-06-02", "kategoria": "jedzenie", "opis": "kawa",
         "kwota": "18.00"},
        {"data": "2026-06-04", "kategoria": "transport", "opis": "bilet",
         "kwota": "abc"},
        {"data": "2026-06-06", "kategoria": "rozrywka", "opis": "gra",
         "kwota": ""},
        {"data": "2026-06-07", "kategoria": "jedzenie", "opis": "zwrot",
         "kwota": "-20.00"},
        {"data": "2026-06-09", "kategoria": "transport", "opis": "paliwo",
         "kwota": "150.00"},
    ]


@pytest.fixture
def df_wydatki() -> pd.DataFrame:
    """Gotowy DataFrame 7 wydatków (kwoty już jako float) — zadania 04-06.

    Args:
        Brak.

    Returns:
        pd.DataFrame: kolumny kategoria, opis, kwota; te same wartości
            co w wydatki_csv (suma całkowita 739.0).
    """
    return pd.DataFrame({
        "kategoria": ["jedzenie", "transport", "jedzenie", "rozrywka",
                      "jedzenie", "transport", "rozrywka"],
        "opis": ["zakupy spozywcze", "bilet miesieczny", "obiad na miescie",
                 "kino", "zakupy spozywcze", "paliwo", "koncert"],
        "kwota": [120.50, 110.00, 45.00, 38.00, 95.50, 180.00, 150.00],
    })


@pytest.fixture
def df_raport() -> pd.DataFrame:
    """Gotowy zagregowany raport (NIEposortowany) — zadania 07-09.

    Args:
        Brak.

    Returns:
        pd.DataFrame: kolumny kategoria, suma, srednia, liczba;
            wiersze: jedzenie 261.0/87.0/3, transport 290.0/145.0/2,
            rozrywka 188.0/94.0/2.
    """
    return pd.DataFrame({
        "kategoria": ["jedzenie", "transport", "rozrywka"],
        "suma": [261.0, 290.0, 188.0],
        "srednia": [87.0, 145.0, 94.0],
        "liczba": [3, 2, 2],
    })


@pytest.fixture
def raport_xlsx(tmp_path: Path) -> Path:
    """Gotowy plik Excel z raportem bez formatowania — zadania 10-12.

    Args:
        tmp_path: wstrzykiwany przez pytest katalog tymczasowy.

    Returns:
        Path: plik .xlsx z nagłówkami kategoria/suma/srednia/liczba
            w wierszu 1 i trzema wierszami danych: jedzenie 261.0,
            transport 290.0, rozrywka 188.0 (sumy w kolumnie B).
    """
    wb = Workbook()
    ws = wb.active
    ws.append(["kategoria", "suma", "srednia", "liczba"])
    ws.append(["jedzenie", 261.0, 87.0, 3])
    ws.append(["transport", 290.0, 145.0, 2])
    ws.append(["rozrywka", 188.0, 94.0, 2])
    sciezka = tmp_path / "raport.xlsx"
    wb.save(str(sciezka))
    return sciezka
