import sys
import os
import json
from pathlib import Path
from typing import Any

import pytest
import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class FakeResponse:
    """Atrapa odpowiedzi HTTP — jak w temacie 11 (requests_api_podstawy).

    Args:
        status_code: kod statusu, który atrapa ma udawać (np. 200, 500).
        dane: struktura, którą zwróci metoda json().
    """

    def __init__(self, status_code: int, dane: Any) -> None:
        """Zapamiętuje kod statusu i dane do udawania.

        Args:
            status_code: kod statusu HTTP.
            dane: dane zwracane później przez json().

        Returns:
            None
        """
        # TODO: zapisz status_code w atrybucie self.status_code
        # TODO: zapisz dane w atrybucie self._dane
        pass

    def json(self) -> Any:
        """Zwraca zapamiętane dane — jak .json() prawdziwej odpowiedzi.

        Args:
            Brak.

        Returns:
            Any: dane przekazane przy tworzeniu atrapy.
        """
        # TODO: zwróć self._dane
        pass

    def raise_for_status(self) -> None:
        """Rzuca requests.HTTPError przy kodach 4xx/5xx.

        Args:
            Brak.

        Returns:
            None
        """
        # TODO: jeśli self.status_code >= 400 —
        #       raise requests.HTTPError(f"kod {self.status_code}")
        pass


@pytest.fixture
def plik_konfiguracyjny(tmp_path: Path) -> Path:
    """Tymczasowy plik JSON z konfiguracją — scope domyślny (function).

    Args:
        tmp_path: wstrzykiwany przez pytest katalog tymczasowy.

    Returns:
        Path: ścieżka do pliku JSON z {"jezyk": "pl", "limit": 10}.
    """
    # TODO: utwórz p = tmp_path / "konfiguracja.json"
    # TODO: zapisz dane: p.write_text(
    #           json.dumps({"jezyk": "pl", "limit": 10}), encoding="utf-8")
    # TODO: return p
    pass


@pytest.fixture(scope="module")
def konfiguracja_globalna() -> dict[str, Any]:
    """Słownik konfiguracyjny współdzielony przez cały plik testów.

    scope="module" — pytest utworzy go RAZ dla całego pliku testowego;
    traktuj jako tylko-do-odczytu (nie modyfikuj w testach!).

    Args:
        Brak.

    Returns:
        dict[str, Any]: słownik {"jezyk": "pl", "limit": 10}.
    """
    # TODO: return {"jezyk": "pl", "limit": 10}
    pass
