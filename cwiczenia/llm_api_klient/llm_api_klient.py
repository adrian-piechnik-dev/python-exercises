import logging

import requests


class BladKlientaLLM(Exception):
    """Wyjątek sygnalizujący błąd komunikacji z API modelu."""


def zadanie_01_zbuduj_naglowki(api_key: str) -> dict:
    """Buduje słownik nagłówków wymaganych przez API /v1/messages.

    Args:
        api_key: sekretny klucz API użytkownika.

    Returns:
        dict: trzy nagłówki — "x-api-key" z kluczem, "anthropic-version"
            równe "2023-06-01" i "content-type" równe "application/json".
    """
    # TODO: zwróć słownik z trzema nagłówkami opisanymi w Returns
    return {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }


def zadanie_02_zbuduj_payload(model: str, max_tokens: int, tresc: str) -> dict:
    """Buduje payload zapytania z jedną wiadomością użytkownika.

    Args:
        model: nazwa modelu, np. "claude-sonnet-4-6".
        max_tokens: górny limit długości odpowiedzi.
        tresc: treść pytania użytkownika.

    Returns:
        dict: klucze "model", "max_tokens" oraz "messages" — lista
            z jednym słownikiem {"role": "user", "content": tresc}.
    """
    return {
        "model": model,
        "max_tokens": max_tokens,
        "messages": [
            {"role": "user", "content": tresc},
        ]
    }


def zadanie_03_wyslij_zapytanie(
    url: str, naglowki: dict, payload: dict
) -> requests.Response:
    """Wysyła żądanie POST pod wskazany adres i zwraca surową odpowiedź.

    Args:
        url: adres endpointu API.
        naglowki: słownik nagłówków żądania.
        payload: słownik z treścią zapytania.

    Returns:
        requests.Response: obiekt odpowiedzi zwrócony przez requests.post.
    """
    return requests.post(url, headers=naglowki, json=payload, timeout=30)


def zadanie_04_potwierdz_sukces(odpowiedz: requests.Response) -> dict:
    """Sprawdza kod odpowiedzi i zwraca jej treść jako słownik.

    Args:
        odpowiedz: obiekt odpowiedzi z requests.post.

    Returns:
        dict: treść odpowiedzi po odpowiedz.json(); gdy kod to błąd
            (4xx/5xx), funkcja rzuca requests.exceptions.HTTPError.
    """
    # TODO: wywołaj odpowiedz.raise_for_status()
    # TODO: zwróć odpowiedz.json()
    pass


def zadanie_05_wyciagnij_tekst(dane: dict) -> str:
    """Wyciąga tekst pierwszego bloku treści z odpowiedzi modelu.

    Args:
        dane: słownik odpowiedzi API zawierający klucz "content".

    Returns:
        str: wartość dane["content"][0]["text"].
    """
    # TODO: zwróć dane["content"][0]["text"]
    pass


def zadanie_06_wyciagnij_tekst_bezpiecznie(dane: dict) -> str | None:
    """Wyciąga tekst odpowiedzi albo zwraca None przy zepsutej strukturze.

    Args:
        dane: słownik odpowiedzi API (może nie mieć klucza "content"
            albo mieć pustą listę bloków).

    Returns:
        str | None: tekst pierwszego bloku albo None, gdy struktura
            jest niepoprawna (brak klucza lub pusta lista).
    """
    # TODO: w bloku try zwróć dane["content"][0]["text"]
    # TODO: złap (KeyError, IndexError) i zwróć None
    pass


def zadanie_07_loguj_zapytanie(model: str, max_tokens: int) -> None:
    """Zapisuje w logu informację o wysyłanym zapytaniu.

    Args:
        model: nazwa modelu, do którego leci zapytanie.
        max_tokens: limit długości odpowiedzi.

    Returns:
        None: funkcja tylko loguje, niczego nie zwraca.
    """
    # TODO: wywołaj logging.info z szablonem
    #   "Wysylam zapytanie do modelu %s, max_tokens=%s"
    #   i argumentami model, max_tokens (NIE f-string!)
    pass


def zadanie_08_loguj_blad(komunikat: str) -> None:
    """Zapisuje w logu błąd klienta na poziomie ERROR.

    Args:
        komunikat: opis błędu do zapisania.

    Returns:
        None: funkcja tylko loguje, niczego nie zwraca.
    """
    # TODO: wywołaj logging.error z szablonem "Blad klienta LLM: %s"
    #   i argumentem komunikat
    pass


