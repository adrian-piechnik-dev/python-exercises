from listy_petle import (
    zadanie_01_policz_elementy,
    zadanie_02_suma_liczb,
    zadanie_03_podwoj_elementy,
    zadanie_04_zbierz_parzyste,
    zadanie_05_maksimum_listy,
    zadanie_06_etykiety_z_indeksem,
    zadanie_07_polacz_w_pary,
    zadanie_08_kwadraty,
    zadanie_09_tylko_krotkie,
    zadanie_10_wielkie_litery,
    zadanie_11_znajdz_pierwsza_ujemna,
    zadanie_12_klasyfikuj_liczby,
)


# --- zadanie_01 ---

def test_zadanie_01_policz_elementy_trzy():
    assert zadanie_01_policz_elementy([1, 2, 3]) == 3


def test_zadanie_01_policz_elementy_pusta():
    assert zadanie_01_policz_elementy([]) == 0


def test_zadanie_01_policz_elementy_jeden():
    assert zadanie_01_policz_elementy([42]) == 1


# --- zadanie_02 ---

def test_zadanie_02_suma_liczb_dodatnie():
    assert zadanie_02_suma_liczb([1, 2, 3]) == 6


def test_zadanie_02_suma_liczb_pusta():
    assert zadanie_02_suma_liczb([]) == 0


def test_zadanie_02_suma_liczb_ujemne_i_dodatnie():
    assert zadanie_02_suma_liczb([-1, 1, 0]) == 0


# --- zadanie_03 ---

def test_zadanie_03_podwoj_elementy_typowy():
    assert zadanie_03_podwoj_elementy([1, 2, 3]) == [2, 4, 6]


def test_zadanie_03_podwoj_elementy_pusta():
    assert zadanie_03_podwoj_elementy([]) == []


def test_zadanie_03_podwoj_elementy_z_zerem_i_ujemna():
    assert zadanie_03_podwoj_elementy([0, -1]) == [0, -2]


# --- zadanie_04 ---

def test_zadanie_04_zbierz_parzyste_mieszane():
    assert zadanie_04_zbierz_parzyste([1, 2, 3, 4, 5]) == [2, 4]


def test_zadanie_04_zbierz_parzyste_same_nieparzyste():
    assert zadanie_04_zbierz_parzyste([1, 3, 5]) == []


def test_zadanie_04_zbierz_parzyste_same_parzyste():
    assert zadanie_04_zbierz_parzyste([2, 4, 6]) == [2, 4, 6]


# --- zadanie_05 ---

def test_zadanie_05_maksimum_listy_typowy():
    assert zadanie_05_maksimum_listy([3, 1, 4, 1, 5]) == 5


def test_zadanie_05_maksimum_listy_pusta_zwraca_none():
    assert zadanie_05_maksimum_listy([]) is None


def test_zadanie_05_maksimum_listy_same_ujemne():
    assert zadanie_05_maksimum_listy([-5, -2, -8]) == -2


def test_zadanie_05_maksimum_listy_jeden_element():
    assert zadanie_05_maksimum_listy([7]) == 7


# --- zadanie_06 ---

def test_zadanie_06_etykiety_z_indeksem_typowy():
    assert zadanie_06_etykiety_z_indeksem(["Anna", "Bob"]) == ["1. Anna", "2. Bob"]


def test_zadanie_06_etykiety_z_indeksem_pusta():
    assert zadanie_06_etykiety_z_indeksem([]) == []


def test_zadanie_06_etykiety_z_indeksem_jeden():
    assert zadanie_06_etykiety_z_indeksem(["X"]) == ["1. X"]


# --- zadanie_07 ---

def test_zadanie_07_polacz_w_pary_typowy():
    assert zadanie_07_polacz_w_pary(["a", "b"], [1, 2]) == ["a: 1", "b: 2"]


def test_zadanie_07_polacz_w_pary_puste():
    assert zadanie_07_polacz_w_pary([], []) == []


def test_zadanie_07_polacz_w_pary_jeden_element():
    assert zadanie_07_polacz_w_pary(["wiek"], [25]) == ["wiek: 25"]


# --- zadanie_08 ---

def test_zadanie_08_kwadraty_typowy():
    assert zadanie_08_kwadraty([1, 2, 3, 4]) == [1, 4, 9, 16]


def test_zadanie_08_kwadraty_pusta():
    assert zadanie_08_kwadraty([]) == []


def test_zadanie_08_kwadraty_z_zerem_i_ujemna():
    assert zadanie_08_kwadraty([0, -2, 3]) == [0, 4, 9]


# --- zadanie_09 ---

def test_zadanie_09_tylko_krotkie_filtruje():
    assert zadanie_09_tylko_krotkie(["a", "bb", "ccc", "d"], 2) == ["a", "bb", "d"]


def test_zadanie_09_tylko_krotkie_pusta():
    assert zadanie_09_tylko_krotkie([], 5) == []


def test_zadanie_09_tylko_krotkie_zadne_nie_spelnia():
    assert zadanie_09_tylko_krotkie(["hello", "world"], 3) == []


def test_zadanie_09_tylko_krotkie_dokladnie_na_granicy():
    assert zadanie_09_tylko_krotkie(["hi", "hey"], 2) == ["hi"]


# --- zadanie_10 ---

def test_zadanie_10_wielkie_litery_typowy():
    assert zadanie_10_wielkie_litery(["ala", "ota"]) == ["ALA", "OTA"]


def test_zadanie_10_wielkie_litery_pusta():
    assert zadanie_10_wielkie_litery([]) == []


def test_zadanie_10_wielkie_litery_jedno_slowo():
    assert zadanie_10_wielkie_litery(["Python"]) == ["PYTHON"]


# --- zadanie_11 ---

def test_zadanie_11_znajdz_pierwsza_ujemna_typowy():
    assert zadanie_11_znajdz_pierwsza_ujemna([5, -3, 2, -8]) == -3


def test_zadanie_11_znajdz_pierwsza_ujemna_brak_ujemnych_zwraca_none():
    assert zadanie_11_znajdz_pierwsza_ujemna([5, 2, 8]) is None


def test_zadanie_11_znajdz_pierwsza_ujemna_pusta_zwraca_none():
    assert zadanie_11_znajdz_pierwsza_ujemna([]) is None


def test_zadanie_11_znajdz_pierwsza_ujemna_pierwsza_to_ujemna():
    assert zadanie_11_znajdz_pierwsza_ujemna([-1, 2, 3]) == -1


# --- zadanie_12 ---

def test_zadanie_12_klasyfikuj_liczby_mieszane():
    assert zadanie_12_klasyfikuj_liczby([1, 0, -2, 3]) == ["dodatnia", "zero", "ujemna", "dodatnia"]


def test_zadanie_12_klasyfikuj_liczby_pusta():
    assert zadanie_12_klasyfikuj_liczby([]) == []


def test_zadanie_12_klasyfikuj_liczby_same_ujemne():
    assert zadanie_12_klasyfikuj_liczby([-1, -5]) == ["ujemna", "ujemna"]


def test_zadanie_12_klasyfikuj_liczby_zero():
    assert zadanie_12_klasyfikuj_liczby([0]) == ["zero"]
