import csv
from pathlib import Path

from csv_dict_reader_writer import (
    zadanie_01_wczytaj_wiersze,
    zadanie_02_wczytaj_naglowki,
    zadanie_03_policz_wiersze,
    zadanie_04_wartosc_z_kolumny,
    zadanie_05_zapisz_wiersze,
    zadanie_06_dopisz_wiersz,
    zadanie_07_filtruj_wiersze,
    zadanie_08_szukaj_wiersza,
    zadanie_09_zsumuj_kolumne,
    zadanie_10_wczytaj_bezpiecznie,
    zadanie_11_filtruj_i_zapisz,
    zadanie_12_zlicz_po_wartosci,
)


# --- zadanie_01 ---

def test_zadanie_01_zwraca_liste_slownikow(plik_csv: Path) -> None:
    """Co testuje: czy DictReader zwraca listę słowników z poprawnymi kluczami.
    Co udaje: nic — używam fixture plik_csv z 3 wierszami.
    Co sprawdzam: wynik to lista 3 słowników, pierwszy ma klucz 'imie' == 'Anna'.
    """
    wynik = zadanie_01_wczytaj_wiersze(str(plik_csv))
    assert len(wynik) == 3
    assert wynik[0]["imie"] == "Anna"


def test_zadanie_01_pusty_csv_zwraca_pusta_liste(plik_pusty_csv: Path) -> None:
    """Co testuje: zachowanie przy pliku z samym nagłówkiem i bez wierszy danych.
    Co udaje: nic — używam fixture plik_pusty_csv.
    Co sprawdzam: wynik == [] (pusta lista, nie None).
    """
    wynik = zadanie_01_wczytaj_wiersze(str(plik_pusty_csv))
    assert wynik == []


# --- zadanie_02 ---

def test_zadanie_02_zwraca_nazwy_kolumn(plik_csv: Path) -> None:
    """Co testuje: czy fieldnames odpowiadają nagłówkowi z pliku.
    Co udaje: nic — używam fixture plik_csv (nagłówek: imie,wiek,miasto).
    Co sprawdzam: wynik == ['imie', 'wiek', 'miasto'].
    """
    wynik = zadanie_02_wczytaj_naglowki(str(plik_csv))
    assert wynik == ['imie', 'wiek', 'miasto']


def test_zadanie_02_zwraca_liste(plik_csv: Path) -> None:
    """Co testuje: czy zwracany typ to list (nie dict_keys ani inne).
    Co udaje: nic — używam fixture plik_csv.
    Co sprawdzam: isinstance(wynik, list) is True.
    """
    wynik = zadanie_02_wczytaj_naglowki(str(plik_csv))
    assert isinstance(wynik, list) is True


# --- zadanie_03 ---

def test_zadanie_03_trzy_wiersze(plik_csv: Path) -> None:
    """Co testuje: czy funkcja poprawnie liczy wiersze danych (bez nagłówka).
    Co udaje: nic — używam fixture plik_csv (3 wiersze danych).
    Co sprawdzam: wynik == 3.
    """
    wynik = zadanie_03_policz_wiersze(str(plik_csv))
    assert wynik == 3


def test_zadanie_03_pusty_csv_zero(plik_pusty_csv: Path) -> None:
    """Co testuje: czy plik z samym nagłówkiem zwraca 0, nie 1.
    Co udaje: nic — używam fixture plik_pusty_csv.
    Co sprawdzam: wynik == 0.
    """
    wynik = zadanie_03_policz_wiersze(str(plik_pusty_csv))
    assert wynik == 0


# --- zadanie_04 ---

def test_zadanie_04_kolumna_imie(plik_csv: Path) -> None:
    """Co testuje: czy funkcja zbiera wszystkie wartości z kolumny 'imie'.
    Co udaje: nic — używam fixture plik_csv.
    Co sprawdzam: wynik == ['Anna', 'Piotr', 'Zofia'].
    """
    wynik = zadanie_04_wartosc_z_kolumny(str(plik_csv), "imie")
    assert wynik == ['Anna', 'Piotr', 'Zofia']


def test_zadanie_04_pusta_lista_dla_pustego_csv(plik_pusty_csv: Path) -> None:
    """Co testuje: pusta lista gdy brak wierszy danych.
    Co udaje: nic — używam fixture plik_pusty_csv.
    Co sprawdzam: wynik == [].
    """
    wynik = zadanie_04_wartosc_z_kolumny(str(plik_pusty_csv), "imie")
    assert wynik == []


# --- zadanie_05 ---

