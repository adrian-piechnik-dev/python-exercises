from pathlib import Path
from typing import Optional


def zadanie_01_podziel_bezpiecznie(a: int, b: int) -> Optional[int]:
    """Dzieli a przez b (całkowicie). Zwraca None gdy b wynosi zero.

    Args:
        a: dzielna.
        b: dzielnik.

    Returns:
        Optional[int]: wynik a // b lub None przy dzieleniu przez zero.
    """
    try:
        return a // b
    except ZeroDivisionError:
        return None


def zadanie_02_parsuj_int(tekst: str) -> Optional[int]:
    """Konwertuje tekst na int. Zwraca None gdy konwersja się nie powiodła.

    Args:
        tekst: ciąg znaków do skonwertowania.

    Returns:
        Optional[int]: sparsowana liczba całkowita lub None.
    """
    try:
        return int(tekst)
    except ValueError:
        return None


def zadanie_03_parsuj_float(tekst: str) -> Optional[float]:
    """Konwertuje tekst na float. Zwraca None gdy konwersja się nie powiodła.

    Args:
        tekst: ciąg znaków do skonwertowania.

    Returns:
        Optional[float]: sparsowana liczba zmiennoprzecinkowa lub None.
    """
    try:
        return float(tekst)
    except ValueError:
        return None


def zadanie_04_pobierz_z_listy(lista: list[int], indeks: int) -> Optional[int]:
    """Zwraca element listy pod danym indeksem lub None gdy indeks poza zakresem.

    Args:
        lista: lista liczb całkowitych.
        indeks: indeks elementu do pobrania (może być ujemny).

    Returns:
        Optional[int]: element listy lub None.
    """
    try:
        return lista[indeks]
    except IndexError:
        return None


def zadanie_05_dwa_wyjatki(tekst: str, dzielnik: int) -> Optional[float]:
    """Parsuje tekst jako float i dzieli przez dzielnik.

    Zwraca None przy błędzie konwersji LUB dzieleniu przez zero.

    Args:
        tekst: ciąg do skonwertowania na float.
        dzielnik: liczba przez którą dzielimy.

    Returns:
        Optional[float]: wynik float(tekst) / dzielnik lub None.
    """
    try:
        return float(tekst) / dzielnik
    except ValueError:
        return None
    except ZeroDivisionError:
        return None


def zadanie_06_nazwa_pliku(sciezka: str) -> str:
    """Zwraca samą nazwę pliku (z rozszerzeniem) ze ścieżki.

    Args:
        sciezka: ścieżka do pliku jako tekst.

    Returns:
        str: nazwa pliku, np. "raport.csv" dla "/dane/raport.csv".
    """
    return Path(sciezka).name


def zadanie_07_rozszerzenie(sciezka: str) -> str:
    """Zwraca rozszerzenie pliku (z kropką) ze ścieżki.

    Args:
        sciezka: ścieżka do pliku jako tekst.

    Returns:
        str: rozszerzenie z kropką np. ".csv", lub "" gdy plik bez rozszerzenia.
    """
    return Path(sciezka).suffix


def zadanie_08_katalog_nadrzedny(sciezka: str) -> str:
    """Zwraca ścieżkę do katalogu nadrzędnego jako tekst.

    Args:
        sciezka: ścieżka do pliku lub katalogu.

    Returns:
        str: ścieżka rodzica, np. "katalog" dla "katalog/plik.txt".
    """
    return str(Path(sciezka).parent)


def zadanie_09_polacz_sciezki(katalog: str, plik: str) -> str:
    """Łączy katalog i plik w jedną ścieżkę operatorem /.

    Args:
        katalog: ścieżka do katalogu.
        plik: nazwa pliku lub podfolderu.

    Returns:
        str: połączona ścieżka jako tekst.
    """
    return str(Path(katalog) / plik)


def zadanie_10_zmien_rozszerzenie(sciezka: str, nowe_rozszerzenie: str) -> str:
    """Zwraca ścieżkę z zmienionym rozszerzeniem.

    Args:
        sciezka: oryginalna ścieżka do pliku.
        nowe_rozszerzenie: nowe rozszerzenie z kropką, np. ".txt".

    Returns:
        str: ścieżka z podmienionym rozszerzeniem.
    """
    return str(Path(sciezka).with_suffix(nowe_rozszerzenie))


def zadanie_11_parsuj_config(linie: list[str]) -> dict[str, str]:
    """Parsuje linie konfiguracji w formacie "klucz=wartosc" do słownika.

    Linie niezawierające znaku "=" są pomijane. Klucz i wartość są
    obcinane ze spacji (str.strip).

    Args:
        linie: lista linii tekstowych.

    Returns:
        dict[str, str]: słownik z parami klucz→wartość.
    """
    wynik = {}
    for linia in linie:
        if "=" not in linia:
            continue
        klucz, wartosc = linia.split("=", 1)
        wynik[klucz.strip()] = wartosc.strip()
    return wynik


def zadanie_12_wczytaj_config(sciezka: str) -> dict[str, str]:
    """Czyta plik konfiguracyjny i zwraca słownik klucz→wartość.

    Format pliku: jedna para "klucz=wartosc" na linię; linie bez "="
    są pomijane. Przy braku pliku zwraca pusty słownik.

    Args:
        sciezka: ścieżka do pliku konfiguracyjnego.

    Returns:
        dict[str, str]: słownik z parami lub {} gdy plik nie istnieje.
    """
    try:
        config = Path(sciezka).read_text(encoding="utf-8").splitlines()
        wynik = {}
        for linia in config:
            if "=" not in linia:
                continue
            klucz, wartosc = linia.split("=", 1)
            wynik[klucz.strip()] = wartosc.strip()
        return wynik
    except FileNotFoundError:
        return {}
