from pathlib import Path

from github_actions_ci import (
    zadanie_01_zbuduj_trigger_push,
    zadanie_02_zbuduj_krok_run,
    zadanie_03_zbuduj_krok_uses,
    zadanie_04_zbuduj_krok_setup_python,
    zadanie_05_zbuduj_job,
    zadanie_06_zbuduj_workflow,
    zadanie_07_workflow_do_yaml,
    zadanie_08_zapisz_workflow,
    zadanie_09_wczytaj_workflow,
    zadanie_10_wyciagnij_nazwy_krokow,
    zadanie_11_zbuduj_badge,
    zadanie_12_workflow_dla_pytest,
    zadanie_13_workflow_pytest_w_kontenerze,
)


# --- zadanie_01 ---

def test_zadanie_01_buduje_trigger_na_main() -> None:
    """Co testuje: czy wyzwalacz dla galezi "main" ma pelna strukture push/branches.
    Co udaje: nic — czysta funkcja na slownikach.
    Co sprawdzam: wynik == {"push": {"branches": ["main"]}}.
    """
    wynik = zadanie_01_zbuduj_trigger_push("main")
    assert wynik == {"push": {"branches": ["main"]}}


def test_zadanie_01_galaz_trafia_do_listy() -> None:
    """Co testuje: czy inna galaz ("develop") laduje w liscie branches.
    Co udaje: nic — czysta funkcja na slownikach.
    Co sprawdzam: wynik["push"]["branches"] == ["develop"].
    """
    wynik = zadanie_01_zbuduj_trigger_push("develop")
    assert wynik["push"]["branches"] == ["develop"]


# --- zadanie_02 ---

def test_zadanie_02_buduje_krok_run() -> None:
    """Co testuje: czy krok run ma poprawne klucze name i run.
    Co udaje: nic — czysta funkcja na slownikach.
    Co sprawdzam: wynik == {"name": "Uruchom testy", "run": "pytest -v"}.
    """
    wynik = zadanie_02_zbuduj_krok_run("Uruchom testy", "pytest -v")
    assert wynik == {"name": "Uruchom testy", "run": "pytest -v"}


def test_zadanie_02_krok_run_nie_ma_klucza_uses() -> None:
    """Co testuje: czy krok run NIE zawiera klucza uses (krok robi jedna rzecz).
    Co udaje: nic — czysta funkcja na slownikach.
    Co sprawdzam: "uses" not in wynik.
    """
    wynik = zadanie_02_zbuduj_krok_run("Uruchom testy", "pytest -v")
    assert "uses" not in wynik


# --- zadanie_03 ---

def test_zadanie_03_buduje_krok_checkout() -> None:
    """Co testuje: czy krok uses dla checkout ma poprawne klucze.
    Co udaje: nic — czysta funkcja na slownikach.
    Co sprawdzam: wynik == {"name": "Pobierz kod", "uses": "actions/checkout@v4"}.
    """
    wynik = zadanie_03_zbuduj_krok_uses("Pobierz kod", "actions/checkout@v4")
    assert wynik == {"name": "Pobierz kod", "uses": "actions/checkout@v4"}


def test_zadanie_03_krok_uses_nie_ma_klucza_run() -> None:
    """Co testuje: czy krok uses NIE zawiera klucza run.
    Co udaje: nic — czysta funkcja na slownikach.
    Co sprawdzam: "run" not in wynik.
    """
    wynik = zadanie_03_zbuduj_krok_uses("Pobierz kod", "actions/checkout@v4")
    assert "run" not in wynik


# --- zadanie_04 ---

def test_zadanie_04_setup_python_ma_wersje_w_with() -> None:
    """Co testuje: czy wersja Pythona laduje w with/python-version jako tekst.
    Co udaje: nic — czysta funkcja na slownikach.
    Co sprawdzam: wynik["with"] == {"python-version": "3.13"}.
    """
    wynik = zadanie_04_zbuduj_krok_setup_python("3.13")
    assert wynik["with"] == {"python-version": "3.13"}


