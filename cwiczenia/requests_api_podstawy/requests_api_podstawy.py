import csv
import json
from typing import Any, Optional

import requests

# --- SPIS ZADAŃ ---
# zadanie_01 — pobierz kod statusu odpowiedzi (GET + timeout)
# zadanie_02 — pobierz treść odpowiedzi jako słownik (response.json)
# zadanie_03 — pobierz dane z parametrami zapytania (params)
# zadanie_04 — sprawdź, czy zapytanie się powiodło (status_code == 200)
# zadanie_05 — pobierz dane z kontrolą błędów serwera (raise_for_status)
# zadanie_06 — pobierz dane bezpiecznie (RequestException → None)
# zadanie_07 — wyślij dane POST-em i zwróć kod statusu (json=)
# zadanie_08 — wyślij dane POST-em z nagłówkami (headers=)
# zadanie_09 — pobierz listę użytkowników (GET + raise_for_status + json)
# zadanie_10 — pobierz jedno pole z odpowiedzi (brak pola → None)
# zadanie_11 — pobierz dane i zapisz je do pliku JSON (zazębienie: temat 7)
# zadanie_12 — pobierz listę użytkowników i zapisz do CSV (zazębienie: temat 6)


def zadanie_01_pobierz_status(url: str) -> int:
    """Wysyła zapytanie GET i zwraca kod statusu odpowiedzi.

    Args:
        url: adres API do odpytania.

    Returns:
        int: kod statusu HTTP odpowiedzi (np. 200).
    """
    # TODO: wywołaj requests.get(url, timeout=10) i zapisz do zmiennej response
    # TODO: zwróć response.status_code
    pass


def zadanie_02_pobierz_json(url: str) -> dict[str, Any]:
    """Wysyła zapytanie GET i zwraca treść odpowiedzi jako słownik.

    Args:
        url: adres API do odpytania.

    Returns:
        dict[str, Any]: sparsowana treść odpowiedzi.
    """
    # TODO: wywołaj requests.get(url, timeout=10)
    # TODO: zwróć response.json() (z nawiasami — to metoda!)
    pass


def zadanie_03_pobierz_z_parametrami(
    url: str, parametry: dict[str, Any]
) -> dict[str, Any]:
    """Wysyła zapytanie GET z parametrami zapytania i zwraca treść jako słownik.

    Args:
        url: adres API do odpytania.
        parametry: słownik parametrów zapytania (np. {"miasto": "Warszawa"}).

    Returns:
        dict[str, Any]: sparsowana treść odpowiedzi.
    """
    # TODO: wywołaj requests.get(url, params=parametry, timeout=10)
    # TODO: zwróć response.json()
    pass


def zadanie_04_czy_sukces(url: str) -> bool:
    """Sprawdza, czy zapytanie GET zakończyło się kodem 200.

    Args:
        url: adres API do odpytania.

    Returns:
        bool: True gdy status_code == 200, w przeciwnym razie False.
    """
    # TODO: wywołaj requests.get(url, timeout=10)
    # TODO: zwróć wynik porównania response.status_code == 200
    pass


def zadanie_05_pobierz_z_kontrola(url: str) -> dict[str, Any]:
    """Pobiera dane GET-em, rzucając HTTPError przy kodach błędów 4xx/5xx.

    Args:
        url: adres API do odpytania.

    Returns:
        dict[str, Any]: sparsowana treść odpowiedzi (tylko przy sukcesie).
    """
    # TODO: wywołaj requests.get(url, timeout=10)
    # TODO: wywołaj response.raise_for_status() (PRZED .json()!)
    # TODO: zwróć response.json()
    pass


def zadanie_06_pobierz_bezpiecznie(url: str) -> Optional[dict[str, Any]]:
    """Pobiera dane GET-em; każdy błąd sieciowy lub HTTP zamienia na None.

    Args:
        url: adres API do odpytania.

    Returns:
        Optional[dict[str, Any]]: sparsowana treść odpowiedzi lub None
            przy dowolnym błędzie z rodziny RequestException.
    """
    # TODO: użyj try/except requests.RequestException
    # TODO: w try: requests.get(url, timeout=10), potem raise_for_status(),
    #       potem return response.json()
    # TODO: w except: return None
    pass


