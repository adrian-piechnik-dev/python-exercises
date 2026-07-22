# Raport review — github_actions_ci

**Data:** 2026-07-22
**Tryb:** re-review nr 1

## Wynik pytest

```
============================= test session starts =============================
platform win32 -- Python 3.13.5, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\Piechu\Desktop\CC_cwiczenia\cwiczenia\github_actions_ci
collected 26 items

test_github_actions_ci.py ... (26 testów) ...                          [100%]

============================= 26 passed in 0.09s ==============================
```

Wszystkie 26 testów zielone.

## Status uwag z poprzedniej rundy

**1. 🔴 Zadanie 13 — `test_github_actions_ci.py` — fałszywie zielony test** → **NAPRAWIONE**
   Zamiast iteracji po słowniku joba jest teraz:
   ```python
   lista_krokow = [krok["name"] for krok in wynik["jobs"]["testy"]["steps"]]
   assert len(lista_krokow) == 3
   ```
   Liczy realne kroki (nie klucze joba) — assert sprawdza to, co deklaruje
   docstring. Rozwiązanie dodatkowo scala pomiar z listą nazw (czyściej).

**2. 🟡 `conftest.py` — TODO zostawione po zrobieniu** → **NAPRAWIONE**
   Komentarz `# TODO: ...` nad `return` usunięty.

**3. 🟡 `test_github_actions_ci.py` — jedna pusta linia zamiast dwóch** → **NAPRAWIONE**
   Między `test_zadanie_13_*` są teraz dwie puste linie.

**4. 🟡 `github_actions_ci.py`, linia 117 — myląca nazwa `test`** → **NAPRAWIONE**
   Zmienna przemianowana na `tekst`. Przy okazji poprawiono też
   `Path ,` → `Path,` w sygnaturze fixture `plik_workflow` (uwaga 🟢).

## Uwagi bieżącej rundy

Brak nowych uwag 🔴/🟡.

### 🟢 Do zapamiętania na przyszłość (nie blokują)

- `github_actions_ci.py`, linia 57: `"name" : "Ustaw Pythona"` — zbędna
  spacja przed dwukropkiem (`"name":`).
- `github_actions_ci.py`, linie 198, 231: zmienna `triger` — literówka
  (`trigger`).

## Werdykt

**ZALICZONE — gotowe do dalej.** pytest zielony, zero uwag 🔴/🟡.
