import sys
import os
import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi_pydantic import zadanie_12_pelne_api


@pytest.fixture
def plik_produktow(tmp_path: Path) -> Path:
    """Tymczasowy plik JSON z listą trzech produktów — do zadań 10-12.

    Args:
        tmp_path: wstrzykiwany przez pytest katalog tymczasowy.

    Returns:
        Path: ścieżka do pliku JSON z listą:
            Klawiatura/99.0, Mysz/49.0, Monitor/899.0.
    """
    # TODO: utwórz p = tmp_path / "produkty.json"
    # TODO: zdefiniuj liste = [
    #           {"nazwa": "Klawiatura", "cena": 99.0},
    #           {"nazwa": "Mysz", "cena": 49.0},
    #           {"nazwa": "Monitor", "cena": 899.0},
    #       ]
    # TODO: zapisz: p.write_text(json.dumps(liste), encoding="utf-8")
    # TODO: return p
    pass


@pytest.fixture
def klient_api(plik_produktow: Path) -> TestClient:
    """TestClient pełnego API z zadania 12 — "specjalny fixture" (temat 13),
    który zamiast danych podaje gotowego klienta.

    Args:
        plik_produktow: fixture z plikiem JSON produktów (magazyn API).

    Returns:
        TestClient: klient aplikacji zbudowanej na pliku produktów.
    """
    # TODO: zbuduj aplikację: app = zadanie_12_pelne_api(str(plik_produktow))
    # TODO: return TestClient(app)
    pass
