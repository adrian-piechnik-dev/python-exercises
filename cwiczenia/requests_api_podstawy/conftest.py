import sys
import os
from typing import Any

import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class FakeResponse:
    """Atrapa odpowiedzi HTTP — udaje obiekt zwracany przez requests.get/post.

    Args:
        status_code: kod statusu, który atrapa ma udawać (np. 200, 404).
        dane: struktura (dict lub list), którą zwróci metoda json().
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
        # TODO: zapisz dane w atrybucie self._dane (podkreślenie = wewnętrzny)
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
        """Rzuca requests.HTTPError przy kodach 4xx/5xx — jak prawdziwa odpowiedź.

        Args:
            Brak.

        Returns:
            None
        """
        # TODO: jeśli self.status_code >= 400 —
        #       raise requests.HTTPError(f"kod {self.status_code}")
        pass