def test_zadanie_04_setup_python_uzywa_akcji_v5() -> None:
    """Co testuje: czy krok wskazuje akcje actions/setup-python@v5.
    Co udaje: nic — czysta funkcja na slownikach.
    Co sprawdzam: wynik["uses"] == "actions/setup-python@v5".
    """
    wynik = zadanie_04_zbuduj_krok_setup_python("3.13")
    assert wynik["uses"] == "actions/setup-python@v5"


# --- zadanie_05 ---

def test_zadanie_05_job_biegnie_na_ubuntu() -> None:
    """Co testuje: czy job dostaje runs-on ubuntu-latest.
    Co udaje: nic — czysta funkcja na slownikach.
    Co sprawdzam: wynik["runs-on"] == "ubuntu-latest".
    """
    kroki = [{"name": "Pobierz kod", "run": "echo"}]
    wynik = zadanie_05_zbuduj_job(kroki)
    assert wynik["runs-on"] == "ubuntu-latest"


def test_zadanie_05_kroki_trafiaja_do_steps() -> None:
    """Co testuje: czy przekazana lista krokow laduje bez zmian pod kluczem steps.
    Co udaje: nic — czysta funkcja na slownikach.
    Co sprawdzam: wynik["steps"] to dokladnie przekazana lista (dlugosc
    i zawartosc sie zgadzaja).
    """
    kroki = [{"name": "Pobierz kod", "run": "echo"}]
    wynik = zadanie_05_zbuduj_job(kroki)
    assert wynik["steps"] == kroki


# --- zadanie_06 ---

def test_zadanie_06_workflow_ma_trzy_klucze() -> None:
    """Co testuje: czy workflow sklada name, on i jobs w jeden slownik.
    Co udaje: nic — czysta funkcja na slownikach.
    Co sprawdzam: wynik["name"], wynik["on"] i wynik["jobs"] rowne wejsciom.
    """
    triger = {"push": {"branches": ["main"]}}
    joby = [{"name": "Pobierz kod", "run": "echo"}]
    wynik = zadanie_06_zbuduj_workflow("CI", triger, joby)
    assert wynik["name"] == "CI"
    assert wynik["on"] == triger
    assert wynik["jobs"] == joby


def test_zadanie_06_zachowuje_kolejnosc_kluczy() -> None:
    """Co testuje: czy klucze workflow ida w kolejnosci name, on, jobs.
    Co udaje: nic — czysta funkcja na slownikach.
    Co sprawdzam: list(wynik.keys()) == ["name", "on", "jobs"].
    """
    triger = {"push": {"branches": ["main"]}}
    joby = [{"name": "Pobierz kod", "run": "echo"}]
    wynik = zadanie_06_zbuduj_workflow("CI", triger, joby)
    assert list(wynik.keys()) == ["name", "on", "jobs"]


# --- zadanie_07 ---

def test_zadanie_07_yaml_zawiera_nazwe_workflow() -> None:
    """Co testuje: czy wynikowy tekst YAML zawiera linijke "name: CI".
    Co udaje: nic — konwersja slownika na tekst w pamieci.
    Co sprawdzam: "name: CI" in wynik.
    """
    workflow = {"name": "CI", "on": {"push": {"branches": ["main"]}}}
    wynik = zadanie_07_workflow_do_yaml(workflow)
    assert "name: CI" in wynik


def test_zadanie_07_yaml_nie_sortuje_kluczy() -> None:
    """Co testuje: czy name zostaje PRZED jobs (sort_keys=False dziala).
    Co udaje: nic — konwersja slownika na tekst w pamieci.
    Co sprawdzam: pozycja "name:" w tekscie < pozycja "jobs:" (str.index).
    """
    workflow = {
        "name": "CI", "on": {"push": {"branches": ["main"]}},
        "jobs": {"name": "Pobierz kod", "run": "echo"}
    }
    wynik = zadanie_07_workflow_do_yaml(workflow)
    assert wynik.index("name:") < wynik.index("jobs:")


