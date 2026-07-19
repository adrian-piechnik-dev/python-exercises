import logging

import pytest
import requests

from conftest import FalszywaOdpowiedz
from llm_api_klient import (
    BladKlientaLLM,
    zadanie_01_zbuduj_naglowki,
    zadanie_02_zbuduj_payload,
    zadanie_03_wyslij_zapytanie,
    zadanie_04_potwierdz_sukces,
    zadanie_05_wyciagnij_tekst,
    zadanie_06_wyciagnij_tekst_bezpiecznie,
    zadanie_07_loguj_zapytanie,
    zadanie_08_loguj_blad,
    zadanie_09_wyslij_z_obsluga_timeout,
    zadanie_10_wyslij_z_pelna_obsluga,
    zadanie_11_zapytaj_model,
    zadanie_12_pelny_klient,
)


# --- zadanie_01 ---

def test_zadanie_01_naglowki_zawieraja_klucz_i_wersje() -> None:
    """Co testuje: czy nagłówki mają klucz API i wersję API.
    Co udaje: nic — używam literału "sk-test-123" jako klucza.
    Co sprawdzam: wynik["x-api-key"]=="sk-test-123"
    i wynik["anthropic-version"]=="2023-06-01".
    """
    wynik = zadanie_01_zbuduj_naglowki("sk-test-123")
    assert wynik["x-api-key"] == "sk-test-123"
    assert wynik["anthropic-version"] == "2023-06-01"


def test_zadanie_01_naglowki_maja_content_type_i_nic_wiecej() -> None:
    """Co testuje: czy nagłówki mają content-type i dokładnie 3 wpisy.
    Co udaje: nic — używam literału jako klucza.
    Co sprawdzam: wynik["content-type"]=="application/json" i len(wynik)==3.
    """
    wynik = zadanie_01_zbuduj_naglowki("sk-test-123")
    assert wynik["content-type"] == "application/json"
    assert len(wynik) == 3


# --- zadanie_02 ---

def test_zadanie_02_payload_ma_model_i_max_tokens() -> None:
    """Co testuje: czy payload zawiera przekazany model i limit tokenów.
    Co udaje: nic — używam literałów.
    Co sprawdzam: wynik["model"]=="claude-sonnet-4-6" i wynik["max_tokens"]==100.
    """
    wynik = zadanie_02_zbuduj_payload("claude-sonnet-4-6", 100, "Czesc")
    assert wynik["model"] == "claude-sonnet-4-6"
    assert wynik["max_tokens"] == 100


def test_zadanie_02_messages_to_lista_z_rola_user() -> None:
    """Co testuje: czy messages to lista z jednym słownikiem roli user.
    Co udaje: nic — używam literałów.
    Co sprawdzam: messages[0]["role"]=="user" i messages[0]["content"]==treść.
    """
    wynik = zadanie_02_zbuduj_payload("claude-sonnet-4-6", 100, "Jaka jest stolica Polski?")
    assert isinstance(wynik["messages"], list) is True
    assert len(wynik["messages"]) == 1
    assert wynik["messages"][0]["role"] == "user"
    assert wynik["messages"][0]["content"] == "Jaka jest stolica Polski?"


# --- zadanie_03 ---

def test_zadanie_03_zwraca_odpowiedz_z_post(
    monkeypatch: pytest.MonkeyPatch, odpowiedz_ok: FalszywaOdpowiedz
) -> None:
    """Co testuje: czy funkcja zwraca dokładnie to, co zwróci requests.post.
    Co udaje: requests.post — monkeypatch podmienia go na fałszywkę
    zwracającą odpowiedz_ok.
    Co sprawdzam: wynik is odpowiedz_ok.
    """

    def falszywy_post(
            url: str | None = None,
            headers: dict | None = None,
            json: dict | None = None,
            timeout: int | None = None,
    ) -> FalszywaOdpowiedz:
        return odpowiedz_ok
    monkeypatch.setattr("llm_api_klient.requests.post", falszywy_post)
    wynik = zadanie_03_wyslij_zapytanie("https://api.anthropic.com/v1/messages", {}, {})
    assert wynik is odpowiedz_ok