def zadanie_07_wyslij_post(url: str, dane: dict[str, Any]) -> int:
    """Wysyła słownik POST-em jako JSON i zwraca kod statusu odpowiedzi.

    Args:
        url: adres API przyjmującego dane.
        dane: słownik do wysłania w treści zapytania.

    Returns:
        int: kod statusu HTTP odpowiedzi (np. 201 = utworzono).
    """
    # TODO: wywołaj requests.post(url, json=dane, timeout=10)
    #       — nazwany argument json=, nie pozycyjny!
    # TODO: zwróć response.status_code
    pass


def zadanie_08_wyslij_post_z_naglowkami(
    url: str, dane: dict[str, Any], naglowki: dict[str, str]
) -> dict[str, Any]:
    """Wysyła słownik POST-em z nagłówkami i zwraca treść odpowiedzi.

    Args:
        url: adres API przyjmującego dane.
        dane: słownik do wysłania w treści zapytania.
        naglowki: słownik nagłówków HTTP (np. {"Authorization": "Bearer klucz"}).

    Returns:
        dict[str, Any]: sparsowana treść odpowiedzi serwera.
    """
    # TODO: wywołaj requests.post(url, json=dane, headers=naglowki, timeout=10)
    # TODO: zwróć response.json()
    pass


def zadanie_09_pobierz_liste_uzytkownikow(url: str) -> list[dict[str, Any]]:
    """Pobiera listę użytkowników GET-em z kontrolą błędów serwera.

    Args:
        url: adres API zwracającego listę użytkowników.

    Returns:
        list[dict[str, Any]]: lista słowników z danymi użytkowników.
    """
    # TODO: wywołaj requests.get(url, timeout=10)
    # TODO: wywołaj response.raise_for_status()
    # TODO: zwróć response.json() (tym razem to lista słowników)
    pass


def zadanie_10_pobierz_pole(url: str, pole: str) -> Optional[Any]:
    """Pobiera dane GET-em i zwraca wartość jednego pola ze słownika odpowiedzi.

    Args:
        url: adres API do odpytania.
        pole: nazwa klucza do wyciągnięcia z odpowiedzi.

    Returns:
        Optional[Any]: wartość pola lub None, gdy pola nie ma w odpowiedzi.
    """
    # TODO: wywołaj requests.get(url, timeout=10) i pobierz dane przez .json()
    # TODO: zwróć dane.get(pole) — .get zwraca None gdy klucza brak
    #       (znasz to z tematu 3 — Słowniki)
    pass


def zadanie_11_zapisz_odpowiedz_do_json(url: str, sciezka: str) -> bool:
    """Pobiera dane GET-em i zapisuje je do pliku JSON.

    Args:
        url: adres API do odpytania.
        sciezka: ścieżka do pliku wynikowego .json.

    Returns:
        bool: True po pomyślnym pobraniu i zapisie.
    """
    # TODO: wywołaj requests.get(url, timeout=10)
    # TODO: wywołaj response.raise_for_status()
    # TODO: pobierz dane przez response.json()
    # TODO: otwórz plik: open(sciezka, "w", encoding="utf-8") w bloku with
    #       i zapisz dane przez json.dump(dane, f) (znasz z tematu 7)
    # TODO: return True
    pass


def zadanie_12_zapisz_uzytkownikow_do_csv(url: str, sciezka: str) -> int:
    """Pobiera listę użytkowników GET-em i zapisuje ją do pliku CSV.

    Args:
        url: adres API zwracającego listę słowników o tych samych kluczach.
        sciezka: ścieżka do pliku wynikowego .csv.

    Returns:
        int: liczba zapisanych wierszy danych (bez nagłówka).
    """
    # TODO: wywołaj requests.get(url, timeout=10) i raise_for_status()
    # TODO: pobierz listę przez response.json()
    # TODO: wyznacz fieldnames: list(lista[0].keys()) — klucze pierwszego słownika
    # TODO: otwórz plik: open(sciezka, "w", newline="", encoding="utf-8")
    #       w bloku with (newline="" — pamiętasz z tematu 6!)
    # TODO: utwórz writer = csv.DictWriter(f, fieldnames=fieldnames),
    #       wywołaj writer.writeheader() i writer.writerows(lista)
    # TODO: zwróć len(lista)
    pass
