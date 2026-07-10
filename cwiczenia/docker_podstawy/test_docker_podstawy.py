from docker_podstawy import (
    zadanie_01_linia_from,
    zadanie_02_linia_copy,
    zadanie_03_linia_run,
    zadanie_04_linia_cmd,
    zadanie_05_zbuduj_dockerfile,
    zadanie_06_polecenie_build,
    zadanie_07_parsuj_porty,
    zadanie_08_polecenie_run,
    zadanie_09_usluga_compose,
    zadanie_10_zbuduj_compose,
    zadanie_11_dockerfile_dla_api,
    zadanie_12_flagi_chrome_dla_kontenera,
    zadanie_13_compose_dla_scrapera,
)


# --- zadanie_01 ---


def test_zadanie_01_buduje_linie_from_dla_pythona() -> None:
    """Co testuję: budowanie linii FROM ze wzoru nazwa:tag.
    Co udaję: nic — funkcja tylko skleja napis.
    Co sprawdzam: wynik to dokładnie "FROM python:3.12-slim".
    """
    # TODO: przygotuj obraz "python" i tag "3.12-slim"
    # TODO: wywołaj zadanie_01_linia_from
    # TODO: sprawdź, że wynik == "FROM python:3.12-slim"
    pass


def test_zadanie_01_dziala_dla_innego_obrazu() -> None:
    """Co testuję: że obraz i tag nie są zahardkodowane w funkcji.
    Co udaję: nic — czyste dane.
    Co sprawdzam: dla obrazu "nginx" i taga "1.25" wynik to
    "FROM nginx:1.25".
    """
    # TODO: przygotuj obraz "nginx" i tag "1.25"
    # TODO: wywołaj zadanie_01_linia_from
    # TODO: sprawdź, że wynik == "FROM nginx:1.25"
    pass


# --- zadanie_02 ---


def test_zadanie_02_buduje_linie_copy_do_kropki() -> None:
    """Co testuję: budowanie linii COPY ze źródłem i celem.
    Co udaję: nic — funkcja tylko skleja napis.
    Co sprawdzam: wynik to dokładnie "COPY requirements.txt .".
    """
    # TODO: przygotuj źródło "requirements.txt" i cel "."
    # TODO: wywołaj zadanie_02_linia_copy
    # TODO: sprawdź, że wynik == "COPY requirements.txt ."
    pass


def test_zadanie_02_buduje_linie_copy_do_podfolderu() -> None:
    """Co testuję: że cel inny niż kropka trafia do linii bez zmian.
    Co udaję: nic — czyste dane.
    Co sprawdzam: dla źródła "app.py" i celu "/app" wynik to
    "COPY app.py /app".
    """
    # TODO: przygotuj źródło "app.py" i cel "/app"
    # TODO: wywołaj zadanie_02_linia_copy
    # TODO: sprawdź, że wynik == "COPY app.py /app"
    pass


# --- zadanie_03 ---


def test_zadanie_03_laczy_dwa_polecenia_operatorem_and() -> None:
    """Co testuję: sklejanie dwóch poleceń w jedną linię RUN przez &&.
    Co udaję: nic — czyste dane.
    Co sprawdzam: wynik to dokładnie
    "RUN pip install -r requirements.txt && pip list".
    """
    # TODO: przygotuj listę ["pip install -r requirements.txt", "pip list"]
    # TODO: wywołaj zadanie_03_linia_run
    # TODO: sprawdź, że wynik ==
    #   "RUN pip install -r requirements.txt && pip list"
    pass


def test_zadanie_03_zwraca_none_dla_pustej_listy() -> None:
    """Co testuję: kontrakt None przy braku poleceń.
    Co udaję: nic — pusta lista to legalny argument.
    Co sprawdzam: dla pustej listy wynik to None (nie pusty napis).
    """
    # TODO: przygotuj pustą listę
    # TODO: wywołaj zadanie_03_linia_run
    # TODO: sprawdź (assert ... is None), że wynik to None
    pass


# --- zadanie_04 ---


def test_zadanie_04_buduje_cmd_w_formie_exec() -> None:
    """Co testuję: budowanie linii CMD jako listy JSON (json.dumps).
    Co udaję: nic — czyste dane.
    Co sprawdzam: wynik to dokładnie 'CMD ["python", "app.py"]'
    (cudzysłowy podwójne, przecinek ze spacją — format JSON).
    """
    # TODO: przygotuj listę ["python", "app.py"]
    # TODO: wywołaj zadanie_04_linia_cmd
    # TODO: sprawdź, że wynik == 'CMD ["python", "app.py"]'
    pass


