from pathlib import Path

import yaml


def zadanie_01_zbuduj_trigger_push(galaz: str) -> dict:
    """Buduje slownik wyzwalacza: push na wskazana galaz.

    Args:
        galaz: nazwa galezi, np. "main".

    Returns:
        dict: {"push": {"branches": [galaz]}}.
    """
    return {"push": {"branches": [galaz]}}


def zadanie_02_zbuduj_krok_run(nazwa: str, polecenie: str) -> dict:
    """Buduje krok workflow wykonujacy polecenie terminalowe.

    Args:
        nazwa: opisowy podpis kroku (klucz "name").
        polecenie: polecenie do wykonania (klucz "run").

    Returns:
        dict: {"name": nazwa, "run": polecenie}.
    """
    return {"name": nazwa, "run": polecenie}


def zadanie_03_zbuduj_krok_uses(nazwa: str, akcja: str) -> dict:
    """Buduje krok workflow uzywajacy gotowej akcji.

    Args:
        nazwa: opisowy podpis kroku (klucz "name").
        akcja: akcja w formacie autor/nazwa@wersja,
            np. "actions/checkout@v4".

    Returns:
        dict: {"name": nazwa, "uses": akcja}.
    """
    return {"name": nazwa, "uses": akcja}


def zadanie_04_zbuduj_krok_setup_python(wersja: str) -> dict:
    """Buduje krok instalujacy Pythona w podanej wersji.

    Args:
        wersja: wersja Pythona jako tekst, np. "3.13".

    Returns:
        dict: krok z kluczami "name" ("Ustaw Pythona"),
            "uses" ("actions/setup-python@v5")
            i "with" ({"python-version": wersja}).
    """
    return {
        "name": "Ustaw Pythona",
        "uses": "actions/setup-python@v5",
        "with": {"python-version": wersja}
    }


def zadanie_05_zbuduj_job(kroki: list[dict]) -> dict:
    """Buduje job wykonywany na ubuntu-latest z podana lista krokow.

    Args:
        kroki: lista slownikow-krokow (z zadan 02-04).

    Returns:
        dict: {"runs-on": "ubuntu-latest", "steps": kroki}.
    """
    return {"runs-on": "ubuntu-latest", "steps": kroki}


def zadanie_06_zbuduj_workflow(nazwa: str, trigger: dict, joby: dict) -> dict:
    """Sklada kompletny workflow z nazwy, wyzwalacza i slownika jobow.

    Args:
        nazwa: nazwa workflow (klucz "name"), np. "CI".
        trigger: slownik wyzwalacza (z zadania 01) — klucz "on".
        joby: slownik jobow, np. {"testy": job_z_zadania_05}.

    Returns:
        dict: {"name": nazwa, "on": trigger, "jobs": joby}.
    """
    return {"name": nazwa, "on": trigger, "jobs": joby}


def zadanie_07_workflow_do_yaml(workflow: dict) -> str:
    """Zamienia slownik workflow na tekst w formacie YAML.

    Args:
        workflow: slownik workflow (z zadania 06).

    Returns:
        str: tekst YAML z zachowana kolejnoscia kluczy.
    """
    return yaml.safe_dump(workflow, sort_keys=False, allow_unicode=True)


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
    sciezka = Path(folder_repo) / ".github" / "workflows"
    sciezka.mkdir(parents=True, exist_ok=True)
    plik = sciezka / nazwa_pliku
    tekst = zadanie_07_workflow_do_yaml(workflow)
    plik.write_text(tekst, encoding="utf-8")
    return True


def zadanie_09_wczytaj_workflow(sciezka: str) -> dict | None:
    """Wczytuje plik YAML do slownika; brak pliku sygnalizuje przez None.

    Args:
        sciezka: sciezka do pliku .yml.

    Returns:
        dict | None: slownik workflow albo None, gdy plik nie istnieje.
    """
    if not Path(sciezka).exists():
        return None
    tekst = Path(sciezka).read_text(encoding="utf-8")
    return yaml.safe_load(tekst)


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
    job = workflow["jobs"].get(nazwa_joba)
    if job is None:
        return None
    return [krok["name"] for krok in job["steps"]]


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
    adres = f"https://github.com/{uzytkownik}/{repo}/actions/workflows/{plik_workflow}/badge.svg"
    return f"![CI]({adres})"


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
    krok_1 = zadanie_03_zbuduj_krok_uses("Pobierz kod", "actions/checkout@v4")
    krok_2 = zadanie_04_zbuduj_krok_setup_python("3.13")
    krok_3 = zadanie_02_zbuduj_krok_run(
        "Zainstaluj zaleznosci",
        "pip install pytest"
    )
    krok_4 = zadanie_02_zbuduj_krok_run(
        "Uruchom testy",
        f"pytest {sciezka_testow} -v"
    )
    kroki = [krok_1, krok_2, krok_3, krok_4]
    joby = {"testy": zadanie_05_zbuduj_job(kroki)}
    trigger = zadanie_01_zbuduj_trigger_push("main")
    return zadanie_06_zbuduj_workflow("CI", trigger, joby)


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
    krok_1 = zadanie_03_zbuduj_krok_uses("Pobierz kod", "actions/checkout@v4")
    krok_2 = zadanie_02_zbuduj_krok_run(
        "Zainstaluj zaleznosci",
        "pip install pytest"
    )
    krok_3 = zadanie_02_zbuduj_krok_run(
        "Uruchom testy",
        f"pytest {sciezka_testow} -v"
    )
    kroki = [krok_1, krok_2, krok_3]
    job = zadanie_05_zbuduj_job(kroki)
    job["container"] = obraz
    trigger = zadanie_01_zbuduj_trigger_push("main")
    return zadanie_06_zbuduj_workflow("CI", trigger, joby={"testy": job})
