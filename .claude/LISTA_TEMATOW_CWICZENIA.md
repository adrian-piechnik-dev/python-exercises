# LISTA TEMATÓW — mini-kursy ćwiczeniowe (cwiczenia/)

Ten plik mapuje etapy głównego kursu na osobne
mini-kursy ćwiczeniowe generowane przez CC w cwiczenia/<temat_slug>/.
Każdy temat = jeden folder, 4 pliki (teoria.md, conftest.py, <temat_slug>.py,
test_<temat_slug>.py), 10–15 zadań, zgodnie z procedurą /nowy-temat.

Kolejność = kolejność nauki. Spirala: każdy temat od punktu 2 wzwyż zazębia
się z co najmniej jednym pojęciem z tematu poprzedniego.

---

## Etap 0-1 — Podstawy i struktura programu

### 1. `funkcje_return_warunki` ✅ WYGENEROWANY
Zakres: return vs print, if/elif/else, early return, kontrakt funkcji,
None jako sygnał braku wartości.

### 2. `listy_petle`
Zakres: iteracja for, akumulator, enumerate, zip, list comprehension.
Zazębienie: funkcja z zadania 1 użyta jako warunek filtrowania w pętli.

### 3. `slowniki`
Zakres: dostęp przez klucz, .get(), iteracja po .items(), budowanie słownika
w pętli, sprawdzanie obecności klucza (in).
Zazębienie: list comprehension z tematu 2 przy budowaniu słownika.

### 4. `import_try_except_pathlib`
Zakres: podział kodu na pliki, import lokalny, try/except (kolejność
wyjątków szczegółowy→ogólny), pathlib (Path, parent, /), if __name__ ==
"__main__".
Zazębienie: funkcja ze słownikami (temat 3) importowana z innego pliku.

---

## Etap 2A — Pliki tekstowe

### 5. `pliki_tekstowe`
Zakres: open(), with, read()/readlines(), write(), tryb "r"/"w"/"a",
newline, encoding="utf-8".
Zazębienie: try/except z tematu 4 przy otwieraniu nieistniejącego pliku.

---

## Etap 2B — CSV

### 6. `csv_dict_reader_writer`
Zakres: csv.DictReader, csv.DictWriter, newline="" przy open(), fieldnames,
iteracja po wierszach jako słownik.
Zazębienie: słowniki z tematu 3, obsługa błędu pliku z tematu 5.

---

## Etap 2C — JSON

### 7. `json_load_dump`
Zakres: json.load/dump (pliki), json.loads/dumps (stringi), zagnieżdżone
struktury (lista słowników), json.JSONDecodeError.
Zazębienie: struktura danych ze słowników (temat 3) zapisana jako JSON.

---

## Etap 3A — pandas wstęp

### 8. `pandas_wstep`
Zakres: pd.read_csv/read_excel, df["kolumna"], .sum()/.mean(), filtrowanie
boolean (df[df["kolumna"] > x]), brak side effects (.copy()).
Zazębienie: dane wejściowe z CSV (temat 6).

---

## Etap 3B — pandas zaawansowany

### 9. `pandas_groupby_chaining`
Zakres: .groupby(), agregacje (.agg(), COUNT/AVG/SUM odpowiedniki),
.assign(), method chaining, .copy() w łańcuchu.
Zazębienie: filtrowanie boolean z tematu 8 jako krok w chainingu.

---

## Etap 3C — Excel z formatowaniem

### 10. `openpyxl_formatowanie`
Zakres: load_workbook, Font, PatternFill, Alignment, Border/Side,
freeze_panes, iter_rows, column_dimensions, index=False przy
df.to_excel(), wb.save() przed return True.
Zazębienie: DataFrame z tematu 9 jako źródło danych do wyeksportowania.

---

## Etap 4 — API i requests

### 11. `requests_api_podstawy`
Zakres: requests.get z params/timeout, requests.post z json/headers,
status_code, raise_for_status(), RequestException, parsowanie
response.json().
Zazębienie: zapis odpowiedzi API do CSV/JSON (tematy 6-7).

---

## Etap 5 — Web scraping

### 12. `scraping_beautifulsoup`
Zakres: BeautifulSoup, find/find_all, selektory CSS, .text/.get_text(),
atrybuty (.get("href")), robots.txt + User-Agent, rate limiting (time.sleep).
Zazębienie: requests z tematu 11 jako źródło HTML, zapis wyniku do CSV.

