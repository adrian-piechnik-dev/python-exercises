from pathlib import Path

import pandas as pd
from openpyxl import Workbook, load_workbook

from openpyxl_formatowanie import (
    zadanie_01_utworz_i_zapisz,
    zadanie_02_wczytaj_komorke,
    zadanie_03_pogrub_naglowki,
    zadanie_04_koloruj_czcionke,
    zadanie_05_wypelnij_tlo,
    zadanie_06_wysrodkuj_naglowki,
    zadanie_07_dodaj_obramowanie,
    zadanie_08_zamroz_naglowek,
    zadanie_09_ustaw_szerokosc,
    zadanie_10_zsumuj_kolumne_b,
    zadanie_11_zapisz_dataframe,
    zadanie_12_raport_sprzedazy,
)


# --- zadanie_01 ---

def test_zadanie_01_tworzy_plik_na_dysku(tmp_path: Path) -> None:
    """Co testuje: czy po wywołaniu funkcji plik .xlsx istnieje na dysku.
    Co udaje: nic — używam tmp_path jako cel zapisu.
    Co sprawdzam: ścieżka wskazuje istniejący plik (p.exists() is True).
    """
    p = tmp_path / "nowy.xlsx"
    zadanie_01_utworz_i_zapisz(str(p), "Raport")
    assert p.exists() is True


def test_zadanie_01_zapisuje_wartosc_i_zwraca_true(tmp_path: Path) -> None:
    """Co testuje: czy wartość trafia do A1 i funkcja zwraca True.
    Co udaje: nic — używam tmp_path jako cel zapisu.
    Co sprawdzam: wynik is True; po otwarciu pliku ws["A1"].value == "Raport".
    """
    p = tmp_path / "nowy.xlsx"
    wynik = zadanie_01_utworz_i_zapisz(str(p), "Raport")
    assert wynik is True


# --- zadanie_02 ---

def test_zadanie_02_odczytuje_naglowek(plik_xlsx: Path) -> None:
    """Co testuje: czy funkcja zwraca wartość tekstową komórki A1.
    Co udaje: nic — używam fixture plik_xlsx (A1 zawiera "miasto").
    Co sprawdzam: wynik == "miasto".
    """
    # TODO: wywołaj zadanie_02_wczytaj_komorke(str(plik_xlsx), "A1")
    # TODO: sprawdź wynik == "miasto"
    pass


def test_zadanie_02_odczytuje_liczbe(plik_xlsx: Path) -> None:
    """Co testuje: czy funkcja zwraca wartość liczbową (int, nie obiekt Cell).
    Co udaje: nic — używam fixture plik_xlsx (B2 zawiera 100).
    Co sprawdzam: wynik == 100.
    """
    # TODO: wywołaj zadanie_02_wczytaj_komorke(str(plik_xlsx), "B2")
    # TODO: sprawdź wynik == 100
    pass


# --- zadanie_03 ---

def test_zadanie_03_naglowki_pogrubione(plik_xlsx: Path) -> None:
    """Co testuje: czy po wywołaniu funkcji A1 i B1 mają pogrubioną czcionkę.
    Co udaje: nic — używam fixture plik_xlsx.
    Co sprawdzam: po ponownym otwarciu pliku font.bold is True dla A1 i B1.
    """
    # TODO: wywołaj zadanie_03_pogrub_naglowki(str(plik_xlsx))
    # TODO: otwórz plik przez load_workbook, pobierz ws = wb.active
    # TODO: sprawdź ws["A1"].font.bold is True
    # TODO: sprawdź ws["B1"].font.bold is True
    pass


def test_zadanie_03_zwraca_true(plik_xlsx: Path) -> None:
    """Co testuje: czy funkcja zwraca True po zapisie (kontrakt bool).
    Co udaje: nic — używam fixture plik_xlsx.
    Co sprawdzam: wynik is True.
    """
    # TODO: wywołaj zadanie_03_pogrub_naglowki(str(plik_xlsx)) i zapisz wynik
    # TODO: sprawdź wynik is True
    pass


