from typing import Optional


def zadanie_01_policz_elementy(lista: list) -> int:
    """Zlicza wszystkie elementy w liście, niezależnie od ich wartości.

    Args:
        lista: dowolna lista elementów.

    Returns:
        int: liczba elementów w liście (0 gdy lista pusta).
    """
    licznik = 0
    for _ in lista:
        licznik += 1
    return licznik


def zadanie_02_suma_liczb(liczby: list[int]) -> int:
    """Zwraca sumę wszystkich liczb z listy.

    Args:
        liczby: lista liczb całkowitych.

    Returns:
        int: suma wszystkich elementów (0 gdy lista pusta).
    """
    suma = 0
    for liczba in liczby:
        suma += liczba
    return suma


def zadanie_03_podwoj_elementy(liczby: list[int]) -> list[int]:
    """Zwraca nową listę, w której każdy element jest podwojony.

    Args:
        liczby: lista liczb całkowitych.

    Returns:
        list[int]: nowa lista z wartościami pomnożonymi przez 2.
    """
    wynik = []
    for liczba in liczby:
        wynik.append(liczba * 2)
    return wynik


def zadanie_04_zbierz_parzyste(liczby: list[int]) -> list[int]:
    """Zbiera z listy tylko liczby parzyste.

    Args:
        liczby: lista liczb całkowitych.

    Returns:
        list[int]: nowa lista zawierająca tylko liczby parzyste, w oryginalnej kolejności.
    """
    wynik = []
    for liczba in liczby:
        if liczba % 2 == 0:
            wynik.append(liczba)
    return wynik


def zadanie_05_maksimum_listy(liczby: list[int]) -> Optional[int]:
    """Zwraca największą liczbę z listy; dla pustej listy zwraca None.

    Args:
        liczby: lista liczb całkowitych.

    Returns:
        Optional[int]: największy element lub None gdy lista jest pusta.
    """
    maks = None
    for liczba in liczby:
        if maks is None or liczba > maks:
            maks = liczba
    return maks


def zadanie_06_etykiety_z_indeksem(slowa: list[str]) -> list[str]:
    """Zwraca listę słów z numerami porządkowymi od 1.

    Args:
        slowa: lista słów.

    Returns:
        list[str]: lista napisów w formacie "1. slowo", "2. slowo" itd.
    """
    wynik = []
    for numer, slowo in enumerate(slowa, start=1):
        wynik.append(f"{numer}. {slowo}")
    return wynik


def zadanie_07_polacz_w_pary(klucze: list[str], wartosci: list[int]) -> list[str]:
    """Łączy dwie listy w listę napisów w formacie "klucz: wartosc".

    Args:
        klucze: lista tekstowych kluczy.
        wartosci: lista liczb całkowitych.

    Returns:
        list[str]: lista napisów "klucz: wartosc" dla każdej pary.
    """
    wynik = []
    for klucz, wartosc in zip(klucze, wartosci):
        wynik.append(f"{klucz}: {wartosc}")
    return wynik


def zadanie_08_kwadraty(liczby: list[int]) -> list[int]:
    """Zwraca listę kwadratów podanych liczb.

    Args:
        liczby: lista liczb całkowitych.

    Returns:
        list[int]: lista kwadratów (każda liczba podniesiona do potęgi 2).
    """
    return [liczba ** 2 for liczba in liczby]


def zadanie_09_tylko_krotkie(slowa: list[str], max_dlugosc: int) -> list[str]:
    """Filtruje listę słów, zostawiając tylko te nieprzekraczające podanej długości.

    Args:
        slowa: lista słów.
        max_dlugosc: maksymalna dopuszczalna długość słowa (włącznie).

    Returns:
        list[str]: lista słów, których długość wynosi <= max_dlugosc.
    """
    return [slowo for slowo in slowa if len(slowo) <= max_dlugosc]


def zadanie_10_wielkie_litery(slowa: list[str]) -> list[str]:
    """Zamienia wszystkie słowa na wielkie litery.

    Args:
        slowa: lista słów.

    Returns:
        list[str]: nowa lista ze słowami zamienionymi na wielkie litery.
    """
    return [slowo.upper() for slowo in slowa]


def zadanie_11_znajdz_pierwsza_ujemna(liczby: list[int]) -> Optional[int]:
    """Zwraca pierwszą ujemną liczbę z listy lub None gdy brak ujemnych.

    Spirala z funkcje_return_warunki: early return i None jako sygnał braku wartości.

    Args:
        liczby: lista liczb całkowitych.

    Returns:
        Optional[int]: pierwsza ujemna liczba lub None gdy lista pusta lub bez ujemnych.
    """
    for liczba in liczby:
        if liczba < 0:
            return liczba
    return None


def zadanie_12_klasyfikuj_liczby(liczby: list[int]) -> list[str]:
    """Klasyfikuje każdą liczbę jako "ujemna", "zero" lub "dodatnia".

    Spirala z funkcje_return_warunki: if/elif/else użyty wewnątrz pętli for.

    Args:
        liczby: lista liczb całkowitych.

    Returns:
        list[str]: lista klasyfikacji w tej samej kolejności co wejście.
    """
    wynik = []
    for liczba in liczby:
        if liczba < 0:
            wynik.append("ujemna")
        elif liczba == 0:
            wynik.append("zero")
        else:
            wynik.append("dodatnia")
    return wynik
