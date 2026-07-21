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
    return f"FROM {obraz}:{tag}"


def zadanie_02_linia_copy(zrodlo: str, cel: str) -> str:
    """Buduje instrukcję COPY kopiującą plik do obrazu.

    Args:
        zrodlo: ścieżka pliku na komputerze, np. "requirements.txt".
        cel: miejsce docelowe w obrazie, np. ".".

    Returns:
        str: linia w formacie "COPY zrodlo cel",
            np. "COPY requirements.txt .".
    """
    return f"COPY {zrodlo} {cel}"


def zadanie_03_linia_run(polecenia: list) -> str | None:
    """Buduje instrukcję RUN łączącą polecenia operatorem &&.

    Args:
        polecenia: lista poleceń terminala,
            np. ["pip install -r requirements.txt", "pip list"].

    Returns:
        str | None: linia "RUN polecenie1 && polecenie2 && ...";
            None, gdy lista poleceń jest pusta.
    """
    if not polecenia:
        return None
    run = " && ".join(polecenia)
    return f"RUN {run}"


def zadanie_04_linia_cmd(czesci: list) -> str | None:
    """Buduje instrukcję CMD w formie exec (lista JSON).

    Args:
        czesci: kawałki polecenia startowego, np. ["python", "app.py"].

    Returns:
        str | None: linia w formacie 'CMD ["python", "app.py"]';
            None, gdy lista części jest pusta.
    """
    if not czesci:
        return None
    wynik = json.dumps(czesci)
    return f"CMD {wynik}"


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
    linie = [zadanie_01_linia_from(obraz, tag)]
    for para in kopiowania:
        zrodlo = para[0]
        cel = para[1]
        linie.append(zadanie_02_linia_copy(zrodlo, cel))
    linia_run = zadanie_03_linia_run(polecenia_run)
    if linia_run is not None:
        linie.append(linia_run)
    linia_cmd = zadanie_04_linia_cmd(cmd)
    if linia_cmd is not None:
        linie.append(linia_cmd)
    return "\n".join(linie)


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
    return f"docker build -t {nazwa}:{tag} {kontekst}"


def zadanie_07_parsuj_porty(mapowanie: str) -> tuple | None:
    """Parsuje mapowanie portów "host:kontener" na krotkę liczb.

    Args:
        mapowanie: napis w formacie "8000:80".

    Returns:
        tuple | None: krotka (port_hosta, port_kontenera) jako liczby
            int, np. (8000, 80); None, gdy mapowanie nie ma dokładnie
            dwóch części albo któraś część nie jest liczbą.
    """
    kawalki = mapowanie.split(":")
    if len(kawalki) != 2:
        return None
    if not kawalki[0].isdigit() or not kawalki[1].isdigit():
        return None
    return (int(kawalki[0]), int(kawalki[1]))


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
    wynik = zadanie_07_parsuj_porty(mapowanie)
    if wynik is None:
        return None
    return f"docker run -d --name {nazwa} -p {mapowanie} {obraz}"


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
    apka = {"image": obraz}
    if porty:
        apka["ports"] = porty
    if wolumeny:
        apka["volumes"] = wolumeny
    return apka


def zadanie_10_zbuduj_compose(uslugi: dict) -> dict | None:
    """Składa pełną konfigurację docker-compose z usług.

    Args:
        uslugi: słownik nazwa_uslugi -> konfiguracja usługi
            (jak z zadania 09).

    Returns:
        dict | None: słownik {"services": uslugi}; None, gdy słownik
            usług jest pusty (compose bez usług nie ma sensu).
    """
    if not uslugi:
        return None
    return {"services": uslugi}


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
    obraz = "python"
    tag = "3.12-slim"
    kopiowania = [["requirements.txt", "."], [plik_aplikacji, "."]]
    polecenia_run = ["pip install -r requirements.txt"]
    cmd = ["python", plik_aplikacji]
    return zadanie_05_zbuduj_dockerfile(obraz, tag, kopiowania, polecenia_run, cmd)


def zadanie_12_flagi_chrome_dla_kontenera(headless: bool) -> list:
    """Buduje listę flag Chrome potrzebnych w kontenerze (CI).

    Args:
        headless: True, gdy przeglądarka ma działać bez okna.

    Returns:
        list: zawsze flagi "--no-sandbox" i "--disable-gpu"
            (w tej kolejności); gdy headless is True — dodatkowo
            "--headless=new" na końcu.
    """
    flagi = ["--no-sandbox", "--disable-gpu"]
    if headless is True:
        flagi.append("--headless=new")
    return flagi


def zadanie_13_compose_dla_scrapera(obraz: str, folder_wynikow: str) -> dict | None:
    """Buduje konfigurację compose dla scrapera z tematu 12.

    Args:
        obraz: obraz scrapera, np. "moj-scraper:1.0".
        folder_wynikow: nazwa lokalnego folderu na wyniki CSV,
            np. "wyniki".

    Returns:
        dict | None: pełna konfiguracja compose z jedną usługą "scraper":
            obraz oraz wolumen "./<folder_wynikow>:/app/wyniki";
            bez mapowania portów (scraper ich nie potrzebuje).
    """
    wolumen = [f"./{folder_wynikow}:/app/wyniki"]
    usluga = zadanie_09_usluga_compose(obraz, [], wolumen)
    return zadanie_10_zbuduj_compose({"scraper": usluga})
