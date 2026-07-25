import json
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

from conftest import FakeResponse
from mini_api_katalog import (
    zadanie_01_pobierz_katalog,
    zadanie_02_pobierz_strony,
    zadanie_03_filtruj_dostepne,
    zadanie_04_wybierz_pola,
    zadanie_05_znajdz_produkt,
    zadanie_06_zapisz_katalog,
    zadanie_07_wczytaj_katalog,
    zadanie_08_waliduj_produkt,
    zadanie_09_api_listy,
    zadanie_10_api_szczegolow,
    zadanie_11_api_dodawania,
    zadanie_12_zbuduj_katalog,
    zadanie_13_pelne_api,
)


# --- zadanie_01 ---

def test_zadanie_01_zwraca_liste_produktow(
    monkeypatch: pytest.MonkeyPatch,
    surowe_produkty: list[dict[str, Any]],
) -> None:
    """Co testuje: pobranie i sparsowanie katalogu przy zdrowym API.
    Co udaje: requests.get w module tematu — zwraca FakeResponse(200,
    surowe_produkty).
    Co sprawdzam: wynik to dokładnie lista z atrapy.
    """
    def podmieniony_get(
            url: str,
            params: dict[str, Any] | None = None,
            timeout: int | None = None,
    ) -> FakeResponse:
        """Atrapa requests.get zwracająca zdrową odpowiedź z fixture.

        Args:
            url: ignorowany adres.
            params: ignorowane parametry zapytania.
            timeout: ignorowany limit czasu.

        Returns:
            FakeResponse: atrapa z kodem 200 i danymi z fixture.
        """
        return FakeResponse(200, surowe_produkty)
    monkeypatch.setattr("mini_api_katalog.requests.get", podmieniony_get)
    wynik = zadanie_01_pobierz_katalog("https://www.example.pl")
    assert wynik == surowe_produkty


