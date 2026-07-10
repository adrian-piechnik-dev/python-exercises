# Zadania — playwright_podstawy
#
# Spis zadan:
# zadanie_01 — pelny rytual startowy: otworz strone i zwroc jej tytul
# zadanie_02 — locator get_by_role: tekst naglowka strony
# zadanie_03 — locator get_by_text: czy tekst jest widoczny (migawka)
# zadanie_04 — locator get_by_label + akcja fill: wypelnij pole formularza
# zadanie_05 — akcja check: odhacz pole zgody i potwierdz stan
# zadanie_06 — akcja click: kliknij przycisk o podanej nazwie
# zadanie_07 — count: policz elementy o danej roli
# zadanie_08 — get_attribute: adres linku (None gdy linku brak)
# zadanie_09 — expect + to_be_visible: poczekaj na tekst z opoznieniem
# zadanie_10 — zlozenie: wypelnij, odhacz, kliknij i odczytaj komunikat
# zadanie_11 — zazebienie: tlumacz pojec Selenium -> Playwright
# zadanie_12 — zazebienie: scenariusz logowania znany z tematu Selenium

from playwright.sync_api import Page, expect, sync_playwright


def zadanie_01_pobierz_tytul(url: str) -> str:
    """Otwiera strone w niewidzialnej przegladarce i zwraca jej tytul.

    Args:
        url: adres strony (moze byc file:// z dysku).

    Returns:
        str: tytul strony (zawartosc znacznika <title>).
    """
    # TODO: uzyj pelnego rytualu: with sync_playwright() as p:
    # TODO: odpal przegladarke p.chromium.launch(headless=True)
    # TODO: otworz karte browser.new_page() i wejdz na url przez goto
    # TODO: odczytaj tytul przez page.title() i zapisz do zmiennej
    # TODO: zamknij przegladarke (browser.close()) i zwroc tytul
    pass


def zadanie_02_pobierz_tekst_naglowka(page: Page) -> str:
    """Zwraca widoczny tekst naglowka strony.

    Args:
        page: karta przegladarki z wczytana strona.

    Returns:
        str: tekst elementu o roli "heading".
    """
    # TODO: zbuduj locator page.get_by_role("heading")
    # TODO: zwroc jego .inner_text()
    pass


def zadanie_03_czy_tekst_widoczny(page: Page, tekst: str) -> bool:
    """Sprawdza migawkowo, czy podany tekst jest teraz widoczny na stronie.

    Args:
        page: karta przegladarki z wczytana strona.
        tekst: szukany widoczny tekst.

    Returns:
        bool: True gdy tekst jest teraz widoczny, False w przeciwnym razie.
    """
    # TODO: zbuduj locator page.get_by_text(tekst)
    # TODO: zwroc wynik .is_visible() (migawka — bez czekania)
    pass


def zadanie_04_wypelnij_pole(page: Page, etykieta: str, tekst: str) -> str:
    """Wypelnia pole formularza wskazane etykieta i zwraca jego zawartosc.

    Args:
        page: karta przegladarki z wczytana strona.
        etykieta: tekst etykiety pola (label), np. "Imie".
        tekst: tekst do wpisania.

    Returns:
        str: aktualna zawartosc pola po wpisaniu (input_value).
    """
    # TODO: zbuduj locator page.get_by_label(etykieta)
    # TODO: wpisz tekst akcja .fill(tekst)
    # TODO: zwroc .input_value() tego samego locatora
    pass


def zadanie_05_zaznacz_zgode(page: Page, nazwa: str) -> bool:
    """Odhacza pole wyboru o podanej nazwie i zwraca jego stan.

    Args:
        page: karta przegladarki z wczytana strona.
        nazwa: widoczna nazwa checkboxa, np. "Akceptuje regulamin".

    Returns:
        bool: True gdy pole jest po operacji odhaczone.
    """
    # TODO: zbuduj locator page.get_by_role("checkbox", name=nazwa)
    # TODO: odhacz akcja .check()
    # TODO: zwroc wynik .is_checked()
    pass


def zadanie_06_kliknij_przycisk(page: Page, nazwa: str) -> None:
    """Klika przycisk o podanej nazwie (auto-waiting zrobi reszte).

    Args:
        page: karta przegladarki z wczytana strona.
        nazwa: widoczny napis na przycisku, np. "Wyslij".

    Returns:
        None: funkcja wykonuje akcje, niczego nie zwraca.
    """
    # TODO: zbuduj locator page.get_by_role("button", name=nazwa)
    # TODO: kliknij akcja .click() (bez return — kontrakt None)
    pass


