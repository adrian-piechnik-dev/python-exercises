# Spis zadań:
# 01 — zbuduj prompt ekstrakcji z szablonem JSON (podwójne klamry w f-stringu)
# 02 — zbuduj prompt z dynamiczną listą pól (join + potrójna klamra)
# 03 — usuń prefiks markdown z odpowiedzi (removeprefix)
# 04 — usuń sufiks markdown z odpowiedzi (removesuffix)
# 05 — wyczyść pełną odpowiedź modelu (strip + prefiks + sufiks + strip)
# 06 — sparsuj JSON defensywnie (json.loads + JSONDecodeError → None)
# 07 — sparsuj odpowiedź modelu (czyszczenie + parsowanie)
# 08 — warstwa 1: wyciągnij tekst z koperty API (KeyError/IndexError → None)
# 09 — dwie warstwy: z koperty API do słownika danych
# 10 — zazębienie: zapytaj model (klient z tematu 19)
# 11 — zazębienie: pełna ekstrakcja (prompt + klient + dwie warstwy)
# 12 — zazębienie: ekstrakcja z kontrolą wymaganych pól

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
    # TODO: zwróć f-string o treści:
    #   Wyciagnij z tekstu imie i wiek. Zwroc TYLKO JSON w formacie
    #   {"imie": "...", "wiek": 0}. Tekst: <tutaj tekst>
    # TODO: literalne klamry szablonu zapisz jako {{ i }},
    #   a zmienną tekst wstaw przez {tekst}
    pass


def zadanie_02_zbuduj_prompt_z_polami(pola: list, tekst: str) -> str:
    """Buduje prompt z szablonem JSON złożonym z podanych nazw pól.

    Args:
        pola: lista nazw pól, np. ["imie", "wiek"].
        tekst: tekst źródłowy, z którego model ma wyciągnąć dane.

    Returns:
        str: prompt z szablonem w stylu {"imie": "...", "wiek": "..."}
            zbudowanym z listy pola oraz doklejonym tekstem źródłowym.
    """
    # TODO: zbuduj środek szablonu:
    #   srodek = ", ".join(f'"{pole}": "..."' for pole in pola)
    # TODO: zwróć f-string o treści:
    #   Zwroc TYLKO JSON w formacie {<srodek>}. Tekst: <tekst>
    #   (użyj potrójnej klamry: {{{srodek}}} — patrz teoria)
    pass


def zadanie_03_usun_prefix_markdown(tekst: str) -> str:
    """Zdejmuje otwarcie bloku markdown z początku tekstu.

    Args:
        tekst: odpowiedź modelu, być może zaczynająca się od ```json lub ```.

    Returns:
        str: tekst bez prefiksu ```json / ```; gdy prefiksu nie było —
            tekst bez zmian.
    """
    # TODO: zwróć tekst.removeprefix("```json").removeprefix("```")
    pass


def zadanie_04_usun_suffix_markdown(tekst: str) -> str:
    """Zdejmuje zamknięcie bloku markdown z końca tekstu.

    Args:
        tekst: odpowiedź modelu, być może zakończona ```.

    Returns:
        str: tekst bez sufiksu ```; gdy sufiksu nie było — tekst bez zmian.
    """
    # TODO: zwróć tekst.removesuffix("```")
    pass


def zadanie_05_wyczysc_odpowiedz(tekst: str) -> str:
    """Czyści odpowiedź modelu z bloku markdown i białych znaków.

    Args:
        tekst: surowa odpowiedź modelu (może zawierać ```json ... ```
            i entery na końcach).

    Returns:
        str: czysty tekst gotowy do parsowania jako JSON.
    """
    # TODO: wykonaj po kolei: tekst.strip(), potem
    #   zadanie_03_usun_prefix_markdown, potem
    #   zadanie_04_usun_suffix_markdown, na końcu jeszcze raz .strip()
    # TODO: zwróć wynik
    pass