# --- zadanie_04 ---

def test_zadanie_04_kolor_czcionki_ustawiony(plik_xlsx: Path) -> None:
    """Co testuje: czy komórka A1 dostała czerwoną czcionkę.
    Co udaje: nic — używam fixture plik_xlsx.
    Co sprawdzam: font.color.rgb kończy się na "FF0000" (przez doklejaną alfę).
    """
    # TODO: wywołaj zadanie_04_koloruj_czcionke(str(plik_xlsx), "A1", "FF0000")
    # TODO: otwórz plik przez load_workbook, pobierz ws = wb.active
    # TODO: sprawdź ws["A1"].font.color.rgb.endswith("FF0000") is True
    pass


def test_zadanie_04_zwraca_true(plik_xlsx: Path) -> None:
    """Co testuje: czy funkcja zwraca True po zapisie (kontrakt bool).
    Co udaje: nic — używam fixture plik_xlsx.
    Co sprawdzam: wynik is True.
    """
    # TODO: wywołaj zadanie_04_koloruj_czcionke(str(plik_xlsx), "A1", "FF0000")
    #       i zapisz wynik
    # TODO: sprawdź wynik is True
    pass


# --- zadanie_05 ---

def test_zadanie_05_tlo_wypelnione_kolorem(plik_xlsx: Path) -> None:
    """Co testuje: czy komórka A1 dostała żółte tło z pełnym wypełnieniem.
    Co udaje: nic — używam fixture plik_xlsx.
    Co sprawdzam: fill.start_color.rgb kończy się na "FFFF00"
    i fill.fill_type == "solid".
    """
    # TODO: wywołaj zadanie_05_wypelnij_tlo(str(plik_xlsx), "A1", "FFFF00")
    # TODO: otwórz plik przez load_workbook, pobierz ws = wb.active
    # TODO: sprawdź ws["A1"].fill.start_color.rgb.endswith("FFFF00") is True
    # TODO: sprawdź ws["A1"].fill.fill_type == "solid"
    pass


def test_zadanie_05_zwraca_true(plik_xlsx: Path) -> None:
    """Co testuje: czy funkcja zwraca True po zapisie (kontrakt bool).
    Co udaje: nic — używam fixture plik_xlsx.
    Co sprawdzam: wynik is True.
    """
    # TODO: wywołaj zadanie_05_wypelnij_tlo(str(plik_xlsx), "B1", "FFFF00")
    #       i zapisz wynik
    # TODO: sprawdź wynik is True
    pass


# --- zadanie_06 ---

def test_zadanie_06_naglowki_wysrodkowane(plik_xlsx: Path) -> None:
    """Co testuje: czy A1 i B1 mają wyśrodkowanie poziome i pionowe.
    Co udaje: nic — używam fixture plik_xlsx.
    Co sprawdzam: alignment.horizontal == "center"
    i alignment.vertical == "center" dla obu komórek.
    """
    # TODO: wywołaj zadanie_06_wysrodkuj_naglowki(str(plik_xlsx))
    # TODO: otwórz plik przez load_workbook, pobierz ws = wb.active
    # TODO: sprawdź ws["A1"].alignment.horizontal == "center"
    #       i ws["A1"].alignment.vertical == "center"
    # TODO: sprawdź to samo dla ws["B1"]
    pass


def test_zadanie_06_zwraca_true(plik_xlsx: Path) -> None:
    """Co testuje: czy funkcja zwraca True po zapisie (kontrakt bool).
    Co udaje: nic — używam fixture plik_xlsx.
    Co sprawdzam: wynik is True.
    """
    # TODO: wywołaj zadanie_06_wysrodkuj_naglowki(str(plik_xlsx)) i zapisz wynik
    # TODO: sprawdź wynik is True
    pass


# --- zadanie_07 ---

