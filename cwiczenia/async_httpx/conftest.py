import os
import sys

import httpx
import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def odpowiadacz(request: httpx.Request) -> httpx.Response:
    """Recepcjonistka udawanego internetu — odpowiada na zapytania testowe.

    Args:
        request: obiekt zapytania httpx.Request przekazany przez MockTransport.

    Returns:
        httpx.Response: odpowiedz zalezna od koncowki adresu (request.url.path):
            "/ok"      -> 200, text "ok"
            "/brak"    -> 404, text "nie ma"
            "/dane"    -> 200, json {"miasto": "Krakow", "sprzedaz": 200}
            "/strona"  -> 200, text "<html><head><title>Testowa strona</title></head></html>"
            "/strona2" -> 200, text "<html><head><title>Druga strona</title></head></html>"
            "/pusta"   -> 200, text "<html><body>bez tytulu</body></html>"
            inne       -> 200, text "ok"
    """
    if request.url.path == "/ok":
        return httpx.Response(
            200, text="ok"
        )
    elif request.url.path == "/brak":
        return httpx.Response(
            404, text="nie ma"
        )
    elif request.url.path == "/dane":
        return httpx.Response(
            200, json={"miasto": "Krakow", "sprzedaz": 200}
        )
    elif request.url.path == "/strona":
        return httpx.Response(
            200, text="<html><head><title>Testowa strona</title></head></html>"
        )
    elif request.url.path == "/strona2":
        return httpx.Response(
            200, text="<html><head><title>Druga strona</title></head></html>")
    elif request.url.path == "/pusta":
        return httpx.Response(
            200, text="<html><body>bez tytulu</body></html>"
        )
    else:
        return httpx.Response(
            200, text="ok"
        )


@pytest.fixture
def klient_testowy() -> httpx.AsyncClient:
    """Klient httpx z podmienionym transportem — internet udawany w pamieci.

    Args:
        Brak.

    Returns:
        httpx.AsyncClient: klient, ktorego zapytania obsluguje funkcja
            odpowiadacz zamiast prawdziwej sieci.
    """
    return httpx.AsyncClient(transport=httpx.MockTransport(odpowiadacz))
