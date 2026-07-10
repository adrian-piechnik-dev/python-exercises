# Zadania — playwright_pytest_network
#
# Spis zadan:
# zadanie_01 — rozgrzewka na fixture wtyczki: naglowek strony z set_content
# zadanie_02 — celnik fulfill: podmien cala strone HTML pod adresem
# zadanie_03 — celnik fulfill(json=...): podmien odpowiedz API
# zadanie_04 — celnik abort: zablokuj wszystkie obrazki .png
# zadanie_05 — request_context: status odpowiedzi API
# zadanie_06 — request_context: JSON wzorcem z requests (None gdy nie ok)
# zadanie_07 — request_context: POST nowych danych i kod odpowiedzi
# zadanie_08 — zbuduj komende terminalowa codegen dla adresu
# zadanie_09 — zbuduj komende terminalowa show-trace dla pliku
# zadanie_10 — nagraj trace kontekstu do pliku .zip
# zadanie_11 — zazebienie: tlumacz starych podmian (monkeypatch/mock) na nowe
# zadanie_12 — final: sklep offline — celnicy podstawiaja strone I jej API

from playwright.sync_api import APIRequestContext, BrowserContext, Page, expect


def zadanie_01_naglowek_strony(page: Page, html: str) -> str:
    """Wstrzykuje HTML do karty z wtyczki i zwraca tekst naglowka.

    Args:
        page: karta przegladarki (fixture wtyczki pytest-playwright).
        html: kod HTML do wyrenderowania.

    Returns:
        str: tekst elementu o roli "heading".
    """
    # TODO: wstrzyknij html przez page.set_content(html)
    # TODO: zwroc inner_text() locatora page.get_by_role("heading")
    pass


def zadanie_02_podmien_strone(page: Page, url: str, html: str) -> None:
    """Rejestruje celnika podstawiajacego wlasny HTML pod podanym adresem.

    Args:
        page: karta przegladarki.
        url: wzorzec adresu do przechwycenia, np. "https://sklep.testowy/sklep".
        html: kod HTML, ktory ma dostac przegladarka zamiast internetu.

    Returns:
        None: funkcja tylko rejestruje celnika (goto robi test).
    """
    # TODO: zdefiniuj wewnatrz funkcje-celnika def celnik(route):
    #       ktora robi route.fulfill(status=200, body=html,
    #       content_type="text/html") — domkniecie pamieta html
    # TODO: zarejestruj celnika przez page.route(url, celnik)
    #       (celnik BEZ nawiasow!)
    pass


def zadanie_03_podmien_api_json(
    page: Page, url: str, dane: dict | list
) -> None:
    """Rejestruje celnika podstawiajacego JSON pod adresem API.

    Args:
        page: karta przegladarki.
        url: wzorzec adresu API, np. "**/api/dane".
        dane: slownik albo lista — tresc odpowiedzi JSON.

    Returns:
        None: funkcja tylko rejestruje celnika.
    """
    # TODO: zdefiniuj wewnatrz celnika robiacego
    #       route.fulfill(status=200, json=dane)
    # TODO: zarejestruj go przez page.route(url, celnik)
    pass


def zadanie_04_zablokuj_obrazki(page: Page) -> None:
    """Rejestruje celnika ubijajacego wszystkie zapytania o pliki .png.

    Args:
        page: karta przegladarki.

    Returns:
        None: funkcja tylko rejestruje celnika.
    """
    # TODO: zdefiniuj wewnatrz celnika robiacego route.abort()
    # TODO: zarejestruj go na wzorcu "**/*.png"
    pass


def zadanie_05_pobierz_status_api(api: APIRequestContext, url: str) -> int:
    """Odpytuje API bez przegladarki i zwraca kod statusu.

    Args:
        api: kontekst zapytan API (playwright.request.new_context()).
        url: pelny adres punktu API.

    Returns:
        int: kod statusu odpowiedzi (np. 200 albo 404).
    """
    # TODO: wykonaj response = api.get(url)
    # TODO: zwroc response.status
    pass


def zadanie_06_pobierz_json_api(
    api: APIRequestContext, url: str
) -> dict | None:
    """Pobiera JSON z API wzorcem z requests; blad sygnalizuje przez None.

    Args:
        api: kontekst zapytan API.
        url: pelny adres punktu API.

    Returns:
        dict | None: slownik z response.json() gdy response.ok,
            None w przeciwnym razie.
    """
    # TODO: wykonaj response = api.get(url)
    # TODO: jesli response.ok is False — zwroc None
    # TODO: w przeciwnym razie zwroc response.json()
    pass