def test_zadanie_07_obramowanie_ze_wszystkich_stron(plik_xlsx: Path) -> None:
    """Co testuje: czy komórka A1 ma cienką ramkę z każdej z czterech stron.
    Co udaje: nic — używam fixture plik_xlsx.
    Co sprawdzam: border.left/right/top/bottom.style == "thin".
    """
    # TODO: wywołaj zadanie_07_dodaj_obramowanie(str(plik_xlsx), "A1")
    # TODO: otwórz plik przez load_workbook, pobierz ws = wb.active
    # TODO: sprawdź ws["A1"].border.left.style == "thin"
    # TODO: sprawdź to samo dla .right, .top i .bottom
    pass


def test_zadanie_07_zwraca_true(plik_xlsx: Path) -> None:
    """Co testuje: czy funkcja zwraca True po zapisie (kontrakt bool).
    Co udaje: nic — używam fixture plik_xlsx.
    Co sprawdzam: wynik is True.
    """
    # TODO: wywołaj zadanie_07_dodaj_obramowanie(str(plik_xlsx), "B2")
    #       i zapisz wynik
    # TODO: sprawdź wynik is True
    pass


# --- zadanie_08 ---

def test_zadanie_08_freeze_ustawiony_na_a2(plik_xlsx: Path) -> None:
    """Co testuje: czy arkusz ma zamrożony wiersz nagłówków.
    Co udaje: nic — używam fixture plik_xlsx.
    Co sprawdzam: ws.freeze_panes == "A2" po ponownym otwarciu pliku.
    """
    # TODO: wywołaj zadanie_08_zamroz_naglowek(str(plik_xlsx))
    # TODO: otwórz plik przez load_workbook, pobierz ws = wb.active
    # TODO: sprawdź ws.freeze_panes == "A2"
    pass


def test_zadanie_08_zwraca_true(plik_xlsx: Path) -> None:
    """Co testuje: czy funkcja zwraca True po zapisie (kontrakt bool).
    Co udaje: nic — używam fixture plik_xlsx.
    Co sprawdzam: wynik is True.
    """
    # TODO: wywołaj zadanie_08_zamroz_naglowek(str(plik_xlsx)) i zapisz wynik
    # TODO: sprawdź wynik is True
    pass


# --- zadanie_09 ---

def test_zadanie_09_szerokosc_kolumny_ustawiona(plik_xlsx: Path) -> None:
    """Co testuje: czy kolumna A dostała szerokość 25.
    Co udaje: nic — używam fixture plik_xlsx.
    Co sprawdzam: ws.column_dimensions["A"].width == 25 po otwarciu pliku.
    """
    # TODO: wywołaj zadanie_09_ustaw_szerokosc(str(plik_xlsx), "A", 25)
    # TODO: otwórz plik przez load_workbook, pobierz ws = wb.active
    # TODO: sprawdź ws.column_dimensions["A"].width == 25
    pass


def test_zadanie_09_zwraca_true(plik_xlsx: Path) -> None:
    """Co testuje: czy funkcja zwraca True po zapisie (kontrakt bool).
    Co udaje: nic — używam fixture plik_xlsx.
    Co sprawdzam: wynik is True.
    """
    # TODO: wywołaj zadanie_09_ustaw_szerokosc(str(plik_xlsx), "B", 30)
    #       i zapisz wynik
    # TODO: sprawdź wynik is True
    pass


# --- zadanie_10 ---

def test_zadanie_10_sumuje_kolumne_b(plik_xlsx: Path) -> None:
    """Co testuje: czy suma kolumny B pomija nagłówek i liczy tylko dane.
    Co udaje: nic — używam fixture plik_xlsx (100 + 200 + 300 = 600).
    Co sprawdzam: wynik == 600.
    """
    # TODO: wywołaj zadanie_10_zsumuj_kolumne_b(str(plik_xlsx))
    # TODO: sprawdź wynik == 600
    pass


def test_zadanie_10_same_naglowki_daja_zero(tmp_path: Path) -> None:
    """Co testuje: czy plik z samymi nagłówkami (bez wierszy danych) daje 0.
    Co udaje: nic — buduję własny plik przez Workbook i tmp_path.
    Co sprawdzam: wynik == 0 (a nie błąd ani None).
    """
    # TODO: przygotuj wb = Workbook(), ws = wb.active,
    #       ws.append(["miasto", "sprzedaz"]) — tylko nagłówki, zero danych
    # TODO: zapisz do p = tmp_path / "puste.xlsx" przez wb.save(str(p))
    # TODO: wywołaj zadanie_10_zsumuj_kolumne_b(str(p))
    # TODO: sprawdź wynik == 0
    pass


