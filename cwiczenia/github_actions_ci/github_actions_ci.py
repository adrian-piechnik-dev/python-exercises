# Zadania — github_actions_ci
#
# Spis zadan:
# zadanie_01 — zbuduj slownik wyzwalacza push na wskazana galaz
# zadanie_02 — zbuduj krok typu run (nazwa + polecenie terminalowe)
# zadanie_03 — zbuduj krok typu uses (nazwa + gotowa akcja z wersja)
# zadanie_04 — zbuduj krok setup-python z parametrem with/python-version
# zadanie_05 — zbuduj job (runs-on + lista krokow)
# zadanie_06 — zloz caly workflow (name + on + jobs)
# zadanie_07 — zamien slownik workflow na tekst YAML
# zadanie_08 — zapisz workflow do .github/workflows/ w podanym folderze
# zadanie_09 — wczytaj plik YAML do slownika (None gdy pliku brak)
# zadanie_10 — wyciagnij nazwy krokow joba (None gdy job nie istnieje)
# zadanie_11 — zbuduj markdown badge'a CI dla repo
# zadanie_12 — gotowy workflow: pytest na testach ukonczonego tematu
# zadanie_13 — wariant z tematu docker: job pytest w kontenerze

from pathlib import Path

import yaml


def zadanie_01_zbuduj_trigger_push(galaz: str) -> dict:
    """Buduje slownik wyzwalacza: push na wskazana galaz.

    Args:
        galaz: nazwa galezi, np. "main".

    Returns:
        dict: {"push": {"branches": [galaz]}}.
    """
    # TODO: zwroc slownik z kluczem "push", ktorego wartoscia jest
    #       slownik {"branches": lista z jedna galezia}
    pass


def zadanie_02_zbuduj_krok_run(nazwa: str, polecenie: str) -> dict:
    """Buduje krok workflow wykonujacy polecenie terminalowe.

    Args:
        nazwa: opisowy podpis kroku (klucz "name").
        polecenie: polecenie do wykonania (klucz "run").

    Returns:
        dict: {"name": nazwa, "run": polecenie}.
    """
    # TODO: zwroc slownik z dwoma kluczami: "name" i "run"
    pass


def zadanie_03_zbuduj_krok_uses(nazwa: str, akcja: str) -> dict:
    """Buduje krok workflow uzywajacy gotowej akcji.

    Args:
        nazwa: opisowy podpis kroku (klucz "name").
        akcja: akcja w formacie autor/nazwa@wersja,
            np. "actions/checkout@v4".

    Returns:
        dict: {"name": nazwa, "uses": akcja}.
    """
    # TODO: zwroc slownik z dwoma kluczami: "name" i "uses"
    pass


def zadanie_04_zbuduj_krok_setup_python(wersja: str) -> dict:
    """Buduje krok instalujacy Pythona w podanej wersji.

    Args:
        wersja: wersja Pythona jako tekst, np. "3.13".

    Returns:
        dict: krok z kluczami "name" ("Ustaw Pythona"),
            "uses" ("actions/setup-python@v5")
            i "with" ({"python-version": wersja}).
    """
    # TODO: zwroc slownik z trzema kluczami: "name", "uses" i "with";
    #       wartoscia "with" jest slownik {"python-version": wersja}
    pass


def zadanie_05_zbuduj_job(kroki: list[dict]) -> dict:
    """Buduje job wykonywany na ubuntu-latest z podana lista krokow.

    Args:
        kroki: lista slownikow-krokow (z zadan 02-04).

    Returns:
        dict: {"runs-on": "ubuntu-latest", "steps": kroki}.
    """
    # TODO: zwroc slownik z kluczami "runs-on" (zawsze "ubuntu-latest")
    #       i "steps" (przekazana lista krokow)
    pass


def zadanie_06_zbuduj_workflow(nazwa: str, trigger: dict, joby: dict) -> dict:
    """Sklada kompletny workflow z nazwy, wyzwalacza i slownika jobow.

    Args:
        nazwa: nazwa workflow (klucz "name"), np. "CI".
        trigger: slownik wyzwalacza (z zadania 01) — klucz "on".
        joby: slownik jobow, np. {"testy": job_z_zadania_05}.

    Returns:
        dict: {"name": nazwa, "on": trigger, "jobs": joby}.
    """
    # TODO: zwroc slownik z trzema kluczami w kolejnosci:
    #       "name", "on", "jobs"
    pass


def zadanie_07_workflow_do_yaml(workflow: dict) -> str:
    """Zamienia slownik workflow na tekst w formacie YAML.

    Args:
        workflow: slownik workflow (z zadania 06).

    Returns:
        str: tekst YAML z zachowana kolejnoscia kluczy.
    """
    # TODO: uzyj yaml.safe_dump z sort_keys=False i allow_unicode=True,
    #       zwroc wynik
    pass


