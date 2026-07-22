import os
import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture
def przykladowy_workflow() -> dict:
    """Gotowy slownik workflow do testow zadan 09-10.

    Args:
        Brak.

    Returns:
        dict: workflow o nazwie "CI", wyzwalany pushem na "main",
            z jednym jobem "testy" (runs-on ubuntu-latest) o dwoch
            krokach: "Pobierz kod" (uses actions/checkout@v4)
            i "Uruchom testy" (run "pytest -v").
    """
    return {
        "name": "CI",
        "on": {
            "push": {
                "branches": ["main"]
            }
        },
        "jobs": {
            "testy": {
                "runs-on": "ubuntu-latest",
                "steps": [
                    {"name": "Pobierz kod", "uses": "actions/checkout@v4"},
                    {"name": "Uruchom testy", "run": "pytest -v"}
                ]
            }
        }
    }


@pytest.fixture
def plik_workflow(tmp_path: Path, przykladowy_workflow: dict) -> Path:
    """Plik ci.yml zapisany w folderze tymczasowym — do testow zadania 09.

    Args:
        tmp_path: wstrzykiwany przez pytest katalog tymczasowy.
        przykladowy_workflow: slownik workflow z fixture powyzej.

    Returns:
        Path: sciezka do zapisanego pliku ci.yml.
    """
    workflow = przykladowy_workflow
    tekst = yaml.safe_dump(workflow, sort_keys=False, allow_unicode=True)
    plik = tmp_path / "ci.yml"
    plik.write_text(tekst, encoding="utf-8")
    return plik

