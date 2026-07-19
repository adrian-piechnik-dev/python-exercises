from unittest.mock import patch

from llm_structured_extraction import (
    zadanie_01_zbuduj_prompt_ekstrakcji,
    zadanie_02_zbuduj_prompt_z_polami,
    zadanie_03_usun_prefix_markdown,
    zadanie_04_usun_suffix_markdown,
    zadanie_05_wyczysc_odpowiedz,
    zadanie_06_parsuj_json,
    zadanie_07_parsuj_odpowiedz_modelu,
    zadanie_08_wyciagnij_tekst_z_api,
    zadanie_09_wyciagnij_dane_z_odpowiedzi,
    zadanie_10_zapytaj_model,
    zadanie_11_wyekstrahuj_dane,
    zadanie_12_wyekstrahuj_pola,
)


# --- zadanie_01 ---

def test_zadanie_01_prompt_zawiera_tekst_zrodlowy() -> None:
    """Co testuje: czy tekst źródłowy trafia do promptu.
    Co udaje: nic — używam literału "Anna ma 30 lat.".
    Co sprawdzam: "Anna ma 30 lat." in wynik.
    """
    wynik = zadanie_01_zbuduj_prompt_ekstrakcji("Anna ma 30 lat.")
    assert "Anna ma 30 lat." in wynik


def test_zadanie_01_prompt_zawiera_literalne_klamry_szablonu() -> None:
    """Co testuje: czy podwójne klamry dały LITERALNY szablon JSON.
    Co udaje: nic — używam literału tekstu.
    Co sprawdzam: fragment '{"imie": "..."' oraz '"wiek": 0}' in wynik.
    """
    wynik = zadanie_01_zbuduj_prompt_ekstrakcji("cokolwiek")
    assert '{"imie": "..."' in wynik
    assert '"wiek": 0}' in wynik


# --- zadanie_02 ---

def test_zadanie_02_szablon_z_dwoch_pol() -> None:
    """Co testuje: czy szablon skleja się z listy dwóch pól.
    Co udaje: nic — używam literałów.
    Co sprawdzam: '{"imie": "...", "wiek": "..."}' in wynik.
    """
    wynik = zadanie_02_zbuduj_prompt_z_polami(["imie", "wiek"], "Anna ma 30 lat.")
    assert '{"imie": "...", "wiek": "..."}' in wynik


def test_zadanie_02_szablon_z_jednego_pola_i_tekst() -> None:
    """Co testuje: przypadek brzegowy jednoelementowej listy pól + obecność tekstu.
    Co udaje: nic — używam literałów.
    Co sprawdzam: '{"email": "..."}' in wynik oraz tekst źródłowy in wynik.
    """
    wynik = zadanie_02_zbuduj_prompt_z_polami(["email"], "Napisz do jan@firma.pl")
    assert '{"email": "..."}' in wynik
    assert "Napisz do jan@firma.pl" in wynik


# --- zadanie_03 ---

def test_zadanie_03_zdejmuje_prefix_json() -> None:
    """Co testuje: czy prefiks ```json znika z początku tekstu.
    Co udaje: nic — używam literału z prefiksem.
    Co sprawdzam: wynik == '{"a": 1}'.
    """
    wynik = zadanie_03_usun_prefix_markdown('```json{"a": 1}')
    assert wynik == '{"a": 1}'


def test_zadanie_03_tekst_bez_prefiksu_bez_zmian() -> None:
    """Co testuje: defensywność — brak prefiksu nie psuje tekstu.
    Co udaje: nic — używam czystego literału JSON.
    Co sprawdzam: wynik == '{"a": 1}' (bez zmian, bez wyjątku).
    """
    wynik = zadanie_03_usun_prefix_markdown('{"a": 1}')
    assert wynik == '{"a": 1}'


# --- zadanie_04 ---

def test_zadanie_04_zdejmuje_suffix() -> None:
    """Co testuje: czy sufiks ``` znika z końca tekstu.
    Co udaje: nic — używam literału z sufiksem.
    Co sprawdzam: wynik == '{"a": 1}'.
    """
    wynik = zadanie_04_usun_suffix_markdown('{"a": 1}```')
    assert wynik == '{"a": 1}'


def test_zadanie_04_tekst_bez_sufiksu_bez_zmian() -> None:
    """Co testuje: defensywność — brak sufiksu nie psuje tekstu.
    Co udaje: nic — używam czystego literału JSON.
    Co sprawdzam: wynik == '{"a": 1}' (bez zmian, bez wyjątku).
    """
    wynik = zadanie_04_usun_suffix_markdown('{"a": 1}')
    assert wynik == '{"a": 1}'


# --- zadanie_05 ---

def test_zadanie_05_czysci_pelny_blok_markdown() -> None:
    """Co testuje: pełne czyszczenie odpowiedzi z markdown i enterów.
    Co udaje: nic — używam literału '```json\\n{"imie": "Anna"}\\n```'.
    Co sprawdzam: wynik == '{"imie": "Anna"}'.
    """
    wynik = zadanie_05_wyczysc_odpowiedz('```json\n{"imie": "Anna"}\n```')
    assert wynik == '{"imie": "Anna"}'