def test_zadanie_04_zwraca_none_dla_pustej_listy() -> None:
    """Co testuję: kontrakt None przy braku polecenia startowego.
    Co udaję: nic — pusta lista to legalny argument.
    Co sprawdzam: dla pustej listy wynik to None.
    """
    # TODO: przygotuj pustą listę
    # TODO: wywołaj zadanie_04_linia_cmd
    # TODO: sprawdź, że wynik is None
    pass


# --- zadanie_05 ---


def test_zadanie_05_sklada_pelny_dockerfile_w_kolejnosci() -> None:
    """Co testuję: złożenie linii FROM, COPY, RUN i CMD w jeden tekst.
    Co udaję: nic — czyste dane.
    Co sprawdzam: wynik to dokładnie pięć linii rozdzielonych "\\n":
    FROM, dwa COPY, RUN i CMD — w tej kolejności.
    """
    # TODO: przygotuj argumenty: obraz "python", tag "3.12-slim",
    #   kopiowania [["requirements.txt", "."], ["app.py", "."]],
    #   polecenia_run ["pip install -r requirements.txt"],
    #   cmd ["python", "app.py"]
    # TODO: wywołaj zadanie_05_zbuduj_dockerfile
    # TODO: przygotuj oczekiwany tekst: sklej "\n".join z listy pięciu
    #   oczekiwanych linii (od "FROM python:3.12-slim"
    #   do 'CMD ["python", "app.py"]')
    # TODO: sprawdź, że wynik == oczekiwany tekst
    pass


def test_zadanie_05_pomija_run_gdy_brak_polecen() -> None:
    """Co testuję: brzeg — pusta lista polecenia_run nie tworzy linii RUN.
    Co udaję: nic — czyste dane.
    Co sprawdzam: w wyniku nie ma fragmentu "RUN"
    (assert "RUN" not in wynik).
    """
    # TODO: przygotuj argumenty jak w teście wyżej, ale polecenia_run
    #   jako pustą listę
    # TODO: wywołaj zadanie_05_zbuduj_dockerfile
    # TODO: sprawdź, że "RUN" not in wynik
    pass


# --- zadanie_06 ---


def test_zadanie_06_buduje_polecenie_z_domyslnym_kontekstem() -> None:
    """Co testuję: budowanie docker build z kontekstem domyślnym.
    Co udaję: nic — czyste dane.
    Co sprawdzam: wywołanie BEZ kontekstu daje
    "docker build -t moja-apka:1.0 ." (kropka z wartości domyślnej).
    """
    # TODO: przygotuj nazwę "moja-apka" i tag "1.0"
    # TODO: wywołaj zadanie_06_polecenie_build bez trzeciego argumentu
    # TODO: sprawdź, że wynik == "docker build -t moja-apka:1.0 ."
    pass


def test_zadanie_06_uzywa_podanego_kontekstu() -> None:
    """Co testuję: że jawnie podany kontekst nadpisuje domyślną kropkę.
    Co udaję: nic — czyste dane.
    Co sprawdzam: dla kontekstu "backend" wynik kończy się " backend".
    """
    # TODO: przygotuj nazwę "moja-apka", tag "1.0" i kontekst "backend"
    # TODO: wywołaj zadanie_06_polecenie_build z trzema argumentami
    # TODO: sprawdź, że wynik == "docker build -t moja-apka:1.0 backend"
    pass


# --- zadanie_07 ---


def test_zadanie_07_parsuje_poprawne_mapowanie_na_krotke() -> None:
    """Co testuję: zamianę "8000:80" na krotkę dwóch liczb int.
    Co udaję: nic — czyste dane.
    Co sprawdzam: wynik to dokładnie krotka (8000, 80).
    """
    # TODO: przygotuj mapowanie "8000:80"
    # TODO: wywołaj zadanie_07_parsuj_porty
    # TODO: sprawdź, że wynik == (8000, 80)
    pass


def test_zadanie_07_zwraca_none_gdy_brak_dwukropka() -> None:
    """Co testuję: brzeg — mapowanie bez dwukropka jest niepoprawne.
    Co udaję: nic — czyste dane.
    Co sprawdzam: dla "8000" wynik to None.
    """
    # TODO: przygotuj mapowanie "8000" (bez dwukropka)
    # TODO: wywołaj zadanie_07_parsuj_porty
    # TODO: sprawdź, że wynik is None
    pass


