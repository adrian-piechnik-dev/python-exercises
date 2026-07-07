from pathlib import Path

import pytest

from import_try_except_pathlib import (
    zadanie_01_podziel_bezpiecznie,
    zadanie_02_parsuj_int,
    zadanie_03_parsuj_float,
    zadanie_04_pobierz_z_listy,
    zadanie_05_dwa_wyjatki,
    zadanie_06_nazwa_pliku,
    zadanie_07_rozszerzenie,
    zadanie_08_katalog_nadrzedny,
    zadanie_09_polacz_sciezki,
    zadanie_10_zmien_rozszerzenie,
    zadanie_11_parsuj_config,
    zadanie_12_wczytaj_config,
)


# --- zadanie 01 ---

def test_zadanie_01_normalne_dzielenie():
    assert zadanie_01_podziel_bezpiecznie(10, 2) == 5


def test_zadanie_01_dzielenie_przez_zero_zwraca_none():
    assert zadanie_01_podziel_bezpiecznie(10, 0) is None


def test_zadanie_01_dzielna_zero():
    assert zadanie_01_podziel_bezpiecznie(0, 5) == 0


# --- zadanie 02 ---

def test_zadanie_02_poprawny_int():
    assert zadanie_02_parsuj_int("42") == 42


def test_zadanie_02_niepoprawny_tekst_zwraca_none():
    assert zadanie_02_parsuj_int("abc") is None


def test_zadanie_02_ujemna_liczba():
    assert zadanie_02_parsuj_int("-7") == -7


# --- zadanie 03 ---

def test_zadanie_03_poprawny_float():
    assert zadanie_03_parsuj_float("3.14") == pytest.approx(3.14)


def test_zadanie_03_niepoprawny_tekst_zwraca_none():
    assert zadanie_03_parsuj_float("xyz") is None


def test_zadanie_03_ujemny_float():
    assert zadanie_03_parsuj_float("-1.5") == pytest.approx(-1.5)


# --- zadanie 04 ---

def test_zadanie_04_poprawny_indeks():
    assert zadanie_04_pobierz_z_listy([1, 2, 3], 0) == 1


def test_zadanie_04_indeks_poza_zakresem_zwraca_none():
    assert zadanie_04_pobierz_z_listy([1, 2, 3], 10) is None


def test_zadanie_04_ujemny_indeks():
    assert zadanie_04_pobierz_z_listy([1, 2, 3], -1) == 3


# --- zadanie 05 ---

def test_zadanie_05_poprawne_dzielenie():
    assert zadanie_05_dwa_wyjatki("6.0", 2) == pytest.approx(3.0)


def test_zadanie_05_zly_tekst_zwraca_none():
    assert zadanie_05_dwa_wyjatki("abc", 2) is None


def test_zadanie_05_dzielenie_przez_zero_zwraca_none():
    assert zadanie_05_dwa_wyjatki("6.0", 0) is None


# --- zadanie 06 ---

def test_zadanie_06_sciezka_absolutna():
    assert zadanie_06_nazwa_pliku("/dane/raport.csv") == "raport.csv"


def test_zadanie_06_sama_nazwa():
    assert zadanie_06_nazwa_pliku("plik.txt") == "plik.txt"


def test_zadanie_06_zagniezdzona_sciezka():
    assert zadanie_06_nazwa_pliku("/a/b/c.json") == "c.json"


# --- zadanie 07 ---

def test_zadanie_07_rozszerzenie_csv():
    assert zadanie_07_rozszerzenie("raport.csv") == ".csv"


def test_zadanie_07_rozszerzenie_txt():
    assert zadanie_07_rozszerzenie("plik.txt") == ".txt"


def test_zadanie_07_brak_rozszerzenia():
    assert zadanie_07_rozszerzenie("README") == ""


# --- zadanie 08 ---

def test_zadanie_08_jeden_poziom():
    wynik = zadanie_08_katalog_nadrzedny("katalog/plik.txt")
    assert Path(wynik) == Path("katalog")


def test_zadanie_08_dwa_poziomy():
    wynik = zadanie_08_katalog_nadrzedny("a/b/c.csv")
    assert Path(wynik) == Path("a/b")


def test_zadanie_08_sama_nazwa_pliku():
    wynik = zadanie_08_katalog_nadrzedny("plik.txt")
    assert Path(wynik) == Path(".")


# --- zadanie 09 ---

def test_zadanie_09_prosty():
    wynik = zadanie_09_polacz_sciezki("dane", "raport.csv")
    assert Path(wynik) == Path("dane") / "raport.csv"


def test_zadanie_09_zagniezdzone():
    wynik = zadanie_09_polacz_sciezki("a/b", "c.txt")
    assert Path(wynik) == Path("a/b") / "c.txt"


def test_zadanie_09_biezacy_katalog():
    wynik = zadanie_09_polacz_sciezki(".", "test.py")
    assert Path(wynik) == Path(".") / "test.py"


# --- zadanie 10 ---

def test_zadanie_10_csv_na_txt():
    wynik = zadanie_10_zmien_rozszerzenie("raport.csv", ".txt")
    assert Path(wynik) == Path("raport.txt")


def test_zadanie_10_zagniezdzona_sciezka():
    wynik = zadanie_10_zmien_rozszerzenie("dane/plik.py", ".json")
    assert Path(wynik) == Path("dane/plik.json")


def test_zadanie_10_brak_rozszerzenia():
    wynik = zadanie_10_zmien_rozszerzenie("README", ".md")
    assert Path(wynik) == Path("README.md")


# --- zadanie 11 ---

def test_zadanie_11_typowy():
    wynik = zadanie_11_parsuj_config(["host=localhost", "port=8080"])
    assert wynik == {"host": "localhost", "port": "8080"}


def test_zadanie_11_pusta_lista():
    assert zadanie_11_parsuj_config([]) == {}


def test_zadanie_11_pomija_linie_bez_rownosci():
    wynik = zadanie_11_parsuj_config(["bad_line", "ok=val"])
    assert wynik == {"ok": "val"}


def test_zadanie_11_obcina_spacje():
    wynik = zadanie_11_parsuj_config(["  key = value  "])
    assert wynik == {"key": "value"}


# --- zadanie 12 ---

def test_zadanie_12_czyta_plik(plik_config: Path):
    wynik = zadanie_12_wczytaj_config(str(plik_config))
    assert wynik == {"host": "localhost", "port": "8080", "user": "admin"}


def test_zadanie_12_brak_pliku_zwraca_pusty_slownik():
    assert zadanie_12_wczytaj_config("/nieistniejacy/plik.txt") == {}


def test_zadanie_12_plik_tylko_ze_zlymi_liniami(tmp_path: Path):
    p = tmp_path / "empty_config.txt"
    p.write_text("komentarz\ninne_smieci\n", encoding="utf-8")
    assert zadanie_12_wczytaj_config(str(p)) == {}
