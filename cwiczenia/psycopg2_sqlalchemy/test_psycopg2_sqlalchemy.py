import pandas as pd
import pytest
import psycopg2
from sqlalchemy.engine import Engine

from conftest import FakeConnection
from psycopg2_sqlalchemy import (
    zadanie_01_polacz,
    zadanie_02_utworz_tabele,
    zadanie_03_wstaw_produkt,
    zadanie_04_wstaw_wiele,
    zadanie_05_wszystkie_produkty,
    zadanie_06_znajdz_produkt,
    zadanie_07_polacz_bezpiecznie,
    zadanie_08_policz_produkty,
    zadanie_09_utworz_silnik,
    zadanie_10_df_do_bazy,
    zadanie_11_czytaj_do_df,
    zadanie_12_raport_do_bazy,
)


# --- zadanie_01 ---

def test_zadanie_01_przekazuje_dane_logowania(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Co testuje: czy funkcja przekazuje host/bazę/login/hasło do connect.
    Co udaje: psycopg2.connect — zamiennik ZAPISUJE otrzymane argumenty
    i zwraca FakeConnection().
    Co sprawdzam: zapisane argumenty == ("localhost", "sklep", "anna", "tajne").
    """
    # TODO: przygotuj pustą listę zapamietane = []
    # TODO: przygotuj zamiennik:
    #       def podmieniony_connect(host=None, dbname=None,
    #                               user=None, password=None):
    #           zapamietane.append((host, dbname, user, password))
    #           return FakeConnection()
    # TODO: podmień: monkeypatch.setattr(
    #           "psycopg2_sqlalchemy.psycopg2.connect", podmieniony_connect)
    # TODO: wywołaj zadanie_01_polacz("localhost", "sklep", "anna", "tajne")
    # TODO: sprawdź zapamietane[0] == ("localhost", "sklep", "anna", "tajne")
    pass


def test_zadanie_01_zwraca_polaczenie(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Co testuje: czy funkcja zwraca to, co dał psycopg2.connect.
    Co udaje: psycopg2.connect — zwraca konkretną atrapę FakeConnection.
    Co sprawdzam: wynik is ta_sama_atrapa.
    """
    # TODO: przygotuj atrapa = FakeConnection()
    # TODO: przygotuj zamiennik connect zwracający atrapa
    # TODO: podmień "psycopg2_sqlalchemy.psycopg2.connect"
    # TODO: wywołaj zadanie_01_polacz("localhost", "sklep", "anna", "tajne")
    # TODO: sprawdź wynik is atrapa
    pass


# --- zadanie_02 ---

def test_zadanie_02_wysyla_create_table(
) -> None:
    """Co testuje: czy funkcja wysyła zapytanie CREATE TABLE produkty.
    Co udaje: połączenie — FakeConnection z kursorem-szpiegiem.
    Co sprawdzam: zapisany SQL zawiera "CREATE TABLE produkty".
    """
    # TODO: przygotuj polaczenie = FakeConnection()
    # TODO: wywołaj zadanie_02_utworz_tabele(polaczenie)
    # TODO: odbierz (sql, parametry) = polaczenie.kursor.wykonane[0]
    # TODO: sprawdź "CREATE TABLE produkty" in sql
    pass


def test_zadanie_02_zatwierdza_zmiany(
) -> None:
    """Co testuje: czy po CREATE TABLE następuje commit (bez niego zmiany
    przepadną).
    Co udaje: połączenie — FakeConnection zliczające commity.
    Co sprawdzam: polaczenie.liczba_commitow == 1.
    """
    # TODO: przygotuj polaczenie = FakeConnection()
    # TODO: wywołaj zadanie_02_utworz_tabele(polaczenie)
    # TODO: sprawdź polaczenie.liczba_commitow == 1
    pass


# --- zadanie_03 ---

def test_zadanie_03_uzywa_zaslepek_i_parametrow(
) -> None:
    """Co testuje: czy INSERT idzie przez %s z parametrami OSOBNO (nie f-string).
    Co udaje: połączenie — FakeConnection z kursorem-szpiegiem.
    Co sprawdzam: SQL zawiera "%s", a parametry == ("Klawiatura", 99.0);
    wartości NIE są wklejone w tekst zapytania.
    """
    # TODO: przygotuj polaczenie = FakeConnection()
    # TODO: wywołaj zadanie_03_wstaw_produkt(polaczenie, "Klawiatura", 99.0)
    # TODO: odbierz (sql, parametry) = polaczenie.kursor.wykonane[0]
    # TODO: sprawdź "%s" in sql
    # TODO: sprawdź parametry == ("Klawiatura", 99.0)
    # TODO: sprawdź "Klawiatura" not in sql (wartość nie sklejona w SQL!)
    pass


def test_zadanie_03_zatwierdza_zmiany(
) -> None:
    """Co testuje: czy po INSERT następuje commit.
    Co udaje: połączenie — FakeConnection zliczające commity.
    Co sprawdzam: polaczenie.liczba_commitow == 1.
    """
    # TODO: przygotuj polaczenie = FakeConnection()
    # TODO: wywołaj zadanie_03_wstaw_produkt(polaczenie, "Mysz", 49.0)
    # TODO: sprawdź polaczenie.liczba_commitow == 1
    pass


# --- zadanie_04 ---

def test_zadanie_04_uzywa_executemany(
) -> None:
    """Co testuje: czy wstawianie hurtowe idzie przez executemany z całą listą.
    Co udaje: połączenie — FakeConnection z kursorem-szpiegiem.
    Co sprawdzam: wykonane_wiele zawiera zapis z listą trzech krotek.
    """
    # TODO: przygotuj polaczenie = FakeConnection()
    # TODO: przygotuj produkty = [("Klawiatura", 99.0), ("Mysz", 49.0),
    #       ("Monitor", 899.0)]
    # TODO: wywołaj zadanie_04_wstaw_wiele(polaczenie, produkty)
    # TODO: odbierz (sql, lista) = polaczenie.kursor.wykonane_wiele[0]
    # TODO: sprawdź "%s" in sql i lista == produkty
    pass


def test_zadanie_04_zatwierdza_raz(
) -> None:
    """Co testuje: czy hurtowe wstawienie kończy się JEDNYM commitem.
    Co udaje: połączenie — FakeConnection zliczające commity.
    Co sprawdzam: polaczenie.liczba_commitow == 1 (nie po jednym na wiersz).
    """
    # TODO: przygotuj polaczenie = FakeConnection()
    # TODO: wywołaj zadanie_04_wstaw_wiele(polaczenie, [("Mysz", 49.0)])
    # TODO: sprawdź polaczenie.liczba_commitow == 1
    pass


# --- zadanie_05 ---

def test_zadanie_05_zwraca_wiersze_z_kursora(
) -> None:
    """Co testuje: czy funkcja zwraca to, co dał fetchall.
    Co udaje: połączenie — FakeConnection z zaprogramowanymi 2 wierszami.
    Co sprawdzam: wynik == [(1, "Klawiatura", 99.0), (2, "Mysz", 49.0)].
    """
    # TODO: przygotuj wiersze = [(1, "Klawiatura", 99.0), (2, "Mysz", 49.0)]
    # TODO: przygotuj polaczenie = FakeConnection(wiersze)
    # TODO: wywołaj zadanie_05_wszystkie_produkty(polaczenie)
    # TODO: sprawdź wynik == wiersze
    pass


def test_zadanie_05_wysyla_select(
) -> None:
    """Co testuje: czy funkcja wysyła zapytanie SELECT do tabeli produkty.
    Co udaje: połączenie — FakeConnection z kursorem-szpiegiem.
    Co sprawdzam: zapisany SQL zawiera "SELECT" i "produkty".
    """
    # TODO: przygotuj polaczenie = FakeConnection()
    # TODO: wywołaj zadanie_05_wszystkie_produkty(polaczenie)
    # TODO: odbierz (sql, parametry) = polaczenie.kursor.wykonane[0]
    # TODO: sprawdź "SELECT" in sql i "produkty" in sql
    pass


# --- zadanie_06 ---

def test_zadanie_06_zwraca_znaleziony_wiersz(
) -> None:
    """Co testuje: czy funkcja zwraca pierwszy pasujący wiersz.
    Co udaje: połączenie — FakeConnection z jednym zaprogramowanym wierszem.
    Co sprawdzam: wynik == (1, "Klawiatura", 99.0) i parametry == ("Klawiatura",).
    """
    # TODO: przygotuj polaczenie = FakeConnection([(1, "Klawiatura", 99.0)])
    # TODO: wywołaj zadanie_06_znajdz_produkt(polaczenie, "Klawiatura")
    # TODO: sprawdź wynik == (1, "Klawiatura", 99.0)
    # TODO: odbierz (sql, parametry) = polaczenie.kursor.wykonane[0]
    # TODO: sprawdź parametry == ("Klawiatura",) — krotka jednoelementowa
    pass


def test_zadanie_06_brak_produktu_zwraca_none(
) -> None:
    """Co testuje: kontrakt None, gdy zapytanie nic nie znajduje.
    Co udaje: połączenie — FakeConnection bez wierszy (fetchone da None).
    Co sprawdzam: wynik is None.
    """
    # TODO: przygotuj polaczenie = FakeConnection()  (bez wierszy)
    # TODO: wywołaj zadanie_06_znajdz_produkt(polaczenie, "Drukarka")
    # TODO: sprawdź wynik is None
    pass


# --- zadanie_07 ---

def test_zadanie_07_sukces_zwraca_polaczenie(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Co testuje: czy przy udanym połączeniu funkcja zwraca je dalej.
    Co udaje: psycopg2.connect — zwraca konkretną atrapę FakeConnection.
    Co sprawdzam: wynik is ta_sama_atrapa (nie None).
    """
    # TODO: przygotuj atrapa = FakeConnection()
    # TODO: przygotuj zamiennik connect zwracający atrapa
    # TODO: podmień "psycopg2_sqlalchemy.psycopg2.connect"
    # TODO: wywołaj zadanie_07_polacz_bezpiecznie(
    #           "localhost", "sklep", "anna", "tajne")
    # TODO: sprawdź wynik is atrapa
    pass


def test_zadanie_07_blad_bazy_zwraca_none(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Co testuje: kontrakt None przy odmowie serwera (try/except z tematu 4).
    Co udaje: psycopg2.connect — RZUCA psycopg2.OperationalError
    (dziecko psycopg2.Error), jak przy wyłączonym serwerze.
    Co sprawdzam: wynik is None (wyjątek złapany w funkcji).
    """
    # TODO: przygotuj zamiennik, który zamiast return robi:
    #       raise psycopg2.OperationalError("serwer nie odpowiada")
    # TODO: podmień "psycopg2_sqlalchemy.psycopg2.connect"
    # TODO: wywołaj zadanie_07_polacz_bezpiecznie(
    #           "localhost", "sklep", "anna", "tajne")
    # TODO: sprawdź wynik is None
    pass


# --- zadanie_08 ---

def test_zadanie_08_zwraca_liczbe(
) -> None:
    """Co testuje: czy funkcja rozpakowuje wynik COUNT z krotki fetchone.
    Co udaje: połączenie — FakeConnection z wierszem (7,) (tak COUNT wraca
    z bazy).
    Co sprawdzam: wynik == 7 i isinstance(wynik, int) is True.
    """
    # TODO: przygotuj polaczenie = FakeConnection([(7,)])
    # TODO: wywołaj zadanie_08_policz_produkty(polaczenie)
    # TODO: sprawdź wynik == 7
    # TODO: sprawdź isinstance(wynik, int) is True
    pass


def test_zadanie_08_wysyla_count(
) -> None:
    """Co testuje: czy funkcja wysyła zapytanie z COUNT(*).
    Co udaje: połączenie — FakeConnection z wierszem (0,).
    Co sprawdzam: zapisany SQL zawiera "COUNT(*)".
    """
    # TODO: przygotuj polaczenie = FakeConnection([(0,)])
    # TODO: wywołaj zadanie_08_policz_produkty(polaczenie)
    # TODO: odbierz (sql, parametry) = polaczenie.kursor.wykonane[0]
    # TODO: sprawdź "COUNT(*)" in sql
    pass


# --- zadanie_09 ---

def test_zadanie_09_zwraca_engine(tmp_path) -> None:
    """Co testuje: czy funkcja buduje prawdziwy silnik SQLAlchemy.
    Co udaje: nic — sqlite w pliku tymczasowym to prawdziwa baza.
    Co sprawdzam: isinstance(wynik, Engine) is True.
    """
    # TODO: przygotuj adres = f"sqlite:///{tmp_path / 'test.db'}"
    # TODO: wywołaj zadanie_09_utworz_silnik(adres)
    # TODO: sprawdź isinstance(wynik, Engine) is True
    pass


def test_zadanie_09_silnik_dziala_z_pandas(tmp_path) -> None:
    """Co testuje: czy zwrócony silnik nadaje się do pracy z pandas.
    Co udaje: nic — prawdziwy sqlite w pliku tymczasowym.
    Co sprawdzam: to_sql + read_sql na tym silniku dają z powrotem 2 wiersze.
    """
    # TODO: przygotuj adres = f"sqlite:///{tmp_path / 'test.db'}"
    # TODO: wywołaj zadanie_09_utworz_silnik(adres) i zapisz jako silnik
    # TODO: przygotuj df = pd.DataFrame({"x": [1, 2]})
    # TODO: zapisz df.to_sql("proba", silnik, index=False)
    # TODO: wczytaj z powrotem pd.read_sql("SELECT * FROM proba", silnik)
    # TODO: sprawdź len(wczytany) == 2
    pass


# --- zadanie_10 ---

def test_zadanie_10_tabela_powstaje_w_bazie(
    silnik_sqlite: Engine,
) -> None:
    """Co testuje: czy DataFrame ląduje w bazie jako tabela o podanej nazwie.
    Co udaje: nic — fixture silnik_sqlite to prawdziwa baza w pliku tmp.
    Co sprawdzam: read_sql z tej tabeli zwraca 3 wiersze i kolumnę "miasto".
    """
    # TODO: przygotuj df = pd.DataFrame({
    #           "miasto": ["Warszawa", "Krakow", "Warszawa"],
    #           "sprzedaz": [100, 200, 300],
    #       })
    # TODO: wywołaj zadanie_10_df_do_bazy(df, "sprzedaz", silnik_sqlite)
    # TODO: wczytaj pd.read_sql("SELECT * FROM sprzedaz", silnik_sqlite)
    # TODO: sprawdź len(wczytany) == 3
    # TODO: sprawdź "miasto" in wczytany.columns
    pass


def test_zadanie_10_nadpisuje_istniejaca_tabele(
    silnik_sqlite: Engine,
) -> None:
    """Co testuje: czy if_exists="replace" zastępuje starą tabelę nową.
    Co udaje: nic — fixture silnik_sqlite.
    Co sprawdzam: po dwóch zapisach w tabeli są dane z DRUGIEGO zapisu
    (1 wiersz, nie 3+1).
    """
    # TODO: przygotuj df_stary = pd.DataFrame({"miasto": ["A", "B", "C"],
    #       "sprzedaz": [1, 2, 3]})
    # TODO: przygotuj df_nowy = pd.DataFrame({"miasto": ["Gdansk"],
    #       "sprzedaz": [999]})
    # TODO: wywołaj zadanie_10_df_do_bazy dwa razy: najpierw z df_stary,
    #       potem z df_nowy (ta sama nazwa tabeli "sprzedaz")
    # TODO: wczytaj tabelę przez read_sql
    # TODO: sprawdź len(wczytany) == 1
    pass


# --- zadanie_11 ---

def test_zadanie_11_zwraca_dataframe(silnik_sqlite: Engine) -> None:
    """Co testuje: czy zapytanie wraca jako DataFrame z danymi.
    Co udaje: nic — najpierw wkładam dane do prawdziwej bazy przez to_sql.
    Co sprawdzam: isinstance(wynik, pd.DataFrame) i len(wynik) == 2.
    """
    # TODO: przygotuj dane w bazie: pd.DataFrame({"nazwa": ["Mysz",
    #       "Monitor"], "cena": [49, 899]}).to_sql("produkty",
    #       silnik_sqlite, index=False)
    # TODO: wywołaj zadanie_11_czytaj_do_df(
    #           "SELECT * FROM produkty", silnik_sqlite)
    # TODO: sprawdź isinstance(wynik, pd.DataFrame) is True
    # TODO: sprawdź len(wynik) == 2
    pass


def test_zadanie_11_dziala_z_where(silnik_sqlite: Engine) -> None:
    """Co testuje: czy SQL z WHERE (temat 14) filtruje wiersze w read_sql.
    Co udaje: nic — dane w prawdziwej bazie sqlite.
    Co sprawdzam: zapytanie z WHERE cena > 100 zwraca 1 wiersz (Monitor).
    """
    # TODO: przygotuj dane jak w teście wyżej (Mysz/49, Monitor/899)
    # TODO: wywołaj zadanie_11_czytaj_do_df(
    #           "SELECT * FROM produkty WHERE cena > 100", silnik_sqlite)
    # TODO: sprawdź len(wynik) == 1
    # TODO: sprawdź wynik["nazwa"].tolist() == ["Monitor"]
    pass


# --- zadanie_12 ---

def test_zadanie_12_raport_w_bazie(silnik_sqlite: Engine) -> None:
    """Co testuje: czy zagregowany raport (groupby z tematu 9) ląduje w tabeli
    raport.
    Co udaje: nic — prawdziwa baza sqlite z fixture.
    Co sprawdzam: tabela raport ma 2 wiersze (Krakow 200, Warszawa 400 —
    groupby sortuje alfabetycznie).
    """
    # TODO: przygotuj df = pd.DataFrame({
    #           "miasto": ["Warszawa", "Krakow", "Warszawa"],
    #           "sprzedaz": [100, 200, 300],
    #       })
    # TODO: wywołaj zadanie_12_raport_do_bazy(df, silnik_sqlite)
    # TODO: wczytaj pd.read_sql("SELECT * FROM raport", silnik_sqlite)
    # TODO: sprawdź len(wczytany) == 2
    # TODO: sprawdź wczytany["sprzedaz"].tolist() == [200, 400]
    pass


def test_zadanie_12_zwraca_liczbe_wierszy_raportu(
    silnik_sqlite: Engine,
) -> None:
    """Co testuje: czy funkcja zwraca liczbę wierszy raportu (unikalnych miast).
    Co udaje: nic — prawdziwa baza sqlite z fixture.
    Co sprawdzam: wynik == 2 dla danych z dwoma miastami.
    """
    # TODO: przygotuj df jak w teście wyżej (3 wiersze, 2 miasta)
    # TODO: wywołaj zadanie_12_raport_do_bazy(df, silnik_sqlite) i zapisz wynik
    # TODO: sprawdź wynik == 2
    pass
