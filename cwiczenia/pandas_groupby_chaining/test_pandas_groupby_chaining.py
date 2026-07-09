import pandas as pd

from pandas_groupby_chaining import (
    zadanie_01_grupuj_i_licz,
    zadanie_02_grupuj_i_sumuj,
    zadanie_03_grupuj_i_srednia,
    zadanie_04_agg_suma,
    zadanie_05_agg_srednia,
    zadanie_06_agg_wiele_kolumn,
    zadanie_07_assign_stala,
    zadanie_08_assign_lambda,
    zadanie_09_chain_assign_grupuj,
    zadanie_10_copy_assign,
    zadanie_11_filtruj_i_grupuj,
    zadanie_12_pelny_lancuch,
)


# --- zadanie_01 ---

def test_zadanie_01_zlicza_grupy_po_miescie(df_osoby: pd.DataFrame) -> None:
    """Co testuje: czy .groupby + .size zwraca poprawną liczbę wierszy per miasto.
    Co udaje: nic — używam fixture df_osoby (Warszawa×3, Krakow×2).
    Co sprawdzam: wynik["Warszawa"]==3 i wynik["Krakow"]==2.
    """
    # TODO: wywołaj zadanie_01_grupuj_i_licz(df_osoby, "miasto")
    # TODO: sprawdź że wynik["Warszawa"] == 3
    # TODO: sprawdź że wynik["Krakow"] == 2
    pass


def test_zadanie_01_wynik_jest_series(df_osoby: pd.DataFrame) -> None:
    """Co testuje: czy funkcja zwraca obiekt pd.Series.
    Co udaje: nic — używam fixture df_osoby.
    Co sprawdzam: isinstance(wynik, pd.Series) jest True.
    """
    # TODO: wywołaj zadanie_01_grupuj_i_licz(df_osoby, "miasto")
    # TODO: sprawdź że wynik jest instancją pd.Series
    pass


# --- zadanie_02 ---

def test_zadanie_02_sumuje_wiek_po_miescie(df_osoby: pd.DataFrame) -> None:
    """Co testuje: czy suma "wiek" per miasto jest poprawna.
    Co udaje: nic — używam fixture df_osoby (Warszawa: 20+40+35=95, Krakow: 30+25=55).
    Co sprawdzam: wynik["Warszawa"]==95 i wynik["Krakow"]==55.
    """
    # TODO: wywołaj zadanie_02_grupuj_i_sumuj(df_osoby, "miasto", "wiek")
    # TODO: sprawdź że wynik["Warszawa"] == 95
    # TODO: sprawdź że wynik["Krakow"] == 55
    pass


def test_zadanie_02_wynik_jest_series(df_osoby: pd.DataFrame) -> None:
    """Co testuje: czy funkcja zwraca obiekt pd.Series.
    Co udaje: nic — używam fixture df_osoby.
    Co sprawdzam: isinstance(wynik, pd.Series) jest True.
    """
    # TODO: wywołaj zadanie_02_grupuj_i_sumuj(df_osoby, "miasto", "wiek")
    # TODO: sprawdź że wynik jest instancją pd.Series
    pass


# --- zadanie_03 ---

def test_zadanie_03_srednia_wiek_krakow(df_osoby: pd.DataFrame) -> None:
    """Co testuje: czy średnia "wiek" w grupie Krakow jest poprawna.
    Co udaje: nic — używam fixture df_osoby (Krakow: 30+25=55, /2=27.5).
    Co sprawdzam: wynik["Krakow"] == 27.5.
    """
    # TODO: wywołaj zadanie_03_grupuj_i_srednia(df_osoby, "miasto", "wiek")
    # TODO: sprawdź że wynik["Krakow"] == 27.5
    pass


