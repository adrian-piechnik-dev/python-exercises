import json
import math
import os
from typing import Any, Optional

import requests

# --- SPIS ZADAŃ ---
# Uwaga: funkcje w tym temacie są celowo proste — nowa wiedza siedzi
# w testach, które do nich napiszesz (parametrize, raises, approx, setenv).
#
# zadanie_01 — dzielenie z wyjątkiem ValueError przy dzielniku 0
# zadanie_02 — średnia listy z wyjątkiem ValueError przy pustej liście
# zadanie_03 — kategoria wiekowa (dziecko/nastolatek/dorosly) + ValueError
# zadanie_04 — pole koła (math.pi) z wyjątkiem przy ujemnym promieniu
# zadanie_05 — odczyt zmiennej środowiskowej (brak → None)
# zadanie_06 — odczyt klucza API ze środowiska (brak → ValueError)
# zadanie_07 — prosta walidacja adresu e-mail (bool)
# zadanie_08 — cena brutto z VAT + ValueError przy ujemnym netto
# zadanie_09 — wczytanie konfiguracji z pliku JSON
# zadanie_10 — odczyt ustawienia ze słownika konfiguracji (brak → None)
# zadanie_11 — pobranie kursu waluty z API (zazębienie: temat 11)
# zadanie_12 — pobranie kursu bezpiecznie (RequestException → None,
#              zazębienie: tematy 4 i 11)


def zadanie_01_podziel(dzielna: float, dzielnik: float) -> float:
    """Dzieli dzielną przez dzielnik; dzielnik 0 to błąd danych wejściowych.

    Args:
        dzielna: liczba dzielona.
        dzielnik: liczba, przez którą dzielimy; nie może być 0.

    Returns:
        float: wynik dzielenia. Rzuca ValueError, gdy dzielnik == 0.
    """
    # TODO: jeśli dzielnik == 0 — raise ValueError("dzielnik nie moze byc zerem")
    # TODO: zwróć dzielna / dzielnik
    pass


def zadanie_02_srednia(liczby: list[float]) -> float:
    """Liczy średnią arytmetyczną listy liczb; pusta lista to błąd.

    Args:
        liczby: lista liczb; nie może być pusta.

    Returns:
        float: średnia arytmetyczna. Rzuca ValueError dla pustej listy.
    """
    # TODO: jeśli len(liczby) == 0 — raise ValueError("pusta lista")
    # TODO: zwróć sum(liczby) / len(liczby)
    pass


def zadanie_03_kategoria_wieku(wiek: int) -> str:
    """Przypisuje kategorię wiekową; ujemny wiek to błąd danych.

    Args:
        wiek: wiek w latach; nie może być ujemny.

    Returns:
        str: "dziecko" (0-12), "nastolatek" (13-17) lub "dorosly" (18+).
            Rzuca ValueError dla wieku ujemnego.
    """
    # TODO: jeśli wiek < 0 — raise ValueError("wiek nie moze byc ujemny")
    # TODO: jeśli wiek < 13 — return "dziecko"
    # TODO: jeśli wiek < 18 — return "nastolatek"
    # TODO: w pozostałych przypadkach — return "dorosly"
    pass


def zadanie_04_pole_kola(promien: float) -> float:
    """Liczy pole koła o podanym promieniu; ujemny promień to błąd.

    Args:
        promien: promień koła; nie może być ujemny.

    Returns:
        float: pole koła (pi * promien**2). Rzuca ValueError dla
            promienia ujemnego.
    """
    # TODO: jeśli promien < 0 — raise ValueError("promien nie moze byc ujemny")
    # TODO: zwróć math.pi * promien ** 2
    pass


def zadanie_05_czytaj_ustawienie(nazwa: str) -> Optional[str]:
    """Czyta wartość zmiennej środowiskowej o podanej nazwie.

    Args:
        nazwa: nazwa zmiennej środowiskowej.

    Returns:
        Optional[str]: wartość zmiennej lub None, gdy nie jest ustawiona.
    """
    # TODO: zwróć os.environ.get(nazwa) — .get daje None gdy zmiennej brak
    pass


def zadanie_06_klucz_api() -> str:
    """Czyta klucz API ze zmiennej środowiskowej API_KLUCZ; brak to błąd.

    Args:
        Brak.

    Returns:
        str: wartość zmiennej API_KLUCZ. Rzuca ValueError, gdy zmienna
            nie jest ustawiona.
    """
    # TODO: pobierz klucz = os.environ.get("API_KLUCZ")
    # TODO: jeśli klucz is None — raise ValueError("brak klucza API")
    # TODO: return klucz
    pass


def zadanie_07_waliduj_email(email: str) -> bool:
    """Sprawdza prostą poprawność adresu e-mail (obecność @ i kropki).

    Args:
        email: tekst do sprawdzenia.

    Returns:
        bool: True gdy tekst zawiera znak "@" ORAZ znak "."; inaczej False.
    """
    # TODO: zwróć wynik wyrażenia: "@" in email and "." in email
    pass


def zadanie_08_cena_brutto(netto: float, stawka_vat: float) -> float:
    """Liczy cenę brutto z ceny netto i stawki VAT; ujemne netto to błąd.

    Args:
        netto: cena netto; nie może być ujemna.
        stawka_vat: stawka VAT jako ułamek (np. 0.23 = 23%).

    Returns:
        float: cena brutto (netto * (1 + stawka_vat)). Rzuca ValueError
            dla ujemnego netto.
    """
    # TODO: jeśli netto < 0 — raise ValueError("cena netto nie moze byc ujemna")
    # TODO: zwróć netto * (1 + stawka_vat)
    pass


def zadanie_09_wczytaj_konfiguracje(sciezka: str) -> dict[str, Any]:
    """Wczytuje słownik konfiguracji z pliku JSON.

    Args:
        sciezka: ścieżka do istniejącego pliku JSON z obiektem.

    Returns:
        dict[str, Any]: słownik konfiguracji odtworzony z pliku.
    """
    # TODO: otwórz plik: open(sciezka, "r", encoding="utf-8") w bloku with
    # TODO: zwróć json.load(f) (wzorzec z tematu 7)
    pass


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
    # TODO: zwróć konfiguracja.get(klucz) (wzorzec z tematu 3)
    pass


def zadanie_11_pobierz_kurs(url: str) -> float:
    """Pobiera z API kurs waluty; błędy HTTP przepuszcza jako wyjątki.

    Args:
        url: adres API zwracającego {"kurs": <liczba>}.

    Returns:
        float: wartość pola "kurs" z odpowiedzi jako float.
    """
    # TODO: wywołaj requests.get(url, timeout=10) (wzorzec z tematu 11)
    # TODO: wywołaj response.raise_for_status()
    # TODO: pobierz dane przez response.json()
    # TODO: zwróć float(dane["kurs"])
    pass


def zadanie_12_pobierz_kurs_bezpiecznie(url: str) -> Optional[float]:
    """Pobiera kurs waluty; każdy błąd sieciowy lub HTTP zamienia na None.

    Args:
        url: adres API zwracającego {"kurs": <liczba>}.

    Returns:
        Optional[float]: kurs jako float lub None przy dowolnym błędzie
            z rodziny RequestException.
    """
    # TODO: użyj try/except requests.RequestException (wzorzec z tematu 4:
    #       sygnalizacja błędu przez None)
    # TODO: w try: requests.get(url, timeout=10), raise_for_status(),
    #       return float(response.json()["kurs"])
    # TODO: w except: return None
    pass