---

## Etap 6 — pytest zaawansowany

### 13. `pytest_fixtures_parametrize`
Zakres: fixture (scope function/module/session), conftest.py, parametrize,
pytest.raises, pytest.approx, monkeypatch (setenv/setattr).
Zazębienie: testowanie funkcji z tematu 11 (mock requests) i tematu 4
(try/except) przez pytest.raises.

---

## Etap 6.5 — SQL + PostgreSQL

### 14. `sql_podstawy`
Zakres: CREATE TABLE, INSERT, SELECT/WHERE/ORDER BY/LIMIT, GROUP BY/HAVING,
agregacje (COUNT/AVG/SUM), JOIN (INNER/LEFT).
Zazębienie: brak (SQL czysty, poza Pythonem) — most do tematu 15.

### 15. `psycopg2_sqlalchemy`
Zakres: psycopg2.connect/cursor/execute, zapytania parametryzowane (%s),
executemany, context manager (with), SQLAlchemy create_engine,
pd.read_sql/to_sql.
Zazębienie: SQL z tematu 14, DataFrame z tematu 9, try/except z tematu 4
(psycopg2.Error).

---

## Etap 7 — Testy API + FastAPI

### 16. `fastapi_pydantic`
Zakres: FastAPI(), @app.get/@app.post, parametr ścieżki, BaseModel,
walidacja przez type hint, response_model, TestClient, kod 422.
Zazębienie: JSON z tematu 7 jako response_model, testy z tematu 13
(TestClient jako specjalny fixture).

---

## Etap 8 — Selenium

### 17. `selenium_podstawy`
Zakres: webdriver.Chrome, Service, Options (headless, window-size),
find_element/find_elements + By, WebDriverWait + expected_conditions,
send_keys/click, try/finally + quit().
Zazębienie: try/except z tematu 4 (TimeoutException), logging wprowadzony
tu pierwszy raz jako nowy element stdlib (pełna teoria przed zadaniem).

### 18. `selenium_alerty_screenshoty`
Zakres: save_screenshot (Path→str), switch_to.alert, accept/dismiss,
alert_is_present.
Zazębienie: Path z tematu 4, driver z tematu 17.

---

## Etap 8.5 — AI / LLM API

### 19. `llm_api_klient`
Zakres: request/response do /v1/messages (nagłówki x-api-key,
anthropic-version), payload (model, max_tokens, messages), parsowanie
content[0]["text"], 4-warstwowa obsługa wyjątków z raise...from error,
logging (%s, basicConfig w __main__).
Zazębienie: requests z tematu 11, try/except z tematu 4, logging
z tematu 17.

### 20. `llm_structured_extraction`
Zakres: prompt engineering (podwójne klamry w f-stringu), dwie warstwy
błędu JSON (struktura API vs treść modelu), json.loads + JSONDecodeError,
defensywne czyszczenie markdown (removeprefix/removesuffix), mock
w testach (patch tam gdzie używane).
Zazębienie: json.loads z tematu 7, klient z tematu 19, mock z tematu 13.

---

## Etap 9 — brak nowego tematu ćwiczeniowego
Etap 9 to portfolio + proposale, nie nowa wiedza techniczna — tematy 1-20
się tu kończą. Dalsza ścieżka po ukończeniu tematu 20 — trzy tory poniżej.

---

## PO TEMACIE 20 — TOR A: przyszłe tematy techniczne (numery 21+)
Kolejność priorytetowa (zgodna z planem po Etapie 9):

### 21. `docker_podstawy`
Zakres: Dockerfile (FROM, COPY, RUN, CMD), docker build/run, docker-compose
(services, ports, volumes), konteneryzacja jednego istniejącego projektu.
Zazębienie: projekt z tematów 11-12 (API/scraping) jako obiekt konteneryzacji;
tu wracają flagi --no-sandbox / --disable-gpu z Selenium dla CI.

### 22. `github_actions_ci`
Zakres: workflow YAML (on: push, jobs, steps), uses/run, actions/checkout,
setup-python, uruchomienie pytest w CI, badge w README.
Zazębienie: testy z dowolnego ukończonego tematu jako obiekt automatyzacji;
Docker z tematu 21 (opcjonalnie job w kontenerze).