def test_zadanie_03_wynik_jest_series(df_osoby: pd.DataFrame) -> None:
    """Co testuje: czy funkcja zwraca obiekt pd.Series.
    Co udaje: nic — używam fixture df_osoby.
    Co sprawdzam: isinstance(wynik, pd.Series) jest True.
    """
    # TODO: wywołaj zadanie_03_grupuj_i_srednia(df_osoby, "miasto", "wiek")
    # TODO: sprawdź że wynik jest instancją pd.Series
    pass


# --- zadanie_04 ---

def test_zadanie_04_agg_suma_zwraca_dataframe(df_osoby: pd.DataFrame) -> None:
    """Co testuje: czy .agg({"wiek": "sum"}) zwraca pd.DataFrame (nie Series).
    Co udaje: nic — używam fixture df_osoby.
    Co sprawdzam: isinstance(wynik, pd.DataFrame) jest True.
    """
    # TODO: wywołaj zadanie_04_agg_suma(df_osoby, "miasto", "wiek")
    # TODO: sprawdź że wynik jest instancją pd.DataFrame
    pass


def test_zadanie_04_suma_wiek_warszawa(df_osoby: pd.DataFrame) -> None:
    """Co testuje: czy wartość komórki ["wiek"]["Warszawa"] wynosi 95.
    Co udaje: nic — używam fixture df_osoby (Anna 20 + Zofia 40 + Ewa 35 = 95).
    Co sprawdzam: wynik["wiek"]["Warszawa"] == 95.
    """
    # TODO: wywołaj zadanie_04_agg_suma(df_osoby, "miasto", "wiek")
    # TODO: sprawdź że wynik["wiek"]["Warszawa"] == 95
    pass


# --- zadanie_05 ---

def test_zadanie_05_agg_srednia_zwraca_dataframe(df_osoby: pd.DataFrame) -> None:
    """Co testuje: czy .agg({"wynagrodzenie": "mean"}) zwraca pd.DataFrame.
    Co udaje: nic — używam fixture df_osoby.
    Co sprawdzam: isinstance(wynik, pd.DataFrame) jest True.
    """
    # TODO: wywołaj zadanie_05_agg_srednia(df_osoby, "miasto", "wynagrodzenie")
    # TODO: sprawdź że wynik jest instancją pd.DataFrame
    pass


def test_zadanie_05_srednia_wynagrodzenie_krakow(df_osoby: pd.DataFrame) -> None:
    """Co testuje: czy średnie wynagrodzenie w Krakowie wynosi 3750.0.
    Co udaje: nic — używam fixture df_osoby (Piotr 4000 + Marek 3500, /2 = 3750.0).
    Co sprawdzam: wynik["wynagrodzenie"]["Krakow"] == 3750.0.
    """
    # TODO: wywołaj zadanie_05_agg_srednia(df_osoby, "miasto", "wynagrodzenie")
    # TODO: sprawdź że wynik["wynagrodzenie"]["Krakow"] == 3750.0
    pass


# --- zadanie_06 ---

def test_zadanie_06_agg_wiele_kolumn_zwraca_dataframe(
    df_osoby: pd.DataFrame,
) -> None:
    """Co testuje: czy funkcja zwraca pd.DataFrame z dwiema kolumnami.
    Co udaje: nic — używam fixture df_osoby.
    Co sprawdzam: isinstance(wynik, pd.DataFrame) i obie kolumny istnieją.
    """
    # TODO: wywołaj zadanie_06_agg_wiele_kolumn(df_osoby, "miasto")
    # TODO: sprawdź że wynik jest instancją pd.DataFrame
    # TODO: sprawdź że "wiek" in wynik.columns
    # TODO: sprawdź że "wynagrodzenie" in wynik.columns
    pass


