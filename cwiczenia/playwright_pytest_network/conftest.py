import json
import os
import sys
import threading
from collections.abc import Iterator
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer

import pytest
from playwright.sync_api import APIRequestContext
from playwright.sync_api import Playwright

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

HTML_SKLEP = """
<html>
<head><title>Sklep online</title></head>
<body>
  <h1>Katalog</h1>
  <ul id="lista"></ul>
  <div role="status" id="stan" hidden></div>
  <script>
    fetch("/api/produkty")
      .then(function (odpowiedz) { return odpowiedz.json(); })
      .then(function (produkty) {
        var lista = document.getElementById("lista");
        produkty.forEach(function (produkt) {
          var element = document.createElement("li");
          element.textContent = produkt.nazwa;
          lista.appendChild(element);
        });
        var stan = document.getElementById("stan");
        stan.textContent = "zaladowano";
        stan.hidden = false;
      });
  </script>
</body>
</html>
"""


class Sprzedawca(BaseHTTPRequestHandler):
    """Obsluga zapytan budki-serwera testowego API produktow.

    Odpowiedzi (wszystkie z naglowkiem Content-Type: application/json):
        GET  /produkty   -> 200, [{"id": 1, "nazwa": "kubek"},
                                  {"id": 2, "nazwa": "talerz"}]
        GET  /produkt/1  -> 200, {"id": 1, "nazwa": "kubek"}
        GET  inne        -> 404, {"blad": "nie znaleziono"}
        POST /produkty   -> 201, {"utworzono": true}
        POST inne        -> 404, {"blad": "nie znaleziono"}
    """

    def do_GET(self) -> None:
        """Obsługuje GET wedlug tabeli tras z docstringa klasy.

        Args:
            Brak.

        Returns:
            None
        """
        if self.path == "/produkty":
            dane = [{"id": 1, "nazwa": "kubek"}, {"id": 2, "nazwa": "talerz"}]
            kod = 200
        elif self.path == "/produkt/1":
            dane = {"id": 1, "nazwa": "kubek"}
            kod = 200
        else:
            dane = {"blad": "nie znaleziono"}
            kod = 404
        self.send_response(kod)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(dane).encode("utf-8"))

    def do_POST(self) -> None:
        """Obsługuje POST wedlug tabeli tras z docstringa klasy.

        Args:
            Brak.

        Returns:
            None
        """
        self.rfile.read(int(self.headers.get("Content-Length", 0)))

        if self.path == "/produkty":
            dane = {"utworzono": True}
            kod = 201
        else:
            dane = {"blad": "nie znaleziono"}
            kod = 404

        self.send_response(kod)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(dane).encode("utf-8"))

    def log_message(self, format, *args) -> None:
        """Ucisza logi serwera w konsoli.

        Args:
            format: format stringa logu (ignorowany).
            *args: argumenty logu (ignorowane).

        Returns:
            None
        """
        pass


@pytest.fixture(scope="session")
def serwer_api() -> Iterator[str]:
    """Lokalna budka-serwer API na losowym wolnym porcie.

    Args:
        Brak.

    Returns:
        str: bazowy adres budki, np. "http://127.0.0.1:54321"
            (bez ukosnika na koncu); po sesji budka jest zamykana.
    """
    serwer = HTTPServer(("127.0.0.1", 0), Sprzedawca)
    port = serwer.server_address[1]
    watek = threading.Thread(target=serwer.serve_forever, daemon=True)
    watek.start()
    yield f"http://127.0.0.1:{port}"
    serwer.shutdown()


@pytest.fixture
def api(playwright: Playwright) -> APIRequestContext:
    """Kontekst zapytan API zbudowany z silnika wtyczki.

    Args:
        playwright: silnik Playwright (wbudowana fixture wtyczki
            pytest-playwright).

    Returns:
        APIRequestContext: telefon do API (get/post);
            po tescie odkladany przez dispose().
    """
    kontekst = playwright.request.new_context()
    yield kontekst
    kontekst.dispose()


@pytest.fixture
def html_sklepu() -> str:
    """Strona sklepu do zadania 12 (final offline).

    Args:
        Brak.

    Returns:
        str: zawartosc stalej HTML_SKLEP.
    """
    return HTML_SKLEP
