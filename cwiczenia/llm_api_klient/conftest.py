import os
import sys

import pytest
import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class FalszywaOdpowiedz:
    """Atrapa obiektu requests.Response do testów bez internetu.

    Udaje tylko to, czego używa testowany kod: metody json()
    i raise_for_status().
    """

    def __init__(self, dane: dict, blad_http: bool = False) -> None:
        """Zapamiętuje dane odpowiedzi i tryb błędu HTTP.

        Args:
            dane: słownik, który zwróci metoda json().
            blad_http: True, gdy odpowiedź ma udawać błąd HTTP (4xx/5xx).

        Returns:
            None: konstruktor niczego nie zwraca.
        """
        # TODO: zapisz dane w atrybucie self.dane
        # TODO: zapisz blad_http w atrybucie self.blad_http
        pass

    def json(self) -> dict:
        """Zwraca zapamiętany słownik — jak prawdziwe Response.json().

        Args:
            Brak.

        Returns:
            dict: dane przekazane przy tworzeniu atrapy.
        """
        # TODO: zwróć self.dane
        pass

    def raise_for_status(self) -> None:
        """Rzuca HTTPError w trybie błędu — jak prawdziwe raise_for_status().

        Args:
            Brak.

        Returns:
            None: przy sukcesie nie robi nic; w trybie błędu rzuca
                requests.exceptions.HTTPError.
        """
        # TODO: jeśli self.blad_http is True — rzuć
        #   requests.exceptions.HTTPError("Serwer zwrocil blad")
        # TODO: w przeciwnym razie nie rób nic (funkcja po prostu się kończy)
        pass


@pytest.fixture
def odpowiedz_ok() -> FalszywaOdpowiedz:
    """Atrapa poprawnej odpowiedzi API z jednym blokiem tekstu.

    Args:
        Brak.

    Returns:
        FalszywaOdpowiedz: odpowiedź z danymi
            {"content": [{"type": "text", "text": "Czesc, jestem Claude!"}]}.
    """
    # TODO: zwróć FalszywaOdpowiedz z danymi opisanymi w Returns
    pass


@pytest.fixture
def odpowiedz_blad_http() -> FalszywaOdpowiedz:
    """Atrapa odpowiedzi, której raise_for_status() rzuca HTTPError.

    Args:
        Brak.

    Returns:
        FalszywaOdpowiedz: odpowiedź z pustym słownikiem danych
            i włączonym trybem błędu HTTP.
    """
    # TODO: zwróć FalszywaOdpowiedz({}, blad_http=True)
    pass
