# Spis zadań (mini-projekt M2 — pipeline: zewnętrzne API -> plik JSON -> własne API):
# 01 — pobranie katalogu z zewnętrznego API z kontrolą błędów (None przy awarii)
# 02 — pobranie katalogu strona po stronie (paginacja + extend)
# 03 — filtr produktów dostępnych (list comprehension)
# 04 — przycięcie produktów do pól id, nazwa, cena
# 05 — wyszukanie produktu po id (None gdy brak)
# 06 — zapis katalogu do pliku JSON
# 07 — odczyt katalogu z pliku (None gdy brak pliku lub zepsuty JSON)
# 08 — bramkarz Pydantic: słownik -> obiekt Produkt (None gdy złe dane)
# 09 — aplikacja FastAPI: GET z listą produktów z pliku
# 10 — aplikacja FastAPI: GET szczegółów produktu po id (404 gdy brak)
# 11 — aplikacja FastAPI: POST dodający produkt do pliku (422 przy złych danych)
# 12 — dyrygent zaopatrzenia: z zewnętrznego API do pliku katalogu
# 13 — dyrygent całości: zaopatrzenie + pełne API sklepu (None gdy hurtownia padła)

import json
from typing import Any

import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError


class Produkt(BaseModel):
    """Model produktu w katalogu — bramkarz danych wchodzących do sklepu.

    Args:
        id: numer produktu (int).
        nazwa: nazwa produktu.
        cena: cena produktu (float).

    Returns:
        Produkt: obiekt z polami id, nazwa i cena po walidacji.
    """

    # TODO: zadeklaruj trzy pola modelu zgodnie z danymi katalogu
    #       (deklarację pól BaseModel znasz z tematu 16)
    pass


def zadanie_01_pobierz_katalog(url: str) -> list[dict[str, Any]] | None:
    """Pobiera pełny katalog produktów z zewnętrznego API.

    Args:
        url: adres endpointu zwracającego listę produktów jako JSON.

    Returns:
        list[dict[str, Any]] | None: sparsowana lista produktów albo None
            przy jakimkolwiek błędzie sieci lub serwera (także 4xx/5xx).
    """
    # TODO: pobierz dane z kontrolą błędów serwera i sieci — pełny
    #       bezpieczny wzorzec (timeout, kontrola kodu, wspólny rodzic
    #       wyjątków sieciowych) znasz z tematu 11
    # TODO: awaria to spodziewana sytuacja — kontrakt None, nie wyjątek
    pass


def zadanie_02_pobierz_strony(
    url: str, liczba_stron: int,
) -> list[dict[str, Any]]:
    """Pobiera katalog strona po stronie i skleja wyniki w jedną listę.

    Args:
        url: adres endpointu przyjmującego parametr zapytania "strona".
        liczba_stron: ile stron pobrać (numeracja od 1).

    Returns:
        list[dict[str, Any]]: produkty ze wszystkich stron w jednej,
            płaskiej liście; pusta lista dla liczba_stron równego 0.
    """
    # TODO: w pętli po numerach stron pobieraj kolejne porcje —
    #       numer strony przekazuj parametrem zapytania "strona"
    #       (params i timeout znasz z tematu 11)
    # TODO: porcje doklejaj do akumulatora wzorcem z teorii (sekcja 3) —
    #       uważaj na pułapkę append vs extend
    pass


