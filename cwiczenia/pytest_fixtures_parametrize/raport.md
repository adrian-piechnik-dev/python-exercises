# Raport review — pytest_fixtures_parametrize

**Data:** 2026-07-11
**Tryb:** pełny (pierwszy review)

## Wynik pytest

```
============================= test session starts =============================
platform win32 -- Python 3.13.5, pytest-9.1.1, pluggy-1.6.0
collected 36 items

test_pytest_fixtures_parametrize.py::test_zadanie_01_dzieli_poprawnie[10-2-5.0] PASSED
... (parametrize + fixtures + mocki, 36 przypadków) ...
test_pytest_fixtures_parametrize.py::test_zadanie_12_awaria_sieci_zwraca_none PASSED [100%]

============================= 36 passed in 0.18s ==============================
```

## Uwagi

Kod zgodny z checklistą techniczną w całości:
- type hinty na każdej funkcji (także testowych `-> None`), ✓
- docstringi Args/Returns, `Args: "Brak."` przy funkcjach bezargumentowych
  (zad. 06, `konfiguracja_globalna`, `raise_for_status`), ✓
- `is None` / `is False` / `is oczekiwane` — nigdzie `== None`/`== True`, ✓
- dwie puste linie między funkcjami, ✓
- brak martwego kodu — wszystkie importy używane (`math`, `json`, `os`,
  `Any`, `Optional`, `requests`, `Path`, `FakeResponse`), ✓
- kontrakt: każda funkcja zwraca jeden typ albo sygnalizuje błąd wyjątkiem
  (`ValueError`) / `None` — nigdzie string-jako-błąd, ✓
- kolejność importów stdlib → third-party → local we wszystkich trzech plikach, ✓
- testy: schemat przygotuj → podmień → wywołaj → sprawdź zachowany (monkeypatch
  env w 05/06, mock `requests.get` w 11/12), asserty zgodne z docstringami, ✓
- fixture'y: `tmp_path` + prawdziwy plik JSON (09), `scope="module"` z adnotacją
  „tylko-do-odczytu" (10), `plik_konfiguracyjny` z `encoding="utf-8"`, ✓
- parametrize z czytelnymi zestawami i przypadkami brzegowymi (granice 12/13,
  17/18 w zad. 03; VAT 0% w zad. 08), ✓

### 🟢 Do zapamiętania na przyszłość (nie blokują zaliczenia)
- `test_pytest_fixtures_parametrize.py:52` — `zadanie_01_podziel(10,0)`:
  brak spacji po przecinku (PEP8 E231). Reszta wywołań ma spacje — drobna
  niekonsekwencja.
- `conftest.py:55` — `raise requests.HTTPError(f" kod {self.status_code}")`:
  wiodąca spacja w treści komunikatu. Kosmetyka, nie wpływa na testy.

## Werdykt

**ZALICZONE — gotowe do dalej.** Pytest zielony (36 passed), zero uwag 🔴,
zero uwag 🟡. Temat zamknięty.
