from pathlib import Path

import pandas as pd

from pandas_wstep import (
    zadanie_01_wczytaj_csv,
    zadanie_02_pobierz_kolumne,
    zadanie_03_suma_kolumny,
    zadanie_04_srednia_kolumny,
    zadanie_05_filtruj_wieksze,
    zadanie_06_filtruj_rowne,
    zadanie_07_kopiuj_df,
    zadanie_08_wczytaj_excel,
    zadanie_09_filtruj_mniejsze_rowne,
    zadanie_10_suma_po_filtrze,
    zadanie_11_kopiuj_i_dodaj_kolumne,
    zadanie_12_wczytaj_i_filtruj_srednia,
)


# --- zadanie_01 ---

def test_zadanie_01_zwraca_dataframe(csv_osoby: Path) -> None:
    """Co testuje: czy funkcja zwraca obiekt pd.DataFrame.
    Co udaje: nic — używam fixture csv_osoby (prawdziwy plik CSV na dysku).
    Co sprawdzam: isinstance(wynik, pd.DataFrame) jest True.
    """
    wynik = zadanie_01_wczytaj_csv(str(csv_osoby))
    assert isinstance(wynik, pd.DataFrame)


def test_zadanie_01_ma_kolumne_wiek(csv_osoby: Path) -> None:
    """Co testuje: czy wczytany DataFrame zawiera kolumnę "wiek".
    Co udaje: nic — używam fixture csv_osoby.
    Co sprawdzam: "wiek" in wynik.columns.
    """
    wynik = zadanie_01_wczytaj_csv(str(csv_osoby))
    assert "wiek" in wynik.columns


# --- zadanie_02 ---

def test_zadanie_02_zwraca_liste(df_osoby: pd.DataFrame) -> None:
    """Co testuje: czy funkcja zwraca zwykłą listę Pythona (nie Series).
    Co udaje: nic — używam fixture df_osoby.
    Co sprawdzam: isinstance(wynik, list) jest True.
    """
    wynik = zadanie_02_pobierz_kolumne(df_osoby, "imie")
    assert isinstance(wynik, list)


def test_zadanie_02_poprawna_liczba_elementow(df_osoby: pd.DataFrame) -> None:
    """Co testuje: czy lista zawiera tyle elementów co wierszy w DataFrame.
    Co udaje: nic — używam fixture df_osoby (3 wiersze).
    Co sprawdzam: len(wynik) == 3.
    """
    wynik = zadanie_02_pobierz_kolumne(df_osoby, "imie")
    assert len(wynik) == 3


# --- zadanie_03 ---

def test_zadanie_03_suma_wiekow(df_osoby: pd.DataFrame) -> None:
    """Co testuje: czy suma kolumny "wiek" jest poprawna.
    Co udaje: nic — używam fixture df_osoby (wieki: 20, 30, 40 → suma = 90).
    Co sprawdzam: wynik == 90.
    """
    wynik = zadanie_03_suma_kolumny(df_osoby, "wiek")
    assert wynik == 90


def test_zadanie_03_suma_jednej_wartosci() -> None:
    """Co testuje: czy suma DataFrame z jednym wierszem jest równa tej wartości.
    Co udaje: nic — tworzę minimalny DataFrame bezpośrednio w teście.
    Co sprawdzam: wynik == 15.
    """
    df = pd.DataFrame({"wiek": [15]})
    wynik = zadanie_03_suma_kolumny(df, "wiek")
    assert wynik == 15


# --- zadanie_04 ---

def test_zadanie_04_srednia_wiekow(df_osoby: pd.DataFrame) -> None:
    """Co testuje: czy średnia kolumny "wiek" jest poprawna.
    Co udaje: nic — używam fixture df_osoby (wieki: 20, 30, 40 → średnia = 30.0).
    Co sprawdzam: wynik == 30.0.
    """
    wynik = zadanie_04_srednia_kolumny(df_osoby, "wiek")
    assert wynik == 30.0


def test_zadanie_04_srednia_jednej_wartosci() -> None:
    """Co testuje: czy średnia DataFrame z jednym wierszem jest równa tej wartości.
    Co udaje: nic — tworzę minimalny DataFrame bezpośrednio w teście.
    Co sprawdzam: wynik == 25.0.
    """
    df = pd.DataFrame({"wiek": [25]})
    wynik = zadanie_04_srednia_kolumny(df, "wiek")
    assert wynik == 25.0


