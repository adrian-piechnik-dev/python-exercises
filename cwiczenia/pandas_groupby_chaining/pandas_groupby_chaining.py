import pandas as pd


def zadanie_01_grupuj_i_licz(df: pd.DataFrame, klucz: str) -> pd.Series:
    """Zwraca liczbę wierszy w każdej grupie kolumny klucz.

    Args:
        df: tabela danych.
        klucz: nazwa kolumny, według której grupujemy.

    Returns:
        pd.Series: indeks = nazwy grup, wartości = liczba wierszy w grupie.
    """
    return df.groupby(klucz).size()


def zadanie_02_grupuj_i_sumuj(
    df: pd.DataFrame, klucz: str, kolumna: str
) -> pd.Series:
    """Zwraca sumę wartości kolumny numerycznej w każdej grupie.

    Args:
        df: tabela danych.
        klucz: nazwa kolumny, według której grupujemy.
        kolumna: nazwa kolumny numerycznej do zsumowania.

    Returns:
        pd.Series: indeks = nazwy grup, wartości = suma kolumna w danej grupie.
    """
    return df.groupby(klucz)[kolumna].sum()


def zadanie_03_grupuj_i_srednia(
    df: pd.DataFrame, klucz: str, kolumna: str
) -> pd.Series:
    """Zwraca średnią wartości kolumny numerycznej w każdej grupie.

    Args:
        df: tabela danych.
        klucz: nazwa kolumny, według której grupujemy.
        kolumna: nazwa kolumny numerycznej do uśrednienia.

    Returns:
        pd.Series: indeks = nazwy grup, wartości = średnia kolumna w danej grupie.
    """
    return df.groupby(klucz)[kolumna].mean()


def zadanie_04_agg_suma(
    df: pd.DataFrame, klucz: str, kolumna: str
) -> pd.DataFrame:
    """Grupuje dane i zwraca sumę wybranej kolumny przez .agg.

    Args:
        df: tabela danych.
        klucz: nazwa kolumny, według której grupujemy.
        kolumna: nazwa kolumny numerycznej do zagregowania.

    Returns:
        pd.DataFrame: indeks = nazwy grup, jedna kolumna z sumą.
    """
    return df.groupby(klucz).agg({kolumna: "sum"})


def zadanie_05_agg_srednia(
    df: pd.DataFrame, klucz: str, kolumna: str
) -> pd.DataFrame:
    """Grupuje dane i zwraca średnią wybranej kolumny przez .agg.

    Args:
        df: tabela danych.
        klucz: nazwa kolumny, według której grupujemy.
        kolumna: nazwa kolumny numerycznej do zagregowania.

    Returns:
        pd.DataFrame: indeks = nazwy grup, jedna kolumna ze średnią.
    """
    return df.groupby(klucz).agg({kolumna: "mean"})


def zadanie_06_agg_wiele_kolumn(df: pd.DataFrame, klucz: str) -> pd.DataFrame:
    """Grupuje dane i zwraca sumę "wiek" oraz średnią "wynagrodzenie" per grupa.

    Args:
        df: tabela danych z kolumnami "wiek" i "wynagrodzenie".
        klucz: nazwa kolumny, według której grupujemy.

    Returns:
        pd.DataFrame: indeks = nazwy grup, kolumny "wiek" (suma) i "wynagrodzenie" (średnia).
    """
    return df.groupby(klucz).agg({"wiek": "sum", "wynagrodzenie": "mean"})


def zadanie_07_assign_stala(df: pd.DataFrame, wartosc: str) -> pd.DataFrame:
    """Zwraca kopię DataFrame z nową kolumną "region" wypełnioną stałą wartością.

    Args:
        df: tabela danych.
        wartosc: wartość tekstowa wpisana do każdego wiersza w kolumnie "region".

    Returns:
        pd.DataFrame: DataFrame z dodaną kolumną "region"; oryginał niezmieniony.
    """
    return df.assign(region=wartosc)


def zadanie_08_assign_lambda(df: pd.DataFrame, mnoznik: float) -> pd.DataFrame:
    """Zwraca kopię DataFrame z nową kolumną "premia" = wynagrodzenie * mnoznik.

    Args:
        df: tabela danych z kolumną "wynagrodzenie".
        mnoznik: współczynnik mnożenia wynagrodzenia (np. 0.1 = 10% premia).

    Returns:
        pd.DataFrame: DataFrame z dodaną kolumną "premia"; oryginał niezmieniony.
    """
    return df.assign(premia=lambda d: d["wynagrodzenie"] * mnoznik)


def zadanie_09_chain_assign_grupuj(
    df: pd.DataFrame, mnoznik: float, klucz: str
) -> pd.Series:
    """Dodaje kolumnę "premia" (wynagrodzenie * mnoznik) i zwraca jej sumę per grupa.

    Całą operację realizuje w jednym łańcuchu bez zmiennych pośrednich.

    Args:
        df: tabela danych z kolumną "wynagrodzenie".
        mnoznik: współczynnik do obliczenia premii.
        klucz: nazwa kolumny, według której grupujemy.

    Returns:
        pd.Series: indeks = nazwy grup, wartości = suma premii w danej grupie.
    """
    return (
        df
        .assign(premia=lambda d: d["wynagrodzenie"] * mnoznik)
        .groupby(klucz)["premia"]
        .sum()
    )


def zadanie_10_copy_assign(df: pd.DataFrame, wartosc: str) -> pd.DataFrame:
    """Zwraca kopię DataFrame z kolumną "region"; oryginał na pewno niezmieniony.

    Args:
        df: tabela danych.
        wartosc: wartość tekstowa dla kolumny "region".

    Returns:
        pd.DataFrame: kopia df z dodaną kolumną "region".
    """
    return (
        df
        .copy()
        .assign(region=wartosc)
    )


def zadanie_11_filtruj_i_grupuj(
    df: pd.DataFrame, kolumna: str, prog: float, klucz: str
) -> pd.Series:
    """Filtruje wiersze (kolumna > prog) i zlicza je per grupa klucza.

    Args:
        df: tabela danych.
        kolumna: nazwa kolumny numerycznej do filtrowania.
        prog: wartość progowa; wiersze z wartością > prog przejdą przez filtr.
        klucz: nazwa kolumny, według której grupujemy wyfiltrowane wiersze.

    Returns:
        pd.Series: indeks = nazwy grup, wartości = liczba wierszy po filtrze.
    """
    return (
        df[df[kolumna] > prog]
        .groupby(klucz)
        .size()
    )


def zadanie_12_pelny_lancuch(df: pd.DataFrame, prog_wiek: int) -> pd.DataFrame:
    """Filtruje osoby w wieku >= prog_wiek i zwraca sumę wynagrodzeń per miasto.

    Całą operację realizuje w jednym łańcuchu bez zmiennych pośrednich.

    Args:
        df: tabela danych z kolumnami "wiek", "wynagrodzenie", "miasto".
        prog_wiek: minimalny wiek (włącznie); wiersze z wiekiem < prog_wiek odpadają.

    Returns:
        pd.DataFrame: indeks = nazwy miast, kolumna "wynagrodzenie" z sumą.
    """
    return (
        df[df["wiek"] >= prog_wiek]
        .groupby("miasto")
        .agg({"wynagrodzenie": "sum"})
    )