def test_zadanie_06_suma_wiek_i_srednia_wynagrodzenie(
    df_osoby: pd.DataFrame,
) -> None:
    """Co testuje: czy suma "wiek" w Warszawie = 95 i średnia "wynagrodzenie" w Krakowie = 3750.0.
    Co udaje: nic — używam fixture df_osoby.
    Co sprawdzam: wynik["wiek"]["Warszawa"]==95 i wynik["wynagrodzenie"]["Krakow"]==3750.0.
    """
    # TODO: wywołaj zadanie_06_agg_wiele_kolumn(df_osoby, "miasto")
    # TODO: sprawdź że wynik["wiek"]["Warszawa"] == 95
    # TODO: sprawdź że wynik["wynagrodzenie"]["Krakow"] == 3750.0
    pass


# --- zadanie_07 ---

def test_zadanie_07_assign_dodaje_kolumne_region(df_osoby: pd.DataFrame) -> None:
    """Co testuje: czy wynik zawiera kolumnę "region" z podaną wartością.
    Co udaje: nic — używam fixture df_osoby.
    Co sprawdzam: "region" in wynik.columns i wynik["region"].tolist() == ["Europa"]*5.
    """
    # TODO: wywołaj zadanie_07_assign_stala(df_osoby, "Europa")
    # TODO: sprawdź że "region" in wynik.columns
    # TODO: sprawdź że wynik["region"].tolist() == ["Europa"] * 5
    pass


def test_zadanie_07_oryginal_bez_kolumny_region(df_osoby: pd.DataFrame) -> None:
    """Co testuje: czy oryginalny DataFrame nie zyskał kolumny "region" po assign.
    Co udaje: nic — używam fixture df_osoby.
    Co sprawdzam: "region" not in df_osoby.columns po wywołaniu funkcji.
    """
    # TODO: wywołaj zadanie_07_assign_stala(df_osoby, "Europa")
    # TODO: sprawdź że "region" NIE jest w df_osoby.columns (oryginał niezmieniony)
    pass


# --- zadanie_08 ---

def test_zadanie_08_assign_dodaje_kolumne_premia(df_osoby: pd.DataFrame) -> None:
    """Co testuje: czy wynik zawiera kolumnę "premia".
    Co udaje: nic — używam fixture df_osoby.
    Co sprawdzam: "premia" in wynik.columns.
    """
    # TODO: wywołaj zadanie_08_assign_lambda(df_osoby, 0.1)
    # TODO: sprawdź że "premia" in wynik.columns
    pass


def test_zadanie_08_premia_to_10_procent_wynagrodzenia(
    df_osoby: pd.DataFrame,
) -> None:
    """Co testuje: czy premia = wynagrodzenie * 0.1 dla każdego wiersza.
    Co udaje: nic — używam fixture df_osoby (3000,4000,5000,3500,4500 → *0.1).
    Co sprawdzam: wynik["premia"].tolist() == [300.0, 400.0, 500.0, 350.0, 450.0].
    """
    # TODO: wywołaj zadanie_08_assign_lambda(df_osoby, 0.1)
    # TODO: sprawdź że wynik["premia"].tolist() == [300.0, 400.0, 500.0, 350.0, 450.0]
    pass


# --- zadanie_09 ---

def test_zadanie_09_chain_zwraca_series(df_osoby: pd.DataFrame) -> None:
    """Co testuje: czy łańcuch assign+groupby+sum zwraca pd.Series.
    Co udaje: nic — używam fixture df_osoby.
    Co sprawdzam: isinstance(wynik, pd.Series) jest True.
    """
    # TODO: wywołaj zadanie_09_chain_assign_grupuj(df_osoby, 0.1, "miasto")
    # TODO: sprawdź że wynik jest instancją pd.Series
    pass


def test_zadanie_09_suma_premii_warszawa(df_osoby: pd.DataFrame) -> None:
    """Co testuje: czy suma premii (10% wynagrodzenia) w Warszawie wynosi 1250.0.
    Co udaje: nic — używam fixture df_osoby (Warszawa: 300+500+450=1250.0).
    Co sprawdzam: wynik["Warszawa"] == 1250.0.
    """
    # TODO: wywołaj zadanie_09_chain_assign_grupuj(df_osoby, 0.1, "miasto")
    # TODO: sprawdź że wynik["Warszawa"] == 1250.0
    pass


