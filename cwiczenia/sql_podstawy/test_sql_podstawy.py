import sqlite3

import pytest

from sql_podstawy import (
    zadanie_01_utworz_tabele,
    zadanie_02_wstaw_pracownikow,
    zadanie_03_wszyscy_pracownicy,
    zadanie_04_imiona_z_warszawy,
    zadanie_05_pensje_malejaco,
    zadanie_06_najlepiej_oplacani,
    zadanie_07_liczba_pracownikow,
    zadanie_08_srednia_pensja,
    zadanie_09_suma_pensji_po_miescie,
    zadanie_10_miasta_z_trojka,
    zadanie_11_pracownicy_z_dzialami,
    zadanie_12_wszyscy_z_dzialami,
)


# --- zadanie_01 ---

def test_zadanie_01_tabela_istnieje(pusta_baza: sqlite3.Connection) -> None:
    """Co testuje: czy CREATE TABLE faktycznie tworzy tabelę pracownicy.
    Co udaje: bazę — fixture pusta_baza daje ulotną bazę w pamięci.
    Co sprawdzam: sqlite_master zawiera wpis o nazwie 'pracownicy'.
    """
    zadanie_01_utworz_tabele(pusta_baza)
    wynik = pusta_baza.execute(
        "SELECT name FROM sqlite_master WHERE name = 'pracownicy'"
    ).fetchone()
    assert wynik is not None


def test_zadanie_01_nowa_tabela_jest_pusta(
    pusta_baza: sqlite3.Connection,
) -> None:
    """Co testuje: czy świeżo utworzona tabela ma zero wierszy.
    Co udaje: bazę — fixture pusta_baza.
    Co sprawdzam: SELECT COUNT(*) FROM pracownicy daje 0.
    """
    zadanie_01_utworz_tabele(pusta_baza)
    wynik = pusta_baza.execute("SELECT COUNT(*) FROM pracownicy").fetchone()[0]
    assert wynik == 0


# --- zadanie_02 ---

def test_zadanie_02_wstawia_trzy_wiersze(
    baza_z_tabela: sqlite3.Connection,
) -> None:
    """Co testuje: czy INSERT wstawia dokładnie trzy wiersze.
    Co udaje: bazę — fixture baza_z_tabela (pusta tabela pracownicy).
    Co sprawdzam: SELECT COUNT(*) FROM pracownicy daje 3.
    """
    zadanie_02_wstaw_pracownikow(baza_z_tabela)
    wynik = baza_z_tabela.execute("SELECT COUNT(*) FROM pracownicy").fetchone()[0]
    assert wynik == 3


def test_zadanie_02_anna_jest_w_tabeli(
    baza_z_tabela: sqlite3.Connection,
) -> None:
    """Co testuje: czy wstawiony wiersz ma poprawne wartości kolumn.
    Co udaje: bazę — fixture baza_z_tabela.
    Co sprawdzam: wiersz z imieniem Anna ma miasto Warszawa i pensję 8000.
    """
    zadanie_02_wstaw_pracownikow(baza_z_tabela)
    wiersz = baza_z_tabela.execute(
        "SELECT miasto, pensja FROM pracownicy WHERE imie = 'Anna'"
    ).fetchone()
    assert wiersz == ('Warszawa', 8000)


# --- zadanie_03 ---

def test_zadanie_03_zwraca_piec_wierszy(
    baza_z_danymi: sqlite3.Connection,
) -> None:
    """Co testuje: czy SELECT * zwraca wszystkie wiersze tabeli.
    Co udaje: bazę — fixture baza_z_danymi (5 pracowników).
    Co sprawdzam: len(wynik) == 5.
    """
    wynik = zadanie_03_wszyscy_pracownicy(baza_z_danymi)
    assert len(wynik) == 5


def test_zadanie_03_wiersz_ma_wszystkie_kolumny(
    baza_z_danymi: sqlite3.Connection,
) -> None:
    """Co testuje: czy SELECT * zwraca komplet pięciu kolumn na wiersz.
    Co udaje: bazę — fixture baza_z_danymi.
    Co sprawdzam: pierwszy wiersz to pełna krotka
    (1, 'Anna', 'Warszawa', 8000, 1).
    """
    wynik = zadanie_03_wszyscy_pracownicy(baza_z_danymi)
    assert wynik[0] == (1, 'Anna', 'Warszawa', 8000, 1)


# --- zadanie_04 ---

def test_zadanie_04_trzy_osoby_z_warszawy(
    baza_z_danymi: sqlite3.Connection,
) -> None:
    """Co testuje: czy WHERE przepuszcza tylko wiersze z Warszawy.
    Co udaje: bazę — fixture baza_z_danymi (Anna, Zofia i Ewa z Warszawy).
    Co sprawdzam: wynik == [('Anna',), ('Zofia',), ('Ewa',)].
    """
    wynik = zadanie_04_imiona_z_warszawy(baza_z_danymi)
    assert wynik == [('Anna',), ('Zofia',), ('Ewa',)]


