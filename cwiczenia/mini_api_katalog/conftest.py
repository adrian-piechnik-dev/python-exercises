# UWAGA (reguły mini-projektu M2): ten conftest dostajesz GOTOWY, bez TODO.
# Infrastruktura testowa (FakeResponse) i dane są żmudne, a niczego nowego
# nie uczą — twoja praca to logika w mini_api_katalog.py i asserty w testach.
# Przeczytaj jednak całość uważnie: musisz znać dane, żeby testować.

import json
import os
import sys
from pathlib import Path
from typing import Any

import pytest
import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class FakeResponse:
    """Atrapa odpowiedzi HTTP — udaje obiekt zwracany przez requests.get.

    Args:
        status_code: kod statusu, który atrapa ma udawać (np. 200, 500).
        dane: struktura (list lub dict), którą zwróci metoda json().
    """

    def __init__(self, status_code: int, dane: Any) -> None:
        """Zapamiętuje kod statusu i dane do udawania.

        Args:
            status_code: kod statusu HTTP.
            dane: dane zwracane później przez json().

        Returns:
            None
        """
        self.status_code = status_code
        self._dane = dane

    def json(self) -> Any:
        """Zwraca zapamiętane dane — jak .json() prawdziwej odpowiedzi.

        Args:
            Brak.

        Returns:
            Any: dane przekazane przy tworzeniu atrapy.
        """
        return self._dane

    def raise_for_status(self) -> None:
        """Rzuca requests.HTTPError przy kodach 4xx/5xx — jak prawdziwa odpowiedź.

        Args:
            Brak.

        Returns:
            None
        """
        if self.status_code >= 400:
            raise requests.HTTPError(f"kod {self.status_code}")


@pytest.fixture
def surowe_produkty() -> list[dict[str, Any]]:
    """Surowa lista 4 produktów z hurtowni — z nadmiarowymi polami.

    Args:
        Brak.

    Returns:
        list[dict[str, Any]]: produkty z polami id/nazwa/cena/dostepny/
            magazyn; dostępne są 3 (id 1, 3, 4), Mysz (id 2) nie.
    """
    return [
        {"id": 1, "nazwa": "Klawiatura", "cena": 99.0,
         "dostepny": True, "magazyn": "A1"},
        {"id": 2, "nazwa": "Mysz", "cena": 49.0,
         "dostepny": False, "magazyn": "A2"},
        {"id": 3, "nazwa": "Monitor", "cena": 899.0,
         "dostepny": True, "magazyn": "B1"},
        {"id": 4, "nazwa": "Kabel HDMI", "cena": 25.0,
         "dostepny": True, "magazyn": "B2"},
    ]


@pytest.fixture
def czyste_produkty() -> list[dict[str, Any]]:
    """Czysty katalog: 3 dostępne produkty przycięte do id/nazwa/cena.

    Args:
        Brak.

    Returns:
        list[dict[str, Any]]: Klawiatura 99.0 (id 1), Monitor 899.0 (id 3),
            Kabel HDMI 25.0 (id 4).
    """
    return [
        {"id": 1, "nazwa": "Klawiatura", "cena": 99.0},
        {"id": 3, "nazwa": "Monitor", "cena": 899.0},
        {"id": 4, "nazwa": "Kabel HDMI", "cena": 25.0},
    ]


@pytest.fixture
def katalog_json(tmp_path: Path, czyste_produkty: list[dict[str, Any]]) -> Path:
    """Gotowy plik JSON z czystym katalogiem — do zadań 07 i 09-11.

    Args:
        tmp_path: wstrzykiwany przez pytest katalog tymczasowy.
        czyste_produkty: fixture z listą 3 czystych produktów.

    Returns:
        Path: ścieżka do pliku katalog.json z zawartością czyste_produkty.
    """
    sciezka = tmp_path / "katalog.json"
    sciezka.write_text(json.dumps(czyste_produkty), encoding="utf-8")
    return sciezka


@pytest.fixture
def zepsuty_json(tmp_path: Path) -> Path:
    """Plik, który JSON-em tylko udaje — do testu odczytu (zadanie 07).

    Args:
        tmp_path: wstrzykiwany przez pytest katalog tymczasowy.

    Returns:
        Path: ścieżka do pliku z treścią niebędącą poprawnym JSON-em.
    """
    sciezka = tmp_path / "zepsuty.json"
    sciezka.write_text("to nie jest {json[", encoding="utf-8")
    return sciezka
