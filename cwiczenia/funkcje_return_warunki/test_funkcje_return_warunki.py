from funkcje_return_warunki import (
    zadanie_01_przywitaj,
    zadanie_02_suma_dwoch,
    zadanie_03_czy_parzysta,
    zadanie_04_wieksza_z_dwoch,
    zadanie_05_znak_liczby,
    zadanie_06_opis_dnia,
    zadanie_07_ocena_slowna,
    zadanie_08_podziel,
    zadanie_09_kategoria_wieku,
    zadanie_10_opis_temperatury,
    zadanie_11_czy_kwalifikuje,
    zadanie_12_kategoria_bmi,
)


# --- zadanie_01 ---

def test_zadanie_01_przywitaj_zwykle_imie():
    assert zadanie_01_przywitaj("Anna") == "Cześć, Anna!"


def test_zadanie_01_przywitaj_inne_imie():
    assert zadanie_01_przywitaj("Piotr") == "Cześć, Piotr!"


# --- zadanie_02 ---

def test_zadanie_02_suma_dwoch_liczby_dodatnie():
    assert zadanie_02_suma_dwoch(3, 5) == 8


def test_zadanie_02_suma_dwoch_z_liczba_ujemna():
    assert zadanie_02_suma_dwoch(-1, 1) == 0


def test_zadanie_02_suma_dwoch_oba_ujemne():
    assert zadanie_02_suma_dwoch(-3, -4) == -7


# --- zadanie_03 ---

def test_zadanie_03_czy_parzysta_liczba_parzysta():
    assert zadanie_03_czy_parzysta(4) is True


def test_zadanie_03_czy_parzysta_liczba_nieparzysta():
    assert zadanie_03_czy_parzysta(7) is False


def test_zadanie_03_czy_parzysta_zero_jest_parzyste():
    assert zadanie_03_czy_parzysta(0) is True


def test_zadanie_03_czy_parzysta_ujemna_parzysta():
    assert zadanie_03_czy_parzysta(-6) is True


# --- zadanie_04 ---

def test_zadanie_04_wieksza_z_dwoch_pierwsza_wieksza():
    assert zadanie_04_wieksza_z_dwoch(5, 3) == 5


def test_zadanie_04_wieksza_z_dwoch_druga_wieksza():
    assert zadanie_04_wieksza_z_dwoch(2, 8) == 8


def test_zadanie_04_wieksza_z_dwoch_rowne_zwraca_a():
    assert zadanie_04_wieksza_z_dwoch(4, 4) == 4


# --- zadanie_05 ---

def test_zadanie_05_znak_liczby_dodatnia():
    assert zadanie_05_znak_liczby(5) == "dodatnia"


def test_zadanie_05_znak_liczby_ujemna():
    assert zadanie_05_znak_liczby(-3) == "ujemna"


def test_zadanie_05_znak_liczby_zero():
    assert zadanie_05_znak_liczby(0) == "zero"


# --- zadanie_06 ---

def test_zadanie_06_opis_dnia_poniedzialek():
    assert zadanie_06_opis_dnia(1) == "poniedziałek"


def test_zadanie_06_opis_dnia_sroda():
    assert zadanie_06_opis_dnia(3) == "środa"


def test_zadanie_06_opis_dnia_niedziela():
    assert zadanie_06_opis_dnia(7) == "niedziela"


def test_zadanie_06_opis_dnia_zero_zwraca_none():
    assert zadanie_06_opis_dnia(0) is None


def test_zadanie_06_opis_dnia_osiem_zwraca_none():
    assert zadanie_06_opis_dnia(8) is None


# --- zadanie_07 ---

def test_zadanie_07_ocena_slowna_celujacy():
    assert zadanie_07_ocena_slowna(95) == "celujący"


def test_zadanie_07_ocena_slowna_dobry():
    assert zadanie_07_ocena_slowna(80) == "dobry"


def test_zadanie_07_ocena_slowna_dostateczny():
    assert zadanie_07_ocena_slowna(60) == "dostateczny"


def test_zadanie_07_ocena_slowna_niedostateczny():
    assert zadanie_07_ocena_slowna(30) == "niedostateczny"


def test_zadanie_07_ocena_slowna_granica_celujacy():
    assert zadanie_07_ocena_slowna(90) == "celujący"