### 23. `async_httpx`
Zakres: async/await (coroutine, event loop), httpx.AsyncClient, asyncio.gather,
równoległe pobieranie wielu URL-i, porównanie czasu sync vs async.
Zazębienie: requests z tematu 11 (ten sam wzorzec, inna biblioteka),
scraping z tematu 12 (skala).

## PO TEMACIE 20 — TOR B: Playwright (tematy 24+)
Szczegółowy plan i kolejność podtematów: playwright_todo.md (w tym repo).
Zasady: wersja SYNC najpierw (async dopiero po temacie 23), locator-first
zamiast selektorów CSS/XPath, pytest-playwright jako integracja.
Sloty tematów (generować przez /nowy-temat jak dotychczas):

### 24. `playwright_podstawy`
Zakres: sync_playwright, browser/new_page/goto, locatory (get_by_role,
get_by_text, get_by_label), akcje z auto-waiting (click, fill, check),
expect + to_be_visible.
Zazębienie: Selenium z tematów 17-18 (mapowanie pojęć: By → locatory,
WebDriverWait → auto-wait, expected_conditions → actionability).

### 25. `playwright_pytest_network`
Zakres: pytest-playwright (fixture page/browser, --headed/--headless),
page.route (przechwytywanie i mockowanie requestów), request_context
(testy REST API przez Playwright), codegen + trace viewer.
Zazębienie: mock/monkeypatch z tematów 11/13 (ta sama idea podmiany,
inne narzędzie), testy API z tematu 16.

Notatka rynkowa (z playwright_todo.md): Playwright nie blokuje Fazy 1 —
wchodzić dopiero, gdy realnie zabraknie ofert pod Selenium.

## PO TEMACIE 20 — TOR C: mini-projekty utrwalające (M1, M2, ...)
Mini-projekty łączą kilka ukończonych tematów w jedno zadanie — INNE niż
projekty portfolio (nie duplikować scrapera cytatów, walidatora, pipeline'u
pogodowego itd.). Generowane przez /nowy-temat z REGUŁAMI ZAOSTRZONYMI
(sekcja poniżej). Przykładowe sloty (dobierać wg potrzeb utrwalania):

### M1. `mini_raport_wydatkow`
Łączy: CSV (6) + pandas (8-9) + openpyxl (10).
Brief: wczytaj wydatki z CSV, agreguj po kategoriach, wygeneruj
sformatowany raport Excel.

### M2. `mini_api_katalog`
Łączy: requests (11) + JSON (7) + FastAPI (16).
Brief: pobierz dane z publicznego API, przefiltruj, wystaw własnym
endpointem FastAPI z walidacją Pydantic.

### M3. `mini_monitor_cen`
Łączy: scraping (12) + SQL (14-15) + pytest (13).
Brief: scrapuj ceny z piaskownicy, zapisuj do PostgreSQL, raportuj
zmiany; testy z mockiem sieci.

Kolejne mini-projekty (M4+): dopisywać tu przed generowaniem, z jawną
listą łączonych tematów i briefem 1-2 zdania.

---

## REGUŁY ZAOSTRZONE dla mini-projektów (TOR C) — nadpisują /nowy-temat:
Obowiązują TYLKO dla slotów M1, M2, ... (tematy numerowane 1-25 bez zmian).

1. TODO = instrukcje naprowadzające, NIE kod do przepisania:
   - ZAKAZ: `# TODO: wywołaj requests.get(url, timeout=10) i zwróć
     response.json()` (gotowiec — user przepisuje bez myślenia).
   - ZAMIAST: `# TODO: pobierz dane z API z kontrolą błędów serwera
     i zwróć sparsowaną treść (wzorzec znasz z tematu 11)`.
   - TODO mówi CO osiągnąć i ewentualnie ODSYŁA do tematu/wzorca —
     nie mówi JAK linijka po linijce, nie podaje nazw metod z argumentami.
   - Dopuszczalny wyjątek: konkretny import, którego user nie ćwiczył
     osobno (zasada kompletności briefu z INSTRUKCJI) — import podać wprost.

