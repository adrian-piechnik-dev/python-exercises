from typing import Optional


def zadanie_01_czytaj_calosc(sciezka: str) -> str:
    """Wczytuje całą zawartość pliku jako jeden ciąg tekstu.

    Args:
        sciezka: ścieżka do pliku tekstowego.

    Returns:
        str: pełna zawartość pliku (włącznie ze znakami nowej linii).
    """
    with open(sciezka, "r", encoding="utf-8") as f:
        return f.read()


def zadanie_02_czytaj_linie(sciezka: str) -> list[str]:
    """Wczytuje plik i zwraca listę linii bez znaków nowej linii.

    Args:
        sciezka: ścieżka do pliku tekstowego.

    Returns:
        list[str]: lista linii; pusta lista gdy plik jest pusty.
    """
    with open(sciezka, "r", encoding="utf-8") as f:
        return f.read().splitlines()


def zadanie_03_policz_linie(sciezka: str) -> int:
    """Zlicza liczbę linii w pliku.

    Args:
        sciezka: ścieżka do pliku tekstowego.

    Returns:
        int: liczba linii; 0 dla pustego pliku.
    """
    with open(sciezka, "r", encoding="utf-8") as f:
        linie = f.read().splitlines()
        return len(linie)


def zadanie_04_zapisz_tekst(sciezka: str, tresc: str) -> None:
    """Zapisuje tekst do pliku, nadpisując poprzednią zawartość.

    Args:
        sciezka: ścieżka do pliku docelowego.
        tresc: tekst do zapisania.

    Returns:
        None
    """
    with open(sciezka, "w", encoding="utf-8") as f:
        f.write(tresc)


def zadanie_05_zapisz_linie(sciezka: str, linie: list[str]) -> None:
    """Zapisuje listę linii do pliku, oddzielając je znakiem nowej linii.

    Args:
        sciezka: ścieżka do pliku docelowego.
        linie: lista ciągów do zapisania jako kolejne linie.

    Returns:
        None
    """
    with open(sciezka, "w", encoding="utf-8") as f:
        f.write("\n".join(linie))


def zadanie_06_dopisz_linie(sciezka: str, linia: str) -> None:
    """Dopisuje jedną linię na końcu pliku zakończoną znakiem nowej linii.

    Plik zostanie utworzony gdy nie istnieje.

    Args:
        sciezka: ścieżka do pliku (istniejącego lub nowego).
        linia: tekst do dopisania.

    Returns:
        None
    """
    with open(sciezka, "a", encoding="utf-8") as f:
        f.write(linia + "\n")


def zadanie_07_pierwsza_linia(sciezka: str) -> Optional[str]:
    """Zwraca pierwszą linię pliku lub None gdy plik jest pusty.

    Args:
        sciezka: ścieżka do pliku tekstowego.

    Returns:
        Optional[str]: pierwsza linia bez znaku nowej linii, lub None.
    """
    with open(sciezka, "r", encoding="utf-8") as f:
        linie = f.read().splitlines()
        if not linie:
            return None
        return linie[0]


def zadanie_08_szukaj_frazy(sciezka: str, fraza: str) -> list[str]:
    """Zwraca linie pliku zawierające podaną frazę (rozróżnia wielkość liter).

    Args:
        sciezka: ścieżka do pliku tekstowego.
        fraza: szukana fraza.

    Returns:
        list[str]: linie zawierające frazę, bez znaków nowej linii.
    """
    with open(sciezka, "r", encoding="utf-8") as f:
        linie = f.read().splitlines()
        return [l for l in linie if fraza in l]


def zadanie_09_licz_slowa(sciezka: str) -> int:
    """Zlicza łączną liczbę słów w pliku (słowa rozdzielone białymi znakami).

    Args:
        sciezka: ścieżka do pliku tekstowego.

    Returns:
        int: łączna liczba słów; 0 dla pustego pliku.
    """
    with open(sciezka, "r", encoding="utf-8") as f:
        slowa = f.read().split()
        return len(slowa)


def zadanie_10_czytaj_bezpiecznie(sciezka: str) -> Optional[str]:
    """Wczytuje plik. Zwraca None gdy plik nie istnieje.

    Args:
        sciezka: ścieżka do pliku tekstowego.

    Returns:
        Optional[str]: zawartość pliku lub None gdy plik nie istnieje.
    """
    try:
        with open(sciezka, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return None


def zadanie_11_skopiuj_plik(zrodlo: str, cel: str) -> bool:
    """Kopiuje zawartość pliku źródłowego do pliku docelowego.

    Args:
        zrodlo: ścieżka do pliku źródłowego.
        cel: ścieżka do pliku docelowego (nadpisywana gdy istnieje).

    Returns:
        bool: True gdy kopiowanie się powiodło, False gdy plik źródłowy nie istnieje.
    """
    try:
        with open(zrodlo, "r", encoding="utf-8") as src:
            tekst = src.read()
            with open(cel, "w", encoding="utf-8") as dst:
                dst.write(tekst)
        return True
    except FileNotFoundError:
        return False


def zadanie_12_filtruj_i_zapisz(wejscie: str, wyjscie: str, fraza: str) -> int:
    """Filtruje linie z pliku wejściowego i zapisuje pasujące do pliku wyjściowego.

    Kopiuje tylko linie zawierające frazę. Zwraca 0 gdy plik wejściowy nie istnieje.

    Args:
        wejscie: ścieżka do pliku wejściowego.
        wyjscie: ścieżka do pliku wyjściowego.
        fraza: fraza do filtrowania (rozróżnia wielkość liter).

    Returns:
        int: liczba zapisanych linii; 0 gdy plik wejściowy nie istnieje.
    """
    try:
        with open(wejscie, "r", encoding="utf-8") as fin:
            linie = fin.read().splitlines()
            pasujace = [l for l in linie if fraza in l]
            with open(wyjscie, "w", encoding="utf-8") as fout:
                fout.write("\n".join(pasujace))
        return len(pasujace)
    except FileNotFoundError:
        return 0