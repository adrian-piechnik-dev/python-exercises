import csv
import json
from typing import Any, Optional

import requests
from requests import RequestException


def zadanie_01_pobierz_status(url: str) -> int:
    """Wysyła zapytanie GET i zwraca kod statusu odpowiedzi.

    Args:
        url: adres API do odpytania.

    Returns:
        int: kod statusu HTTP odpowiedzi (np. 200).
    """
    response = requests.get(url, timeout=10)
    return response.status_code


def zadanie_02_pobierz_json(url: str) -> dict[str, Any]:
    """Wysyła zapytanie GET i zwraca treść odpowiedzi jako słownik.

    Args:
        url: adres API do odpytania.

    Returns:
        dict[str, Any]: sparsowana treść odpowiedzi.
    """
    response = requests.get(url, timeout=10)
    return response.json()


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
    response = requests.get(url, params=parametry, timeout=10)
    return response.json()


def zadanie_04_czy_sukces(url: str) -> bool:
    """Sprawdza, czy zapytanie GET zakończyło się kodem 200.

    Args:
        url: adres API do odpytania.

    Returns:
        bool: True gdy status_code == 200, w przeciwnym razie False.
    """
    response = requests.get(url, timeout=10)
    return response.status_code == 200


def zadanie_05_pobierz_z_kontrola(url: str) -> dict[str, Any]:
    """Pobiera dane GET-em, rzucając HTTPError przy kodach błędów 4xx/5xx.

    Args:
        url: adres API do odpytania.

    Returns:
        dict[str, Any]: sparsowana treść odpowiedzi (tylko przy sukcesie).
    """
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def zadanie_06_pobierz_bezpiecznie(url: str) -> Optional[dict[str, Any]]:
    """Pobiera dane GET-em; każdy błąd sieciowy lub HTTP zamienia na None.

    Args:
        url: adres API do odpytania.

    Returns:
        Optional[dict[str, Any]]: sparsowana treść odpowiedzi lub None
            przy dowolnym błędzie z rodziny RequestException.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except RequestException:
        return None


def zadanie_07_wyslij_post(url: str, dane: dict[str, Any]) -> int:
    """Wysyła słownik POST-em jako JSON i zwraca kod statusu odpowiedzi.

    Args:
        url: adres API przyjmującego dane.
        dane: słownik do wysłania w treści zapytania.

    Returns:
        int: kod statusu HTTP odpowiedzi (np. 201 = utworzono).
    """
    response = requests.post(url, json=dane, timeout=10)
    return response.status_code


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
    response = requests.post(url, json=dane, headers=naglowki, timeout=10)
    return response.json()


def zadanie_09_pobierz_liste_uzytkownikow(url: str) -> list[dict[str, Any]]:
    """Pobiera listę użytkowników GET-em z kontrolą błędów serwera.

    Args:
        url: adres API zwracającego listę użytkowników.

    Returns:
        list[dict[str, Any]]: lista słowników z danymi użytkowników.
    """
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def zadanie_10_pobierz_pole(url: str, pole: str) -> Optional[Any]:
    """Pobiera dane GET-em i zwraca wartość jednego pola ze słownika odpowiedzi.

    Args:
        url: adres API do odpytania.
        pole: nazwa klucza do wyciągnięcia z odpowiedzi.

    Returns:
        Optional[Any]: wartość pola lub None, gdy pola nie ma w odpowiedzi.
    """
    response = requests.get(url, timeout=10)
    dane = response.json()
    return dane.get(pole)


def zadanie_11_zapisz_odpowiedz_do_json(url: str, sciezka: str) -> bool:
    """Pobiera dane GET-em i zapisuje je do pliku JSON.

    Args:
        url: adres API do odpytania.
        sciezka: ścieżka do pliku wynikowego .json.

    Returns:
        bool: True po pomyślnym pobraniu i zapisie.
    """
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    dane = response.json()
    with open(sciezka, "w", encoding="utf-8") as f:
        json.dump(dane, f)
    return True


def zadanie_12_zapisz_uzytkownikow_do_csv(url: str, sciezka: str) -> int:
    """Pobiera listę użytkowników GET-em i zapisuje ją do pliku CSV.

    Args:
        url: adres API zwracającego listę słowników o tych samych kluczach.
        sciezka: ścieżka do pliku wynikowego .csv.

    Returns:
        int: liczba zapisanych wierszy danych (bez nagłówka).
    """
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    lista = response.json()
    fieldnames = list(lista[0].keys())
    with open(sciezka, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(lista)
    return len(lista)

