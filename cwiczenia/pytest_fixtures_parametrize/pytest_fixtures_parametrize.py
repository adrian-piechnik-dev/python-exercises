import json
import math
import os
from typing import Any, Optional

import requests


def zadanie_01_podziel(dzielna: float, dzielnik: float) -> float:
    """Dzieli dzielną przez dzielnik; dzielnik 0 to błąd danych wejściowych.

    Args:
        dzielna: liczba dzielona.
        dzielnik: liczba, przez którą dzielimy; nie może być 0.

    Returns:
        float: wynik dzielenia. Rzuca ValueError, gdy dzielnik == 0.
    """
    if dzielnik == 0:
        raise ValueError("dzielnik nie moze byc zerem")
    return dzielna / dzielnik


def zadanie_02_srednia(liczby: list[float]) -> float:
    """Liczy średnią arytmetyczną listy liczb; pusta lista to błąd.

    Args:
        liczby: lista liczb; nie może być pusta.

    Returns:
        float: średnia arytmetyczna. Rzuca ValueError dla pustej listy.
    """
    if len(liczby) == 0:
        raise ValueError("pusta lista")
    return sum(liczby) / len(liczby)


def zadanie_03_kategoria_wieku(wiek: int) -> str:
    """Przypisuje kategorię wiekową; ujemny wiek to błąd danych.

    Args:
        wiek: wiek w latach; nie może być ujemny.

    Returns:
        str: "dziecko" (0-12), "nastolatek" (13-17) lub "dorosly" (18+).
            Rzuca ValueError dla wieku ujemnego.
    """
    if wiek < 0:
        raise ValueError("wiek nie moze byc ujemny")
    if wiek < 13:
        return "dziecko"
    elif wiek < 18:
        return "nastolatek"
    else:
        return "dorosly"


def zadanie_04_pole_kola(promien: float) -> float:
    """Liczy pole koła o podanym promieniu; ujemny promień to błąd.

    Args:
        promien: promień koła; nie może być ujemny.

    Returns:
        float: pole koła (pi * promien**2). Rzuca ValueError dla
            promienia ujemnego.
    """
    if promien < 0:
        raise ValueError("promien nie moze byc ujemny")
    return math.pi * promien ** 2


def zadanie_05_czytaj_ustawienie(nazwa: str) -> Optional[str]:
    """Czyta wartość zmiennej środowiskowej o podanej nazwie.

    Args:
        nazwa: nazwa zmiennej środowiskowej.

    Returns:
        Optional[str]: wartość zmiennej lub None, gdy nie jest ustawiona.
    """
    return os.environ.get(nazwa)


def zadanie_06_klucz_api() -> str:
    """Czyta klucz API ze zmiennej środowiskowej API_KLUCZ; brak to błąd.

    Args:
        Brak.

    Returns:
        str: wartość zmiennej API_KLUCZ. Rzuca ValueError, gdy zmienna
            nie jest ustawiona.
    """
    klucz = os.environ.get("API_KLUCZ")
    if klucz is None:
        raise ValueError("brak klucza API")
    return klucz


def zadanie_07_waliduj_email(email: str) -> bool:
    """Sprawdza prostą poprawność adresu e-mail (obecność @ i kropki).

    Args:
        email: tekst do sprawdzenia.

    Returns:
        bool: True gdy tekst zawiera znak "@" ORAZ znak "."; inaczej False.
    """
    return "@" in email and "." in email


def zadanie_08_cena_brutto(netto: float, stawka_vat: float) -> float:
    """Liczy cenę brutto z ceny netto i stawki VAT; ujemne netto to błąd.

    Args:
        netto: cena netto; nie może być ujemna.
        stawka_vat: stawka VAT jako ułamek (np. 0.23 = 23%).

    Returns:
        float: cena brutto (netto * (1 + stawka_vat)). Rzuca ValueError
            dla ujemnego netto.
    """
    if netto < 0:
        raise ValueError("cena netto nie moze byc ujemna")
    return netto * (1 + stawka_vat)


def zadanie_09_wczytaj_konfiguracje(sciezka: str) -> dict[str, Any]:
    """Wczytuje słownik konfiguracji z pliku JSON.

    Args:
        sciezka: ścieżka do istniejącego pliku JSON z obiektem.

    Returns:
        dict[str, Any]: słownik konfiguracji odtworzony z pliku.
    """
    with open(sciezka, "r", encoding="utf-8") as f:
        return json.load(f)


def zadanie_10_pobierz_ustawienie(
    konfiguracja: dict[str, Any], klucz: str
) -> Optional[Any]:
    """Pobiera wartość ustawienia ze słownika konfiguracji.

    Args:
        konfiguracja: słownik z ustawieniami.
        klucz: nazwa ustawienia do pobrania.

    Returns:
        Optional[Any]: wartość ustawienia lub None, gdy klucza brak.
    """
    return konfiguracja.get(klucz)


def zadanie_11_pobierz_kurs(url: str) -> float:
    """Pobiera z API kurs waluty; błędy HTTP przepuszcza jako wyjątki.

    Args:
        url: adres API zwracającego {"kurs": <liczba>}.

    Returns:
        float: wartość pola "kurs" z odpowiedzi jako float.
    """
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    dane = response.json()
    return float(dane["kurs"])


def zadanie_12_pobierz_kurs_bezpiecznie(url: str) -> Optional[float]:
    """Pobiera kurs waluty; każdy błąd sieciowy lub HTTP zamienia na None.

    Args:
        url: adres API zwracającego {"kurs": <liczba>}.

    Returns:
        Optional[float]: kurs jako float lub None przy dowolnym błędzie
            z rodziny RequestException.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return float(response.json()["kurs"])
    except requests.RequestException:
        return None