# --- zadanie_10 ---

def test_zadanie_10_copy_assign_dodaje_kolumne(df_osoby: pd.DataFrame) -> None:
    """Co testuje: czy wynik zawiera kolumnę "region".
    Co udaje: nic — używam fixture df_osoby.
    Co sprawdzam: "region" in wynik.columns.
    """
    # TODO: wywołaj zadanie_10_copy_assign(df_osoby, "PL")
    # TODO: sprawdź że "region" in wynik.columns
    pass


def test_zadanie_10_oryginal_niezmieniony(df_osoby: pd.DataFrame) -> None:
    """Co testuje: czy copy() chroni oryginał przed zmianą.
    Co udaje: nic — używam fixture df_osoby.
    Co sprawdzam: "region" not in df_osoby.columns po wywołaniu.
    """
    # TODO: wywołaj zadanie_10_copy_assign(df_osoby, "PL")
    # TODO: sprawdź że "region" NIE jest w df_osoby.columns
    pass


# --- zadanie_11 ---

def test_zadanie_11_filtruje_i_liczy_grupy(df_osoby: pd.DataFrame) -> None:
    """Co testuje: czy filtr wiek>28 + groupby+size daje Warszawa=2, Krakow=1.
    Co udaje: nic — używam fixture df_osoby (>28: Piotr/30, Zofia/40, Ewa/35).
    Co sprawdzam: wynik["Warszawa"]==2 i wynik["Krakow"]==1.
    """
    # TODO: wywołaj zadanie_11_filtruj_i_grupuj(df_osoby, "wiek", 28, "miasto")
    # TODO: sprawdź że wynik["Warszawa"] == 2
    # TODO: sprawdź że wynik["Krakow"] == 1
    pass


def test_zadanie_11_bardzo_wysoki_prog_daje_jedna_grupe(
    df_osoby: pd.DataFrame,
) -> None:
    """Co testuje: czy filtr wiek>39 pozostawia tylko jedną grupę z jednym wierszem.
    Co udaje: nic — używam fixture df_osoby (>39: tylko Zofia/40/Warszawa).
    Co sprawdzam: len(wynik)==1 i wynik["Warszawa"]==1.
    """
    # TODO: wywołaj zadanie_11_filtruj_i_grupuj(df_osoby, "wiek", 39, "miasto")
    # TODO: sprawdź że len(wynik) == 1
    # TODO: sprawdź że wynik["Warszawa"] == 1
    pass


# --- zadanie_12 ---

def test_zadanie_12_suma_wynagrodzen_po_miescie(df_osoby: pd.DataFrame) -> None:
    """Co testuje: czy filtr wiek>=30 + agg sum daje Warszawa=9500, Krakow=4000.
    Co udaje: nic — używam fixture df_osoby (>=30: Piotr/4000, Zofia/5000, Ewa/4500).
    Co sprawdzam: wynik["wynagrodzenie"]["Warszawa"]==9500 i ["Krakow"]==4000.
    """
    # TODO: wywołaj zadanie_12_pelny_lancuch(df_osoby, 30)
    # TODO: sprawdź że wynik["wynagrodzenie"]["Warszawa"] == 9500
    # TODO: sprawdź że wynik["wynagrodzenie"]["Krakow"] == 4000
    pass


def test_zadanie_12_prog_powyzej_max_zwraca_pusty_dataframe(
    df_osoby: pd.DataFrame,
) -> None:
    """Co testuje: czy prog wyższy niż max wiek daje pusty DataFrame.
    Co udaje: nic — używam fixture df_osoby z prog_wiek=99 (nikt nie ma >= 99 lat).
    Co sprawdzam: len(wynik) == 0.
    """
    # TODO: wywołaj zadanie_12_pelny_lancuch(df_osoby, 99)
    # TODO: sprawdź że len(wynik) == 0
    pass