def test_zadanie_05_zapisuje_wiersze(tmp_path: Path) -> None:
    """Co testuje: czy plik wynikowy zawiera nagłówek i poprawne wiersze danych.
    Co udaje: nic — tworzę ścieżkę przez tmp_path, plik jeszcze nie istnieje.
    Co sprawdzam: wczytanie pliku przez DictReader daje listę z tymi samymi słownikami.
    """
    p = tmp_path / "dane.csv"
    wiersze = [
        {'imie': 'Anna', 'wiek': '30', 'miasto': 'Warszawa'},
        {'imie': 'Piotr', 'wiek': '25', 'miasto': 'Kraków'},
    ]
    fieldnames = ['imie', 'wiek', 'miasto']
    zadanie_05_zapisz_wiersze(str(p), wiersze, fieldnames)
    with open(str(p), "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        assert list(reader) == wiersze


def test_zadanie_05_pusty_plik_z_naglowkiem(tmp_path: Path) -> None:
    """Co testuje: pusta lista wierszy → plik zawiera tylko nagłówek.
    Co udaje: nic — tworzę ścieżkę przez tmp_path.
    Co sprawdzam: wczytanie pliku daje [] (pusta lista wierszy).
    """
    p = tmp_path / "dane.csv"
    wiersze = []
    fieldnames = ['imie', 'wiek', 'miasto']
    zadanie_05_zapisz_wiersze(str(p), wiersze, fieldnames)
    with open(str(p), "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        assert list(reader) == []


# --- zadanie_06 ---

def test_zadanie_06_dopisuje_wiersz(plik_csv: Path) -> None:
    """Co testuje: czy nowy wiersz pojawia się na końcu pliku po dopisaniu.
    Co udaje: nic — używam fixture plik_csv jako istniejący plik.
    Co sprawdzam: po dopisaniu len(wiersze) == 4 i ostatni wiersz to dopisany.
    """
    nowy_wiersz = {"imie": "Marek", "wiek": "28", "miasto": "Poznan"}
    fieldnames = ['imie', 'wiek', 'miasto']
    zadanie_06_dopisz_wiersz(str(plik_csv), nowy_wiersz, fieldnames)
    with open(str(plik_csv), "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        wiersze = list(reader)
        assert len(wiersze) == 4
        assert wiersze[-1] == nowy_wiersz


def test_zadanie_06_nie_duplikuje_naglowka(plik_csv: Path) -> None:
    """Co testuje: że tryb 'a' nie wstawia drugiego nagłówka w środku danych.
    Co udaje: nic — używam fixture plik_csv.
    Co sprawdzam: po dopisaniu nadal tylko 4 wiersze danych (nie 5 z nagłówkiem jako wiersz).
    """
    nowy_wiersz = {"imie": "Marek", "wiek": "28", "miasto": "Poznan"}
    fieldnames = ['imie', 'wiek', 'miasto']
    zadanie_06_dopisz_wiersz(str(plik_csv), nowy_wiersz, fieldnames)
    with open(str(plik_csv), "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        assert len(list(reader)) == 4


# --- zadanie_07 ---

def test_zadanie_07_filtruje_po_miescie(plik_csv: Path) -> None:
    """Co testuje: czy zwracane są tylko wiersze spełniające kryterium kolumna==wartość.
    Co udaje: nic — używam fixture plik_csv; 'Warszawa' jest w jednym wierszu.
    Co sprawdzam: wynik to lista z jednym słownikiem, gdzie imie == 'Anna'.
    """
    wynik = zadanie_07_filtruj_wiersze(
        str(plik_csv), "miasto", "Warszawa"
    )
    assert len(wynik) == 1
    assert wynik[0]["imie"] == "Anna"


def test_zadanie_07_brak_dopasowania_pusta_lista(plik_csv: Path) -> None:
    """Co testuje: pusta lista gdy żaden wiersz nie pasuje do kryterium.
    Co udaje: nic — używam fixture plik_csv; 'Gdynia' nie istnieje w danych.
    Co sprawdzam: wynik == [].
    """
    wynik = zadanie_07_filtruj_wiersze(
        str(plik_csv), "miasto", "Gdynia"
    )
    assert wynik == []


# --- zadanie_08 ---

def test_zadanie_08_zwraca_pierwszy_pasujacy(plik_csv: Path) -> None:
    """Co testuje: czy funkcja zwraca słownik pierwszego pasującego wiersza.
    Co udaje: nic — używam fixture plik_csv; 'Piotr' jest w drugim wierszu.
    Co sprawdzam: wynik['imie'] == 'Piotr' i wynik['wiek'] == '25'.
    """
    wynik = zadanie_08_szukaj_wiersza(str(plik_csv), "imie", "Piotr")
    assert wynik["imie"] == "Piotr"
    assert wynik["wiek"] == "25"


def test_zadanie_08_brak_wiersza_zwraca_none(plik_csv: Path) -> None:
    """Co testuje: kontrakt None gdy żaden wiersz nie spełnia kryterium.
    Co udaje: nic — używam fixture plik_csv; 'Marek' nie istnieje w danych.
    Co sprawdzam: wynik is None.
    """
    wynik = zadanie_08_szukaj_wiersza(str(plik_csv), "imie", "Marek")
    assert wynik is None



# --- zadanie_09 ---

def test_zadanie_09_suma_wieku(plik_csv: Path) -> None:
    """Co testuje: czy wartości str są konwertowane na int przed sumowaniem.
    Co udaje: nic — używam fixture plik_csv; wiek: 30 + 25 + 35 = 90.
    Co sprawdzam: wynik == 90.
    """
    wynik = zadanie_09_zsumuj_kolumne(str(plik_csv), "wiek")
    assert wynik == 90


def test_zadanie_09_pusty_csv_zwraca_zero(plik_pusty_csv: Path) -> None:
    """Co testuje: suma dla pliku bez wierszy danych to 0, nie błąd.
    Co udaje: nic — używam fixture plik_pusty_csv.
    Co sprawdzam: wynik == 0.
    """
    wynik = zadanie_09_zsumuj_kolumne(str(plik_pusty_csv), "wiek")
    assert wynik == 0


# --- zadanie_10 ---

def test_zadanie_10_istniejacy_plik(plik_csv: Path) -> None:
    """Co testuje: normalne czytanie gdy plik istnieje.
    Co udaje: nic — używam fixture plik_csv.
    Co sprawdzam: wynik to lista 3 słowników (nie None).
    """
    wynik = zadanie_10_wczytaj_bezpiecznie(str(plik_csv))
    assert len(wynik) == 3


def test_zadanie_10_brak_pliku_zwraca_none() -> None:
    """Co testuje: kontrakt None zamiast FileNotFoundError przy braku pliku.
    Co udaje: nic — używam ścieżki do pliku, który na pewno nie istnieje.
    Co sprawdzam: wynik is None.
    """
    wynik = zadanie_10_wczytaj_bezpiecznie("nieistniejący.csv")
    assert wynik is None


# --- zadanie_11 ---

def test_zadanie_11_filtruje_i_zapisuje(plik_csv: Path, tmp_path: Path) -> None:
    """Co testuje: czy pasujące wiersze trafiają do pliku wyjściowego, wynik to ich liczba.
    Co udaje: nic — używam plik_csv jako wejście, tmp_path jako cel.
    Co sprawdzam: wynik == 1 i plik wyjściowy zawiera jeden wiersz z 'Warszawa'.
    """
    cel = tmp_path / "dane.csv"
    wynik = zadanie_11_filtruj_i_zapisz(str(plik_csv), str(cel), "miasto", "Warszawa")
    assert wynik == 1
    with open(str(cel), "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        wiersze = list(reader)
        assert len(wiersze) == 1
        assert wiersze[0]["miasto"] == "Warszawa"


def test_zadanie_11_zero_gdy_brak_dopasowania(plik_csv: Path, tmp_path: Path) -> None:
    """Co testuje: zwraca 0 i tworzy plik z samym nagłówkiem gdy nic nie pasuje.
    Co udaje: nic — używam plik_csv, szukam 'Gdynia' (nie istnieje).
    Co sprawdzam: wynik == 0.
    """
    cel = tmp_path / "dane.csv"
    wynik = zadanie_11_filtruj_i_zapisz(str(plik_csv), str(cel), "miasto", "Gdynia")
    assert wynik == 0


# --- zadanie_12 ---

def test_zadanie_12_zlicza_po_miescie(plik_csv: Path) -> None:
    """Co testuje: czy każde unikalne miasto dostaje osobny klucz z liczbą wierszy.
    Co udaje: nic — używam fixture plik_csv (3 różne miasta, każde raz).
    Co sprawdzam: wynik == {'Warszawa': 1, 'Krakow': 1, 'Gdansk': 1}.
    """
    wynik = zadanie_12_zlicz_po_wartosci(str(plik_csv), "miasto")
    assert wynik == {'Warszawa': 1, 'Krakow': 1, "Gdansk": 1}


def test_zadanie_12_pusty_csv_zwraca_pusty_slownik(plik_pusty_csv: Path) -> None:
    """Co testuje: plik bez wierszy danych daje pusty słownik, nie błąd.
    Co udaje: nic — używam fixture plik_pusty_csv.
    Co sprawdzam: wynik == {}.
    """
    wynik = zadanie_12_zlicz_po_wartosci(str(plik_pusty_csv), "miasto")
    assert wynik == {}