def zadanie_07_policz_elementy(page: Page, rola: str) -> int:
    """Liczy elementy o podanej roli na stronie.

    Args:
        page: karta przegladarki z wczytana strona.
        rola: rola ARIA, np. "button" albo "link".

    Returns:
        int: liczba pasujacych elementow (0 gdy brak).
    """
    # TODO: zbuduj locator page.get_by_role(rola)
    # TODO: zwroc jego .count()
    pass


def zadanie_08_pobierz_adres_linku(page: Page, nazwa: str) -> str | None:
    """Zwraca adres (href) linku o podanej nazwie; brak linku daje None.

    Args:
        page: karta przegladarki z wczytana strona.
        nazwa: widoczny tekst linku, np. "Kontakt".

    Returns:
        str | None: wartosc atrybutu href albo None, gdy takiego linku
            nie ma na stronie.
    """
    # TODO: zbuduj locator page.get_by_role("link", name=nazwa)
    # TODO: jesli .count() == 0 — zwroc None (istnienie bez czekania)
    # TODO: w przeciwnym razie zwroc .get_attribute("href")
    pass


def zadanie_09_poczekaj_na_tekst(page: Page, tekst: str) -> bool:
    """Czeka cierpliwie (expect), az podany tekst stanie sie widoczny.

    Args:
        page: karta przegladarki z wczytana strona.
        tekst: tekst, ktory MA sie pojawic (moze z opoznieniem).

    Returns:
        bool: True gdy tekst stal sie widoczny w limicie 2 sekund
            (gdy nie — expect rzuca AssertionError).
    """
    # TODO: uzyj expect(page.get_by_text(tekst)).to_be_visible(timeout=2000)
    # TODO: po udanym expect zwroc True
    pass


def zadanie_10_wyslij_formularz(page: Page, imie: str) -> str:
    """Przechodzi caly formularz: wypelnia, odhacza zgode, klika, czyta wynik.

    Args:
        page: karta przegladarki ze strona formularza.
        imie: imie do wpisania w pole "Imie".

    Returns:
        str: tekst komunikatu (element o roli "status") po wyslaniu.
    """
    # TODO: wypelnij pole "Imie" (get_by_label + fill)
    # TODO: odhacz checkbox "Akceptuje regulamin" (get_by_role + check)
    # TODO: kliknij przycisk "Wyslij" (get_by_role + click)
    # TODO: poczekaj na komunikat: expect(page.get_by_role("status"))
    #       .to_be_visible(timeout=2000)
    # TODO: zwroc .inner_text() elementu o roli "status"
    pass


def zadanie_11_przetlumacz_selenium(pojecie: str) -> str | None:
    """Tlumaczy pojecie z Selenium na odpowiednik w Playwright.

    Args:
        pojecie: nazwa z Selenium, jedna z: "find_element", "send_keys",
            "WebDriverWait", "expected_conditions", "driver.get".

    Returns:
        str | None: odpowiednik w Playwright wedlug sciagi z teorii
            ("locatory", "fill", "auto-waiting", "expect", "page.goto");
            None dla nieznanego pojecia.
    """
    # TODO: zbuduj slownik tlumaczen (5 par wedlug sekcji 8 teorii):
    #       "find_element" -> "locatory", "send_keys" -> "fill",
    #       "WebDriverWait" -> "auto-waiting",
    #       "expected_conditions" -> "expect", "driver.get" -> "page.goto"
    # TODO: zwroc slownik.get(pojecie) — get bez domyslnej daje None
    #       dla nieznanego klucza
    pass


def zadanie_12_zaloguj(page: Page, login: str, haslo: str) -> str:
    """Odtwarza scenariusz logowania z tematu Selenium — teraz w Playwright.

    Args:
        page: karta przegladarki ze strona logowania.
        login: login do wpisania w pole "Login".
        haslo: haslo do wpisania w pole "Haslo".

    Returns:
        str: tekst komunikatu (rola "status") po probie logowania —
            powitanie albo informacja o blednych danych.
    """
    # TODO: wypelnij pole "Login" (get_by_label + fill)
    # TODO: wypelnij pole "Haslo" (get_by_label + fill)
    # TODO: kliknij przycisk "Zaloguj" (get_by_role + click)
    # TODO: poczekaj na komunikat (expect + to_be_visible, timeout=2000,
    #       rola "status")
    # TODO: zwroc .inner_text() komunikatu
    pass