def zadanie_09_wyslij_z_obsluga_timeout(
    url: str, naglowki: dict, payload: dict
) -> requests.Response:
    """Wysyła żądanie POST, zamieniając Timeout na BladKlientaLLM.

    Args:
        url: adres endpointu API.
        naglowki: słownik nagłówków żądania.
        payload: słownik z treścią zapytania.

    Returns:
        requests.Response: odpowiedź serwera; przy przekroczeniu czasu
            funkcja rzuca BladKlientaLLM z oryginalną przyczyną (from).
    """
    # TODO: w bloku try wywołaj requests.post(url, headers=naglowki,
    #   json=payload, timeout=30) i zwróć wynik
    # TODO: złap requests.exceptions.Timeout as error i rzuć
    #   BladKlientaLLM("Przekroczono limit czasu") from error
    pass


def zadanie_10_wyslij_z_pelna_obsluga(
    url: str, naglowki: dict, payload: dict
) -> dict:
    """Wysyła żądanie POST z 4-warstwową obsługą wyjątków requests.

    Args:
        url: adres endpointu API.
        naglowki: słownik nagłówków żądania.
        payload: słownik z treścią zapytania.

    Returns:
        dict: treść odpowiedzi po .json(); każdy błąd requests zamienia
            się w BladKlientaLLM z oryginalną przyczyną (from).
    """
    # TODO: w bloku try:
    #   - wywołaj requests.post(url, headers=naglowki, json=payload, timeout=30)
    #   - wywołaj raise_for_status() na odpowiedzi
    #   - zwróć odpowiedz.json()
    # TODO: 4 warstwy except, każda: raise BladKlientaLLM("...") from error
    #   1) requests.exceptions.Timeout — "Przekroczono limit czasu"
    #   2) requests.exceptions.ConnectionError — "Brak polaczenia z serwerem"
    #   3) requests.exceptions.HTTPError — "Serwer zwrocil blad HTTP"
    #   4) requests.exceptions.RequestException — "Blad zadania" (OSTATNI!)
    pass


def zadanie_11_zapytaj_model(
    url: str, api_key: str, model: str, max_tokens: int, tresc: str
) -> dict:
    """Buduje nagłówki i payload, po czym wysyła pełne zapytanie do modelu.

    Args:
        url: adres endpointu API.
        api_key: sekretny klucz API.
        model: nazwa modelu.
        max_tokens: limit długości odpowiedzi.
        tresc: treść pytania użytkownika.

    Returns:
        dict: treść odpowiedzi; błędy requests lecą jako BladKlientaLLM.
    """
    # TODO: zbuduj nagłówki przez zadanie_01_zbuduj_naglowki(api_key)
    # TODO: zbuduj payload przez zadanie_02_zbuduj_payload(model, max_tokens, tresc)
    # TODO: zwróć wynik zadanie_10_wyslij_z_pelna_obsluga(url, naglowki, payload)
    pass


def zadanie_12_pelny_klient(
    url: str, api_key: str, model: str, max_tokens: int, tresc: str
) -> str | None:
    """Wysyła zapytanie z logowaniem i zwraca tekst odpowiedzi albo None.

    Args:
        url: adres endpointu API.
        api_key: sekretny klucz API.
        model: nazwa modelu.
        max_tokens: limit długości odpowiedzi.
        tresc: treść pytania użytkownika.

    Returns:
        str | None: tekst odpowiedzi modelu; None gdy wystąpił błąd
            komunikacji (zalogowany przez logging.error) albo odpowiedź
            ma zepsutą strukturę.
    """
    # TODO: zaloguj wysyłkę przez zadanie_07_loguj_zapytanie(model, max_tokens)
    # TODO: w bloku try pobierz dane przez zadanie_11_zapytaj_model(...)
    # TODO: złap BladKlientaLLM as error — zaloguj przez
    #   zadanie_08_loguj_blad(str(error)) i zwróć None
    # TODO: po udanym pobraniu zwróć zadanie_06_wyciagnij_tekst_bezpiecznie(dane)
    pass


if __name__ == "__main__":
    # TODO: skonfiguruj logging.basicConfig(level=logging.INFO)
    # TODO: wywołaj zadanie_07_loguj_zapytanie("claude-sonnet-4-6", 100),
    #   żeby zobaczyć wpis INFO w konsoli
    pass
