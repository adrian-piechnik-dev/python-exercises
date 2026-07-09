from typing import Any

import pandas as pd


def zadanie_01_wczytaj_csv(sciezka: str) -> pd.DataFrame:
    """Wczytuje plik CSV i zwraca jego zawartość jako DataFrame.

    Args:
        sciezka: ścieżka do pliku CSV z nagłówkiem w pierwszej linii.

    Returns:
        pd.DataFrame: tabela danych wczytana z pliku.
    """
    return pd.read_csv(sciezka)


def zadanie_02_pobierz_kolumne(df: pd.DataFrame, kolumna: str) -> list[Any]:
    """Zwraca wszystkie wartości wskazanej kolumny jako listę Pythona.

    Args:
        df: tabela danych.
        kolumna: nazwa kolumny do pobrania.

    Returns:
        list[Any]: lista wartości z wybranej kolumny.
    """
    return df[kolumna].tolist()


def zadanie_03_suma_kolumny(df: pd.DataFrame, kolumna: str) -> float:
    """Zwraca sumę wartości wskazanej kolumny numerycznej.

    Args:
        df: tabela danych.
        kolumna: nazwa kolumny numerycznej.

    Returns:
        float: suma wartości w kolumnie.
    """
    return df[kolumna].sum()


def zadanie_04_srednia_kolumny(df: pd.DataFrame, kolumna: str) -> float:
    """Zwraca średnią arytmetyczną wartości wskazanej kolumny numerycznej.

    Args:
        df: tabela danych.
        kolumna: nazwa kolumny numerycznej.

    Returns:
        float: średnia wartości w kolumnie.
    """
    return df[kolumna].mean()


def zadanie_05_filtruj_wieksze(
    df: pd.DataFrame, kolumna: str, prog: float
) -> pd.DataFrame:
    """Zwraca wiersze, w których wartość kolumny jest ściśle większa od progu.

    Args:
        df: tabela danych.
        kolumna: nazwa kolumny numerycznej do filtrowania.
        prog: wartość progowa; wiersze z wartością > prog przejdą przez filtr.

    Returns:
        pd.DataFrame: przefiltrowany DataFrame (może być pusty).
    """
    maska = df[kolumna] > prog
    return df[maska]


def zadanie_06_filtruj_rowne(
    df: pd.DataFrame, kolumna: str, wartosc: str
) -> pd.DataFrame:
    """Zwraca wiersze, w których wartość kolumny tekstowej jest równa podanej wartości.

    Args:
        df: tabela danych.
        kolumna: nazwa kolumny tekstowej do filtrowania.
        wartosc: wartość, której szukamy w kolumnie.

    Returns:
        pd.DataFrame: przefiltrowany DataFrame (może być pusty).
    """
    maska = df[kolumna] == wartosc
    return df[maska]


def zadanie_07_kopiuj_df(df: pd.DataFrame) -> pd.DataFrame:
    """Zwraca niezależną kopię DataFrame; oryginał pozostaje niezmieniony.

    Args:
        df: tabela danych do skopiowania.

    Returns:
        pd.DataFrame: głęboka kopia przekazanego DataFrame.
    """
    return df.copy()


def zadanie_08_wczytaj_excel(sciezka: str) -> pd.DataFrame:
    """Wczytuje plik Excel (.xlsx) i zwraca jego zawartość jako DataFrame.

    Args:
        sciezka: ścieżka do pliku Excel z nagłówkiem w pierwszym wierszu.

    Returns:
        pd.DataFrame: tabela danych wczytana z pierwszego arkusza pliku.
    """
    return pd.read_excel(sciezka)


def zadanie_09_filtruj_mniejsze_rowne(
    df: pd.DataFrame, kolumna: str, prog: float
) -> pd.DataFrame:
    """Zwraca wiersze, w których wartość kolumny jest mniejsza lub równa progowi.

    Args:
        df: tabela danych.
        kolumna: nazwa kolumny numerycznej do filtrowania.
        prog: wartość progowa; wiersze z wartością <= prog przejdą przez filtr.

    Returns:
        pd.DataFrame: przefiltrowany DataFrame (może być pusty).
    """
    maska = df[kolumna] <= prog
    return df[maska]


def zadanie_10_suma_po_filtrze(
    df: pd.DataFrame, kolumna_filtru: str, prog: float, kolumna_sumy: str
) -> float:
    """Filtruje wiersze (kolumna_filtru > prog) i zwraca sumę innej kolumny.

    Args:
        df: tabela danych.
        kolumna_filtru: nazwa kolumny, po której filtrujemy (wartość > prog).
        prog: wartość progowa dla filtru.
        kolumna_sumy: nazwa kolumny numerycznej, z której liczymy sumę.

    Returns:
        float: suma wartości kolumna_sumy w wyfiltrowanych wierszach; 0.0 gdy brak wierszy.
    """
    wynik = df[df[kolumna_filtru] > prog]
    return wynik[kolumna_sumy].sum()


def zadanie_11_kopiuj_i_dodaj_kolumne(
    df: pd.DataFrame, nazwa: str, wartosci: list[Any]
) -> pd.DataFrame:
    """Zwraca kopię DataFrame z dodaną nową kolumną; oryginał pozostaje niezmieniony.

    Args:
        df: tabela danych do skopiowania.
        nazwa: nazwa nowej kolumny.
        wartosci: lista wartości nowej kolumny (tyle elementów co wierszy w df).

    Returns:
        pd.DataFrame: kopia df z nową kolumną o podanej nazwie i wartościach.
    """
    kopia = df.copy()
    kopia[nazwa] = wartosci
    return kopia


def zadanie_12_wczytaj_i_filtruj_srednia(sciezka: str, kolumna: str) -> pd.DataFrame:
    """Wczytuje CSV i zwraca wiersze, gdzie wartość kolumny przekracza jej średnią.

    Args:
        sciezka: ścieżka do pliku CSV zawierającego kolumnę numeryczną.
        kolumna: nazwa kolumny numerycznej, po której filtrujemy.

    Returns:
        pd.DataFrame: wiersze gdzie df[kolumna] > df[kolumna].mean().
    """
    df = pd.read_csv(sciezka)
    srednia = df[kolumna].mean()
    wynik = df[df[kolumna] > srednia]
    return wynik