def zadanie_07_utworz_produkt_api(
    api: APIRequestContext, url: str, dane: dict
) -> int:
    """Wysyla POST z danymi nowego produktu i zwraca kod odpowiedzi.

    Args:
        api: kontekst zapytan API.
        url: pelny adres punktu API przyjmujacego POST.
        dane: slownik z danymi produktu (poleci jako JSON).

    Returns:
        int: kod statusu odpowiedzi (np. 201 gdy utworzono).
    """
    # TODO: wykonaj response = api.post(url, data=dane)
    # TODO: zwroc response.status
    pass


def zadanie_08_polecenie_codegen(url: str) -> str:
    """Buduje komende terminalowa uruchamiajaca nagrywanie codegen.

    Args:
        url: adres strony, na ktorej ma sie zaczac nagrywanie.

    Returns:
        str: komenda w formacie "playwright codegen <url>".
    """
    # TODO: zwroc f-string "playwright codegen {url}"
    pass


def zadanie_09_polecenie_trace(plik: str) -> str:
    """Buduje komende terminalowa otwierajaca nagrany trace.

    Args:
        plik: sciezka do nagrania, np. "nagranie.zip".

    Returns:
        str: komenda w formacie "playwright show-trace <plik>".
    """
    # TODO: zwroc f-string "playwright show-trace {plik}"
    pass


def zadanie_10_nagraj_trace(context: BrowserContext, sciezka: str) -> bool:
    """Nagrywa krotki trace (czarna skrzynke) i zapisuje go do pliku.

    Args:
        context: kontekst przegladarki (fixture wtyczki pytest-playwright).
        sciezka: sciezka docelowa pliku .zip z nagraniem.

    Returns:
        bool: True po zapisaniu nagrania.
    """
    # TODO: wlacz nagrywanie: context.tracing.start(screenshots=True,
    #       snapshots=True)
    # TODO: wykonaj cokolwiek do nagrania: otworz karte
    #       (context.new_page()), wstrzyknij prosty HTML przez
    #       set_content (np. "<h1>Nagranie</h1>"), zamknij karte
    # TODO: zatrzymaj i zapisz: context.tracing.stop(path=sciezka)
    # TODO: zwroc True
    pass


def zadanie_11_przetlumacz_podmiane(narzedzie: str) -> str | None:
    """Tlumaczy stare narzedzie podmiany na odpowiednik z tego tematu.

    Args:
        narzedzie: nazwa z tematow 11/13/23, jedna z:
            "monkeypatch.setattr", "return_value", "side_effect",
            "httpx.MockTransport".

    Returns:
        str | None: odpowiednik wedlug sciagi z sekcji 9 teorii
            ("page.route", "route.fulfill", "route.abort", "page.route");
            None dla nieznanego narzedzia.
    """
    # TODO: zbuduj slownik tlumaczen (4 pary wedlug sekcji 9 teorii):
    #       "monkeypatch.setattr" -> "page.route",
    #       "return_value" -> "route.fulfill",
    #       "side_effect" -> "route.abort",
    #       "httpx.MockTransport" -> "page.route"
    # TODO: zwroc slownik.get(narzedzie) — get bez domyslnej daje None
    pass


def zadanie_12_sklep_offline(
    page: Page, html_sklepu: str, produkty: list[dict]
) -> list[str]:
    """Uruchamia sklep w pelni offline: celnicy podstawiaja strone i API.

    Args:
        page: karta przegladarki.
        html_sklepu: HTML strony sklepu (jej skrypt pobiera /api/produkty
            i dorysowuje elementy listy, na koncu pokazuje status
            "zaladowano").
        produkty: lista slownikow z kluczem "nazwa" — odpowiedz atrapy API.

    Returns:
        list[str]: nazwy produktow odczytane z narysowanej listy
            (pusta lista, gdy produkty byly puste).
    """
    # TODO: podmien strone: uzyj zadanie_02_podmien_strone dla wzorca
    #       "**/sklep" i html_sklepu
    # TODO: podmien API: uzyj zadanie_03_podmien_api_json dla wzorca
    #       "**/api/produkty" i... uwaga: fulfill(json=...) przyjmuje
    #       tez liste — przekaz produkty
    # TODO: wejdz na strone: page.goto("https://sklep.testowy/sklep")
    # TODO: poczekaj na koniec rysowania: expect na get_by_text
    #       ("zaladowano") + to_be_visible(timeout=2000)
    # TODO: zwroc page.get_by_role("listitem").all_inner_texts()
    pass