def test_zadanie_03_przekazuje_payload_i_timeout(
    monkeypatch: pytest.MonkeyPatch, odpowiedz_ok: FalszywaOdpowiedz
) -> None:
    """Co testuje: czy funkcja przekazuje payload przez json= i timeout=30.
    Co udaje: requests.post — fałszywka zapisuje otrzymane argumenty
    do słownika i zwraca odpowiedz_ok.
    Co sprawdzam: zapisane["json"] to przekazany payload, zapisane["timeout"]==30.
    """
    zapisane = {}
    def falszywy_post(
            url: str | None = None,
            headers: dict | None = None,
            json: dict | None = None,
            timeout: int | None = None,
    ) -> FalszywaOdpowiedz:
        zapisane["json"] = json
        zapisane["timeout"] = timeout
        return odpowiedz_ok
    monkeypatch.setattr("llm_api_klient.requests.post", falszywy_post)
    zadanie_03_wyslij_zapytanie(
        url="https://api.anthropic.com/v1/messages", naglowki={}, payload={"model": "claude-sonnet-4-6"}
    )
    assert zapisane["json"] == {"model": "claude-sonnet-4-6"}
    assert zapisane["timeout"] == 30


# --- zadanie_04 ---

def test_zadanie_04_zwraca_slownik_dla_poprawnej_odpowiedzi(
    odpowiedz_ok: FalszywaOdpowiedz,
) -> None:
    """Co testuje: czy przy sukcesie funkcja zwraca treść odpowiedzi jako dict.
    Co udaje: obiekt Response — używam atrapy odpowiedz_ok z conftest.
    Co sprawdzam: wynik["content"][0]["text"] == "Czesc, jestem Claude!".
    """
    wynik = zadanie_04_potwierdz_sukces(odpowiedz_ok)
    assert wynik["content"][0]["text"] == "Czesc, jestem Claude!"


def test_zadanie_04_rzuca_httperror_dla_bledu(
    odpowiedz_blad_http: FalszywaOdpowiedz,
) -> None:
    """Co testuje: czy błąd HTTP w odpowiedzi przerywa funkcję wyjątkiem.
    Co udaje: obiekt Response — atrapa odpowiedz_blad_http rzuca HTTPError
    w raise_for_status().
    Co sprawdzam: pytest.raises(requests.exceptions.HTTPError).
    """
    with pytest.raises(requests.exceptions.HTTPError):
        zadanie_04_potwierdz_sukces(odpowiedz_blad_http)


# --- zadanie_05 ---

def test_zadanie_05_wyciaga_tekst_z_odpowiedzi() -> None:
    """Co testuje: czy funkcja wyciąga tekst pierwszego bloku content.
    Co udaje: nic — używam literału słownika o strukturze odpowiedzi API.
    Co sprawdzam: wynik == "Stolica Polski to Warszawa.".
    """
    dane = {"content": [{"type": "text", "text": "Stolica Polski to Warszawa."}]}
    wynik = zadanie_05_wyciagnij_tekst(dane)
    assert wynik == "Stolica Polski to Warszawa."


def test_zadanie_05_rzuca_keyerror_gdy_brak_content() -> None:
    """Co testuje: czy przy braku klucza "content" leci KeyError.
    Co udaje: nic — używam pustego słownika (tak wygląda zepsuta odpowiedź).
    Co sprawdzam: pytest.raises(KeyError).
    """
    with pytest.raises(KeyError):
        zadanie_05_wyciagnij_tekst({})


# --- zadanie_06 ---

