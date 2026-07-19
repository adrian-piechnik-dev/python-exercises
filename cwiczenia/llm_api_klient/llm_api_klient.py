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
    odpowiedz.raise_for_status()
    return odpowiedz.json()


def zadanie_05_wyciagnij_tekst(dane: dict) -> str:
    """Wyciąga tekst pierwszego bloku treści z odpowiedzi modelu.

    Args:
        dane: słownik odpowiedzi API zawierający klucz "content".

    Returns:
        str: wartość dane["content"][0]["text"].
    """
    return dane["content"][0]["text"]


def zadanie_06_wyciagnij_tekst_bezpiecznie(dane: dict) -> str | None:
    """Wyciąga tekst odpowiedzi albo zwraca None przy zepsutej strukturze.

    Args:
        dane: słownik odpowiedzi API (może nie mieć klucza "content"
            albo mieć pustą listę bloków).

    Returns:
        str | None: tekst pierwszego bloku albo None, gdy struktura
            jest niepoprawna (brak klucza lub pusta lista).
    """
    try:
        return dane["content"][0]["text"]
    except (KeyError, IndexError):
        return None


def zadanie_07_loguj_zapytanie(model: str, max_tokens: int) -> None:
    """Zapisuje w logu informację o wysyłanym zapytaniu.

    Args:
        model: nazwa modelu, do którego leci zapytanie.
        max_tokens: limit długości odpowiedzi.

    Returns:
        None: funkcja tylko loguje, niczego nie zwraca.
    """
    logging.info("Wysylam zapytanie do modelu %s, max_tokens=%s", model, max_tokens)


def zadanie_08_loguj_blad(komunikat: str) -> None:
    """Zapisuje w logu błąd klienta na poziomie ERROR.

    Args:
        komunikat: opis błędu do zapisania.

    Returns:
        None: funkcja tylko loguje, niczego nie zwraca.
    """
    logging.error("Blad klienta LLM: %s", komunikat)


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
    try:
        return requests.post(url, headers=naglowki, json=payload, timeout=30)
    except requests.exceptions.Timeout as error:
        raise BladKlientaLLM("Przekroczono limit czasu") from error


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
    try:
        response = requests.post(url, headers=naglowki, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout as error:
        raise BladKlientaLLM("Przekroczono limit czasu") from error
    except requests.exceptions.ConnectionError as error:
        raise BladKlientaLLM("Brak polaczenia z serwerem") from error
    except requests.exceptions.HTTPError as error:
        raise BladKlientaLLM("Serwer zwrocil blad HTTP") from error
    except requests.exceptions.RequestException as error:
        raise BladKlientaLLM("Blad zadania") from error


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
    naglowki = zadanie_01_zbuduj_naglowki(api_key)
    payload = zadanie_02_zbuduj_payload(model, max_tokens, tresc)
    return zadanie_10_wyslij_z_pelna_obsluga(url, naglowki, payload)


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
    zadanie_07_loguj_zapytanie(model, max_tokens)
    try:
        dane = zadanie_11_zapytaj_model(url, api_key, model, max_tokens, tresc)
        return zadanie_06_wyciagnij_tekst_bezpiecznie(dane)
    except BladKlientaLLM as error:
        zadanie_08_loguj_blad(str(error))
        return None


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    zadanie_07_loguj_zapytanie("claude-sonnet-4-6", 100)
