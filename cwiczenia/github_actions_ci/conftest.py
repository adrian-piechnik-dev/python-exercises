# TODO: zaimportuj sys i os (stdlib), a nizej pytest (third-party)
#       — pamietaj o kolejnosci grup importow i pustej linii miedzy nimi

# TODO: dodaj sys.path.insert(0, ...) wskazujacy na folder tego tematu,
#       zeby test_github_actions_ci.py widzial modul github_actions_ci
#       (wzorzec: os.path.dirname(os.path.abspath(__file__)))


# TODO: udekoruj fixture dekoratorem @pytest.fixture
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
    # TODO: zbuduj i zwroc slownik doslownie wedlug opisu z Returns —
    #       recznie, bez funkcji z github_actions_ci.py (fixture nie moze
    #       zalezec od kodu, ktory dopiero testujemy)
    pass


# TODO: udekoruj fixture dekoratorem @pytest.fixture
def plik_workflow(tmp_path, przykladowy_workflow: dict):
    """Plik ci.yml zapisany w folderze tymczasowym — do testow zadania 09.

    Args:
        tmp_path: wstrzykiwany przez pytest katalog tymczasowy.
        przykladowy_workflow: slownik workflow z fixture powyzej.

    Returns:
        Path: sciezka do zapisanego pliku ci.yml.
    """
    # TODO: zaimportuj yaml na gorze pliku (third-party)
    # TODO: zamien przykladowy_workflow na tekst przez yaml.safe_dump
    #       (sort_keys=False, allow_unicode=True)
    # TODO: zapisz tekst do tmp_path / "ci.yml" przez
    #       write_text(..., encoding="utf-8")
    # TODO: zwroc sciezke do pliku
    # TODO: uzupelnij tez type hinty parametru tmp_path i zwracanej
    #       wartosci (Path z pathlib — import na gorze pliku)
    pass