def test_zadanie_06_zwraca_tekst_dla_poprawnych_danych() -> None:
    """Co testuje: czy przy poprawnej strukturze funkcja zwraca tekst.
    Co udaje: nic — używam literału słownika.
    Co sprawdzam: wynik == "Stolica Polski to Warszawa.".
    """
    dane = {"content": [{"type": "text", "text": "Stolica Polski to Warszawa."}]}
    wynik = zadanie_06_wyciagnij_tekst_bezpiecznie(dane)
    assert wynik == "Stolica Polski to Warszawa."


def test_zadanie_06_zwraca_none_dla_zepsutej_struktury() -> None:
    """Co testuje: kontrakt None przy braku klucza i przy pustej liście bloków.
    Co udaje: nic — używam {} (brak "content") i {"content": []} (pusta lista).
    Co sprawdzam: oba wywołania zwracają None (assert ... is None).
    """
    wynik = zadanie_06_wyciagnij_tekst_bezpiecznie({})
    assert wynik is None
    wynik = zadanie_06_wyciagnij_tekst_bezpiecznie({"content": []})
    assert wynik is None


# --- zadanie_07 ---

def test_zadanie_07_loguje_nazwe_modelu(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Co testuje: czy w logu pojawia się nazwa modelu z zapytania.
    Co udaje: nic — caplog przechwytuje prawdziwe wpisy logging.
    Co sprawdzam: "claude-sonnet-4-6" in caplog.text.
    """
    caplog.set_level(logging.INFO)
    zadanie_07_loguj_zapytanie("claude-sonnet-4-6", 100)
    assert "claude-sonnet-4-6" in caplog.text


def test_zadanie_07_zwraca_none() -> None:
    """Co testuje: kontrakt funkcji — logowanie niczego nie zwraca.
    Co udaje: nic — wywołuję funkcję z literałami.
    Co sprawdzam: wynik is None.
    """
    wynik = zadanie_07_loguj_zapytanie("claude-sonnet-4-6", 100)
    assert wynik is None


# --- zadanie_08 ---

def test_zadanie_08_loguje_komunikat_bledu(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Co testuje: czy przekazany komunikat trafia do logu.
    Co udaje: nic — caplog przechwytuje prawdziwe wpisy logging.
    Co sprawdzam: "Przekroczono limit czasu" in caplog.text.
    """
    caplog.set_level(logging.ERROR)
    zadanie_08_loguj_blad("Przekroczono limit czasu")
    assert "Przekroczono limit czasu" in caplog.text


def test_zadanie_08_loguje_na_poziomie_error(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Co testuje: czy wpis ma poziom ERROR, nie INFO.
    Co udaje: nic — caplog przechwytuje prawdziwe wpisy logging.
    Co sprawdzam: "ERROR" in caplog.text.
    """
    caplog.set_level(logging.ERROR)
    zadanie_08_loguj_blad("cokolwiek")
    assert "ERROR" in caplog.text


# --- zadanie_09 ---

def test_zadanie_09_zwraca_odpowiedz_gdy_brak_bledu(
    monkeypatch: pytest.MonkeyPatch, odpowiedz_ok: FalszywaOdpowiedz
) -> None:
    """Co testuje: czy przy sprawnym serwerze funkcja oddaje odpowiedź.
    Co udaje: requests.post — fałszywka zwraca odpowiedz_ok.
    Co sprawdzam: wynik is odpowiedz_ok.
    """

    def falszywy_post(
            url: str | None = None,
            headers: dict | None = None,
            json: dict | None = None,
            timeout: int | None = None,
    ) -> FalszywaOdpowiedz:
        return odpowiedz_ok
    monkeypatch.setattr("llm_api_klient.requests.post", falszywy_post)
    wynik = zadanie_09_wyslij_z_obsluga_timeout("https://api.anthropic.com/v1/messages", {}, {})
    assert wynik is odpowiedz_ok


def test_zadanie_09_rzuca_blad_klienta_przy_timeout(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Co testuje: czy Timeout z requests zamienia się w BladKlientaLLM.
    Co udaje: requests.post — fałszywka rzuca requests.exceptions.Timeout.
    Co sprawdzam: pytest.raises(BladKlientaLLM).
    """

    def falszywy_post(
            url: str | None = None,
            headers: dict | None = None,
            json: dict | None = None,
            timeout: int | None = None,
    ) -> None:
        raise requests.exceptions.Timeout("za dlugo")
    monkeypatch.setattr("llm_api_klient.requests.post", falszywy_post)
    with pytest.raises(BladKlientaLLM):
        zadanie_09_wyslij_z_obsluga_timeout("https://api.anthropic.com/v1/messages", {}, {})


# --- zadanie_10 ---

def test_zadanie_10_zwraca_slownik_dla_sukcesu(
    monkeypatch: pytest.MonkeyPatch, odpowiedz_ok: FalszywaOdpowiedz
) -> None:
    """Co testuje: czy przy sukcesie funkcja zwraca treść odpowiedzi jako dict.
    Co udaje: requests.post — fałszywka zwraca odpowiedz_ok.
    Co sprawdzam: wynik["content"][0]["text"] == "Czesc, jestem Claude!".
    """

    def falszywy_post(
            url: str | None = None,
            headers: dict | None = None,
            json: dict | None = None,
            timeout: int | None = None,
    ) -> FalszywaOdpowiedz:
        return odpowiedz_ok
    monkeypatch.setattr("llm_api_klient.requests.post", falszywy_post)
    wynik = zadanie_10_wyslij_z_pelna_obsluga("https://api.anthropic.com/v1/messages", {}, {})
    assert wynik["content"][0]["text"] == "Czesc, jestem Claude!"


def test_zadanie_10_rzuca_blad_klienta_przy_connectionerror(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Co testuje: czy warstwa ConnectionError zamienia błąd w BladKlientaLLM.
    Co udaje: requests.post — fałszywka rzuca requests.exceptions.ConnectionError.
    Co sprawdzam: pytest.raises(BladKlientaLLM).
    """

    def falszywy_post(
            url: str | None = None,
            headers: dict | None = None,
            json: dict | None = None,
            timeout: int | None = None,
    ) -> None:
        raise requests.exceptions.ConnectionError("brak sieci")
    monkeypatch.setattr("llm_api_klient.requests.post", falszywy_post)
    with pytest.raises(BladKlientaLLM):
        zadanie_10_wyslij_z_pelna_obsluga("https://api.anthropic.com/v1/messages",{}, {})


def test_zadanie_10_rzuca_blad_klienta_przy_bledzie_http(
    monkeypatch: pytest.MonkeyPatch, odpowiedz_blad_http: FalszywaOdpowiedz
) -> None:
    """Co testuje: czy HTTPError z raise_for_status zamienia się w BladKlientaLLM.
    Co udaje: requests.post — fałszywka zwraca odpowiedz_blad_http,
    której raise_for_status() rzuca HTTPError.
    Co sprawdzam: pytest.raises(BladKlientaLLM).
    """

    def falszywy_post(
            url: str | None = None,
            headers: dict | None = None,
            json: dict | None = None,
            timeout: int | None = None,
    ) -> FalszywaOdpowiedz:
        return odpowiedz_blad_http
    monkeypatch.setattr("llm_api_klient.requests.post", falszywy_post)
    with pytest.raises(BladKlientaLLM):
        zadanie_10_wyslij_z_pelna_obsluga("https://api.anthropic.com/v1/messages", {}, {})


# --- zadanie_11 ---

def test_zadanie_11_zwraca_slownik_odpowiedzi(
    monkeypatch: pytest.MonkeyPatch, odpowiedz_ok: FalszywaOdpowiedz
) -> None:
    """Co testuje: czy pełne zapytanie kończy się treścią odpowiedzi.
    Co udaje: requests.post — fałszywka zwraca odpowiedz_ok.
    Co sprawdzam: wynik["content"][0]["text"] == "Czesc, jestem Claude!".
    """

    def falszywy_post(
            url: str | None = None,
            headers: dict | None = None,
            json: dict | None = None,
            timeout: int | None = None,
    ) -> FalszywaOdpowiedz:
        return odpowiedz_ok
    monkeypatch.setattr("llm_api_klient.requests.post", falszywy_post)
    wynik = zadanie_11_zapytaj_model(
        "https://api.anthropic.com/v1/messages","sk-test-123", "claude-sonnet-4-6", 100, "Czesc"
    )
    assert wynik["content"][0]["text"] == "Czesc, jestem Claude!"


def test_zadanie_11_wysyla_naglowki_z_kluczem_api(
    monkeypatch: pytest.MonkeyPatch, odpowiedz_ok: FalszywaOdpowiedz
) -> None:
    """Co testuje: czy zbudowane nagłówki i payload naprawdę lecą do post.
    Co udaje: requests.post — fałszywka zapisuje headers i json do słownika.
    Co sprawdzam: zapisane["headers"]["x-api-key"]=="sk-test-123"
    i zapisane["json"]["model"]=="claude-sonnet-4-6".
    """
    zapisane = {}

    def falszywy_post(
            url: str | None = None,
            headers: dict | None = None,
            json: dict | None = None,
            timeout: int | None = None,
    ) -> FalszywaOdpowiedz:
        zapisane["headers"] = headers
        zapisane["json"] = json
        return odpowiedz_ok
    monkeypatch.setattr("llm_api_klient.requests.post", falszywy_post)
    zadanie_11_zapytaj_model(
        "https://api.anthropic.com/v1/messages","sk-test-123", "claude-sonnet-4-6", 100, "Czesc"
    )
    assert zapisane["headers"]["x-api-key"] == "sk-test-123"
    assert zapisane["json"]["model"] == "claude-sonnet-4-6"


# --- zadanie_12 ---

def test_zadanie_12_zwraca_tekst_odpowiedzi(
    monkeypatch: pytest.MonkeyPatch, odpowiedz_ok: FalszywaOdpowiedz
) -> None:
    """Co testuje: czy pełny klient zwraca sam tekst odpowiedzi modelu.
    Co udaje: requests.post — fałszywka zwraca odpowiedz_ok.
    Co sprawdzam: wynik == "Czesc, jestem Claude!".
    """

    def falszywy_post(
            url: str | None = None,
            headers: dict | None = None,
            json: dict | None = None,
            timeout: int | None = None,
    ) -> FalszywaOdpowiedz:
        return odpowiedz_ok
    monkeypatch.setattr("llm_api_klient.requests.post", falszywy_post)
    wynik = zadanie_12_pelny_klient(
        "https://api.anthropic.com/v1/messages","sk-test-123", "claude-sonnet-4-6", 100, "Czesc"
    )
    assert wynik == "Czesc, jestem Claude!"


def test_zadanie_12_zwraca_none_i_loguje_blad_przy_timeout(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    """Co testuje: kontrakt None + wpis ERROR w logu przy błędzie komunikacji.
    Co udaje: requests.post — fałszywka rzuca requests.exceptions.Timeout;
    caplog przechwytuje logi.
    Co sprawdzam: wynik is None i "ERROR" in caplog.text.
    """
    caplog.set_level(logging.INFO)

    def falszywy_post(
            url: str | None = None,
            headers: dict | None = None,
            json: dict | None = None,
            timeout: int | None = None,
    ) -> None:
        raise requests.exceptions.Timeout("za dlugo")
    monkeypatch.setattr("llm_api_klient.requests.post", falszywy_post)
    wynik = zadanie_12_pelny_klient(
        "https://api.anthropic.com/v1/messages", "sk-test-123", "claude-sonnet-4-6", 100, "Czesc"
    )
    assert wynik is None
    assert "ERROR" in caplog.text

