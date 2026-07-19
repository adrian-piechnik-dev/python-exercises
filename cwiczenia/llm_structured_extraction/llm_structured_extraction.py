import json

import requests


def zadanie_01_zbuduj_prompt_ekstrakcji(tekst: str) -> str:
    """Buduje prompt proszący model o JSON z imieniem i wiekiem.

    Args:
        tekst: tekst źródłowy, z którego model ma wyciągnąć dane.

    Returns:
        str: prompt zawierający dosłowny szablon
            {"imie": "...", "wiek": 0} oraz doklejony tekst źródłowy.
    """
    return f"""
    Wyciagnij z tekstu imie i wiek. Zwroc TYLKO JSON w formacie
    {{"imie": "...", "wiek": 0}}. Tekst: {tekst}
    """


def zadanie_02_zbuduj_prompt_z_polami(pola: list, tekst: str) -> str:
    """Buduje prompt z szablonem JSON złożonym z podanych nazw pól.

    Args:
        pola: lista nazw pól, np. ["imie", "wiek"].
        tekst: tekst źródłowy, z którego model ma wyciągnąć dane.

    Returns:
        str: prompt z szablonem w stylu {"imie": "...", "wiek": "..."}
            zbudowanym z listy pola oraz doklejonym tekstem źródłowym.
    """
    srodek = ", ".join(f'"{pole}": "..."' for pole in pola)
    return f'Zwroc TYLKO JSON w formacie {{{srodek}}}. Tekst: {tekst}'


def zadanie_03_usun_prefix_markdown(tekst: str) -> str:
    """Zdejmuje otwarcie bloku markdown z początku tekstu.

    Args:
        tekst: odpowiedź modelu, być może zaczynająca się od ```json lub ```.

    Returns:
        str: tekst bez prefiksu ```json / ```; gdy prefiksu nie było —
            tekst bez zmian.
    """
    return tekst.removeprefix("```json").removeprefix("```")


def zadanie_04_usun_suffix_markdown(tekst: str) -> str:
    """Zdejmuje zamknięcie bloku markdown z końca tekstu.

    Args:
        tekst: odpowiedź modelu, być może zakończona ```.

    Returns:
        str: tekst bez sufiksu ```; gdy sufiksu nie było — tekst bez zmian.
    """
    return tekst.removesuffix("```")


def zadanie_05_wyczysc_odpowiedz(tekst: str) -> str:
    """Czyści odpowiedź modelu z bloku markdown i białych znaków.

    Args:
        tekst: surowa odpowiedź modelu (może zawierać ```json ... ```
            i entery na końcach).

    Returns:
        str: czysty tekst gotowy do parsowania jako JSON.
    """
    return (
        zadanie_04_usun_suffix_markdown(
            zadanie_03_usun_prefix_markdown(
                tekst.strip())).strip()
    )


def zadanie_06_parsuj_json(tekst: str) -> dict | None:
    """Parsuje tekst jako JSON albo zwraca None przy błędzie składni.

    Args:
        tekst: string, który POWINIEN być JSON-em (warstwa 2 —
            treść wygenerowana przez model).

    Returns:
        dict | None: sparsowany słownik albo None, gdy tekst nie jest
            poprawnym JSON-em.
    """
    try:
        return json.loads(tekst)
    except json.JSONDecodeError:
        return None


def zadanie_07_parsuj_odpowiedz_modelu(tekst: str) -> dict | None:
    """Czyści odpowiedź modelu z markdown i parsuje ją jako JSON.

    Args:
        tekst: surowa odpowiedź modelu.

    Returns:
        dict | None: słownik danych albo None, gdy po wyczyszczeniu
            treść nadal nie jest poprawnym JSON-em.
    """
    dane = zadanie_05_wyczysc_odpowiedz(tekst)
    return zadanie_06_parsuj_json(dane)


