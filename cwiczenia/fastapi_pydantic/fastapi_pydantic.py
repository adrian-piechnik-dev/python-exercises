import json

from fastapi import FastAPI
from pydantic import BaseModel

# --- SPIS ZADAŃ ---
# Każde zadanie buduje i ZWRACA własną mini-aplikację FastAPI
# (endpointy definiujesz wewnątrz funkcji zadania — def w def).
#
# zadanie_01 — aplikacja z jednym endpointem powitalnym (GET /)
# zadanie_02 — aplikacja z dwoma endpointami (GET / i GET /o-nas)
# zadanie_03 — parametr ścieżki z walidacją int (GET /uzytkownicy/{id})
# zadanie_04 — obliczenie na parametrze ścieżki (GET /kwadrat/{liczba})
# zadanie_05 — model Pydantic w akcji: utwórz obiekt Produkt z walidacją
# zadanie_06 — POST z modelem w treści zapytania (422 przy złych danych)
# zadanie_07 — POST z modelem Zamowienie i obliczeniem odpowiedzi
# zadanie_08 — response_model wycina nadmiarowe pola odpowiedzi
# zadanie_09 — POST-echo: response_model na odpowiedzi z modelu
# zadanie_10 — GET czytający dane z pliku JSON (zazębienie: temat 7)
# zadanie_11 — POST dopisujący produkt do pliku JSON
# zadanie_12 — pełne API: GET lista + POST dodawanie na wspólnym pliku


class Produkt(BaseModel):
    """Model produktu sklepowego — bramkarz danych wejściowych.

    Args:
        nazwa: nazwa produktu.
        cena: cena produktu (Pydantic skonwertuje np. "49" na 49.0).

    Returns:
        Produkt: obiekt z polami nazwa i cena po walidacji.
    """

    # TODO: zadeklaruj pole nazwa typu str (składnia: nazwa_pola: typ)
    # TODO: zadeklaruj pole cena typu float
    pass


class Zamowienie(BaseModel):
    """Model zamówienia — nazwa produktu, ilość sztuk i cena jednostkowa.

    Args:
        nazwa: nazwa zamawianego produktu.
        ilosc: liczba sztuk (int).
        cena_jednostkowa: cena jednej sztuki (float).

    Returns:
        Zamowienie: obiekt zamówienia po walidacji.
    """

    # TODO: zadeklaruj pole nazwa typu str
    # TODO: zadeklaruj pole ilosc typu int
    # TODO: zadeklaruj pole cena_jednostkowa typu float
    pass


def zadanie_01_aplikacja_powitalna() -> FastAPI:
    """Buduje aplikację z jednym endpointem GET / zwracającym powitanie.

    Args:
        Brak.

    Returns:
        FastAPI: aplikacja, której GET / odpowiada
            {"wiadomosc": "Witaj w API"}.
    """
    # TODO: utwórz app = FastAPI()
    # TODO: zdefiniuj endpoint (def w def!):
    #       @app.get("/")
    #       def powitanie() -> dict:
    #           return {"wiadomosc": "Witaj w API"}
    # TODO: return app
    pass


def zadanie_02_dwa_endpointy() -> FastAPI:
    """Buduje aplikację z dwoma endpointami GET: / oraz /o-nas.

    Args:
        Brak.

    Returns:
        FastAPI: aplikacja, której GET / odpowiada
            {"wiadomosc": "Witaj w API"}, a GET /o-nas odpowiada
            {"nazwa": "Sklep Python", "wersja": 1}.
    """
    # TODO: utwórz app = FastAPI()
    # TODO: zdefiniuj pierwszy endpoint GET "/" zwracający
    #       {"wiadomosc": "Witaj w API"}
    # TODO: zdefiniuj drugi endpoint GET "/o-nas" zwracający
    #       {"nazwa": "Sklep Python", "wersja": 1}
    #       (druga funkcja z dekoratorem, inna nazwa funkcji)
    # TODO: return app
    pass


def zadanie_03_parametr_sciezki() -> FastAPI:
    """Buduje aplikację z endpointem o parametrze ścieżki walidowanym jako int.

    Args:
        Brak.

    Returns:
        FastAPI: aplikacja, której GET /uzytkownicy/{id_uzytkownika}
            odpowiada {"id": <int z adresu>}; tekst zamiast liczby
            w adresie daje automatyczne 422.
    """
    # TODO: utwórz app = FastAPI()
    # TODO: zdefiniuj endpoint @app.get("/uzytkownicy/{id_uzytkownika}")
    #       z funkcją przyjmującą id_uzytkownika: int (type hint = walidacja!)
    #       i zwracającą {"id": id_uzytkownika}
    # TODO: return app
    pass


def zadanie_04_kwadrat_liczby() -> FastAPI:
    """Buduje aplikację liczącą kwadrat liczby z parametru ścieżki.

    Args:
        Brak.

    Returns:
        FastAPI: aplikacja, której GET /kwadrat/{liczba} odpowiada
            {"wynik": liczba * liczba}; parametr walidowany jako int.
    """
    # TODO: utwórz app = FastAPI()
    # TODO: zdefiniuj endpoint @app.get("/kwadrat/{liczba}")
    #       z funkcją przyjmującą liczba: int
    #       i zwracającą {"wynik": liczba * liczba}
    # TODO: return app
    pass


def zadanie_05_utworz_produkt(nazwa: str, cena: object) -> Produkt:
    """Tworzy obiekt Produkt, przepuszczając dane przez walidację Pydantic.

    Args:
        nazwa: nazwa produktu.
        cena: cena — dowolna wartość; Pydantic skonwertuje lub rzuci
            ValidationError.

    Returns:
        Produkt: zwalidowany obiekt produktu. Rzuca
            pydantic.ValidationError, gdy cena nie da się skonwertować
            na float.
    """
    # TODO: zwróć Produkt(nazwa=nazwa, cena=cena)
    #       (walidację robi Pydantic — nie pisz żadnych ifów)
    pass


