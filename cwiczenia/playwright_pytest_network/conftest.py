# TODO: zaimportuj json, sys, os i threading oraz BaseHTTPRequestHandler
#       i HTTPServer z http.server (stdlib), a nizej pytest oraz
#       APIRequestContext i Playwright z playwright.sync_api (third-party)
#       — kolejnosc grup importow i pusta linia miedzy nimi

# TODO: dodaj sys.path.insert(0, ...) wskazujacy na folder tego tematu,
#       zeby test_playwright_pytest_network.py widzial modul
#       playwright_pytest_network
#       (wzorzec: os.path.dirname(os.path.abspath(__file__)))


# Gotowa strona testowa (DANE, nie rozwiazanie — nie zmieniaj tresci,
# testy zaleza od dokladnych tekstow ponizej).

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


# TODO: zbuduj klase Sprzedawca dziedziczaca po BaseHTTPRequestHandler —
#       to budka-serwer dla testow API (zadania 05-07)
class Sprzedawca:
    """Obsluga zapytan budki-serwera testowego API produktow.

    Odpowiedzi (wszystkie z naglowkiem Content-Type: application/json):
        GET  /produkty   -> 200, [{"id": 1, "nazwa": "kubek"},
                                  {"id": 2, "nazwa": "talerz"}]
        GET  /produkt/1  -> 200, {"id": 1, "nazwa": "kubek"}
        GET  inne        -> 404, {"blad": "nie znaleziono"}
        POST /produkty   -> 201, {"utworzono": true}
        POST inne        -> 404, {"blad": "nie znaleziono"}
    """

    # TODO: zmien naglowek klasy na dziedziczenie:
    #       class Sprzedawca(BaseHTTPRequestHandler):

    # TODO: napisz metode do_GET(self) -> None z docstringiem:
    #       rozpoznaj self.path serii if/elif i odpowiedz wedlug tabeli
    #       z docstringa klasy; kazda odpowiedz to trzy kroki:
    #       send_response(kod), send_header("Content-Type",
    #       "application/json") + end_headers(),
    #       wfile.write(json.dumps(dane).encode("utf-8"))

    # TODO: napisz metode do_POST(self) -> None z docstringiem:
    #       najpierw odbierz tresc zapytania:
    #       self.rfile.read(int(self.headers.get("Content-Length", 0))),
    #       potem odpowiedz wedlug tabeli (201 dla /produkty, 404 inne)

    # TODO: napisz metode log_message(self, format, *args) -> None
    #       z docstringiem i samym pass — ucisza logi budki w konsoli
    pass


# TODO: udekoruj fixture dekoratorem @pytest.fixture(scope="session")
#       — jedna budka-serwer na cala sesje testowa
def serwer_api():
    """Lokalna budka-serwer API na losowym wolnym porcie.

    Args:
        Brak.

    Returns:
        str: bazowy adres budki, np. "http://127.0.0.1:54321"
            (bez ukosnika na koncu); po sesji budka jest zamykana.
    """
    # TODO: zbuduj serwer: HTTPServer(("127.0.0.1", 0), Sprzedawca)
    # TODO: odczytaj wylosowany port z serwer.server_address[1]
    # TODO: odpal petle obslugi w watku: threading.Thread(
    #       target=serwer.serve_forever, daemon=True).start()
    # TODO: oddaj adres testom: yield f"http://127.0.0.1:{port}"
    # TODO: po yield zamknij budke: serwer.shutdown()
    pass


# TODO: udekoruj fixture dekoratorem @pytest.fixture
def api(playwright):
    """Kontekst zapytan API zbudowany z silnika wtyczki.

    Args:
        playwright: silnik Playwright (wbudowana fixture wtyczki
            pytest-playwright).

    Returns:
        APIRequestContext: telefon do API (get/post);
            po tescie odkladany przez dispose().
    """
    # TODO: zbuduj kontekst: playwright.request.new_context()
    # TODO: oddaj go testowi przez yield
    # TODO: po yield posprzataj przez .dispose()
    # TODO: uzupelnij type hinty (parametr Playwright,
    #       zwrot APIRequestContext)
    pass


# TODO: udekoruj fixture dekoratorem @pytest.fixture
def html_sklepu():
    """Strona sklepu do zadania 12 (final offline).

    Args:
        Brak.

    Returns:
        str: zawartosc stalej HTML_SKLEP.
    """
    # TODO: zwroc stala HTML_SKLEP (zwykly return — fixture bez sprzatania
    #       nie potrzebuje yield)
    # TODO: uzupelnij type hint zwracanej wartosci (str)
    pass
