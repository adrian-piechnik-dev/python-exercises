from typing import Any, Optional

import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


def zadanie_01_polacz(
    host: str, baza: str, uzytkownik: str, haslo: str
) -> Any:
    """Otwiera połączenie z serwerem PostgreSQL.

    Args:
        host: adres serwera (np. "localhost").
        baza: nazwa bazy danych na serwerze.
        uzytkownik: login użytkownika bazy.
        haslo: hasło użytkownika.

    Returns:
        Any: obiekt połączenia zwrócony przez psycopg2.
    """
    return psycopg2.connect(
        host=host,
        dbname=baza,
        user=uzytkownik,
        password=haslo,
    )


def zadanie_02_utworz_tabele(polaczenie: Any) -> None:
    """Tworzy tabelę produkty i zatwierdza zmianę.

    Args:
        polaczenie: otwarte połączenie z bazą.

    Returns:
        None
    """
    with polaczenie.cursor() as kursor:
        kursor.execute(
            """
            CREATE TABLE produkty (
                id SERIAL PRIMARY KEY,
                nazwa TEXT,
                cena NUMERIC
            )
            """
        )
    polaczenie.commit()


def zadanie_03_wstaw_produkt(
    polaczenie: Any, nazwa: str, cena: float
) -> None:
    """Wstawia jeden produkt zapytaniem parametryzowanym i zatwierdza.

    Args:
        polaczenie: otwarte połączenie z bazą.
        nazwa: nazwa produktu.
        cena: cena produktu.

    Returns:
        None
    """
    with polaczenie.cursor() as kursor:
        kursor.execute(
            "INSERT INTO produkty (nazwa, cena) VALUES (%s, %s)",
            (nazwa, cena)
        )
    polaczenie.commit()


def zadanie_04_wstaw_wiele(
    polaczenie: Any, produkty: list[tuple]
) -> None:
    """Wstawia wiele produktów jednym executemany i zatwierdza.

    Args:
        polaczenie: otwarte połączenie z bazą.
        produkty: lista krotek (nazwa, cena) do wstawienia.

    Returns:
        None
    """
    with polaczenie.cursor() as kursor:
        kursor.executemany("INSERT INTO produkty (nazwa, cena) VALUES (%s, %s)", produkty)
    polaczenie.commit()


def zadanie_05_wszystkie_produkty(polaczenie: Any) -> list[tuple]:
    """Pobiera wszystkie produkty z tabeli.

    Args:
        polaczenie: otwarte połączenie z bazą.

    Returns:
        list[tuple]: wiersze tabeli produkty jako lista krotek.
    """
    with polaczenie.cursor() as kursor:
        kursor.execute("SELECT id, nazwa, cena FROM produkty")
        return kursor.fetchall()


def zadanie_06_znajdz_produkt(
    polaczenie: Any, nazwa: str
) -> Optional[tuple]:
    """Znajduje pierwszy produkt o podanej nazwie lub zwraca None.

    Args:
        polaczenie: otwarte połączenie z bazą.
        nazwa: szukana nazwa produktu.

    Returns:
        Optional[tuple]: wiersz produktu lub None, gdy brak dopasowania.
    """
    with polaczenie.cursor() as kursor:
        kursor.execute(
            "SELECT id, nazwa, cena FROM produkty WHERE nazwa = %s",
            (nazwa,)
        )
        return kursor.fetchone()


def zadanie_07_polacz_bezpiecznie(
    host: str, baza: str, uzytkownik: str, haslo: str
) -> Optional[Any]:
    """Otwiera połączenie z bazą; każdy błąd psycopg2 zamienia na None.

    Args:
        host: adres serwera.
        baza: nazwa bazy danych.
        uzytkownik: login użytkownika.
        haslo: hasło użytkownika.

    Returns:
        Optional[Any]: obiekt połączenia lub None przy błędzie
            z rodziny psycopg2.Error.
    """
    try:
        return psycopg2.connect(
            host=host, dbname=baza, user=uzytkownik, password=haslo
        )
    except psycopg2.Error:
        return None


def zadanie_08_policz_produkty(polaczenie: Any) -> int:
    """Liczy wszystkie produkty w tabeli.

    Args:
        polaczenie: otwarte połączenie z bazą.

    Returns:
        int: liczba wierszy tabeli produkty.
    """
    with polaczenie.cursor() as kursor:
        kursor.execute("SELECT COUNT(*) FROM produkty")
        return kursor.fetchone()[0]


def zadanie_09_utworz_silnik(adres: str) -> Engine:
    """Buduje silnik SQLAlchemy dla podanego adresu bazy.

    Args:
        adres: URL bazy, np. "postgresql://anna:tajne@localhost/sklep"
            albo "sqlite:///C:/dane/test.db".

    Returns:
        Engine: silnik gotowy do użycia przez pandas.
    """
    return create_engine(adres)


def zadanie_10_df_do_bazy(
    df: pd.DataFrame, nazwa_tabeli: str, silnik: Engine
) -> None:
    """Zapisuje DataFrame jako tabelę w bazie (nadpisując istniejącą).

    Args:
        df: tabela danych do zapisania.
        nazwa_tabeli: nazwa tabeli docelowej w bazie.
        silnik: silnik SQLAlchemy wskazujący bazę.

    Returns:
        None
    """
    df.to_sql(nazwa_tabeli, silnik, index=False, if_exists="replace")


def zadanie_11_czytaj_do_df(zapytanie: str, silnik: Engine) -> pd.DataFrame:
    """Wykonuje zapytanie SQL i zwraca wynik jako DataFrame.

    Args:
        zapytanie: zapytanie SELECT (SQL z tematu 14 działa bez zmian).
        silnik: silnik SQLAlchemy wskazujący bazę.

    Returns:
        pd.DataFrame: wynik zapytania jako tabela pandas.
    """
    return pd.read_sql(zapytanie, silnik)


def zadanie_12_raport_do_bazy(df: pd.DataFrame, silnik: Engine) -> int:
    """Buduje raport sumy sprzedaży per miasto i zapisuje go do tabeli raport.

    Args:
        df: tabela danych z kolumnami "miasto" i "sprzedaz".
        silnik: silnik SQLAlchemy wskazujący bazę.

    Returns:
        int: liczba wierszy zapisanego raportu (liczba unikalnych miast).
    """
    wynik = df.groupby("miasto").agg({"sprzedaz": "sum"}).reset_index()
    wynik.to_sql("raport", silnik, index=False, if_exists="replace")
    return len(wynik)