def test_zadanie_01_zwraca_none_przy_bledzie_serwera(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Co testuje: kontrakt None, gdy serwer odpowiada błędem 500.
    Co udaje: requests.get — zwraca FakeResponse(500, []); jej
    raise_for_status rzuci HTTPError jak prawdziwa odpowiedź.
    Co sprawdzam: wynik is None (bez wyjątku na zewnątrz).
    """
    def podmieniony_get(
            url: str,
            params: dict[str, Any] | None = None,
            timeout: int | None = None,
    ) -> FakeResponse:
        """Atrapa requests.get udająca awarię serwera.

        Args:
            url: ignorowany adres.
            params: ignorowane parametry zapytania.
            timeout: ignorowany limit czasu.

        Returns:
            FakeResponse: atrapa z kodem 500 i pustymi danymi — jej
                raise_for_status rzuci HTTPError.
        """
        return FakeResponse(500, [])
    monkeypatch.setattr("mini_api_katalog.requests.get", podmieniony_get)
    wynik = zadanie_01_pobierz_katalog("https://www.example.pl")
    assert wynik is None


# --- zadanie_02 ---

def test_zadanie_02_skleja_strony_w_plaska_liste(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Co testuje: sklejanie porcji z wielu stron w jedną płaską listę.
    Co udaje: requests.get — każde wywołanie zwraca atrapę z listą
    2 produktów, np. [{"id": 1}, {"id": 2}].
    Co sprawdzam: dla 3 stron wynik ma 6 elementów i pierwszy jest
    słownikiem (nie listą — pułapka append vs extend).
    """
    def podmieniony_get(
            url: str,
            params: dict[str, Any] | None = None,
            timeout: int | None = None,
    ) -> FakeResponse:
        """Atrapa requests.get zwracająca zdrową odpowiedź z fixture.

        Args:
            url: ignorowany adres.
            params: ignorowane parametry zapytania.
            timeout: ignorowany limit czasu.

        Returns:
            FakeResponse: atrapa z kodem 200 i danymi jako lista dwóch słowników.
        """
        return FakeResponse(200, [{"id": 1}, {"id": 2}])
    monkeypatch.setattr("mini_api_katalog.requests.get", podmieniony_get)
    wynik = zadanie_02_pobierz_strony("https://www.example.pl", 3)
    assert len(wynik) == 6
    assert isinstance(wynik[0], dict)


def test_zadanie_02_zero_stron_daje_pusta_liste(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Co testuje: zachowanie brzegowe — brak stron do pobrania.
    Co udaje: requests.get — atrapa nie powinna być w ogóle użyta.
    Co sprawdzam: dla liczba_stron równego 0 wynik to pusta lista.
    """
    def podmieniony_get(
            url: str,
            params: dict[str, Any] | None = None,
            timeout: int | None = None,
    ) -> FakeResponse:
        """Atrapa requests.get zwracająca zdrową odpowiedź z fixture.

        Args:
            url: ignorowany adres.
            params: ignorowane parametry zapytania.
            timeout: ignorowany limit czasu.

        Returns:
            FakeResponse: atrapa z kodem 200 i danymi jako lista dwóch słowników.
        """
        return FakeResponse(200, [{"id": 1}, {"id": 2}])

    monkeypatch.setattr("mini_api_katalog.requests.get", podmieniony_get)
    wynik = zadanie_02_pobierz_strony("https://www.example.pl", 0)
    assert wynik == []


# --- zadanie_03 ---

def test_zadanie_03_zostawia_tylko_dostepne(
    surowe_produkty: list[dict[str, Any]],
) -> None:
    """Co testuje: filtr po polu dostepny.
    Co udaje: nic — gotowa lista z fixture surowe_produkty (3 z 4 dostępne).
    Co sprawdzam: wynik ma 3 produkty i nie ma wśród nich Myszy (id 2).
    """
    wynik = zadanie_03_filtruj_dostepne(surowe_produkty)
    assert len(wynik) == 3
    ids_wynik = [p["id"] for p in wynik]
    assert 2 not in ids_wynik


def test_zadanie_03_pusta_lista_daje_pusta_liste() -> None:
    """Co testuje: zachowanie brzegowe dla pustego wejścia.
    Co udaje: nic — podaję pustą listę wprost.
    Co sprawdzam: wynik to pusta lista (nie None, nie wyjątek).
    """
    wynik = zadanie_03_filtruj_dostepne([])
    assert wynik == []


# --- zadanie_04 ---

def test_zadanie_04_zostawia_trzy_pola(
    surowe_produkty: list[dict[str, Any]],
) -> None:
    """Co testuje: przycięcie słowników do pól id/nazwa/cena.
    Co udaje: nic — fixture surowe_produkty (pola nadmiarowe: dostepny,
    magazyn).
    Co sprawdzam: pierwszy produkt wyniku ma DOKŁADNIE klucze id,
    nazwa i cena.
    """
    wynik = zadanie_04_wybierz_pola(surowe_produkty)
    pierwszy_produkt = wynik[0]
    assert set(pierwszy_produkt) == {"id", "nazwa", "cena"}


def test_zadanie_04_nie_modyfikuje_wejscia(
    surowe_produkty: list[dict[str, Any]],
) -> None:
    """Co testuje: brak side effects — wejściowe słowniki zostają pełne.
    Co udaje: nic — fixture surowe_produkty.
    Co sprawdzam: po wywołaniu pierwszy produkt ORYGINAŁU nadal ma
    klucz magazyn.
    """
    zadanie_04_wybierz_pola(surowe_produkty)
    assert "magazyn" in surowe_produkty[0]


# --- zadanie_05 ---

def test_zadanie_05_znajduje_produkt_po_id(
    czyste_produkty: list[dict[str, Any]],
) -> None:
    """Co testuje: wyszukanie istniejącego produktu.
    Co udaje: nic — fixture czyste_produkty.
    Co sprawdzam: dla id 3 wynik to słownik z nazwą Monitor.
    """
    wynik = zadanie_05_znajdz_produkt(czyste_produkty, 3)
    assert wynik["nazwa"] == "Monitor"


def test_zadanie_05_zwraca_none_gdy_brak_id(
    czyste_produkty: list[dict[str, Any]],
) -> None:
    """Co testuje: kontrakt None dla nieistniejącego id.
    Co udaje: nic — fixture czyste_produkty (nie ma id 999).
    Co sprawdzam: wynik is None.
    """
    wynik = zadanie_05_znajdz_produkt(czyste_produkty, 999)
    assert wynik is None


# --- zadanie_06 ---

def test_zadanie_06_tworzy_plik_i_zwraca_true(
    czyste_produkty: list[dict[str, Any]], tmp_path: Path,
) -> None:
    """Co testuje: zapis katalogu na dysk.
    Co udaje: nic — prawdziwy zapis do tmp_path.
    Co sprawdzam: wynik is True i plik istnieje.
    """
    sciezka = tmp_path / "produkty.json"
    wynik = zadanie_06_zapisz_katalog(czyste_produkty, str(sciezka))
    assert wynik is True
    assert sciezka.exists()


def test_zadanie_06_zapisuje_pelna_zawartosc(
    czyste_produkty: list[dict[str, Any]], tmp_path: Path,
) -> None:
    """Co testuje: czy w pliku ląduje dokładnie przekazana lista.
    Co udaje: nic — zapis i samodzielny odczyt pliku.
    Co sprawdzam: treść pliku wczytana JSON-em równa się liście z fixture.
    """
    sciezka = tmp_path / "produkty.json"
    zadanie_06_zapisz_katalog(czyste_produkty, str(sciezka))
    with open(str(sciezka), "r", encoding="utf-8") as f:
        assert json.load(f) == czyste_produkty


# --- zadanie_07 ---

def test_zadanie_07_wczytuje_katalog(katalog_json: Path) -> None:
    """Co testuje: odczyt poprawnego pliku katalogu.
    Co udaje: nic — gotowy plik z fixture katalog_json (3 produkty).
    Co sprawdzam: wynik ma 3 produkty, pierwszy to Klawiatura.
    """
    wynik = zadanie_07_wczytaj_katalog(str(katalog_json))
    assert len(wynik) == 3
    assert wynik[0]["nazwa"] == "Klawiatura"


def test_zadanie_07_none_gdy_brak_pliku(tmp_path: Path) -> None:
    """Co testuje: kontrakt None przy nieistniejącym pliku.
    Co udaje: nic — ścieżka w pustym katalogu tymczasowym.
    Co sprawdzam: wynik is None.
    """
    sciezka = tmp_path / "nieistnieje.json"
    wynik = zadanie_07_wczytaj_katalog(str(sciezka))
    assert wynik is None


def test_zadanie_07_none_gdy_zepsuty_json(zepsuty_json: Path) -> None:
    """Co testuje: kontrakt None przy pliku z niepoprawnym JSON-em.
    Co udaje: nic — gotowy plik-podróbka z fixture zepsuty_json.
    Co sprawdzam: wynik is None (JSONDecodeError złapany w środku).
    """
    wynik = zadanie_07_wczytaj_katalog(str(zepsuty_json))
    assert wynik is None


# --- zadanie_08 ---

def test_zadanie_08_buduje_obiekt_z_poprawnych_danych() -> None:
    """Co testuje: udaną walidację słownika przez model.
    Co udaje: nic — podaję poprawny słownik wprost.
    Co sprawdzam: wynik ma pola nazwa i cena o podanych wartościach
    (dostęp przez kropkę, jak w temacie 16).
    """
    dane = {"id": 1, "nazwa": "Mysz", "cena": 19.99}
    wynik = zadanie_08_waliduj_produkt(dane)
    assert wynik.nazwa == "Mysz"
    assert wynik.cena == 19.99


def test_zadanie_08_zwraca_none_gdy_zle_dane() -> None:
    """Co testuje: kontrakt None przy danych nieprzechodzących walidacji.
    Co udaje: nic — słownik z ceną "darmo" (nie da się skonwertować
    na float).
    Co sprawdzam: wynik is None (ValidationError złapany w środku).
    """
    dane = {"id": 1, "nazwa": "Mysz", "cena": "abc"}
    wynik = zadanie_08_waliduj_produkt(dane)
    assert wynik is None


# --- zadanie_09 ---

def test_zadanie_09_get_zwraca_liste_z_pliku(katalog_json: Path) -> None:
    """Co testuje: endpoint GET /produkty serwujący zawartość pliku.
    Co udaje: nic — TestClient rozmawia z aplikacją bez sieci (temat 16),
    plik jest prawdziwy (fixture katalog_json).
    Co sprawdzam: kod 200 i 3 produkty w odpowiedzi JSON.
    """
    client = TestClient(zadanie_09_api_listy(str(katalog_json)))
    response = client.get("/produkty")
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_zadanie_09_pusty_katalog_daje_pusta_liste(tmp_path: Path) -> None:
    """Co testuje: zachowanie brzegowe — plik z pustą listą.
    Co udaje: nic — sam przygotowuję plik z treścią "[]".
    Co sprawdzam: kod 200 i pusta lista w odpowiedzi.
    """
    sciezka = tmp_path / "pusta.json"
    sciezka.write_text("[]", encoding="utf-8")
    client = TestClient(zadanie_09_api_listy(str(sciezka)))
    response = client.get("/produkty")
    assert response.status_code == 200
    assert response.json() == []


# --- zadanie_10 ---

def test_zadanie_10_zwraca_szczegoly_produktu(katalog_json: Path) -> None:
    """Co testuje: endpoint GET /produkty/{id} dla istniejącego produktu.
    Co udaje: nic — TestClient + prawdziwy plik z fixture.
    Co sprawdzam: kod 200 i nazwa Monitor dla id 3.
    """
    client = TestClient(zadanie_10_api_szczegolow(str(katalog_json)))
    response = client.get("/produkty/3")
    assert response.status_code == 200
    assert response.json()["nazwa"] == "Monitor"


def test_zadanie_10_kod_404_gdy_brak_produktu(katalog_json: Path) -> None:
    """Co testuje: odpowiedź 404 dla nieistniejącego id.
    Co udaje: nic — TestClient + prawdziwy plik (nie ma id 999).
    Co sprawdzam: status_code odpowiedzi to 404.
    """
    client = TestClient(zadanie_10_api_szczegolow(str(katalog_json)))
    response = client.get("/produkty/999")
    assert response.status_code == 404


# --- zadanie_11 ---

def test_zadanie_11_post_dopisuje_produkt(katalog_json: Path) -> None:
    """Co testuje: dodanie produktu przez POST i zapis do pliku.
    Co udaje: nic — TestClient + prawdziwy plik (startowo 3 produkty).
    Co sprawdzam: odpowiedź {"liczba": 4} i 4 pozycje w pliku po zapisie.
    """
    client = TestClient(zadanie_11_api_dodawania(str(katalog_json)))
    nowy_produkt = {"id": 5, "nazwa": "Monitor LG", "cena": 1299.0}
    response = client.post("/produkty", json=nowy_produkt)
    assert response.status_code == 200
    assert response.json() == {"liczba": 4}
    produkty = json.loads(katalog_json.read_text(encoding="utf-8"))
    assert len(produkty) == 4


def test_zadanie_11_kod_422_gdy_zle_dane(katalog_json: Path) -> None:
    """Co testuje: automatyczną walidację treści POST modelem Produkt.
    Co udaje: nic — TestClient + prawdziwy plik.
    Co sprawdzam: POST bez pola cena daje kod 422, a plik ma nadal
    3 pozycje (nic nie dopisano).
    """
    client = TestClient(zadanie_11_api_dodawania(str(katalog_json)))
    nowy_produkt = {"id": 5, "nazwa": "Monitor LG"}
    response = client.post("/produkty", json=nowy_produkt)
    assert response.status_code == 422
    produkty = json.loads(katalog_json.read_text(encoding="utf-8"))
    assert len(produkty) == 3


# --- zadanie_12 ---

def test_zadanie_12_buduje_czysty_katalog_na_dysku(
    monkeypatch: pytest.MonkeyPatch,
    surowe_produkty: list[dict[str, Any]],
    tmp_path: Path,
) -> None:
    """Co testuje: cały tor zaopatrzenia: pobranie -> filtr -> przycięcie -> zapis.
    Co udaje: requests.get — atrapa (200) z surowymi produktami.
    Co sprawdzam: wynik is True; plik ma 3 produkty (bez Myszy),
    a pierwszy nie ma już pola magazyn.
    """
    def podmieniony_get(
            url: str,
            params: dict[str, Any] | None = None,
            timeout: int | None = None,
    ) -> FakeResponse:
        """Atrapa requests.get zwracająca zdrową odpowiedź z fixture.

        Args:
            url: ignorowany adres.
            params: ignorowane parametry zapytania.
            timeout: ignorowany limit czasu.

        Returns:
            FakeResponse: atrapa z kodem 200 i danymi z fixture.
        """
        return FakeResponse(200, surowe_produkty)
    monkeypatch.setattr("mini_api_katalog.requests.get", podmieniony_get)
    sciezka = tmp_path / "produkty.json"
    wynik = zadanie_12_zbuduj_katalog("https://www.example.pl", str(sciezka))
    assert wynik is True
    plik_z_produktami = json.loads(sciezka.read_text(encoding="utf-8"))
    assert len(plik_z_produktami) == 3
    assert "magazyn" not in plik_z_produktami[0]


def test_zadanie_12_none_i_brak_pliku_gdy_api_padlo(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path,
) -> None:
    """Co testuje: propagację kontraktu None przy awarii hurtowni.
    Co udaje: requests.get — atrapa z kodem 500.
    Co sprawdzam: wynik is None i plik katalogu NIE powstał.
    """
    def podmieniony_get(
            url: str,
            params: dict[str, Any] | None = None,
            timeout: int | None = None,
    ) -> FakeResponse:
        """Atrapa requests.get udająca awarię serwera.

        Args:
            url: ignorowany adres.
            params: ignorowane parametry zapytania.
            timeout: ignorowany limit czasu.

        Returns:
            FakeResponse: atrapa z kodem 500 i pustymi danymi — jej
                raise_for_status rzuci HTTPError.
        """
        return FakeResponse(500, [])
    monkeypatch.setattr("mini_api_katalog.requests.get", podmieniony_get)
    sciezka = tmp_path / "produkty.json"
    wynik = zadanie_12_zbuduj_katalog("https://www.example.pl", str(sciezka))
    assert wynik is None
    assert not sciezka.exists()


# --- zadanie_13 ---

def test_zadanie_13_buduje_dzialajacy_sklep(
    monkeypatch: pytest.MonkeyPatch,
    surowe_produkty: list[dict[str, Any]],
    tmp_path: Path,
) -> None:
    """Co testuje: pełny pipeline — od hurtowni do działającego API.
    Co udaje: requests.get — atrapa (200) z surowymi produktami;
    endpointy testuję TestClientem bez sieci.
    Co sprawdzam: GET /produkty daje 3 produkty; GET /produkty/3 daje
    Monitor; GET /produkty/999 daje 404.
    """
    def podmieniony_get(
            url: str,
            params: dict[str, Any] | None = None,
            timeout: int | None = None,
    ) -> FakeResponse:
        """Atrapa requests.get zwracająca zdrową odpowiedź z fixture.

        Args:
            url: ignorowany adres.
            params: ignorowane parametry zapytania.
            timeout: ignorowany limit czasu.

        Returns:
            FakeResponse: atrapa z kodem 200 i danymi z fixture.
        """
        return FakeResponse(200, surowe_produkty)
    monkeypatch.setattr("mini_api_katalog.requests.get", podmieniony_get)
    sciezka = tmp_path / "produkty.json"
    client = TestClient(zadanie_13_pelne_api("https://www.example.pl", str(sciezka)))
    response = client.get("/produkty")
    assert response.status_code == 200
    assert len(response.json()) == 3
    response = client.get("/produkty/3")
    assert response.status_code == 200
    assert response.json()["nazwa"] == "Monitor"
    response = client.get("/produkty/999")
    assert response.status_code == 404


def test_zadanie_13_none_gdy_zaopatrzenie_padlo(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path,
) -> None:
    """Co testuje: kontrakt None całego pipeline'u przy awarii hurtowni.
    Co udaje: requests.get — atrapa z kodem 500.
    Co sprawdzam: wynik is None (aplikacja w ogóle nie powstaje).
    """
    def podmieniony_get(
            url: str,
            params: dict[str, Any] | None = None,
            timeout: int | None = None,
    ) -> FakeResponse:
        """Atrapa requests.get udająca awarię serwera.

        Args:
            url: ignorowany adres.
            params: ignorowane parametry zapytania.
            timeout: ignorowany limit czasu.

        Returns:
            FakeResponse: atrapa z kodem 500 i pustymi danymi — jej
                raise_for_status rzuci HTTPError.
        """
        return FakeResponse(500, [])
    monkeypatch.setattr("mini_api_katalog.requests.get", podmieniony_get)
    sciezka = tmp_path / "produkty.json"
    wynik = zadanie_13_pelne_api("https://www.example.pl", str(sciezka))
    assert wynik is None