def zadanie_06_przyjmij_produkt() -> FastAPI:
    """Buduje aplikację przyjmującą produkt POST-em z walidacją modelu.

    Args:
        Brak.

    Returns:
        FastAPI: aplikacja, której POST /produkty przyjmuje w treści
            JSON pasujący do modelu Produkt i odpowiada
            {"przyjeto": <nazwa produktu>}; złe dane dają 422.
    """
    # TODO: utwórz app = FastAPI()
    # TODO: zdefiniuj endpoint @app.post("/produkty")
    #       z funkcją przyjmującą produkt: Produkt (model = treść zapytania)
    #       i zwracającą {"przyjeto": produkt.nazwa}
    # TODO: return app
    pass


def zadanie_07_przyjmij_zamowienie() -> FastAPI:
    """Buduje aplikację liczącą wartość zamówienia przyjętego POST-em.

    Args:
        Brak.

    Returns:
        FastAPI: aplikacja, której POST /zamowienia przyjmuje model
            Zamowienie i odpowiada
            {"do_zaplaty": ilosc * cena_jednostkowa}.
    """
    # TODO: utwórz app = FastAPI()
    # TODO: zdefiniuj endpoint @app.post("/zamowienia")
    #       z funkcją przyjmującą zamowienie: Zamowienie
    #       i zwracającą {"do_zaplaty":
    #       zamowienie.ilosc * zamowienie.cena_jednostkowa}
    # TODO: return app
    pass


def zadanie_08_response_model() -> FastAPI:
    """Buduje aplikację, w której response_model wycina tajne pole odpowiedzi.

    Args:
        Brak.

    Returns:
        FastAPI: aplikacja, której GET /produkty/polecany odpowiada
            wyłącznie polami modelu Produkt (nazwa, cena), mimo że
            endpoint zwraca też pole "tajny_kod".
    """
    # TODO: utwórz app = FastAPI()
    # TODO: zdefiniuj endpoint @app.get("/produkty/polecany",
    #       response_model=Produkt) z funkcją zwracającą słownik
    #       {"nazwa": "Klawiatura", "cena": 99.0, "tajny_kod": "X99"}
    #       — response_model przytnie odpowiedź do pól modelu
    # TODO: return app
    pass


def zadanie_09_echo_produktu() -> FastAPI:
    """Buduje aplikację-echo: POST zwraca przyjęty produkt przez response_model.

    Args:
        Brak.

    Returns:
        FastAPI: aplikacja, której POST /produkty/echo przyjmuje model
            Produkt i odsyła go z powrotem (response_model=Produkt).
    """
    # TODO: utwórz app = FastAPI()
    # TODO: zdefiniuj endpoint @app.post("/produkty/echo",
    #       response_model=Produkt) z funkcją przyjmującą produkt: Produkt
    #       i zwracającą produkt (cały obiekt — FastAPI sam go zserializuje)
    # TODO: return app
    pass


def zadanie_10_api_konfiguracji(sciezka: str) -> FastAPI:
    """Buduje aplikację serwującą zawartość pliku JSON pod GET /konfiguracja.

    Args:
        sciezka: ścieżka do istniejącego pliku JSON ze słownikiem.

    Returns:
        FastAPI: aplikacja, której GET /konfiguracja odpowiada
            zawartością pliku (czytaną przy każdym zapytaniu).
    """
    # TODO: utwórz app = FastAPI()
    # TODO: zdefiniuj endpoint @app.get("/konfiguracja") z funkcją, która:
    #       - otwiera plik: open(sciezka, "r", encoding="utf-8") w bloku with
    #       - zwraca json.load(f) (wzorzec z tematu 7)
    # TODO: return app
    pass


def zadanie_11_api_dodawania(sciezka: str) -> FastAPI:
    """Buduje aplikację dopisującą produkt POST-em do listy w pliku JSON.

    Args:
        sciezka: ścieżka do istniejącego pliku JSON z listą produktów.

    Returns:
        FastAPI: aplikacja, której POST /produkty dopisuje przyjęty
            produkt na koniec listy w pliku i odpowiada
            {"liczba": <nowa długość listy>}.
    """
    # TODO: utwórz app = FastAPI()
    # TODO: zdefiniuj endpoint @app.post("/produkty") z funkcją
    #       przyjmującą produkt: Produkt, która:
    #       - wczytuje listę z pliku (with + json.load — temat 7)
    #       - dopisuje produkt.model_dump() przez .append
    #       - zapisuje listę z powrotem (with + json.dump)
    #       - zwraca {"liczba": len(listy)}
    # TODO: return app
    pass


def zadanie_12_pelne_api(sciezka: str) -> FastAPI:
    """Buduje pełne API produktów: GET zwraca listę, POST dodaje do pliku.

    Args:
        sciezka: ścieżka do istniejącego pliku JSON z listą produktów.

    Returns:
        FastAPI: aplikacja z GET /produkty (lista z pliku)
            i POST /produkty (walidacja modelem Produkt, dopisanie
            do pliku, odpowiedź {"liczba": <nowa długość>}).
    """
    # TODO: utwórz app = FastAPI()
    # TODO: zdefiniuj endpoint GET "/produkty" zwracający listę
    #       wczytaną z pliku (with + json.load)
    # TODO: zdefiniuj endpoint POST "/produkty" jak w zadaniu 11:
    #       wczytaj listę, dopisz produkt.model_dump(), zapisz,
    #       zwróć {"liczba": len(listy)}
    # TODO: return app
    pass
