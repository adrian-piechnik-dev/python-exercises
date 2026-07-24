from playwright.sync_api import APIRequestContext, BrowserContext, Page, expect


def zadanie_01_naglowek_strony(page: Page, html: str) -> str:
    """Wstrzykuje HTML do karty z wtyczki i zwraca tekst naglowka.

    Args:
        page: karta przegladarki (fixture wtyczki pytest-playwright).
        html: kod HTML do wyrenderowania.

    Returns:
        str: tekst elementu o roli "heading".
    """
    page.set_content(html)
    return page.get_by_role("heading").inner_text()


def zadanie_02_podmien_strone(page: Page, url: str, html: str) -> None:
    """Rejestruje celnika podstawiajacego wlasny HTML pod podanym adresem.

    Args:
        page: karta przegladarki.
        url: wzorzec adresu do przechwycenia, np. "https://sklep.testowy/sklep".
        html: kod HTML, ktory ma dostac przegladarka zamiast internetu.

    Returns:
        None: funkcja tylko rejestruje celnika (goto robi test).
    """
    def celnik(route) -> None:
        route.fulfill(
            status=200,
            body=html,
            content_type="text/html"
        )
    page.route(url, celnik)


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
    def celnik(route) -> None:
        route.fulfill(
            status=200,
            json=dane
        )
    page.route(url, celnik)


def zadanie_04_zablokuj_obrazki(page: Page) -> None:
    """Rejestruje celnika ubijajacego wszystkie zapytania o pliki .png.

    Args:
        page: karta przegladarki.

    Returns:
        None: funkcja tylko rejestruje celnika.
    """
    def celnik(route) -> None:
        route.abort()
    page.route("**/*.png", celnik)


def zadanie_05_pobierz_status_api(api: APIRequestContext, url: str) -> int:
    """Odpytuje API bez przegladarki i zwraca kod statusu.

    Args:
        api: kontekst zapytan API (playwright.request.new_context()).
        url: pelny adres punktu API.

    Returns:
        int: kod statusu odpowiedzi (np. 200 albo 404).
    """
    response = api.get(url)
    return response.status


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
    response = api.get(url)
    if response.ok is False:
        return None
    return response.json()


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
    response = api.post(url, data=dane)
    return response.status


def zadanie_08_polecenie_codegen(url: str) -> str:
    """Buduje komende terminalowa uruchamiajaca nagrywanie codegen.

    Args:
        url: adres strony, na ktorej ma sie zaczac nagrywanie.

    Returns:
        str: komenda w formacie "playwright codegen <url>".
    """
    return f"playwright codegen {url}"


def zadanie_09_polecenie_trace(plik: str) -> str:
    """Buduje komende terminalowa otwierajaca nagrany trace.

    Args:
        plik: sciezka do nagrania, np. "nagranie.zip".

    Returns:
        str: komenda w formacie "playwright show-trace <plik>".
    """
    return f"playwright show-trace {plik}"


def zadanie_10_nagraj_trace(context: BrowserContext, sciezka: str) -> bool:
    """Nagrywa krotki trace (czarna skrzynke) i zapisuje go do pliku.

    Args:
        context: kontekst przegladarki (fixture wtyczki pytest-playwright).
        sciezka: sciezka docelowa pliku .zip z nagraniem.

    Returns:
        bool: True po zapisaniu nagrania.
    """
    context.tracing.start(screenshots=True, snapshots=True)
    page = context.new_page()
    page.set_content("<h1>Nagranie</h1>")
    page.close()
    context.tracing.stop(path=sciezka)
    return True


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
    translator = {
        "monkeypatch.setattr": "page.route",
        "return_value": "route.fulfill",
        "side_effect": "route.abort",
        "httpx.MockTransport": "page.route"
    }
    return translator.get(narzedzie)


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
    zadanie_02_podmien_strone(page, "**/sklep", html_sklepu)
    zadanie_03_podmien_api_json(page, "**/api/produkty", produkty)
    page.goto("https://sklep.testowy/sklep")
    expect(page.get_by_text("zaladowano")).to_be_visible(timeout=2000)
    return page.get_by_role("listitem").all_inner_texts()
