# Raport review — mini_api_katalog

**Data:** 2026-07-25
**Tryb:** re-review nr 2 (końcowy)

---

## Wynik pytest

```
============================= test session starts =============================
collecting ... collected 27 items

test_mini_api_katalog.py::test_zadanie_01_zwraca_liste_produktow PASSED [  3%]
test_mini_api_katalog.py::test_zadanie_01_zwraca_none_przy_bledzie_serwera PASSED [  7%]
test_mini_api_katalog.py::test_zadanie_02_skleja_strony_w_plaska_liste PASSED [ 11%]
test_mini_api_katalog.py::test_zadanie_02_zero_stron_daje_pusta_liste PASSED [ 14%]
test_mini_api_katalog.py::test_zadanie_03_zostawia_tylko_dostepne PASSED [ 18%]
test_mini_api_katalog.py::test_zadanie_03_pusta_lista_daje_pusta_liste PASSED [ 22%]
test_mini_api_katalog.py::test_zadanie_04_zostawia_trzy_pola PASSED [ 25%]
test_mini_api_katalog.py::test_zadanie_04_nie_modyfikuje_wejscia PASSED [ 29%]
test_mini_api_katalog.py::test_zadanie_05_znajduje_produkt_po_id PASSED [ 33%]
test_mini_api_katalog.py::test_zadanie_05_zwraca_none_gdy_brak_id PASSED [ 37%]
test_mini_api_katalog.py::test_zadanie_06_tworzy_plik_i_zwraca_true PASSED [ 40%]
test_mini_api_katalog.py::test_zadanie_06_zapisuje_pelna_zawartosc PASSED [ 44%]
test_mini_api_katalog.py::test_zadanie_07_wczytuje_katalog PASSED [ 48%]
test_mini_api_katalog.py::test_zadanie_07_none_gdy_brak_pliku PASSED [ 51%]
test_mini_api_katalog.py::test_zadanie_07_none_gdy_zepsuty_json PASSED [ 55%]
test_mini_api_katalog.py::test_zadanie_08_buduje_obiekt_z_poprawnych_danych PASSED [ 59%]
test_mini_api_katalog.py::test_zadanie_08_zwraca_none_gdy_zle_dane PASSED [ 62%]
test_mini_api_katalog.py::test_zadanie_09_get_zwraca_liste_z_pliku PASSED [ 66%]
test_mini_api_katalog.py::test_zadanie_09_pusty_katalog_daje_pusta_liste PASSED [ 70%]
test_mini_api_katalog.py::test_zadanie_10_zwraca_szczegoly_produktu PASSED [ 74%]
test_mini_api_katalog.py::test_zadanie_10_kod_404_gdy_brak_produktu PASSED [ 77%]
test_mini_api_katalog.py::test_zadanie_11_post_dopisuje_produkt PASSED [ 81%]
test_mini_api_katalog.py::test_zadanie_11_kod_422_gdy_zle_dane PASSED [ 85%]
test_mini_api_katalog.py::test_zadanie_12_buduje_czysty_katalog_na_dysku PASSED [ 88%]
test_mini_api_katalog.py::test_zadanie_12_none_i_brak_pliku_gdy_api_padlo PASSED [ 92%]
test_mini_api_katalog.py::test_zadanie_13_buduje_dzialajacy_sklep PASSED [ 96%]
test_mini_api_katalog.py::test_zadanie_13_none_gdy_zaopatrzenie_padlo PASSED [100%]

======================== 27 passed, 1 warning in 1.19s ========================
```

---

## Status uwag z rundy nr 2

| # | Uwaga | Status |
|---|---|---|
| 🟡 A | brak strażnika `None` w `zwroc_produkt` (zadanie 13) | ✅ NAPRAWIONE |
| 🟡 B | docstringi trzech atrap 500 opisywały kod 200 | ✅ NAPRAWIONE |
| 🟢 C | `Returns: dict` przy `-> list[dict]` | ✅ NAPRAWIONE |
| 🟢 D | literówka „dodoania" | ✅ NAPRAWIONE |
| 🟢 E | wcięcie w sekcji Args | ✅ NAPRAWIONE |
| 🟢 F | niekonsekwentna pusta linia po docstringu testu | ✅ NAPRAWIONE |
| 🟢 G | licznik wywołań w teście „zero stron" | ⬜ świadomie zostawione |
| 🟢 H | brak `raise_for_status` w zadaniu 02 | ⬜ zgodne z kontraktem |