def zadanie_06_parsuj_json(tekst: str) -> dict | None:
    """Parsuje tekst jako JSON albo zwraca None przy błędzie składni.

    Args:
        tekst: string, który POWINIEN być JSON-em (warstwa 2 —
            treść wygenerowana przez model).

    Returns:
        dict | None: sparsowany słownik albo None, gdy tekst nie jest
            poprawnym JSON-em.
    """
    # TODO: w bloku try zwróć json.loads(tekst)
    # TODO: złap json.JSONDecodeError i zwróć None
    pass


def zadanie_07_parsuj_odpowiedz_modelu(tekst: str) -> dict | None:
    """Czyści odpowiedź modelu z markdown i parsuje ją jako JSON.

    Args:
        tekst: surowa odpowiedź modelu.

    Returns:
        dict | None: słownik danych albo None, gdy po wyczyszczeniu
            treść nadal nie jest poprawnym JSON-em.
    """
    # TODO: wyczyść tekst przez zadanie_05_wyczysc_odpowiedz
    # TODO: zwróć wynik zadanie_06_parsuj_json na wyczyszczonym tekście
    pass


def zadanie_08_wyciagnij_tekst_z_api(dane: dict) -> str | None:
    """Wyciąga tekst modelu z koperty odpowiedzi API (warstwa 1).

    Args:
        dane: słownik odpowiedzi API; przy błędzie serwera może nie mieć
            klucza "content" albo mieć pustą listę bloków.

    Returns:
        str | None: dane["content"][0]["text"] albo None przy zepsutej
            strukturze koperty.
    """
    # TODO: w bloku try zwróć dane["content"][0]["text"]
    # TODO: złap (KeyError, IndexError) i zwróć None
    pass


def zadanie_09_wyciagnij_dane_z_odpowiedzi(dane: dict) -> dict | None:
    """Przechodzi obie warstwy: z koperty API do słownika danych.

    Args:
        dane: słownik odpowiedzi API z tekstem modelu w środku.

    Returns:
        dict | None: słownik wyekstrahowanych danych albo None, gdy
            zawiodła warstwa 1 (koperta) LUB warstwa 2 (treść nie-JSON).
    """
    # TODO: pobierz tekst przez zadanie_08_wyciagnij_tekst_z_api
    # TODO: jeśli tekst is None — zwróć None (warstwa 1 zawiodła)
    # TODO: zwróć wynik zadanie_07_parsuj_odpowiedz_modelu(tekst)
    pass


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
    # TODO: zbuduj słownik nagłówków: "x-api-key", "anthropic-version"
    #   ("2023-06-01"), "content-type" ("application/json")
    # TODO: zbuduj payload: "model", "max_tokens", "messages" —
    #   lista z jednym słownikiem {"role": "user", "content": tresc}
    # TODO: wywołaj requests.post(url, headers=..., json=..., timeout=30)
    # TODO: wywołaj raise_for_status() na odpowiedzi
    # TODO: zwróć odpowiedz.json()
    pass


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
    # TODO: zbuduj prompt przez zadanie_01_zbuduj_prompt_ekstrakcji(tekst)
    # TODO: pobierz kopertę przez zadanie_10_zapytaj_model(url, api_key,
    #   model, max_tokens, prompt)
    # TODO: zwróć wynik zadanie_09_wyciagnij_dane_z_odpowiedzi(dane)
    pass


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
    # TODO: zbuduj prompt przez zadanie_02_zbuduj_prompt_z_polami(pola, tekst)
    # TODO: pobierz kopertę przez zadanie_10_zapytaj_model(...)
    # TODO: wyciągnij dane przez zadanie_09_wyciagnij_dane_z_odpowiedzi
    # TODO: jeśli wynik is None — zwróć None
    # TODO: w pętli sprawdź każde pole z pola; gdy któregoś brakuje
    #   w wyniku (pole not in wynik) — zwróć None
    # TODO: zwróć wynik
    pass