# --- zadanie_08 ---

def test_zadanie_08_tworzy_plik_w_github_workflows(tmp_path: Path) -> None:
    """Co testuje: czy plik laduje w <repo>/.github/workflows/<nazwa>.
    Co udaje: prawdziwe repo — zastepuje je folderem tmp_path.
    Co sprawdzam: (tmp_path / ".github" / "workflows" / "ci.yml").exists() is True.
    """
    workflow = {
        "name": "CI", "on": {"push": {"branches": ["main"]}},
        "jobs": {"name": "Pobierz kod", "run": "echo"}
    }
    zadanie_08_zapisz_workflow(str(tmp_path), "ci.yml", workflow)
    assert (tmp_path / ".github" / "workflows" / "ci.yml").exists() is True


def test_zadanie_08_zwraca_true_i_zapisuje_yaml(tmp_path: Path) -> None:
    """Co testuje: czy funkcja zwraca True, a zapisany plik to poprawny YAML.
    Co udaje: prawdziwe repo — zastepuje je folderem tmp_path.
    Co sprawdzam: wynik is True; tekst pliku zawiera "name:".
    """
    workflow = {
        "name": "CI", "on": {"push": {"branches": ["main"]}},
        "jobs": {"name": "Pobierz kod", "run": "echo"}
    }
    wynik = zadanie_08_zapisz_workflow(str(tmp_path), "ci.yml", workflow)
    assert wynik is True
    sciezka = tmp_path / ".github" / "workflows" / "ci.yml"
    tekst = sciezka.read_text(encoding="utf-8")
    assert "name:" in tekst


# --- zadanie_09 ---

def test_zadanie_09_wczytuje_zapisany_workflow(plik_workflow: Path) -> None:
    """Co testuje: czy funkcja odtwarza slownik z pliku YAML.
    Co udaje: nic — uzywam fixture plik_workflow (prawdziwy plik w tmp_path).
    Co sprawdzam: wynik["name"] == "CI" i "testy" in wynik["jobs"].
    """
    wynik = zadanie_09_wczytaj_workflow(str(plik_workflow))
    assert wynik["name"] == "CI"
    assert "testy" in wynik["jobs"]


def test_zadanie_09_zwraca_none_gdy_pliku_brak(tmp_path: Path) -> None:
    """Co testuje: kontrakt None przy nieistniejacym pliku (zamiast wyjatku).
    Co udaje: nic — uzywam sciezki, ktora na pewno nie istnieje.
    Co sprawdzam: wynik is None.
    """
    sciezka = tmp_path / "nieistniejacy.yml"
    wynik = zadanie_09_wczytaj_workflow(str(sciezka))
    assert wynik is None


# --- zadanie_10 ---

def test_zadanie_10_zwraca_nazwy_krokow(przykladowy_workflow: dict) -> None:
    """Co testuje: czy funkcja wyciaga podpisy krokow joba "testy" po kolei.
    Co udaje: nic — uzywam fixture przykladowy_workflow.
    Co sprawdzam: wynik == ["Pobierz kod", "Uruchom testy"].
    """
    wynik = zadanie_10_wyciagnij_nazwy_krokow(przykladowy_workflow, "testy")
    assert wynik == ["Pobierz kod", "Uruchom testy"]


def test_zadanie_10_zwraca_none_gdy_joba_brak(przykladowy_workflow: dict) -> None:
    """Co testuje: kontrakt None dla nieistniejacej nazwy joba.
    Co udaje: nic — uzywam fixture przykladowy_workflow.
    Co sprawdzam: wynik is None.
    """
    wynik = zadanie_10_wyciagnij_nazwy_krokow(przykladowy_workflow, "deploy")
    assert wynik is None


# --- zadanie_11 ---