**🟡 A** — `mini_api_katalog.py:326-327`: `zwroc_produkt` w zadaniu 13 ma teraz
ten sam strażnik co pozostałe trzy endpointy. Wszystkie cztery miejsca
czytające plik przez `zadanie_07_wczytaj_katalog` reagują tak samo na `None`:
`HTTPException(500)`. Aplikacja z zadania 13 jest wewnętrznie spójna.

**🟡 B** — `test_mini_api_katalog.py:71, 79, 439, 447, 512, 520`: trzy atrapy
awarii mają docstring „Atrapa requests.get **udająca awarię serwera**" i
`Returns: FakeResponse: atrapa z kodem 500 i pustymi danymi — jej
raise_for_status rzuci HTTPError`. Pięć atrap zdrowych zachowało opis kodu 200.
Sprawdziłem wszystkie osiem — każdy docstring zgadza się teraz z tym, co
funkcja faktycznie zwraca.

**🟢 F** — wszystkie osiem atrap ma teraz jednolity układ (bez pustej linii
między docstringiem testu a `def podmieniony_get`).

---

## Uwagi

Zero 🔴, zero 🟡.

### 🟢 Do zapamiętania na przyszłość

**🟢 G. `test_mini_api_katalog.py:121-147` — docstring testu „zero stron" obiecuje więcej, niż assert sprawdza**

„Co udaje: requests.get — atrapa **nie powinna być w ogóle użyta**", a assert
weryfikuje tylko `wynik == []`. Pusta lista wyszłaby również wtedy, gdyby
funkcja odpytała API i dostała puste odpowiedzi. Żeby sprawdzić dokładnie to,
co deklarujesz, potrzebny jest licznik wywołań atrapy (`licznik["wywolania"] += 1`
w atrapie, `assert licznik["wywolania"] == 0` na końcu). Nie blokuje —
zapamiętaj wzorzec „test liczby wywołań" na kolejne tematy z monkeypatch.

**🟢 H. `mini_api_katalog.py:59` — zadanie 02 bez `raise_for_status`**

Kontrakt zadania 02 to czysta `list` bez `| None`, więc brak kontroli błędów
jest zgodny z docstringiem — to świadoma różnica względem zadania 01, nie
przeoczenie. Warto mieć w pamięci, że przy 500 z serwera ta funkcja wrzuciłaby
do wyniku treść strony błędu albo wybuchła na parsowaniu.

---

## Co jest dobre

- **Kontrakty `None` przechodzą przez cały pipeline** — 01 → 12 → 13
  propaguje awarię hurtowni bez wyjątku wyciekającego na zewnątrz, a 07 → 10/11
  zamienia brak pliku na czyste 500. Po poprawkach nie ma już ani jednego
  miejsca, gdzie `None` z `zadanie_07` leci dalej niesprawdzony.
- **Wąskie `except`** — `requests.RequestException`, `FileNotFoundError`,
  `json.JSONDecodeError`, `ValidationError`. Ani jednego gołego `except`.
- **Zadanie 12: early return przed zapisem** — plik nie powstaje przy awarii
  API, i jest na to test (`assert not sciezka.exists()`).
- **Zadania 10 i 11 złożone z gotowych klocków** (07 + 05, 07 + 06) zamiast
  powielonej logiki.
- **`raise HTTPException` zamiast `return`** — pułapka z teorii ominięta we
  wszystkich czterech endpointach.
- **Test 04 „nie modyfikuje wejścia"** — sprawdza brak side effects na
  oryginale, co odróżnia dobry test od naiwnego.
- **Docstringi atrap opisują, co atrapa udaje** — po poprawce z rundy 2 to
  realnie działająca dokumentacja, nie ozdoba.
- **Wszystkie pliki otwierane przez `with` z `encoding="utf-8"`.**

---

## Werdykt

**ZALICZONE — gotowe do dalej**

27/27 testów zielonych, zero uwag 🔴 i 🟡. Dwie uwagi 🟢 zostają jako notatki
na przyszłość, nie blokują zaliczenia. Temat zamknięty — commit wykonany.