# --- zadanie_05 ---

def test_zadanie_05_zwraca_wiersze_powyzej_progu(df_osoby: pd.DataFrame) -> None:
    """Co testuje: czy filtr > 25 zwraca tylko wiersze z wiekiem > 25.
    Co udaje: nic — używam fixture df_osoby (wieki 20/30/40; > 25: Piotr i Zofia).
    Co sprawdzam: len(wynik) == 2.
    """
    wynik = zadanie_05_filtruj_wieksze(df_osoby, "wiek", 25)
    assert len(wynik) == 2


def test_zadanie_05_brak_wierszy_powyzej_progu(df_osoby: pd.DataFrame) -> None:
    """Co testuje: czy filtr z bardzo wysokim progiem zwraca pusty DataFrame.
    Co udaje: nic — używam fixture df_osoby z progiem 9999.
    Co sprawdzam: len(wynik) == 0.
    """
    wynik = zadanie_05_filtruj_wieksze(df_osoby, "wiek", 9999)
    assert len(wynik) == 0


# --- zadanie_06 ---

def test_zadanie_06_filtruje_po_miescie(df_osoby: pd.DataFrame) -> None:
    """Co testuje: czy filtr == "Warszawa" zwraca tylko wiersze z tym miastem.
    Co udaje: nic — używam fixture df_osoby (Warszawa: Anna i Zofia).
    Co sprawdzam: len(wynik) == 2.
    """
    wynik = zadanie_06_filtruj_rowne(df_osoby, "miasto", "Warszawa")
    assert len(wynik) == 2


def test_zadanie_06_brak_dopasowania_zwraca_pusty_df(df_osoby: pd.DataFrame) -> None:
    """Co testuje: czy filtr z nieistniejącą wartością zwraca pusty DataFrame.
    Co udaje: nic — używam fixture df_osoby z miastem "Gdansk" (brak w danych).
    Co sprawdzam: len(wynik) == 0.
    """
    wynik = zadanie_06_filtruj_rowne(df_osoby, "miasto", "Gdansk")
    assert len(wynik) == 0


# --- zadanie_07 ---

def test_zadanie_07_kopia_ma_te_same_dane(df_osoby: pd.DataFrame) -> None:
    """Co testuje: czy kopia zawiera te same dane co oryginał.
    Co udaje: nic — używam fixture df_osoby.
    Co sprawdzam: kopia["wiek"].tolist() == df_osoby["wiek"].tolist().
    """
    kopia = zadanie_07_kopiuj_df(df_osoby)
    assert kopia["wiek"].tolist() == df_osoby["wiek"].tolist()


def test_zadanie_07_modyfikacja_kopii_nie_zmienia_oryginalu(
    df_osoby: pd.DataFrame,
) -> None:
    """Co testuje: czy modyfikacja kopii nie zmienia oryginalnego DataFrame.
    Co udaje: nic — używam fixture df_osoby.
    Co sprawdzam: df_osoby["wiek"].tolist() jest niezmieniony po edycji kopii.
    """
    oryginalne = df_osoby["wiek"].tolist()
    kopia = zadanie_07_kopiuj_df(df_osoby)
    kopia["wiek"] = [0, 0, 0]
    assert df_osoby["wiek"].tolist() == oryginalne


# --- zadanie_08 ---

def test_zadanie_08_zwraca_dataframe(excel_osoby: Path) -> None:
    """Co testuje: czy funkcja zwraca obiekt pd.DataFrame przy wczytaniu pliku Excel.
    Co udaje: nic — używam fixture excel_osoby (prawdziwy plik .xlsx na dysku).
    Co sprawdzam: isinstance(wynik, pd.DataFrame) jest True.
    """
    wynik = zadanie_08_wczytaj_excel(str(excel_osoby))
    assert isinstance(wynik, pd.DataFrame)


def test_zadanie_08_ma_kolumne_imie(excel_osoby: Path) -> None:
    """Co testuje: czy wczytany DataFrame z Excela zawiera kolumnę "imie".
    Co udaje: nic — używam fixture excel_osoby.
    Co sprawdzam: "imie" in wynik.columns.
    """
    wynik = zadanie_08_wczytaj_excel(str(excel_osoby))
    assert "imie" in wynik.columns


# --- zadanie_09 ---

