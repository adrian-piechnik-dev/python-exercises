import json
from typing import Any, Optional


def zadanie_01_serializuj_slownik(slownik: dict[str, Any]) -> str:
    """Zamienia słownik na string w formacie JSON.

    Args:
        slownik: słownik do serializacji (klucze: str, wartości: dowolny typ JSON).

    Returns:
        str: string JSON reprezentujący przekazany słownik.
    """
    return json.dumps(slownik)


def zadanie_02_deserializuj_string(tekst: str) -> dict[str, Any]:
    """Zamienia string JSON na słownik Pythona.

    Args:
        tekst: string w formacie JSON reprezentujący obiekt (słownik).

    Returns:
        dict[str, Any]: słownik odtworzony z JSON-a.
    """
    return json.loads(tekst)


def zadanie_03_zapisz_do_pliku(sciezka: str, slownik: dict[str, Any]) -> None:
    """Zapisuje słownik do pliku JSON (nadpisuje jeśli plik istnieje).

    Args:
        sciezka: ścieżka do pliku wynikowego.
        slownik: słownik do zapisania.

    Returns:
        None
    """
    with open(sciezka, "w", encoding="utf-8") as f:
        json.dump(slownik, f, indent=2)


def zadanie_04_wczytaj_z_pliku(sciezka: str) -> dict[str, Any]:
    """Wczytuje słownik z pliku JSON.

    Args:
        sciezka: ścieżka do istniejącego pliku JSON zawierającego obiekt.

    Returns:
        dict[str, Any]: słownik odtworzony z pliku JSON.
    """
    with open(sciezka, "r", encoding="utf-8") as f:
        return json.load(f)


def zadanie_05_sformatowany_json(slownik: dict[str, Any], wciecie: int) -> str:
    """Zamienia słownik na sformatowany string JSON z wcięciami.

    Args:
        slownik: słownik do serializacji.
        wciecie: liczba spacji wcięcia (np. 2 lub 4).

    Returns:
        str: sformatowany string JSON z wcięciami o podanej szerokości.
    """
    return json.dumps(slownik, indent=wciecie)


def zadanie_06_serializuj_liste(lista: list[dict[str, Any]]) -> str:
    """Zamienia listę słowników na string JSON.

    Args:
        lista: lista słowników do serializacji.

    Returns:
        str: string JSON reprezentujący przekazaną listę słowników.
    """
    return json.dumps(lista)


def zadanie_07_wczytaj_liste_z_pliku(sciezka: str) -> list[dict[str, Any]]:
    """Wczytuje listę słowników z pliku JSON.

    Args:
        sciezka: ścieżka do istniejącego pliku JSON zawierającego tablicę obiektów.

    Returns:
        list[dict[str, Any]]: lista słowników odtworzona z pliku JSON.
    """
    with open(sciezka, "r", encoding="utf-8") as f:
        return json.load(f)


def zadanie_08_parsuj_bezpiecznie(tekst: str) -> Optional[dict[str, Any]]:
    """Parsuje string JSON; zwraca None gdy tekst nie jest poprawnym JSON-em.

    Args:
        tekst: string do sparsowania.

    Returns:
        Optional[dict[str, Any]]: słownik odtworzony z JSON-a lub None przy błędzie formatu.
    """
    try:
        return json.loads(tekst)
    except json.JSONDecodeError:
        return None


def zadanie_09_wczytaj_plik_bezpiecznie(
    sciezka: str,
) -> Optional[list[dict[str, Any]]]:
    """Wczytuje listę słowników z pliku JSON; zwraca None gdy plik nie istnieje lub jest uszkodzony.

    Args:
        sciezka: ścieżka do pliku JSON.

    Returns:
        Optional[list[dict[str, Any]]]: lista słowników lub None gdy brak pliku albo błąd formatu.
    """
    try:
        with open(sciezka, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None


def zadanie_10_zapisz_liste_do_pliku(
    sciezka: str, lista: list[dict[str, Any]]
) -> None:
    """Zapisuje listę słowników do pliku JSON (nadpisuje jeśli plik istnieje).

    Args:
        sciezka: ścieżka do pliku wynikowego.
        lista: lista słowników do zapisania.

    Returns:
        None
    """
    with open(sciezka, "w", encoding="utf-8") as f:
        json.dump(lista, f)


def zadanie_11_dopisz_wpis(sciezka: str, nowy_wpis: dict[str, Any]) -> None:
    """Dopisuje nowy słownik do listy wczytanej z pliku JSON i zapisuje wynik z powrotem.

    Args:
        sciezka: ścieżka do istniejącego pliku JSON zawierającego listę słowników.
        nowy_wpis: słownik do dopisania na koniec listy.

    Returns:
        None
    """
    with open(sciezka, "r", encoding="utf-8") as old:
        lista = json.load(old)
    lista.append(nowy_wpis)
    with open(sciezka, "w", encoding="utf-8") as new:
        json.dump(lista, new)


def zadanie_12_zlicz_po_kluczu(sciezka: str, klucz: str) -> dict[str, int]:
    """Wczytuje listę słowników z pliku JSON i zlicza wpisy pogrupowane według wartości klucza.

    Args:
        sciezka: ścieżka do pliku JSON zawierającego listę słowników.
        klucz: nazwa klucza, po którym grupujemy wpisy.

    Returns:
        dict[str, int]: słownik {wartość_klucza: liczba_wpisów}; pusty gdy lista jest pusta.
    """
    with open(sciezka, "r", encoding="utf-8") as f:
        lista = json.load(f)
        licznik = {}
        for wpis in lista:
            wartosc = wpis[klucz]
            if wartosc in licznik:
                licznik[wartosc] += 1
            else:
                licznik[wartosc] = 1
        return licznik