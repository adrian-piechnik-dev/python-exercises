from typing import Optional


def zadanie_01_wartosc_po_kluczu(slownik: dict[str, int], klucz: str) -> int:
    """Zwraca wartość przypisaną do podanego klucza.

    Args:
        slownik: słownik str -> int.
        klucz: klucz do wyszukania (gwarantowany jako istniejący).

    Returns:
        int: wartość przypisana do klucza.
    """
    return slownik[klucz]


def zadanie_02_get_z_domyslna(slownik: dict[str, int], klucz: str, domyslna: int) -> int:
    """Zwraca wartość klucza lub wartość domyślną gdy klucz nie istnieje.

    Args:
        slownik: słownik str -> int.
        klucz: klucz do wyszukania.
        domyslna: wartość zwracana gdy klucz nie istnieje.

    Returns:
        int: wartość klucza lub domyslna.
    """
    return slownik.get(klucz, domyslna)


def zadanie_03_czy_klucz_istnieje(slownik: dict[str, int], klucz: str) -> bool:
    """Sprawdza czy podany klucz istnieje w słowniku.

    Args:
        slownik: słownik str -> int.
        klucz: klucz do sprawdzenia.

    Returns:
        bool: True jeśli klucz istnieje, False w przeciwnym razie.
    """
    return klucz in slownik


def zadanie_04_dodaj_lub_nadpisz(slownik: dict[str, int], klucz: str, wartosc: int) -> dict[str, int]:
    """Zwraca nowy słownik z dodanym lub nadpisanym kluczem.

    Args:
        slownik: wejściowy słownik str -> int.
        klucz: klucz do dodania lub nadpisania.
        wartosc: nowa wartość.

    Returns:
        dict[str, int]: kopia słownika z wprowadzoną zmianą.
    """
    new_dict = slownik.copy()
    new_dict[klucz] = wartosc
    return new_dict


def zadanie_05_klucze_jako_lista(slownik: dict[str, int]) -> list[str]:
    """Zwraca listę wszystkich kluczy słownika.

    Args:
        slownik: słownik str -> int.

    Returns:
        list[str]: lista kluczy w kolejności wstawienia.
    """
    return list(slownik.keys())


def zadanie_06_wartosci_jako_lista(slownik: dict[str, int]) -> list[int]:
    """Zwraca listę wszystkich wartości słownika.

    Args:
        slownik: słownik str -> int.

    Returns:
        list[int]: lista wartości w kolejności wstawienia.
    """
    return list(slownik.values())


def zadanie_07_opisy_z_items(slownik: dict[str, int]) -> list[str]:
    """Zwraca listę napisów "klucz: wartosc" dla każdej pary w słowniku.

    Args:
        slownik: słownik str -> int.

    Returns:
        list[str]: lista napisów w formacie "klucz: wartosc".
    """
    lista_napisow = []
    for k, v in slownik.items():
        lista_napisow.append(f"{k}: {v}")
    return lista_napisow


def zadanie_08_suma_wartosci(slownik: dict[str, int]) -> int:
    """Zwraca sumę wszystkich wartości słownika.

    Args:
        slownik: słownik str -> int.

    Returns:
        int: suma wartości (0 dla pustego słownika).
    """
    suma = 0
    for v in slownik.values():
        suma += v
    return suma


def zadanie_09_zbuduj_ze_list(klucze: list[str], wartosci: list[int]) -> dict[str, int]:
    """Buduje słownik z listy kluczy i listy wartości, iterując po obu jednocześnie.

    Spirala z listy_petle: użyj zip do iteracji po dwóch listach równocześnie.

    Args:
        klucze: lista kluczy tekstowych.
        wartosci: lista wartości całkowitych (tej samej długości co klucze).

    Returns:
        dict[str, int]: słownik zbudowany z par (klucz, wartość).
    """
    wynik = {}
    for k, v in zip(klucze, wartosci):
        wynik[k] = v
    return wynik


def zadanie_10_zlicz_wystapienia(slowa: list[str]) -> dict[str, int]:
    """Zlicza ile razy każde słowo pojawia się na liście.

    Args:
        slowa: lista słów do zliczenia.

    Returns:
        dict[str, int]: słownik {slowo: liczba_wystapien}.
    """
    licznik = {}
    for slowo in slowa:
        if slowo in licznik:
            licznik[slowo] += 1
        else:
            licznik[slowo] = 1
    return licznik


def zadanie_11_znajdz_klucz_po_wartosci(slownik: dict[str, int], szukana: int) -> Optional[str]:
    """Zwraca pierwszy klucz o podanej wartości lub None gdy brak.

    Args:
        slownik: słownik str -> int.
        szukana: wartość do wyszukania.

    Returns:
        Optional[str]: pierwszy klucz z pasującą wartością lub None.
    """
    for k, v in slownik.items():
        if v == szukana:
            return k


def zadanie_12_klucze_powyzej_progu(slownik: dict[str, int], prog: int) -> list[str]:
    """Zwraca listę kluczy, których wartość jest większa od podanego progu.

    Spirala z listy_petle: użyj list comprehension z filtrem na .items().

    Args:
        slownik: słownik str -> int.
        prog: dolna granica (wyłącznie) dla wartości.

    Returns:
        list[str]: klucze gdzie wartość > prog, w kolejności wstawienia.
    """
    # TODO: list comprehension — [k for k, v in slownik.items() if v > prog]
    return [k for k, v in slownik.items() if v > prog]
