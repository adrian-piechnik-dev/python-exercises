# TODO: zaimportuj sys i os (stdlib), a nizej httpx i pytest (third-party)
#       — kolejnosc grup importow i pusta linia miedzy nimi

# TODO: dodaj sys.path.insert(0, ...) wskazujacy na folder tego tematu,
#       zeby test_async_httpx.py widzial modul async_httpx
#       (wzorzec: os.path.dirname(os.path.abspath(__file__)))


def odpowiadacz(request):
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
    # TODO: sprawdzaj request.url.path serii instrukcji if/elif
    #       i zwracaj httpx.Response dokladnie wedlug tabeli z Returns
    # TODO: na koncu (bez warunku) zwroc domyslne httpx.Response(200, text="ok")
    # TODO: uzupelnij type hinty parametru (httpx.Request)
    #       i zwracanej wartosci (httpx.Response)
    pass


# TODO: udekoruj fixture dekoratorem @pytest.fixture
def klient_testowy():
    """Klient httpx z podmienionym transportem — internet udawany w pamieci.

    Args:
        Brak.

    Returns:
        httpx.AsyncClient: klient, ktorego zapytania obsluguje funkcja
            odpowiadacz zamiast prawdziwej sieci.
    """
    # TODO: zwroc httpx.AsyncClient z argumentem
    #       transport=httpx.MockTransport(odpowiadacz)
    # TODO: uzupelnij type hint zwracanej wartosci (httpx.AsyncClient)
    pass
