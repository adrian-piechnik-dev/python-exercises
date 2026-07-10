import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture
def odpowiedz_api_poprawna() -> dict:
    """Koperta API z JSON-em owiniętym w blok markdown w treści modelu.

    Args:
        Brak.

    Returns:
        dict: słownik {"content": [{"type": "text", "text": ...}]},
            gdzie text to '```json\\n{"imie": "Anna", "wiek": 30}\\n```'.
    """
    # TODO: zwróć słownik z kluczem "content" — listą z jednym słownikiem
    #   {"type": "text", "text": '```json\n{"imie": "Anna", "wiek": 30}\n```'}
    pass


@pytest.fixture
def odpowiedz_api_zepsuta_tresc() -> dict:
    """Koperta API poprawna, ale treść modelu nie jest JSON-em (warstwa 2).

    Args:
        Brak.

    Returns:
        dict: słownik {"content": [{"type": "text", "text":
            "Niestety nie moge wyciagnac danych."}]}.
    """
    # TODO: zwróć słownik z kluczem "content" — listą z jednym słownikiem
    #   {"type": "text", "text": "Niestety nie moge wyciagnac danych."}
    pass