def zadanie_08_zapisz_workflow(
    folder_repo: str, nazwa_pliku: str, workflow: dict
) -> bool:
    """Zapisuje workflow jako plik YAML w .github/workflows/ repozytorium.

    Args:
        folder_repo: sciezka do glownego folderu repozytorium.
        nazwa_pliku: nazwa pliku workflow, np. "ci.yml".
        workflow: slownik workflow do zapisania.

    Returns:
        bool: True po pomyslnym zapisie pliku.
    """
    # TODO: zbuduj sciezke Path(folder_repo) / ".github" / "workflows"
    # TODO: utworz foldery przez mkdir(parents=True, exist_ok=True)
    # TODO: zamien workflow na tekst YAML (uzyj zadanie_07_workflow_do_yaml)
    # TODO: zapisz tekst do pliku (sciezka / nazwa_pliku) przez
    #       write_text(..., encoding="utf-8")
    # TODO: zwroc True
    pass


def zadanie_09_wczytaj_workflow(sciezka: str) -> dict | None:
    """Wczytuje plik YAML do slownika; brak pliku sygnalizuje przez None.

    Args:
        sciezka: sciezka do pliku .yml.

    Returns:
        dict | None: slownik workflow albo None, gdy plik nie istnieje.
    """
    # TODO: sprawdz przez Path(...).exists(), czy plik istnieje;
    #       jesli nie — zwroc None
    # TODO: odczytaj tekst przez read_text(encoding="utf-8")
    # TODO: zwroc wynik yaml.safe_load na tym tekscie
    pass


def zadanie_10_wyciagnij_nazwy_krokow(
    workflow: dict, nazwa_joba: str
) -> list[str] | None:
    """Zwraca liste podpisow (name) krokow wskazanego joba.

    Args:
        workflow: slownik workflow (z kluczami "jobs" itd.).
        nazwa_joba: klucz joba w slowniku "jobs", np. "testy".

    Returns:
        list[str] | None: lista wartosci "name" kolejnych krokow joba
            albo None, gdy joba o tej nazwie nie ma.
    """
    # TODO: pobierz job przez workflow["jobs"].get(nazwa_joba)
    # TODO: jesli job is None — zwroc None
    # TODO: zwroc liste wartosci krok["name"] dla kazdego kroku
    #       z job["steps"] (petla albo list comprehension)
    pass


def zadanie_11_zbuduj_badge(uzytkownik: str, repo: str, plik_workflow: str) -> str:
    """Buduje markdown badge'a pokazujacego status CI repozytorium.

    Args:
        uzytkownik: nazwa uzytkownika GitHub, np. "looki".
        repo: nazwa repozytorium, np. "python-exercises".
        plik_workflow: nazwa pliku workflow, np. "ci.yml".

    Returns:
        str: markdown w formacie
            ![CI](https://github.com/UZYTKOWNIK/REPO/actions/workflows/PLIK/badge.svg).
    """
    # TODO: zloz f-stringiem adres
    #       https://github.com/{uzytkownik}/{repo}/actions/workflows/{plik_workflow}/badge.svg
    # TODO: opakuj go w skladnie obrazka markdown: ![CI](adres)
    pass


def zadanie_12_workflow_dla_pytest(sciezka_testow: str) -> dict:
    """Sklada gotowy workflow CI uruchamiajacy pytest na wskazanych testach.

    Args:
        sciezka_testow: sciezka do testow, np. "cwiczenia/openpyxl_formatowanie".

    Returns:
        dict: workflow o nazwie "CI", wyzwalany pushem na "main",
            z jednym jobem "testy" o czterech krokach:
            1. "Pobierz kod" (uses actions/checkout@v4),
            2. "Ustaw Pythona" (setup-python, wersja "3.13"),
            3. "Zainstaluj zaleznosci" (run "pip install pytest"),
            4. "Uruchom testy" (run "pytest <sciezka_testow> -v").
    """
    # TODO: zbuduj cztery kroki funkcjami z zadan 02-04
    #       (checkout i "Pobierz kod" przez zadanie_03, setup-python przez
    #       zadanie_04, dwa kroki run przez zadanie_02)
    # TODO: zloz job funkcja zadanie_05 i wyzwalacz funkcja zadanie_01
    # TODO: zwroc calosc przez zadanie_06 (nazwa "CI",
    #       joby = {"testy": job})
    pass


def zadanie_13_workflow_pytest_w_kontenerze(
    sciezka_testow: str, obraz: str
) -> dict:
    """Sklada workflow CI z jobem pytest wykonywanym w kontenerze Dockera.

    Args:
        sciezka_testow: sciezka do testow, np. "cwiczenia/slowniki".
        obraz: obraz Dockera z Pythonem, np. "python:3.13-slim".

    Returns:
        dict: workflow o nazwie "CI", wyzwalany pushem na "main",
            z jobem "testy" majacym dodatkowy klucz "container" = obraz
            i TRZY kroki (bez setup-python — obraz ma juz Pythona):
            1. "Pobierz kod" (uses actions/checkout@v4),
            2. "Zainstaluj zaleznosci" (run "pip install pytest"),
            3. "Uruchom testy" (run "pytest <sciezka_testow> -v").
    """
    # TODO: zbuduj trzy kroki funkcjami z zadan 02-03 (BEZ setup-python)
    # TODO: zbuduj job funkcja zadanie_05, a potem DOPISZ do niego
    #       klucz "container" z wartoscia obraz (job["container"] = obraz)
    # TODO: zwroc calosc przez zadanie_06 (nazwa "CI", trigger na "main",
    #       joby = {"testy": job})
    pass
