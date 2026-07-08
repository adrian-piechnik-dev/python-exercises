import csv
from typing import Optional

from pygments.lexers.csound import newline


def zadanie_01_wczytaj_wiersze(sciezka: str) -> list[dict[str, str]]:
    """Wczytuje wszystkie wiersze pliku CSV jako listę słowników.

    Args:
        sciezka: ścieżka do pliku CSV z nagłówkiem.

    Returns:
        list[dict[str, str]]: lista słowników (jeden słownik = jeden wiersz),
            pusta lista gdy plik nie zawiera wierszy danych.
    """
    with open(sciezka, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def zadanie_02_wczytaj_naglowki(sciezka: str) -> list[str]:
    """Zwraca listę nazw kolumn (nagłówków) z pliku CSV.

    Args:
        sciezka: ścieżka do pliku CSV z nagłówkiem.

    Returns:
        list[str]: lista nazw kolumn w kolejności z pliku.
    """
    with open(sciezka, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader.fieldnames)


def zadanie_03_policz_wiersze(sciezka: str) -> int:
    """Zlicza wiersze danych w pliku CSV (bez nagłówka).

    Args:
        sciezka: ścieżka do pliku CSV z nagłówkiem.

    Returns:
        int: liczba wierszy danych; 0 gdy plik zawiera tylko nagłówek.
    """
    with open(sciezka, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return len(list(reader))


def zadanie_04_wartosc_z_kolumny(sciezka: str, kolumna: str) -> list[str]:
    """Zbiera wartości z podanej kolumny jako listę stringów.

    Args:
        sciezka: ścieżka do pliku CSV z nagłówkiem.
        kolumna: nazwa kolumny do zebrania (musi istnieć w pliku).

    Returns:
        list[str]: lista wartości z danej kolumny, w kolejności wierszy.
    """
    with open(sciezka, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        wiersze = list(reader)
        return [w[kolumna] for w in wiersze]


def zadanie_05_zapisz_wiersze(
    sciezka: str, wiersze: list[dict[str, str]], fieldnames: list[str]
) -> None:
    """Zapisuje listę słowników do pliku CSV (nadpisuje jeśli istnieje).

    Args:
        sciezka: ścieżka do pliku wynikowego.
        wiersze: lista słowników do zapisania.
        fieldnames: lista nazw kolumn wyznaczająca kolejność w pliku.

    Returns:
        None
    """
    with open(sciezka, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(wiersze)


def zadanie_06_dopisz_wiersz(
    sciezka: str, wiersz: dict[str, str], fieldnames: list[str]
) -> None:
    """Dopisuje jeden wiersz na końcu istniejącego pliku CSV.

    Args:
        sciezka: ścieżka do istniejącego pliku CSV.
        wiersz: słownik z danymi do dopisania.
        fieldnames: lista nazw kolumn (musi zgadzać się z nagłówkiem pliku).

    Returns:
        None
    """
    with open(sciezka, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow(wiersz)



def zadanie_07_filtruj_wiersze(
    sciezka: str, kolumna: str, wartosc: str
) -> list[dict[str, str]]:
    """Zwraca wiersze, w których podana kolumna ma podaną wartość.

    Args:
        sciezka: ścieżka do pliku CSV z nagłówkiem.
        kolumna: nazwa kolumny do filtrowania.
        wartosc: wartość, którą musi mieć kolumna (porównanie str == str).

    Returns:
        list[dict[str, str]]: lista pasujących wierszy; pusta gdy brak dopasowań.
    """
    with open(sciezka, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [w for w in list(reader) if w[kolumna] == wartosc]


def zadanie_08_szukaj_wiersza(
    sciezka: str, kolumna: str, wartosc: str
) -> Optional[dict[str, str]]:
    """Zwraca pierwszy wiersz, gdzie kolumna == wartość, lub None gdy brak.

    Args:
        sciezka: ścieżka do pliku CSV z nagłówkiem.
        kolumna: nazwa kolumny do przeszukania.
        wartosc: szukana wartość.

    Returns:
        Optional[dict[str, str]]: pierwszy pasujący wiersz jako słownik lub None.
    """
    with open(sciezka, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        wiersze = list(reader)
        for w in wiersze:
            if w[kolumna] == wartosc:
                return w
        return None



def zadanie_09_zsumuj_kolumne(sciezka: str, kolumna: str) -> int:
    """Sumuje wartości liczbowe z podanej kolumny.

    Args:
        sciezka: ścieżka do pliku CSV z nagłówkiem.
        kolumna: nazwa kolumny z wartościami całkowitoliczbowymi.

    Returns:
        int: suma wartości z kolumny; 0 gdy plik nie zawiera wierszy danych.
    """
    # TODO: wczytaj wiersze przez list(DictReader)
    # TODO: akumulator suma = 0, iteruj po wierszach: suma += int(w[kolumna])
    # TODO: zwróć suma
    with open(sciezka, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        wiersze = list(reader)
        suma = 0
        for w in wiersze:
            suma += int(w[kolumna])
        return suma


def zadanie_10_wczytaj_bezpiecznie(
    sciezka: str,
) -> Optional[list[dict[str, str]]]:
    """Wczytuje plik CSV; zwraca None gdy plik nie istnieje.

    Spirala z pliki_tekstowe: try/except FileNotFoundError jako kontrakt None.

    Args:
        sciezka: ścieżka do pliku CSV.

    Returns:
        Optional[list[dict[str, str]]]: lista wierszy lub None gdy brak pliku.
    """
    try:
        with open(sciezka, "r", newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        return None


def zadanie_11_filtruj_i_zapisz(
    wejscie: str, wyjscie: str, kolumna: str, wartosc: str
) -> int:
    """Filtruje wiersze z pliku wejściowego i zapisuje pasujące do pliku wyjściowego.

    Spirala z slowniki: iteracja po wierszach-słownikach + filtrowanie po kluczu.

    Args:
        wejscie: ścieżka do pliku CSV źródłowego.
        wyjscie: ścieżka do pliku CSV wynikowego.
        kolumna: nazwa kolumny do filtrowania.
        wartosc: wartość, którą musi mieć kolumna.

    Returns:
        int: liczba zapisanych wierszy.
    """
    # TODO: wczytaj wiersze i fieldnames z pliku wejscie (list(DictReader))
    # TODO: odfiltruj wiersze gdzie w[kolumna] == wartosc
    # TODO: zapisz pasujące do pliku wyjscie przez DictWriter (writeheader + writerows)
    # TODO: zwróć len(pasujace)
    pass


def zadanie_12_zlicz_po_wartosci(sciezka: str, kolumna: str) -> dict[str, int]:
    """Zlicza wiersze pogrupowane po wartości podanej kolumny.

    Spirala z slowniki: wzorzec akumulatora słownikowego (if klucz in licznik).

    Args:
        sciezka: ścieżka do pliku CSV z nagłówkiem.
        kolumna: nazwa kolumny, po której grupujemy.

    Returns:
        dict[str, int]: słownik {wartość_kolumny: liczba_wierszy}.
    """
    # TODO: wczytaj wiersze przez list(DictReader)
    # TODO: pusty słownik licznik = {}
    # TODO: dla każdego wiersza: wartość = w[kolumna]
    #       if wartość in licznik: licznik[wartość] += 1
    #       else: licznik[wartość] = 1
    # TODO: zwróć licznik
    pass