def zadanie_03_filtruj_dostepne(
    produkty: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Zwraca tylko produkty oznaczone jako dostępne.

    Args:
        produkty: surowa lista produktów z kluczem "dostepny" (bool).

    Returns:
        list[dict[str, Any]]: nowa lista wyłącznie z produktami,
            których "dostepny" to True.
    """
    # TODO: przefiltruj listę jedną linijką — comprehension z warunkiem
    #       znasz z tematu 2
    pass


def zadanie_04_wybierz_pola(
    produkty: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Przycina każdy produkt do trzech pól: id, nazwa, cena.

    Args:
        produkty: lista produktów z nadmiarowymi polami (np. magazyn).

    Returns:
        list[dict[str, Any]]: nowa lista słowników zawierających
            WYŁĄCZNIE klucze id, nazwa i cena.
    """
    # TODO: dla każdego produktu zbuduj NOWY słownik z trzema potrzebnymi
    #       kluczami (budowanie słowników znasz z tematu 3; nie modyfikuj
    #       słowników wejściowych)
    pass


def zadanie_05_znajdz_produkt(
    produkty: list[dict[str, Any]], id_produktu: int,
) -> dict[str, Any] | None:
    """Wyszukuje produkt o podanym id.

    Args:
        produkty: lista produktów z kluczem "id".
        id_produktu: szukany numer produktu.

    Returns:
        dict[str, Any] | None: pierwszy produkt o pasującym id
            albo None, gdy takiego nie ma.
    """
    # TODO: przejdź po liście i porównuj id; znaleziony produkt zwróć
    #       od razu (early return z tematu 1), a po pętli obsłuż brak
    #       kontraktem None
    pass


def zadanie_06_zapisz_katalog(
    produkty: list[dict[str, Any]], sciezka: str,
) -> bool:
    """Zapisuje katalog produktów do pliku JSON.

    Args:
        produkty: lista produktów do zapisania.
        sciezka: ścieżka do pliku wynikowego .json.

    Returns:
        bool: True po pomyślnym zapisie pliku.
    """
    # TODO: zapisz listę do pliku wzorcem z tematu 7 (with + zapis JSON,
    #       encoding jak zawsze przy plikach tekstowych)
    pass


def zadanie_07_wczytaj_katalog(sciezka: str) -> list[dict[str, Any]] | None:
    """Wczytuje katalog produktów z pliku JSON.

    Args:
        sciezka: ścieżka do pliku .json z listą produktów.

    Returns:
        list[dict[str, Any]] | None: lista produktów albo None, gdy plik
            nie istnieje LUB jego treść nie jest poprawnym JSON-em.
    """
    # TODO: wczytaj plik wzorcem z tematu 7
    # TODO: obsłuż DWA spodziewane problemy kontraktem None: brak pliku
    #       (temat 5) i zepsutą treść (wyjątek JSON-a z tematu 7) —
    #       pamiętaj o zasadzie kolejności wyjątków z tematu 4
    pass


def zadanie_08_waliduj_produkt(dane: dict[str, Any]) -> Produkt | None:
    """Przepuszcza słownik przez bramkarza Pydantic.

    Args:
        dane: słownik z (potencjalnie) polami produktu.

    Returns:
        Produkt | None: zwalidowany obiekt Produkt albo None, gdy dane
            nie przechodzą walidacji modelu.
    """
    # TODO: zbuduj obiekt Produkt rozpakowując słownik do argumentów
    #       nazwanych (teoria, sekcja 4)
    # TODO: nieudaną walidację zamień na kontrakt None (łap TYLKO
    #       wyjątek walidacji — teoria, sekcja 4)
    pass


def zadanie_09_api_listy(sciezka: str) -> FastAPI:
    """Buduje aplikację serwującą listę produktów z pliku pod GET /produkty.

    Args:
        sciezka: ścieżka do istniejącego pliku .json z listą produktów.

    Returns:
        FastAPI: aplikacja, której GET /produkty odpowiada zawartością
            pliku (czytaną przy każdym zapytaniu).
    """
    # TODO: zbuduj aplikację-fabrykę z endpointem GET (def w def —
    #       wzorzec z tematu 16); endpoint przy każdym wywołaniu czyta
    #       plik i zwraca listę
    pass


def zadanie_10_api_szczegolow(sciezka: str) -> FastAPI:
    """Buduje aplikację z GET /produkty/{id_produktu} zwracającym jeden produkt.

    Args:
        sciezka: ścieżka do istniejącego pliku .json z listą produktów.

    Returns:
        FastAPI: aplikacja, której GET /produkty/{id_produktu} odpowiada
            produktem o podanym id albo kodem 404, gdy go nie ma;
            tekst zamiast liczby w adresie daje automatyczne 422.
    """
    # TODO: endpoint z parametrem ścieżki walidowanym jako int (temat 16)
    # TODO: wczytaj listę z pliku i znajdź produkt po id — masz już
    #       na to gotowy klocek wśród wcześniejszych zadań, użyj go
    # TODO: brak produktu zgłoś klientowi wzorcem z teorii (sekcja 5) —
    #       pamiętaj o pułapce raise vs return
    pass


def zadanie_11_api_dodawania(sciezka: str) -> FastAPI:
    """Buduje aplikację z POST /produkty dopisującym produkt do pliku.

    Args:
        sciezka: ścieżka do istniejącego pliku .json z listą produktów.

    Returns:
        FastAPI: aplikacja, której POST /produkty przyjmuje JSON pasujący
            do modelu Produkt (złe dane = automatyczne 422), dopisuje
            produkt do pliku i odpowiada {"liczba": <nowa długość listy>}.
    """
    # TODO: endpoint POST przyjmujący model Produkt jako treść zapytania
    #       (temat 16)
    # TODO: wczytaj listę z pliku, dopisz produkt zamieniony na słownik
    #       (metodę modelu znasz z tematu 16), zapisz listę z powrotem
    #       i zwróć nową liczebność
    pass


def zadanie_12_zbuduj_katalog(url: str, sciezka: str) -> bool | None:
    """Dyrygent zaopatrzenia: pobiera, czyści i zapisuje katalog na dysk.

    Args:
        url: adres endpointu zewnętrznego API z produktami.
        sciezka: ścieżka do wynikowego pliku .json katalogu.

    Returns:
        bool | None: True po zapisaniu czystego katalogu; None, gdy
            zewnętrzne API zawiodło (wtedy plik w ogóle nie powstaje).
    """
    # TODO: to dyrygent (teoria, sekcja 6) — połącz klocki: pobranie ->
    #       filtr dostępnych -> przycięcie pól -> zapis do pliku
    # TODO: gdy pobranie zwróci None, przerwij early returnem ZANIM
    #       cokolwiek trafi na dysk
    pass


def zadanie_13_pelne_api(url: str, sciezka: str) -> FastAPI | None:
    """Dyrygent całości: zaopatruje sklep i buduje pełne API katalogu.

    Args:
        url: adres endpointu zewnętrznego API z produktami.
        sciezka: ścieżka do pliku .json, w którym wyląduje katalog.

    Returns:
        FastAPI | None: aplikacja z trzema endpointami — GET /produkty
            (lista z pliku), GET /produkty/{id_produktu} (szczegóły
            albo 404) i POST /produkty (walidacja modelem, dopisanie
            do pliku) — albo None, gdy zaopatrzenie się nie powiodło.
    """
    # TODO: najpierw zaopatrzenie gotowym dyrygentem z zadania 12;
    #       niepowodzenie propaguj kontraktem None (teoria, sekcja 6)
    # TODO: potem zbuduj JEDNĄ aplikację łączącą trzy endpointy,
    #       które ćwiczyłeś w zadaniach 09-11 (wszystkie def w def
    #       na wspólnym app)
    pass