def test_zadanie_09_zwraca_wiersze_mniejsze_rowne_progowi(
    df_osoby: pd.DataFrame,
) -> None:
    """Co testuje: czy filtr <= 30 zwraca wiersze z wiekiem mniejszym lub równym 30.
    Co udaje: nic — używam fixture df_osoby (wieki 20/30/40; <= 30: Anna i Piotr).
    Co sprawdzam: len(wynik) == 2.
    """
    wynik = zadanie_09_filtruj_mniejsze_rowne(df_osoby, "wiek", 30)
    assert len(wynik) == 2


def test_zadanie_09_wszystkie_wiersze_spelniaja_warunek(
    df_osoby: pd.DataFrame,
) -> None:
    """Co testuje: czy bardzo wysoki próg zwraca wszystkie wiersze.
    Co udaje: nic — używam fixture df_osoby z progiem 9999 (wszyscy <= 9999).
    Co sprawdzam: len(wynik) == 3.
    """
    wynik = zadanie_09_filtruj_mniejsze_rowne(df_osoby, "wiek", 9999)
    assert len(wynik) == 3


# --- zadanie_10 ---

def test_zadanie_10_suma_wyfiltrowanych_wierszy(df_osoby: pd.DataFrame) -> None:
    """Co testuje: czy suma "wiek" po filtrze wiek > 25 jest poprawna.
    Co udaje: nic — używam fixture df_osoby (wiek > 25: Piotr=30 i Zofia=40; suma=70).
    Co sprawdzam: wynik == 70.
    """
    wynik = zadanie_10_suma_po_filtrze(df_osoby, "wiek", 25, "wiek")
    assert wynik == 70


def test_zadanie_10_brak_wierszy_suma_wynosi_zero(df_osoby: pd.DataFrame) -> None:
    """Co testuje: czy suma po filtrze bez wyników wynosi 0.
    Co udaje: nic — używam fixture df_osoby z progiem 9999 (brak wierszy > 9999).
    Co sprawdzam: wynik == 0.
    """
    wynik = zadanie_10_suma_po_filtrze(df_osoby, "wiek", 9999, "wiek")
    assert wynik == 0


# --- zadanie_11 ---

def test_zadanie_11_kopia_ma_nowa_kolumne(df_osoby: pd.DataFrame) -> None:
    """Co testuje: czy zwrócony DataFrame posiada nową kolumnę "plec".
    Co udaje: nic — używam fixture df_osoby.
    Co sprawdzam: "plec" in wynik.columns.
    """
    wynik = zadanie_11_kopiuj_i_dodaj_kolumne(
        df_osoby, "plec", ["K", "M", "K"]
    )
    assert "plec" in wynik.columns


def test_zadanie_11_oryginal_nie_ma_nowej_kolumny(df_osoby: pd.DataFrame) -> None:
    """Co testuje: czy oryginalny DataFrame nie został zmieniony po dodaniu kolumny do kopii.
    Co udaje: nic — używam fixture df_osoby.
    Co sprawdzam: "plec" not in df_osoby.columns po wywołaniu funkcji.
    """
    wynik = zadanie_11_kopiuj_i_dodaj_kolumne(
        df_osoby, "plec", ["K", "M", "K"]
    )
    assert "plec" not in df_osoby.columns


# --- zadanie_12 ---

def test_zadanie_12_zwraca_wiersze_powyzej_sredniej(csv_osoby: Path) -> None:
    """Co testuje: czy funkcja zwraca tylko wiersze z wiekiem powyżej średniej.
    Co udaje: nic — używam fixture csv_osoby (wieki: 20/30/40, średnia=30; > 30: Zofia).
    Co sprawdzam: len(wynik) == 1 i wynik["imie"].tolist() == ["Zofia"].
    """
    wynik = zadanie_12_wczytaj_i_filtruj_srednia(str(csv_osoby), "wiek")
    assert len(wynik) == 1
    assert wynik["imie"].tolist() == ["Zofia"]


def test_zadanie_12_wynik_jest_dataframe(csv_osoby: Path) -> None:
    """Co testuje: czy funkcja zwraca obiekt pd.DataFrame.
    Co udaje: nic — używam fixture csv_osoby.
    Co sprawdzam: isinstance(wynik, pd.DataFrame) jest True.
    """
    wynik = zadanie_12_wczytaj_i_filtruj_srednia(str(csv_osoby), "wiek")
    assert isinstance(wynik, pd.DataFrame)