def test_zadanie_07_ocena_slowna_za_malo_zwraca_none():
    assert zadanie_07_ocena_slowna(-1) is None


def test_zadanie_07_ocena_slowna_za_duzo_zwraca_none():
    assert zadanie_07_ocena_slowna(101) is None


# --- zadanie_08 ---

def test_zadanie_08_podziel_wynik_calkowity():
    assert zadanie_08_podziel(10.0, 2.0) == 5.0


def test_zadanie_08_podziel_przez_zero_zwraca_none():
    assert zadanie_08_podziel(7.0, 0.0) is None


def test_zadanie_08_podziel_wynik_ulamkowy():
    assert zadanie_08_podziel(1.0, 4.0) == 0.25


# --- zadanie_09 ---

def test_zadanie_09_kategoria_wieku_dziecko():
    assert zadanie_09_kategoria_wieku(10) == "niepełnoletni"


def test_zadanie_09_kategoria_wieku_dorosly():
    assert zadanie_09_kategoria_wieku(25) == "dorosły"


def test_zadanie_09_kategoria_wieku_senior():
    assert zadanie_09_kategoria_wieku(70) == "senior"


def test_zadanie_09_kategoria_wieku_granica_doroslosci():
    assert zadanie_09_kategoria_wieku(18) == "dorosły"


def test_zadanie_09_kategoria_wieku_granica_seniora():
    assert zadanie_09_kategoria_wieku(65) == "senior"


def test_zadanie_09_kategoria_wieku_ujemny_zwraca_none():
    assert zadanie_09_kategoria_wieku(-1) is None


# --- zadanie_10 ---

def test_zadanie_10_opis_temperatury_mroz():
    assert zadanie_10_opis_temperatury(-5.0) == "mróz"


def test_zadanie_10_opis_temperatury_chlodno_granica():
    assert zadanie_10_opis_temperatury(0.0) == "chłodno"


def test_zadanie_10_opis_temperatury_przyjemnie():
    assert zadanie_10_opis_temperatury(20.0) == "przyjemnie"


def test_zadanie_10_opis_temperatury_goraco():
    assert zadanie_10_opis_temperatury(30.0) == "gorąco"


def test_zadanie_10_opis_temperatury_granica_przyjemnie():
    assert zadanie_10_opis_temperatury(15.0) == "przyjemnie"


# --- zadanie_11 ---

def test_zadanie_11_czy_kwalifikuje_spelnia_oba_warunki():
    assert zadanie_11_czy_kwalifikuje(20, 170) is True


def test_zadanie_11_czy_kwalifikuje_za_mlody():
    assert zadanie_11_czy_kwalifikuje(16, 170) is False


def test_zadanie_11_czy_kwalifikuje_za_niski():
    assert zadanie_11_czy_kwalifikuje(20, 150) is False


def test_zadanie_11_czy_kwalifikuje_ujemny_wiek_zwraca_none():
    assert zadanie_11_czy_kwalifikuje(-1, 170) is None


def test_zadanie_11_czy_kwalifikuje_zerowy_wzrost_zwraca_none():
    assert zadanie_11_czy_kwalifikuje(20, 0) is None


# --- zadanie_12 ---

def test_zadanie_12_kategoria_bmi_norma():
    # 70 / (1.75 ** 2) = 22.86 → norma
    assert zadanie_12_kategoria_bmi(70.0, 175.0) == "norma"


def test_zadanie_12_kategoria_bmi_niedowaga():
    # 50 / (1.75 ** 2) = 16.33 → niedowaga
    assert zadanie_12_kategoria_bmi(50.0, 175.0) == "niedowaga"


def test_zadanie_12_kategoria_bmi_nadwaga():
    # 90 / (1.75 ** 2) = 29.39 → nadwaga
    assert zadanie_12_kategoria_bmi(90.0, 175.0) == "nadwaga"


def test_zadanie_12_kategoria_bmi_otylosc():
    # 100 / (1.75 ** 2) = 32.65 → otyłość
    assert zadanie_12_kategoria_bmi(100.0, 175.0) == "otyłość"


def test_zadanie_12_kategoria_bmi_zerowa_waga_zwraca_none():
    assert zadanie_12_kategoria_bmi(0.0, 175.0) is None


def test_zadanie_12_kategoria_bmi_zerowy_wzrost_zwraca_none():
    assert zadanie_12_kategoria_bmi(70.0, 0.0) is None