def test_zadanie_11_badge_ma_poprawny_adres() -> None:
    """Co testuje: czy badge sklada pelny markdown z adresem svg.
    Co udaje: nic — czysta funkcja na tekstach.
    Co sprawdzam: wynik ==
    "![CI](https://github.com/looki/python-exercises/actions/workflows/ci.yml/badge.svg)".
    """
    wynik = zadanie_11_zbuduj_badge("looki", "python-exercises", "ci.yml")
    assert wynik == "![CI](https://github.com/looki/python-exercises/actions/workflows/ci.yml/badge.svg)"


def test_zadanie_11_badge_zaczyna_sie_od_wykrzyknika() -> None:
    """Co testuje: czy wynik to obrazek markdown (prefiks "!["), nie zwykly link.
    Co udaje: nic — czysta funkcja na tekstach.
    Co sprawdzam: wynik.startswith("![") is True.
    """
    wynik = zadanie_11_zbuduj_badge("looki", "python-exercises", "ci.yml")
    assert wynik.startswith("![") is True


# --- zadanie_12 ---

def test_zadanie_12_workflow_ma_cztery_kroki_w_dobrej_kolejnosci() -> None:
    """Co testuje: czy job "testy" ma 4 kroki w kolejnosci: checkout,
    setup-python, instalacja, testy.
    Co udaje: nic — funkcja tylko sklada slownik.
    Co sprawdzam: lista name'ow krokow == ["Pobierz kod", "Ustaw Pythona",
    "Zainstaluj zaleznosci", "Uruchom testy"].
    """
    sciezka_testow = "cwiczenia/openpyxl_formatowanie"
    wynik = zadanie_12_workflow_dla_pytest(sciezka_testow)
    lista_krokow = [krok["name"] for krok in wynik["jobs"]["testy"]["steps"]]
    assert lista_krokow == [
        "Pobierz kod",
        "Ustaw Pythona",
        "Zainstaluj zaleznosci",
        "Uruchom testy"
    ]


def test_zadanie_12_ostatni_krok_odpala_pytest_na_sciezce() -> None:
    """Co testuje: czy przekazana sciezka testow trafia do polecenia pytest.
    Co udaje: nic — funkcja tylko sklada slownik.
    Co sprawdzam: "cwiczenia/slowniki" in ostatni_krok["run"]
    i wynik["on"] == {"push": {"branches": ["main"]}}.
    """
    sciezka_testow = "cwiczenia/slowniki"
    wynik = zadanie_12_workflow_dla_pytest(sciezka_testow)
    ostatni_krok = wynik["jobs"]["testy"]["steps"][-1]
    assert "cwiczenia/slowniki" in ostatni_krok["run"]


# --- zadanie_13 ---

def test_zadanie_13_job_ma_kontener_z_obrazem() -> None:
    """Co testuje: czy job dostaje klucz container z przekazanym obrazem.
    Co udaje: nic — funkcja tylko sklada slownik.
    Co sprawdzam: wynik["jobs"]["testy"]["container"] == "python:3.13-slim".
    """
    wynik = zadanie_13_workflow_pytest_w_kontenerze("cwiczenia/slowniki", "python:3.13-slim")
    assert wynik["jobs"]["testy"]["container"] == "python:3.13-slim"


def test_zadanie_13_brak_kroku_setup_python() -> None:
    """Co testuje: czy w wariancie kontenerowym sa 3 kroki i zaden nie
    uzywa setup-python (obraz ma juz Pythona).
    Co udaje: nic — funkcja tylko sklada slownik.
    Co sprawdzam: len(steps) == 3 i zaden krok nie ma "setup-python"
    w wartosci "uses".
    """
    wynik = zadanie_13_workflow_pytest_w_kontenerze("cwiczenia/slowniki", "python:3.13-slim")
    lista_krokow = [krok["name"] for krok in wynik["jobs"]["testy"]["steps"]]
    assert len(lista_krokow) == 3
    assert "Ustaw Pythona" not in lista_krokow