def test_zadanie_04_krotki_jednoelementowe(
    baza_z_danymi: sqlite3.Connection,
) -> None:
    """Co testuje: czy SELECT jednej kolumny daje krotki o długości 1.
    Co udaje: bazę — fixture baza_z_danymi.
    Co sprawdzam: len(wynik[0]) == 1 (samo imię, bez innych kolumn).
    """
    wynik = zadanie_04_imiona_z_warszawy(baza_z_danymi)
    assert len(wynik[0]) == 1


# --- zadanie_05 ---

def test_zadanie_05_sortuje_malejaco(
    baza_z_danymi: sqlite3.Connection,
) -> None:
    """Co testuje: czy ORDER BY pensja DESC daje pełny ranking od najwyższej.
    Co udaje: bazę — fixture baza_z_danymi.
    Co sprawdzam: wynik == [('Zofia', 9000), ('Anna', 8000), ('Ewa', 7000),
    ('Piotr', 6000), ('Marek', 5500)].
    """
    wynik = zadanie_05_pensje_malejaco(baza_z_danymi)
    assert wynik == [
        ('Zofia', 9000), ('Anna', 8000), ('Ewa', 7000), ('Piotr', 6000), ('Marek', 5500)
    ]


def test_zadanie_05_najwyzsza_pensja_pierwsza(
    baza_z_danymi: sqlite3.Connection,
) -> None:
    """Co testuje: czy pierwszy wiersz wyniku ma najwyższą pensję (9000).
    Co udaje: bazę — fixture baza_z_danymi.
    Co sprawdzam: wynik[0] == ('Zofia', 9000).
    """
    wynik = zadanie_05_pensje_malejaco(baza_z_danymi)
    assert wynik[0] == ('Zofia', 9000)


# --- zadanie_06 ---

def test_zadanie_06_zwraca_dokladnie_dwoje(
    baza_z_danymi: sqlite3.Connection,
) -> None:
    """Co testuje: czy LIMIT 2 ucina wynik do dwóch wierszy.
    Co udaje: bazę — fixture baza_z_danymi (5 pracowników).
    Co sprawdzam: len(wynik) == 2.
    """
    wynik = zadanie_06_najlepiej_oplacani(baza_z_danymi)
    assert len(wynik) == 2


def test_zadanie_06_to_zofia_i_anna(
    baza_z_danymi: sqlite3.Connection,
) -> None:
    """Co testuje: czy LIMIT działa PO sortowaniu (najwyższe pensje, nie
    pierwsze wiersze tabeli).
    Co udaje: bazę — fixture baza_z_danymi.
    Co sprawdzam: wynik == [('Zofia', 9000), ('Anna', 8000)].
    """
    wynik = zadanie_06_najlepiej_oplacani(baza_z_danymi)
    assert wynik == [('Zofia', 9000), ('Anna', 8000)]


# --- zadanie_07 ---

def test_zadanie_07_liczy_piec_osob(
    baza_z_danymi: sqlite3.Connection,
) -> None:
    """Co testuje: czy COUNT(*) zwraca liczbę wszystkich wierszy.
    Co udaje: bazę — fixture baza_z_danymi (5 pracowników).
    Co sprawdzam: wynik == 5.
    """
    wynik = zadanie_07_liczba_pracownikow(baza_z_danymi)
    assert wynik == 5


def test_zadanie_07_zwraca_int_nie_krotke(
    baza_z_danymi: sqlite3.Connection,
) -> None:
    """Co testuje: czy funkcja rozpakowała krotkę fetchone ([0]).
    Co udaje: bazę — fixture baza_z_danymi.
    Co sprawdzam: isinstance(wynik, int) is True (nie krotka (5,)).
    """
    wynik = zadanie_07_liczba_pracownikow(baza_z_danymi)
    assert isinstance(wynik, int) is True


# --- zadanie_08 ---

def test_zadanie_08_liczy_srednia(baza_z_danymi: sqlite3.Connection) -> None:
    """Co testuje: czy AVG(pensja) daje poprawną średnią.
    Co udaje: bazę — fixture baza_z_danymi
    ((8000+6000+9000+5500+7000)/5 = 7100.0).
    Co sprawdzam: wynik == pytest.approx(7100.0) — float wymaga approx
    (temat 13).
    """
    wynik = zadanie_08_srednia_pensja(baza_z_danymi)
    assert wynik == pytest.approx(7100.0)


def test_zadanie_08_zwraca_liczbe_nie_krotke(
    baza_z_danymi: sqlite3.Connection,
) -> None:
    """Co testuje: czy funkcja rozpakowała krotkę fetchone ([0]).
    Co udaje: bazę — fixture baza_z_danymi.
    Co sprawdzam: isinstance(wynik, float) is True.
    """
    wynik = zadanie_08_srednia_pensja(baza_z_danymi)
    assert isinstance(wynik, float) is True