def test_zadanie_07_zwraca_none_gdy_port_nie_jest_liczba() -> None:
    """Co testuję: brzeg — litery zamiast portu są niepoprawne.
    Co udaję: nic — czyste dane.
    Co sprawdzam: dla "abc:80" wynik to None (isdigit odrzuca litery).
    """
    # TODO: przygotuj mapowanie "abc:80"
    # TODO: wywołaj zadanie_07_parsuj_porty
    # TODO: sprawdź, że wynik is None
    pass


# --- zadanie_08 ---


def test_zadanie_08_buduje_pelne_polecenie_run() -> None:
    """Co testuję: budowanie docker run z flagami -d, --name i -p.
    Co udaję: nic — czyste dane.
    Co sprawdzam: wynik to dokładnie
    "docker run -d --name moj-kontener -p 8000:80 moja-apka:1.0".
    """
    # TODO: przygotuj obraz "moja-apka:1.0", nazwę "moj-kontener"
    #   i mapowanie "8000:80"
    # TODO: wywołaj zadanie_08_polecenie_run
    # TODO: sprawdź, że wynik ==
    #   "docker run -d --name moj-kontener -p 8000:80 moja-apka:1.0"
    pass


def test_zadanie_08_zwraca_none_dla_zlego_mapowania() -> None:
    """Co testuję: brzeg — niepoprawne mapowanie blokuje budowę polecenia.
    Co udaję: nic — czyste dane.
    Co sprawdzam: dla mapowania "abc:80" wynik to None (funkcja
    korzysta z walidacji z zadania 07).
    """
    # TODO: przygotuj obraz, nazwę i niepoprawne mapowanie "abc:80"
    # TODO: wywołaj zadanie_08_polecenie_run
    # TODO: sprawdź, że wynik is None
    pass


# --- zadanie_09 ---


def test_zadanie_09_buduje_usluge_z_portami_i_wolumenami() -> None:
    """Co testuję: budowanie pełnego słownika usługi compose.
    Co udaję: nic — czyste dane.
    Co sprawdzam: wynik to dokładnie słownik z kluczami "image",
    "ports" i "volumes" o podanych wartościach.
    """
    # TODO: przygotuj obraz "moja-apka:1.0", porty ["8000:80"]
    #   i wolumeny ["./dane:/app/dane"]
    # TODO: wywołaj zadanie_09_usluga_compose
    # TODO: sprawdź, że wynik == {"image": "moja-apka:1.0",
    #   "ports": ["8000:80"], "volumes": ["./dane:/app/dane"]}
    pass


def test_zadanie_09_pomija_puste_listy() -> None:
    """Co testuję: brzeg — puste listy nie tworzą kluczy ports/volumes.
    Co udaję: nic — czyste dane.
    Co sprawdzam: dla pustych list wynik to dokładnie
    {"image": "moja-apka:1.0"} — bez kluczy "ports" i "volumes".
    """
    # TODO: przygotuj obraz "moja-apka:1.0" i dwie puste listy
    # TODO: wywołaj zadanie_09_usluga_compose
    # TODO: sprawdź, że wynik == {"image": "moja-apka:1.0"}
    # TODO: sprawdź dodatkowo, że "ports" not in wynik
    pass


# --- zadanie_10 ---


def test_zadanie_10_opakowuje_uslugi_w_klucz_services() -> None:
    """Co testuję: złożenie konfiguracji compose z usług.
    Co udaję: nic — czyste dane.
    Co sprawdzam: wynik to {"services": <przekazany słownik usług>}.
    """
    # TODO: przygotuj słownik usług
    #   {"aplikacja": {"image": "moja-apka:1.0"}}
    # TODO: wywołaj zadanie_10_zbuduj_compose
    # TODO: sprawdź, że wynik ==
    #   {"services": {"aplikacja": {"image": "moja-apka:1.0"}}}
    pass


def test_zadanie_10_zwraca_none_dla_pustych_uslug() -> None:
    """Co testuję: kontrakt None — compose bez usług nie ma sensu.
    Co udaję: nic — pusty słownik to legalny argument.
    Co sprawdzam: dla pustego słownika wynik to None.
    """
    # TODO: przygotuj pusty słownik
    # TODO: wywołaj zadanie_10_zbuduj_compose
    # TODO: sprawdź, że wynik is None
    pass


