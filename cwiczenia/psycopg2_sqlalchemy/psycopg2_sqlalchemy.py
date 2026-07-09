from typing import Any, Optional

import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

# --- SPIS ZADAŃ ---
# Zadania 1-8: psycopg2 (funkcje dostają połączenie albo same je tworzą).
# Zadania 9-12: SQLAlchemy + pandas (engine zamiast ręcznych połączeń).
#
# zadanie_01 — otwórz połączenie z serwerem (psycopg2.connect)
# zadanie_02 — utwórz tabelę produkty (with cursor + commit)
# zadanie_03 — wstaw jeden produkt zapytaniem parametryzowanym (%s)
# zadanie_04 — wstaw wiele produktów hurtem (executemany)
# zadanie_05 — pobierz wszystkie produkty (SELECT + fetchall)
# zadanie_06 — znajdź produkt po nazwie (%s + fetchone, brak → None)
# zadanie_07 — połącz bezpiecznie (psycopg2.Error → None)
# zadanie_08 — policz produkty (COUNT + fetchone[0])
# zadanie_09 — zbuduj silnik SQLAlchemy (create_engine)
# zadanie_10 — zapisz DataFrame do bazy (to_sql, zazębienie: temat 9)
# zadanie_11 — wczytaj zapytanie do DataFrame (read_sql)
# zadanie_12 — raport groupby z DataFrame prosto do bazy (pełne zazębienie)


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
    # TODO: zwróć psycopg2.connect(host=host, dbname=baza,
    #       user=uzytkownik, password=haslo)
    pass


def zadanie_02_utworz_tabele(polaczenie: Any) -> None:
    """Tworzy tabelę produkty i zatwierdza zmianę.

    Args:
        polaczenie: otwarte połączenie z bazą.

    Returns:
        None
    """
    # TODO: otwórz kursor w bloku: with polaczenie.cursor() as kursor:
    # TODO: wewnątrz with wykonaj kursor.execute z zapytaniem:
    #       CREATE TABLE produkty (
    #           id SERIAL PRIMARY KEY,
    #           nazwa TEXT,
    #           cena NUMERIC
    #       )
    #       (SERIAL — postgresowa autonumeracja wierszy)
    # TODO: po bloku with zatwierdź: polaczenie.commit()
    pass


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
    # TODO: otwórz kursor w bloku with polaczenie.cursor() as kursor:
    # TODO: wykonaj kursor.execute z zapytaniem:
    #       INSERT INTO produkty (nazwa, cena) VALUES (%s, %s)
    #       oraz krotką parametrów (nazwa, cena) jako DRUGIM argumentem
    #       — nigdy f-string do sklejania SQL (SQL injection)!
    # TODO: po bloku with zatwierdź: polaczenie.commit()
    pass


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
    # TODO: otwórz kursor w bloku with polaczenie.cursor() as kursor:
    # TODO: wykonaj kursor.executemany z zapytaniem
    #       INSERT INTO produkty (nazwa, cena) VALUES (%s, %s)
    #       i całą listą produkty jako drugim argumentem
    # TODO: po bloku with zatwierdź: polaczenie.commit()
    pass


def zadanie_05_wszystkie_produkty(polaczenie: Any) -> list[tuple]:
    """Pobiera wszystkie produkty z tabeli.

    Args:
        polaczenie: otwarte połączenie z bazą.

    Returns:
        list[tuple]: wiersze tabeli produkty jako lista krotek.
    """
    # TODO: otwórz kursor w bloku with polaczenie.cursor() as kursor:
    # TODO: wykonaj kursor.execute("SELECT id, nazwa, cena FROM produkty")
    # TODO: wewnątrz with zwróć kursor.fetchall()
    #       (SELECT nie zmienia danych — commit zbędny)
    pass


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
    # TODO: otwórz kursor w bloku with polaczenie.cursor() as kursor:
    # TODO: wykonaj kursor.execute z zapytaniem
    #       SELECT id, nazwa, cena FROM produkty WHERE nazwa = %s
    #       i krotką (nazwa,) — przecinek! krotka jednoelementowa
    # TODO: wewnątrz with zwróć kursor.fetchone()
    #       (fetchone sam daje None przy braku wyników)
    pass


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
    # TODO: użyj try/except psycopg2.Error (wzorzec z tematu 4:
    #       sygnalizacja błędu przez None)
    # TODO: w try: return psycopg2.connect(host=host, dbname=baza,
    #       user=uzytkownik, password=haslo)
    # TODO: w except: return None
    pass


def zadanie_08_policz_produkty(polaczenie: Any) -> int:
    """Liczy wszystkie produkty w tabeli.

    Args:
        polaczenie: otwarte połączenie z bazą.

    Returns:
        int: liczba wierszy tabeli produkty.
    """
    # TODO: otwórz kursor w bloku with polaczenie.cursor() as kursor:
    # TODO: wykonaj kursor.execute("SELECT COUNT(*) FROM produkty")
    # TODO: wewnątrz with zwróć kursor.fetchone()[0]
    #       ([0] — fetchone daje krotkę, pamiętasz z tematu 14)
    pass


def zadanie_09_utworz_silnik(adres: str) -> Engine:
    """Buduje silnik SQLAlchemy dla podanego adresu bazy.

    Args:
        adres: URL bazy, np. "postgresql://anna:tajne@localhost/sklep"
            albo "sqlite:///C:/dane/test.db".

    Returns:
        Engine: silnik gotowy do użycia przez pandas.
    """
    # TODO: zwróć create_engine(adres)
    pass


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
    # TODO: wywołaj df.to_sql(nazwa_tabeli, silnik, index=False,
    #       if_exists="replace")
    #       (index=False — bez śmieciowej kolumny; replace — nadpisz)
    pass


def zadanie_11_czytaj_do_df(zapytanie: str, silnik: Engine) -> pd.DataFrame:
    """Wykonuje zapytanie SQL i zwraca wynik jako DataFrame.

    Args:
        zapytanie: zapytanie SELECT (SQL z tematu 14 działa bez zmian).
        silnik: silnik SQLAlchemy wskazujący bazę.

    Returns:
        pd.DataFrame: wynik zapytania jako tabela pandas.
    """
    # TODO: zwróć pd.read_sql(zapytanie, silnik)
    pass


def zadanie_12_raport_do_bazy(df: pd.DataFrame, silnik: Engine) -> int:
    """Buduje raport sumy sprzedaży per miasto i zapisuje go do tabeli raport.

    Args:
        df: tabela danych z kolumnami "miasto" i "sprzedaz".
        silnik: silnik SQLAlchemy wskazujący bazę.

    Returns:
        int: liczba wierszy zapisanego raportu (liczba unikalnych miast).
    """
    # TODO: zbuduj wynik łańcuchem znanym z tematów 9-10:
    #       df.groupby("miasto").agg({"sprzedaz": "sum"}).reset_index()
    # TODO: zapisz wynik przez .to_sql("raport", silnik, index=False,
    #       if_exists="replace")
    # TODO: zwróć len(wynik)
    pass
