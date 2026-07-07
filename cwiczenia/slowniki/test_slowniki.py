from slowniki import (
    zadanie_01_wartosc_po_kluczu,
    zadanie_02_get_z_domyslna,
    zadanie_03_czy_klucz_istnieje,
    zadanie_04_dodaj_lub_nadpisz,
    zadanie_05_klucze_jako_lista,
    zadanie_06_wartosci_jako_lista,
    zadanie_07_opisy_z_items,
    zadanie_08_suma_wartosci,
    zadanie_09_zbuduj_ze_list,
    zadanie_10_zlicz_wystapienia,
    zadanie_11_znajdz_klucz_po_wartosci,
    zadanie_12_klucze_powyzej_progu,
)


# --- zadanie 01 ---

def test_zadanie_01_istniejacy_klucz():
    assert zadanie_01_wartosc_po_kluczu({"Anna": 5, "Piotr": 4}, "Anna") == 5


def test_zadanie_01_drugi_klucz():
    assert zadanie_01_wartosc_po_kluczu({"Anna": 5, "Piotr": 4}, "Piotr") == 4


def test_zadanie_01_jeden_wpis():
    assert zadanie_01_wartosc_po_kluczu({"x": 99}, "x") == 99


# --- zadanie 02 ---

def test_zadanie_02_klucz_istnieje():
    assert zadanie_02_get_z_domyslna({"Anna": 5}, "Anna", 0) == 5


def test_zadanie_02_klucz_nie_istnieje():
    assert zadanie_02_get_z_domyslna({"Anna": 5}, "Zofia", 0) == 0


def test_zadanie_02_pusty_slownik():
    assert zadanie_02_get_z_domyslna({}, "Anna", -1) == -1


# --- zadanie 03 ---

def test_zadanie_03_klucz_istnieje():
    assert zadanie_03_czy_klucz_istnieje({"Anna": 5}, "Anna") is True


def test_zadanie_03_klucz_nie_istnieje():
    assert zadanie_03_czy_klucz_istnieje({"Anna": 5}, "Zofia") is False


def test_zadanie_03_pusty_slownik():
    assert zadanie_03_czy_klucz_istnieje({}, "Anna") is False


# --- zadanie 04 ---

def test_zadanie_04_dodaje_nowy_klucz():
    wynik = zadanie_04_dodaj_lub_nadpisz({"Anna": 5}, "Piotr", 4)
    assert wynik == {"Anna": 5, "Piotr": 4}


def test_zadanie_04_nadpisuje_istniejacy():
    wynik = zadanie_04_dodaj_lub_nadpisz({"Anna": 5}, "Anna", 3)
    assert wynik == {"Anna": 3}


def test_zadanie_04_nie_modyfikuje_oryginalu():
    oryginal = {"Anna": 5}
    zadanie_04_dodaj_lub_nadpisz(oryginal, "Piotr", 4)
    assert oryginal == {"Anna": 5}


# --- zadanie 05 ---

def test_zadanie_05_typowy():
    assert zadanie_05_klucze_jako_lista({"Anna": 5, "Piotr": 4}) == ["Anna", "Piotr"]


def test_zadanie_05_pusty_slownik():
    assert zadanie_05_klucze_jako_lista({}) == []


def test_zadanie_05_jeden_wpis():
    assert zadanie_05_klucze_jako_lista({"x": 1}) == ["x"]


# --- zadanie 06 ---

def test_zadanie_06_typowy():
    assert zadanie_06_wartosci_jako_lista({"Anna": 5, "Piotr": 4}) == [5, 4]


def test_zadanie_06_pusty_slownik():
    assert zadanie_06_wartosci_jako_lista({}) == []


def test_zadanie_06_powtarzajace_sie_wartosci():
    assert zadanie_06_wartosci_jako_lista({"a": 1, "b": 1}) == [1, 1]


# --- zadanie 07 ---

def test_zadanie_07_typowy():
    wynik = zadanie_07_opisy_z_items({"Anna": 5, "Piotr": 4})
    assert wynik == ["Anna: 5", "Piotr: 4"]


def test_zadanie_07_pusty_slownik():
    assert zadanie_07_opisy_z_items({}) == []


def test_zadanie_07_jeden_wpis():
    assert zadanie_07_opisy_z_items({"x": 99}) == ["x: 99"]


# --- zadanie 08 ---

def test_zadanie_08_typowy():
    assert zadanie_08_suma_wartosci({"a": 1, "b": 2, "c": 3}) == 6


def test_zadanie_08_pusty_slownik():
    assert zadanie_08_suma_wartosci({}) == 0


def test_zadanie_08_ujemne():
    assert zadanie_08_suma_wartosci({"a": -1, "b": 3}) == 2


# --- zadanie 09 ---

def test_zadanie_09_typowy():
    wynik = zadanie_09_zbuduj_ze_list(["Anna", "Piotr"], [5, 4])
    assert wynik == {"Anna": 5, "Piotr": 4}


def test_zadanie_09_puste_listy():
    assert zadanie_09_zbuduj_ze_list([], []) == {}


def test_zadanie_09_jeden_element():
    assert zadanie_09_zbuduj_ze_list(["x"], [99]) == {"x": 99}


# --- zadanie 10 ---

def test_zadanie_10_powtorzenia():
    wynik = zadanie_10_zlicz_wystapienia(["pies", "kot", "pies"])
    assert wynik == {"pies": 2, "kot": 1}


def test_zadanie_10_pusta_lista():
    assert zadanie_10_zlicz_wystapienia([]) == {}


def test_zadanie_10_bez_powtorzen():
    wynik = zadanie_10_zlicz_wystapienia(["a", "b", "c"])
    assert wynik == {"a": 1, "b": 1, "c": 1}


def test_zadanie_10_wszystkie_takie_same():
    wynik = zadanie_10_zlicz_wystapienia(["x", "x", "x"])
    assert wynik == {"x": 3}


# --- zadanie 11 ---

def test_zadanie_11_wartosc_istnieje():
    assert zadanie_11_znajdz_klucz_po_wartosci({"Anna": 5, "Piotr": 4}, 5) == "Anna"


def test_zadanie_11_brak_wartosci_zwraca_none():
    assert zadanie_11_znajdz_klucz_po_wartosci({"Anna": 5}, 99) is None


def test_zadanie_11_pusty_slownik_zwraca_none():
    assert zadanie_11_znajdz_klucz_po_wartosci({}, 5) is None


def test_zadanie_11_pierwsza_z_dwoch():
    wynik = zadanie_11_znajdz_klucz_po_wartosci({"a": 1, "b": 1}, 1)
    assert wynik == "a"


# --- zadanie 12 ---

def test_zadanie_12_filtruje():
    wynik = zadanie_12_klucze_powyzej_progu({"Anna": 5, "Piotr": 4, "Zofia": 3}, 4)
    assert wynik == ["Anna"]


def test_zadanie_12_pusty_slownik():
    assert zadanie_12_klucze_powyzej_progu({}, 3) == []


def test_zadanie_12_zadne_nie_spelnia():
    wynik = zadanie_12_klucze_powyzej_progu({"Anna": 2, "Piotr": 1}, 5)
    assert wynik == []


def test_zadanie_12_wszystkie_spelniaja():
    wynik = zadanie_12_klucze_powyzej_progu({"a": 10, "b": 20}, 5)
    assert wynik == ["a", "b"]