def test_zadanie_05_czysta_odpowiedz_bez_zmian() -> None:
    """Co testuje: defensywność — czysty JSON przechodzi nietknięty.
    Co udaje: nic — używam literału bez markdown.
    Co sprawdzam: wynik == '{"imie": "Anna"}'.
    """
    wynik = zadanie_05_wyczysc_odpowiedz('{"imie": "Anna"}')
    assert wynik == '{"imie": "Anna"}'


# --- zadanie_06 ---

def test_zadanie_06_parsuje_poprawny_json() -> None:
    """Co testuje: czy poprawny JSON zamienia się w słownik.
    Co udaje: nic — używam literału '{"imie": "Anna", "wiek": 30}'.
    Co sprawdzam: wynik == {"imie": "Anna", "wiek": 30}.
    """
    wynik = zadanie_06_parsuj_json('{"imie": "Anna", "wiek": 30}')
    assert wynik == {"imie": "Anna", "wiek": 30}


def test_zadanie_06_zwraca_none_dla_nie_jsona() -> None:
    """Co testuje: kontrakt None przy treści, która nie jest JSON-em (warstwa 2).
    Co udaje: nic — używam literału "to nie jest json".
    Co sprawdzam: wynik is None.
    """
    wynik = zadanie_06_parsuj_json("to nie jest json")
    assert wynik is None


# --- zadanie_07 ---

def test_zadanie_07_parsuje_json_owiniety_w_markdown() -> None:
    """Co testuje: potok czyszczenie + parsowanie na owiniętej odpowiedzi.
    Co udaje: nic — używam literału '```json\\n{"wiek": 30}\\n```'.
    Co sprawdzam: wynik == {"wiek": 30}.
    """
    wynik = zadanie_07_parsuj_odpowiedz_modelu('```json\n{"wiek": 30}\n```')
    assert wynik == {"wiek": 30}


def test_zadanie_07_zwraca_none_dla_odmowy_modelu() -> None:
    """Co testuje: kontrakt None, gdy model odpowiedział prozą zamiast JSON-em.
    Co udaje: nic — używam literału "Nie moge tego zrobic.".
    Co sprawdzam: wynik is None.
    """
    wynik = zadanie_07_parsuj_odpowiedz_modelu("Nie moge tego zrobic.")
    assert wynik is None


# --- zadanie_08 ---

def test_zadanie_08_wyciaga_tekst_z_poprawnej_koperty(
    odpowiedz_api_poprawna: dict,
) -> None:
    """Co testuje: warstwę 1 — wyciąganie tekstu modelu z koperty API.
    Co udaje: kopertę API — fixture odpowiedz_api_poprawna z conftest.
    Co sprawdzam: wynik == '```json\\n{"imie": "Anna", "wiek": 30}\\n```'.
    """
    wynik = zadanie_08_wyciagnij_tekst_z_api(odpowiedz_api_poprawna)
    assert wynik == '```json\n{"imie": "Anna", "wiek": 30}\n```'


def test_zadanie_08_zwraca_none_dla_zepsutej_koperty() -> None:
    """Co testuje: kontrakt None przy braku "content" i przy pustej liście bloków.
    Co udaje: nic — używam {} oraz {"content": []}.
    Co sprawdzam: oba wywołania zwracają None (assert ... is None).
    """
    wynik = zadanie_08_wyciagnij_tekst_z_api({})
    assert wynik is None
    wynik = zadanie_08_wyciagnij_tekst_z_api({"content": []})
    assert wynik is None


# --- zadanie_09 ---

def test_zadanie_09_pelne_przejscie_obu_warstw(
    odpowiedz_api_poprawna: dict,
) -> None:
    """Co testuje: pełne przejście: koperta → tekst → czyszczenie → słownik.
    Co udaje: kopertę API — fixture odpowiedz_api_poprawna.
    Co sprawdzam: wynik == {"imie": "Anna", "wiek": 30}.
    """
    wynik = zadanie_09_wyciagnij_dane_z_odpowiedzi(odpowiedz_api_poprawna)
    assert wynik == {"imie": "Anna", "wiek": 30}


def test_zadanie_09_zwraca_none_gdy_tresc_nie_jest_jsonem(
    odpowiedz_api_zepsuta_tresc: dict,
) -> None:
    """Co testuje: warstwę 2 — koperta dobra, ale treść modelu to proza.
    Co udaje: kopertę API — fixture odpowiedz_api_zepsuta_tresc.
    Co sprawdzam: wynik is None.
    """
    wynik = zadanie_09_wyciagnij_dane_z_odpowiedzi(odpowiedz_api_zepsuta_tresc)
    assert wynik is None


def test_zadanie_09_zwraca_none_gdy_koperta_zepsuta() -> None:
    """Co testuje: warstwę 1 — zepsuta koperta ucina potok od razu.
    Co udaje: nic — używam pustego słownika jako koperty.
    Co sprawdzam: wynik is None.
    """
    wynik = zadanie_09_wyciagnij_dane_z_odpowiedzi({})
    assert wynik is None


# --- zadanie_10 ---