2. Gotowe dane WYŻSZE niż dotychczas (to zostaje ułatwione):
   - Żmudne/monotonne dane user dostaje GOTOWE w pliku: przykładowe
     DataFrame'y, snippety HTML do parsowania, listy słowników, payloady
     JSON, dane wejściowe CSV.
   - Cel: user pisze LOGIKĘ, nie przepisuje danych.

3. Teoria: minimalny poziom jak dotychczas, MOŻE być rozszerzona:
   - Pokrycie pojęć: bez zmian (wszystko potrzebne do zadań musi być).
   - Wolno dodać sekcje przekrojowe (jak tematy łączą się w pipeline,
     decyzje architektoniczne), skoro TODO nie prowadzą za rękę.
   - Teoria NIE może zawierać gotowych rozwiązań zadań z projektu
     (przykłady na innych danych/nazwach niż zadania).

4. Struktura plików i review: bez zmian (4 pliki, /review-temat,
   auto-odhaczanie, te same standardy techniczne).

---

## STATUS GENEROWANIA (aktualizować po każdym /nowy-temat):
1. funkcje_return_warunki — ✅ wygenerowany, ✅ wykonany
2. listy_petle — ✅ wygenerowany, ✅ wykonany, ✅ sprawdzony
3. slowniki — ✅ wygenerowany, ✅ wykonany, ✅ sprawdzony
4. import_try_except_pathlib — ✅ wygenerowany, ✅ wykonany, ✅ sprawdzony
5. pliki_tekstowe — ✅ wygenerowany, ✅ wykonany, ✅ sprawdzony
6. csv_dict_reader_writer — ✅ wygenerowany, ✅ wykonany, ✅ sprawdzony
7. json_load_dump — ✅ wygenerowany, ✅ wykonany, ✅ sprawdzony
8. pandas_wstep — ✅ wygenerowany, ✅ wykonany, ✅ sprawdzony
9. pandas_groupby_chaining — ✅ wygenerowany, ✅ wykonany, ✅ sprawdzony
10. openpyxl_formatowanie — ✅ wygenerowany, ✅ wykonany, ✅ sprawdzony
11. requests_api_podstawy — ✅ wygenerowany, ✅ wykonany, ✅ sprawdzony
12. scraping_beautifulsoup — ✅ wygenerowany, ✅ wykonany, ✅ sprawdzony
13. pytest_fixtures_parametrize — ✅ wygenerowany, ✅ wykonany, ✅ sprawdzony
14. sql_podstawy — ✅ wygenerowany, ✅ wykonany, ✅ sprawdzony
15. psycopg2_sqlalchemy — ✅ wygenerowany, ✅ wykonany, ✅ sprawdzony
16. fastapi_pydantic — ✅ wygenerowany, ✅ wykonany, ✅ sprawdzony
17. selenium_podstawy — ✅ wygenerowany, ✅ wykonany, ✅ sprawdzony
18. selenium_alerty_screenshoty — ✅ wygenerowany, ✅ wykonany, ✅ sprawdzony
19. llm_api_klient — ✅ wygenerowany, ✅ wykonany, ✅ sprawdzony
20. llm_structured_extraction — ✅ wygenerowany, ✅ wykonany, ✅ sprawdzony

Po temacie 20 (odblokowane po ✅ sprawdzony na 20):
21. docker_podstawy — ✅ wygenerowany, ✅ wykonany, ✅ sprawdzony
22. github_actions_ci — ✅ wygenerowany, ✅ wykonany, ✅ sprawdzony
23. async_httpx — ✅ wygenerowany, ✅ wykonany, ✅ sprawdzony
24. playwright_podstawy — ✅ wygenerowany
25. playwright_pytest_network — ✅ wygenerowany
M1. mini_raport_wydatkow — ✅ wygenerowany
M2. mini_api_katalog — ✅ wygenerowany
M3. mini_monitor_cen — ✅ wygenerowany

### Zasada auto-odhaczania (dla CC):
- Po wykonaniu /nowy-temat <slug> → CC sam zmienia status z ⬜ na ✅ wygenerowany
- Po /review-temat <slug>, gdy widać że wszystkie TODO uzupełnione (bez pass/...) → ✅ wykonany
- Po /review-temat <slug>, gdy raport.md wychodzi bez 🔴/🟡 → ✅ sprawdzony (można przejść dalej)
- CC edytuje ten plik bezpośrednio po każdej z tych trzech akcji, bez pytania o potwierdzenie