# --- zadanie_09 ---

def test_zadanie_09_sumuje_per_miasto(
    baza_z_danymi: sqlite3.Connection,
) -> None:
    """Co testuje: czy GROUP BY + SUM daje sumę pensji w każdym mieście.
    Co udaje: bazę — fixture baza_z_danymi (Krakow: 6000+5500=11500,
    Warszawa: 8000+9000+7000=24000).
    Co sprawdzam: wynik == [('Krakow', 11500), ('Warszawa', 24000)]
    (alfabetycznie po ORDER BY miasto).
    """
    wynik = zadanie_09_suma_pensji_po_miescie(baza_z_danymi)
    assert wynik == [('Krakow', 11500), ('Warszawa', 24000)]


def test_zadanie_09_jeden_wiersz_na_miasto(
    baza_z_danymi: sqlite3.Connection,
) -> None:
    """Co testuje: czy grupowanie skleja 5 pracowników w 2 grupy-miasta.
    Co udaje: bazę — fixture baza_z_danymi (2 unikalne miasta).
    Co sprawdzam: len(wynik) == 2.
    """
    wynik = zadanie_09_suma_pensji_po_miescie(baza_z_danymi)
    assert len(wynik) == 2


# --- zadanie_10 ---

def test_zadanie_10_tylko_warszawa_przechodzi(
    baza_z_danymi: sqlite3.Connection,
) -> None:
    """Co testuje: czy HAVING COUNT(*) >= 3 odfiltrowuje Kraków (2 osoby).
    Co udaje: bazę — fixture baza_z_danymi (Warszawa: 3, Krakow: 2).
    Co sprawdzam: wynik == [('Warszawa', 3)].
    """
    wynik = zadanie_10_miasta_z_trojka(baza_z_danymi)
    assert wynik == [('Warszawa', 3)]


def test_zadanie_10_dokladnie_jedna_grupa(
    baza_z_danymi: sqlite3.Connection,
) -> None:
    """Co testuje: czy przez filtr HAVING przechodzi dokładnie jedna grupa.
    Co udaje: bazę — fixture baza_z_danymi.
    Co sprawdzam: len(wynik) == 1.
    """
    wynik = zadanie_10_miasta_z_trojka(baza_z_danymi)
    assert len(wynik) == 1


# --- zadanie_11 ---

def test_zadanie_11_laczy_z_nazwami_dzialow(
    baza_z_danymi: sqlite3.Connection,
) -> None:
    """Co testuje: czy INNER JOIN dokleja właściwe nazwy działów.
    Co udaje: bazę — fixture baza_z_danymi (Anna/IT, Piotr/IT, Zofia/HR,
    Ewa/IT).
    Co sprawdzam: wynik == [('Anna', 'IT'), ('Piotr', 'IT'),
    ('Zofia', 'HR'), ('Ewa', 'IT')].
    """
    wynik = zadanie_11_pracownicy_z_dzialami(baza_z_danymi)
    assert wynik == [('Anna', 'IT'), ('Piotr', 'IT'), ('Zofia', 'HR'), ('Ewa', 'IT')]


def test_zadanie_11_marek_bez_dzialu_wypada(
    baza_z_danymi: sqlite3.Connection,
) -> None:
    """Co testuje: czy INNER JOIN pomija pracownika z dzial_id NULL.
    Co udaje: bazę — fixture baza_z_danymi (Marek bez działu).
    Co sprawdzam: len(wynik) == 4 i Marek nie występuje w żadnej krotce.
    """
    wynik = zadanie_11_pracownicy_z_dzialami(baza_z_danymi)
    assert len(wynik) == 4
    lista = [wiersz[0] for wiersz in wynik]
    assert "Marek" not in lista


# --- zadanie_12 ---

def test_zadanie_12_wszyscy_obecni(
    baza_z_danymi: sqlite3.Connection,
) -> None:
    """Co testuje: czy LEFT JOIN zachowuje wszystkich pracowników (też Marka).
    Co udaje: bazę — fixture baza_z_danymi (5 pracowników, 1 bez działu).
    Co sprawdzam: len(wynik) == 5.
    """
    wynik = zadanie_12_wszyscy_z_dzialami(baza_z_danymi)
    assert len(wynik) == 5


def test_zadanie_12_marek_ma_none(
    baza_z_danymi: sqlite3.Connection,
) -> None:
    """Co testuje: czy pracownik bez działu dostaje None w kolumnie nazwy.
    Co udaje: bazę — fixture baza_z_danymi (Marek z dzial_id NULL).
    Co sprawdzam: krotka ('Marek', None) jest w wyniku.
    """
    wynik = zadanie_12_wszyscy_z_dzialami(baza_z_danymi)
    assert ('Marek', None) in wynik