# --- zadanie_11 ---

def test_zadanie_11_plik_ma_naglowki_bez_indeksu(
    tmp_path: Path, df_sprzedaz: pd.DataFrame
) -> None:
    """Co testuje: czy plik zaczyna się od nagłówka "miasto" w A1 (bez kolumny indeksu).
    Co udaje: nic — używam fixture df_sprzedaz i tmp_path.
    Co sprawdzam: ws["A1"].value == "miasto" (indeks nie przesunął kolumn).
    """
    # TODO: przygotuj p = tmp_path / "dane.xlsx"
    # TODO: wywołaj zadanie_11_zapisz_dataframe(str(p), df_sprzedaz)
    # TODO: otwórz plik przez load_workbook, pobierz ws = wb.active
    # TODO: sprawdź ws["A1"].value == "miasto"
    pass


def test_zadanie_11_dwie_kolumny_i_true(
    tmp_path: Path, df_sprzedaz: pd.DataFrame
) -> None:
    """Co testuje: czy plik ma dokładnie 2 kolumny (index=False) i funkcja zwraca True.
    Co udaje: nic — używam fixture df_sprzedaz i tmp_path.
    Co sprawdzam: wynik is True i ws.max_column == 2.
    """
    # TODO: przygotuj p = tmp_path / "dane.xlsx"
    # TODO: wywołaj zadanie_11_zapisz_dataframe(str(p), df_sprzedaz) i zapisz wynik
    # TODO: sprawdź wynik is True
    # TODO: otwórz plik przez load_workbook, pobierz ws = wb.active
    # TODO: sprawdź ws.max_column == 2
    pass


# --- zadanie_12 ---

def test_zadanie_12_raport_ma_zsumowane_wartosci(
    tmp_path: Path, df_sprzedaz: pd.DataFrame
) -> None:
    """Co testuje: czy raport zawiera sprzedaż zsumowaną per miasto.
    Co udaje: nic — używam fixture df_sprzedaz (Krakow=200, Warszawa=100+300=400;
    groupby sortuje grupy alfabetycznie, więc Krakow w wierszu 2, Warszawa w 3).
    Co sprawdzam: A2=="Krakow", B2==200, A3=="Warszawa", B3==400.
    """
    # TODO: przygotuj p = tmp_path / "raport.xlsx"
    # TODO: wywołaj zadanie_12_raport_sprzedazy(str(p), df_sprzedaz)
    # TODO: otwórz plik przez load_workbook, pobierz ws = wb.active
    # TODO: sprawdź ws["A2"].value == "Krakow" i ws["B2"].value == 200
    # TODO: sprawdź ws["A3"].value == "Warszawa" i ws["B3"].value == 400
    pass


def test_zadanie_12_naglowek_pogrubiony_i_zamrozony(
    tmp_path: Path, df_sprzedaz: pd.DataFrame
) -> None:
    """Co testuje: czy raport ma pogrubione nagłówki, zamrożony wiersz 1
    i funkcja zwraca True.
    Co udaje: nic — używam fixture df_sprzedaz i tmp_path.
    Co sprawdzam: wynik is True, font.bold is True dla A1 i B1,
    ws.freeze_panes == "A2".
    """
    # TODO: przygotuj p = tmp_path / "raport.xlsx"
    # TODO: wywołaj zadanie_12_raport_sprzedazy(str(p), df_sprzedaz) i zapisz wynik
    # TODO: sprawdź wynik is True
    # TODO: otwórz plik przez load_workbook, pobierz ws = wb.active
    # TODO: sprawdź ws["A1"].font.bold is True i ws["B1"].font.bold is True
    # TODO: sprawdź ws.freeze_panes == "A2"
    pass
