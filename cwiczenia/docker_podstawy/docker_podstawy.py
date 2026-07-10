# Spis zadań:
# 01 — zbuduj linię FROM z obrazu i taga
# 02 — zbuduj linię COPY ze źródła i celu
# 03 — zbuduj linię RUN z listy poleceń (łączenie przez &&)
# 04 — zbuduj linię CMD w formie exec (json.dumps)
# 05 — złóż pełny Dockerfile z części (funkcje 01-04)
# 06 — zbuduj polecenie docker build (flaga -t, kontekst domyślny)
# 07 — sparsuj mapowanie portów "host:kontener" na krotkę (kontrakt None)
# 08 — zbuduj polecenie docker run z walidacją mapowania (funkcja 07)
# 09 — zbuduj słownik usługi compose (klucze ports/volumes warunkowo)
# 10 — złóż pełną konfigurację compose z usług (kontrakt None)
# 11 — zazębienie: Dockerfile dla aplikacji API z tematu 11 (funkcja 05)
# 12 — zazębienie: flagi Chrome dla kontenera (Selenium z tematu 17)
# 13 — zazębienie: compose dla scrapera z tematu 12 (funkcje 09-10)

import json


def zadanie_01_linia_from(obraz: str, tag: str) -> str:
    """Buduje instrukcję FROM dla podanego obrazu bazowego i taga.

    Args:
        obraz: nazwa obrazu bazowego, np. "python".
        tag: wersja obrazu, np. "3.12-slim".

    Returns:
        str: linia w formacie "FROM obraz:tag",
            np. "FROM python:3.12-slim".
    """
    # TODO: zwróć f-string sklejający "FROM ", obraz, dwukropek i tag
    pass


def zadanie_02_linia_copy(zrodlo: str, cel: str) -> str:
    """Buduje instrukcję COPY kopiującą plik do obrazu.

    Args:
        zrodlo: ścieżka pliku na komputerze, np. "requirements.txt".
        cel: miejsce docelowe w obrazie, np. ".".

    Returns:
        str: linia w formacie "COPY zrodlo cel",
            np. "COPY requirements.txt .".
    """
    # TODO: zwróć f-string ze słowem COPY, źródłem i celem
    #   rozdzielonymi pojedynczymi spacjami
    pass


def zadanie_03_linia_run(polecenia: list) -> str | None:
    """Buduje instrukcję RUN łączącą polecenia operatorem &&.

    Args:
        polecenia: lista poleceń terminala,
            np. ["pip install -r requirements.txt", "pip list"].

    Returns:
        str | None: linia "RUN polecenie1 && polecenie2 && ...";
            None, gdy lista poleceń jest pusta.
    """
    # TODO: jeśli lista jest pusta (if not polecenia:) — zwróć None
    # TODO: sklej polecenia przez " && ".join(polecenia)
    # TODO: zwróć "RUN " + sklejone polecenia
    pass


def zadanie_04_linia_cmd(czesci: list) -> str | None:
    """Buduje instrukcję CMD w formie exec (lista JSON).

    Args:
        czesci: kawałki polecenia startowego, np. ["python", "app.py"].

    Returns:
        str | None: linia w formacie 'CMD ["python", "app.py"]';
            None, gdy lista części jest pusta.
    """
    # TODO: jeśli lista jest pusta — zwróć None
    # TODO: zamień listę na napis JSON przez json.dumps(czesci)
    # TODO: zwróć "CMD " + wynik json.dumps
    pass


def zadanie_05_zbuduj_dockerfile(
    obraz: str,
    tag: str,
    kopiowania: list,
    polecenia_run: list,
    cmd: list,
) -> str:
    """Składa pełną treść Dockerfile z pojedynczych instrukcji.

    Args:
        obraz: nazwa obrazu bazowego dla FROM.
        tag: tag obrazu bazowego dla FROM.
        kopiowania: lista par [zrodlo, cel] dla instrukcji COPY,
            np. [["requirements.txt", "."], ["app.py", "."]].
        polecenia_run: lista poleceń dla jednej instrukcji RUN;
            pusta lista oznacza brak linii RUN.
        cmd: kawałki polecenia startowego dla CMD.

    Returns:
        str: treść Dockerfile — linie FROM, COPY (po jednej na parę),
            RUN (o ile są polecenia) i CMD, sklejone znakiem "\\n".
    """
    # TODO: zacznij od listy linii z wynikiem zadanie_01_linia_from
    # TODO: w pętli po kopiowania dodawaj wyniki zadanie_02_linia_copy
    #   (para to lista dwuelementowa: para[0] = źródło, para[1] = cel)
    # TODO: zbuduj linię RUN przez zadanie_03_linia_run i dodaj ją
    #   TYLKO gdy wynik nie jest None (is not None)
    # TODO: dodaj linię CMD przez zadanie_04_linia_cmd
    # TODO: zwróć "\n".join(linie)
    pass


def zadanie_06_polecenie_build(nazwa: str, tag: str, kontekst: str = ".") -> str:
    """Buduje polecenie docker build z nazwą obrazu i kontekstem.

    Args:
        nazwa: nazwa budowanego obrazu, np. "moja-apka".
        tag: tag budowanego obrazu, np. "1.0".
        kontekst: folder budowania; domyślnie "." (folder bieżący).

    Returns:
        str: polecenie w formacie "docker build -t nazwa:tag kontekst",
            np. "docker build -t moja-apka:1.0 .".
    """
    # TODO: zwróć f-string ze wzorem: docker build -t <nazwa>:<tag> <kontekst>
    pass