def zadanie_08_wyciagnij_tekst_z_api(dane: dict) -> str | None:
    """Wyciąga tekst modelu z koperty odpowiedzi API (warstwa 1).

    Args:
        dane: słownik odpowiedzi API; przy błędzie serwera może nie mieć
            klucza "content" albo mieć pustą listę bloków.

    Returns:
        str | None: dane["content"][0]["text"] albo None przy zepsutej
            strukturze koperty.
    """
    try:
        return dane["content"][0]["text"]
    except (KeyError, IndexError):
        return None


def zadanie_09_wyciagnij_dane_z_odpowiedzi(dane: dict) -> dict | None:
    """Przechodzi obie warstwy: z koperty API do słownika danych.

    Args:
        dane: słownik odpowiedzi API z tekstem modelu w środku.

    Returns:
        dict | None: słownik wyekstrahowanych danych albo None, gdy
            zawiodła warstwa 1 (koperta) LUB warstwa 2 (treść nie-JSON).
    """
    tekst = zadanie_08_wyciagnij_tekst_z_api(dane)
    if tekst is None:
        return None
    return zadanie_07_parsuj_odpowiedz_modelu(tekst)


def zadanie_10_zapytaj_model(
    url: str, api_key: str, model: str, max_tokens: int, tresc: str
) -> dict:
    """Wysyła zapytanie do modelu i zwraca kopertę odpowiedzi (temat 19).

    Args:
        url: adres endpointu API.
        api_key: sekretny klucz API.
        model: nazwa modelu.
        max_tokens: limit długości odpowiedzi.
        tresc: treść wiadomości użytkownika (prompt).

    Returns:
        dict: odpowiedź serwera po .json(); przy kodzie błędu funkcja
            rzuca requests.exceptions.HTTPError z raise_for_status().
    """
    naglowki = {"x-api-key": api_key, "anthropic-version": "2023-06-01", "content-type": "application/json"}
    payload = {"model": model, "max_tokens": max_tokens, "messages": [{"role": "user", "content": tresc}]}
    response = requests.post(url, headers=naglowki, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def zadanie_11_wyekstrahuj_dane(
    url: str, api_key: str, model: str, max_tokens: int, tekst: str
) -> dict | None:
    """Wykonuje pełną ekstrakcję: prompt, zapytanie, dwie warstwy parsowania.

    Args:
        url: adres endpointu API.
        api_key: sekretny klucz API.
        model: nazwa modelu.
        max_tokens: limit długości odpowiedzi.
        tekst: tekst źródłowy do ekstrakcji imienia i wieku.

    Returns:
        dict | None: słownik danych z odpowiedzi modelu albo None,
            gdy odpowiedź ma zepsutą kopertę lub treść nie jest JSON-em.
    """
    prompt = zadanie_01_zbuduj_prompt_ekstrakcji(tekst)
    dane = zadanie_10_zapytaj_model(url, api_key, model, max_tokens, prompt)
    return zadanie_09_wyciagnij_dane_z_odpowiedzi(dane)


def zadanie_12_wyekstrahuj_pola(
    url: str, api_key: str, model: str, max_tokens: int, tekst: str, pola: list
) -> dict | None:
    """Ekstrahuje wskazane pola i sprawdza, czy wszystkie są w wyniku.

    Args:
        url: adres endpointu API.
        api_key: sekretny klucz API.
        model: nazwa modelu.
        max_tokens: limit długości odpowiedzi.
        tekst: tekst źródłowy do ekstrakcji.
        pola: lista nazw pól, które MUSZĄ znaleźć się w wyniku.

    Returns:
        dict | None: słownik danych zawierający wszystkie wymagane pola
            albo None, gdy ekstrakcja zawiodła LUB brakuje choć jednego pola.
    """
    prompt = zadanie_02_zbuduj_prompt_z_polami(pola, tekst)
    dane = zadanie_10_zapytaj_model(url, api_key, model, max_tokens, prompt)
    wynik = zadanie_09_wyciagnij_dane_z_odpowiedzi(dane)
    if wynik is None:
        return None
    for pole in pola:
        if pole not in wynik:
            return None
    return wynik