# --- zadanie_11 ---


def test_zadanie_11_dockerfile_zawiera_wszystkie_linie() -> None:
    """Co testuję: pełny Dockerfile dla aplikacji API (zazębienie
    z tematem 11).
    Co udaję: nic — czyste dane.
    Co sprawdzam: wynik to dokładnie pięć oczekiwanych linii
    rozdzielonych "\\n" (FROM, COPY requirements, RUN pip install,
    COPY app.py, CMD).
    """
    # TODO: wywołaj zadanie_11_dockerfile_dla_api("app.py")
    # TODO: przygotuj oczekiwany tekst: "\n".join z linii
    #   "FROM python:3.12-slim", "COPY requirements.txt .",
    #   "RUN pip install -r requirements.txt", "COPY app.py .",
    #   'CMD ["python", "app.py"]'
    # TODO: sprawdź, że wynik == oczekiwany tekst
    pass


def test_zadanie_11_uzywa_podanej_nazwy_pliku() -> None:
    """Co testuję: że nazwa pliku aplikacji nie jest zahardkodowana.
    Co udaję: nic — czyste dane.
    Co sprawdzam: dla pliku "klient.py" wynik zawiera linię
    "COPY klient.py ." oraz fragment '"klient.py"' w linii CMD.
    """
    # TODO: wywołaj zadanie_11_dockerfile_dla_api("klient.py")
    # TODO: sprawdź, że "COPY klient.py ." in wynik
    # TODO: sprawdź, że '"klient.py"' in wynik
    pass


# --- zadanie_12 ---


def test_zadanie_12_headless_daje_trzy_flagi() -> None:
    """Co testuję: komplet flag Chrome dla kontenera w trybie headless
    (zazębienie z Selenium z tematu 17).
    Co udaję: nic — funkcja tylko buduje listę napisów.
    Co sprawdzam: wynik to dokładnie
    ["--no-sandbox", "--disable-gpu", "--headless=new"].
    """
    # TODO: wywołaj zadanie_12_flagi_chrome_dla_kontenera(True)
    # TODO: sprawdź, że wynik ==
    #   ["--no-sandbox", "--disable-gpu", "--headless=new"]
    pass


def test_zadanie_12_bez_headless_sa_tylko_dwie_flagi() -> None:
    """Co testuję: brzeg — headless=False nie dodaje flagi headless.
    Co udaję: nic — czyste dane.
    Co sprawdzam: wynik to dokładnie ["--no-sandbox", "--disable-gpu"]
    i nie zawiera "--headless=new".
    """
    # TODO: wywołaj zadanie_12_flagi_chrome_dla_kontenera(False)
    # TODO: sprawdź, że wynik == ["--no-sandbox", "--disable-gpu"]
    # TODO: sprawdź dodatkowo, że "--headless=new" not in wynik
    pass


# --- zadanie_13 ---


def test_zadanie_13_buduje_compose_z_usluga_scraper() -> None:
    """Co testuję: pełną konfigurację compose dla scrapera (zazębienie
    z tematem 12 — wolumen na wyniki CSV).
    Co udaję: nic — czyste dane.
    Co sprawdzam: wynik to dokładnie {"services": {"scraper":
    {"image": ..., "volumes": ["./wyniki:/app/wyniki"]}}} — bez
    klucza "ports".
    """
    # TODO: wywołaj zadanie_13_compose_dla_scrapera("moj-scraper:1.0",
    #   "wyniki")
    # TODO: sprawdź, że wynik == {"services": {"scraper":
    #   {"image": "moj-scraper:1.0",
    #    "volumes": ["./wyniki:/app/wyniki"]}}}
    pass


def test_zadanie_13_wolumen_zawiera_podany_folder() -> None:
    """Co testuję: że folder wyników nie jest zahardkodowany.
    Co udaję: nic — czyste dane.
    Co sprawdzam: dla folderu "eksport" wolumen usługi scraper to
    ["./eksport:/app/wyniki"].
    """
    # TODO: wywołaj zadanie_13_compose_dla_scrapera("moj-scraper:1.0",
    #   "eksport")
    # TODO: wyciągnij z wyniku listę wolumenów:
    #   wynik["services"]["scraper"]["volumes"]
    # TODO: sprawdź, że ta lista == ["./eksport:/app/wyniki"]
    pass