def zadanie_07_parsuj_porty(mapowanie: str) -> tuple | None:
    """Parsuje mapowanie portów "host:kontener" na krotkę liczb.

    Args:
        mapowanie: napis w formacie "8000:80".

    Returns:
        tuple | None: krotka (port_hosta, port_kontenera) jako liczby
            int, np. (8000, 80); None, gdy mapowanie nie ma dokładnie
            dwóch części albo któraś część nie jest liczbą.
    """
    # TODO: potnij mapowanie przez mapowanie.split(":")
    # TODO: jeśli liczba kawałków != 2 — zwróć None
    # TODO: jeśli któryś kawałek nie przechodzi .isdigit() — zwróć None
    # TODO: zwróć krotkę (int(pierwszy), int(drugi))
    pass


def zadanie_08_polecenie_run(obraz: str, nazwa: str, mapowanie: str) -> str | None:
    """Buduje polecenie docker run z nazwą, portami i obrazem.

    Args:
        obraz: obraz do uruchomienia, np. "moja-apka:1.0".
        nazwa: nazwa kontenera dla flagi --name.
        mapowanie: mapowanie portów w formacie "8000:80".

    Returns:
        str | None: polecenie w formacie
            "docker run -d --name nazwa -p mapowanie obraz";
            None, gdy mapowanie jest niepoprawne.
    """
    # TODO: sprawdź mapowanie przez zadanie_07_parsuj_porty;
    #   gdy wynik is None — zwróć None
    # TODO: zwróć f-string ze wzorem:
    #   docker run -d --name <nazwa> -p <mapowanie> <obraz>
    pass


def zadanie_09_usluga_compose(obraz: str, porty: list, wolumeny: list) -> dict:
    """Buduje słownik konfiguracji jednej usługi docker-compose.

    Args:
        obraz: obraz usługi, np. "moja-apka:1.0".
        porty: lista mapowań portów, np. ["8000:80"]; może być pusta.
        wolumeny: lista wolumenów, np. ["./dane:/app/dane"];
            może być pusta.

    Returns:
        dict: słownik z kluczem "image" zawsze oraz kluczami "ports"
            i "volumes" TYLKO wtedy, gdy odpowiednia lista nie jest
            pusta.
    """
    # TODO: zacznij od słownika {"image": obraz}
    # TODO: jeśli porty (if porty:) — dodaj klucz "ports" z listą porty
    # TODO: jeśli wolumeny — dodaj klucz "volumes" z listą wolumeny
    # TODO: zwróć słownik
    pass


def zadanie_10_zbuduj_compose(uslugi: dict) -> dict | None:
    """Składa pełną konfigurację docker-compose z usług.

    Args:
        uslugi: słownik nazwa_uslugi -> konfiguracja usługi
            (jak z zadania 09).

    Returns:
        dict | None: słownik {"services": uslugi}; None, gdy słownik
            usług jest pusty (compose bez usług nie ma sensu).
    """
    # TODO: jeśli słownik uslugi jest pusty (if not uslugi:) — zwróć None
    # TODO: zwróć słownik z jednym kluczem "services" i wartością uslugi
    pass


def zadanie_11_dockerfile_dla_api(plik_aplikacji: str) -> str:
    """Buduje Dockerfile dla aplikacji API z tematu 11 (requests).

    Args:
        plik_aplikacji: nazwa pliku z kodem aplikacji, np. "app.py".

    Returns:
        str: pełny Dockerfile: FROM python:3.12-slim, COPY
            requirements.txt do ".", RUN pip install -r
            requirements.txt, COPY pliku aplikacji do ".",
            CMD ["python", plik_aplikacji].
    """
    # TODO: zwróć wynik zadanie_05_zbuduj_dockerfile z argumentami:
    #   obraz "python", tag "3.12-slim",
    #   kopiowania: [["requirements.txt", "."], [plik_aplikacji, "."]],
    #   polecenia_run: ["pip install -r requirements.txt"],
    #   cmd: ["python", plik_aplikacji]
    pass


def zadanie_12_flagi_chrome_dla_kontenera(headless: bool) -> list:
    """Buduje listę flag Chrome potrzebnych w kontenerze (CI).

    Args:
        headless: True, gdy przeglądarka ma działać bez okna.

    Returns:
        list: zawsze flagi "--no-sandbox" i "--disable-gpu"
            (w tej kolejności); gdy headless is True — dodatkowo
            "--headless=new" na końcu.
    """
    # TODO: zbuduj listę z dwiema obowiązkowymi flagami
    # TODO: jeśli headless is True — dopisz "--headless=new"
    #   metodą .append()
    # TODO: zwróć listę
    pass


def zadanie_13_compose_dla_scrapera(obraz: str, folder_wynikow: str) -> dict:
    """Buduje konfigurację compose dla scrapera z tematu 12.

    Args:
        obraz: obraz scrapera, np. "moj-scraper:1.0".
        folder_wynikow: nazwa lokalnego folderu na wyniki CSV,
            np. "wyniki".

    Returns:
        dict: pełna konfiguracja compose z jedną usługą "scraper":
            obraz oraz wolumen "./<folder_wynikow>:/app/wyniki";
            bez mapowania portów (scraper ich nie potrzebuje).
    """
    # TODO: zbuduj napis wolumenu f-stringiem: ./<folder_wynikow>:/app/wyniki
    # TODO: zbuduj usługę przez zadanie_09_usluga_compose
    #   (porty: pusta lista, wolumeny: lista z jednym napisem)
    # TODO: zwróć wynik zadanie_10_zbuduj_compose ze słownikiem
    #   {"scraper": usluga}
    pass