def test_zadanie_10_zwraca_koperte_odpowiedzi() -> None:
    """Co testuje: czy funkcja zwraca to, co odpowiedź serwera ma w .json().
    Co udaje: requests.post — patch("requests.post") z konfiguracją
    return_value.json.return_value.
    Co sprawdzam: wynik == {"content": []}.
    """
    with patch("requests.post") as atrapa_post:
        atrapa_post.return_value.json.return_value = {"content": []}
        wynik = zadanie_10_zapytaj_model(
            "https://api.anthropic.com/v1/messages",
            "sk-test-123", "claude-sonnet-4-6",
            100,
            "Czesc"
        )
    assert wynik == {"content": []}


def test_zadanie_10_przekazuje_model_i_timeout() -> None:
    """Co testuje: czy payload z modelem i timeout=30 naprawdę lecą do post.
    Co udaje: requests.post — patch; atrapa pamięta argumenty wywołania.
    Co sprawdzam: call_args.kwargs["json"]["model"]=="claude-sonnet-4-6"
    i call_args.kwargs["timeout"]==30.
    """
    with patch("requests.post") as atrapa_post:
        atrapa_post.return_value.json.return_value = {"content": []}
        zadanie_10_zapytaj_model(
            "https://api.anthropic.com/v1/messages",
            "sk-test-123",
            "claude-sonnet-4-6",
            100,
            "Czesc"
        )
    assert atrapa_post.call_args.kwargs["json"]["model"] == "claude-sonnet-4-6"
    assert atrapa_post.call_args.kwargs["timeout"] == 30


# --- zadanie_11 ---

def test_zadanie_11_zwraca_slownik_danych(odpowiedz_api_poprawna: dict) -> None:
    """Co testuje: pełną ekstrakcję od tekstu źródłowego do słownika.
    Co udaje: zadanie_10_zapytaj_model — patch tam gdzie używane
    (llm_structured_extraction), return_value = odpowiedz_api_poprawna.
    Co sprawdzam: wynik == {"imie": "Anna", "wiek": 30}.
    """
    with patch("llm_structured_extraction.zadanie_10_zapytaj_model") as atrapa:
        atrapa.return_value = odpowiedz_api_poprawna
        wynik = zadanie_11_wyekstrahuj_dane(
            "https://api.anthropic.com/v1/messages",
            "sk-test-123",
            "claude-sonnet-4-6",
            100,
            "Anna ma 30 lat."
        )
    assert wynik == {"imie": "Anna", "wiek": 30}


def test_zadanie_11_zwraca_none_gdy_model_odmowil(
    odpowiedz_api_zepsuta_tresc: dict,
) -> None:
    """Co testuje: kontrakt None, gdy model nie zwrócił JSON-a.
    Co udaje: zadanie_10_zapytaj_model — patch z return_value =
    odpowiedz_api_zepsuta_tresc.
    Co sprawdzam: wynik is None.
    """
    with patch("llm_structured_extraction.zadanie_10_zapytaj_model") as atrapa:
        atrapa.return_value = odpowiedz_api_zepsuta_tresc
        wynik = zadanie_11_wyekstrahuj_dane(
            "https://api.anthropic.com/v1/messages",
            "sk-test-123",
            "claude-sonnet-4-6",
            100,
            "Anna ma 30 lat."
        )
    assert wynik is None


# --- zadanie_12 ---

def test_zadanie_12_zwraca_dane_gdy_wszystkie_pola_obecne(
    odpowiedz_api_poprawna: dict,
) -> None:
    """Co testuje: ekstrakcję z kontrolą pól, gdy wynik ma wszystkie wymagane.
    Co udaje: zadanie_10_zapytaj_model — patch z return_value =
    odpowiedz_api_poprawna (dane mają pola "imie" i "wiek").
    Co sprawdzam: wynik == {"imie": "Anna", "wiek": 30}.
    """
    with patch("llm_structured_extraction.zadanie_10_zapytaj_model") as atrapa:
        atrapa.return_value = odpowiedz_api_poprawna
        wynik = zadanie_12_wyekstrahuj_pola(
            "https://api.anthropic.com/v1/messages",
            "sk-test-123","claude-sonnet-4-6",
            100,
            "Anna ma 30 lat.",
            ["imie", "wiek"]
        )
    assert wynik == {"imie": "Anna", "wiek": 30}


def test_zadanie_12_zwraca_none_gdy_brakuje_pola(
    odpowiedz_api_poprawna: dict,
) -> None:
    """Co testuje: kontrakt None, gdy w danych brakuje wymaganego pola.
    Co udaje: zadanie_10_zapytaj_model — patch z return_value =
    odpowiedz_api_poprawna (dane NIE mają pola "email").
    Co sprawdzam: wynik is None.
    """
    with patch("llm_structured_extraction.zadanie_10_zapytaj_model") as atrapa:
        atrapa.return_value = odpowiedz_api_poprawna
        wynik = zadanie_12_wyekstrahuj_pola(
            "https://api.anthropic.com/v1/messages",
            "sk-test-123","claude-sonnet-4-6",
            100,
            "Anna ma 30 lat.",
            ["imie", "email"]
        )
    assert wynik is None
