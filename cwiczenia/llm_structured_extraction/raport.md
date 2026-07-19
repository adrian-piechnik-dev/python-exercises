# Raport review — llm_structured_extraction

**Data:** 2026-07-19
**Tryb:** re-review nr 1

## Wynik pytest

Uruchomione interpreterem z venv repo (`.venv\Scripts\python.exe`).

```
============================= test session starts =============================
platform win32 -- Python 3.13.5, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\Lenovo\Desktop\Python - Projekty\CC_Cwiczenia\cwiczenia\llm_structured_extraction
plugins: anyio-4.14.2
collected 25 items

test_llm_structured_extraction.py::test_zadanie_01_prompt_zawiera_tekst_zrodlowy PASSED [  4%]
test_llm_structured_extraction.py::test_zadanie_01_prompt_zawiera_literalne_klamry_szablonu PASSED [  8%]
test_llm_structured_extraction.py::test_zadanie_02_szablon_z_dwoch_pol PASSED [ 12%]
test_llm_structured_extraction.py::test_zadanie_02_szablon_z_jednego_pola_i_tekst PASSED [ 16%]
test_llm_structured_extraction.py::test_zadanie_03_zdejmuje_prefix_json PASSED [ 20%]
test_llm_structured_extraction.py::test_zadanie_03_tekst_bez_prefiksu_bez_zmian PASSED [ 24%]
test_llm_structured_extraction.py::test_zadanie_04_zdejmuje_suffix PASSED [ 28%]
test_llm_structured_extraction.py::test_zadanie_04_tekst_bez_sufiksu_bez_zmian PASSED [ 32%]
test_llm_structured_extraction.py::test_zadanie_05_czysci_pelny_blok_markdown PASSED [ 36%]
test_llm_structured_extraction.py::test_zadanie_05_czysta_odpowiedz_bez_zmian PASSED [ 40%]
test_llm_structured_extraction.py::test_zadanie_06_parsuje_poprawny_json PASSED [ 44%]
test_llm_structured_extraction.py::test_zadanie_06_zwraca_none_dla_nie_jsona PASSED [ 48%]
test_llm_structured_extraction.py::test_zadanie_07_parsuje_json_owiniety_w_markdown PASSED [ 52%]
test_llm_structured_extraction.py::test_zadanie_07_zwraca_none_dla_odmowy_modelu PASSED [ 56%]
test_llm_structured_extraction.py::test_zadanie_08_wyciaga_tekst_z_poprawnej_koperty PASSED [ 60%]
test_llm_structured_extraction.py::test_zadanie_08_zwraca_none_dla_zepsutej_koperty PASSED [ 64%]
test_llm_structured_extraction.py::test_zadanie_09_pelne_przejscie_obu_warstw PASSED [ 68%]
test_llm_structured_extraction.py::test_zadanie_09_zwraca_none_gdy_tresc_nie_jest_jsonem PASSED [ 72%]
test_llm_structured_extraction.py::test_zadanie_09_zwraca_none_gdy_koperta_zepsuta PASSED [ 76%]
test_llm_structured_extraction.py::test_zadanie_10_zwraca_koperte_odpowiedzi PASSED [ 80%]
test_llm_structured_extraction.py::test_zadanie_10_przekazuje_model_i_timeout PASSED [ 84%]
test_llm_structured_extraction.py::test_zadanie_11_zwraca_slownik_danych PASSED [ 88%]
test_llm_structured_extraction.py::test_zadanie_11_zwraca_none_gdy_model_odmowil PASSED [ 92%]
test_llm_structured_extraction.py::test_zadanie_12_zwraca_dane_gdy_wszystkie_pola_obecne PASSED [ 96%]
test_llm_structured_extraction.py::test_zadanie_12_zwraca_none_gdy_brakuje_pola PASSED [100%]

============================= 25 passed in 0.30s ==============================
```

## Status uwag z rundy 1

| # | Uwaga | Plik | Status |
|---|-------|------|--------|
| 1 | 🔴 `"messages"` jako słownik zamiast listy słowników (zad. 10) | `llm_structured_extraction.py:160` | **NAPRAWIONE** — `[{"role": "user", "content": tresc}]` |
| 2 | 🔴 `"content-type": "json"` zamiast `"application/json"` (zad. 10) | `llm_structured_extraction.py:159` | **NAPRAWIONE** |
| 3 | 🟡 Podwójna spacja po `return` (zad. 09) | `llm_structured_extraction.py:140` | **NAPRAWIONE** |
| 4 | 🟢 Spacja na końcu linii w prompcie (zad. 01) | `llm_structured_extraction.py:17` | **NAPRAWIONE** |
| 5 | 🟢 Nieczytelne zagnieżdżenie wywołań (zad. 05) | `llm_structured_extraction.py:72-76` | nadal aktualne — 🟢, nie blokuje |
| 6 | 🟢 Usunięty blok „Spis zadań" z góry pliku | `llm_structured_extraction.py:1` | nadal aktualne — 🟢, nie blokuje |
| 7 | 🟢 Brak spacji po przecinku | `test_llm_structured_extraction.py` | **CZĘŚCIOWO** — zostały linie 310, 330 |
| 8 | 🟢 Długie linie | `llm_structured_extraction.py:159-160`, `conftest.py:20` | nadal aktualne — 🟢, nie blokuje |

Żadna poprawka nie zepsuła niczego innego: 25/25 nadal zielone.

Payload i nagłówki zad. 10 są teraz zgodne z prawdziwym API — gdybyś wpiął tu
realny klucz, żądanie by przeszło. To była jedyna rzecz w tym temacie, której
testy nie mogły złapać za Ciebie.

## Uwagi w tej rundzie

🔴 — brak.
🟡 — brak.

🟢 **Do zapamiętania na przyszłość:**

**1. Zadanie 05 — `llm_structured_extraction.py:72-76`.** Nadal trzy
zagnieżdżone wywołania w jednym wyrażeniu plus zbędne zewnętrzne nawiasy.
Działa poprawnie, ale czyta się od środka na zewnątrz. Wersja krokowa czyta się
w kolejności wykonania:

```python
    czysty = tekst.strip()
    czysty = zadanie_03_usun_prefix_markdown(czysty)
    czysty = zadanie_04_usun_suffix_markdown(czysty)
    return czysty.strip()
```

**2. Usunięty blok „Spis zadań"** z góry `llm_structured_extraction.py` — to
część szkieletu (mapa tematu), nie kod do wypełnienia. W kolejnych tematach
zostawiaj go.

**3. Brak spacji po przecinku** — `test_llm_structured_extraction.py:310, 330`
(`"sk-test-123","claude-sonnet-4-6"`). Większość poprawiłeś, te dwie zostały.

**4. Długie linie** — `llm_structured_extraction.py:159 (108), 160 (106)`,
`conftest.py:20 (96)`.

Punkty 3 i 4 to robota dla formattera. Przy temacie 21 warto wpiąć
`ruff format` — przestaną wracać w każdym raporcie.

## Co jest dobrze

- **Rozdzielenie dwóch warstw parsowania jest wzorowe.** Zad. 08 pilnuje
  koperty API (`KeyError`/`IndexError`), zad. 06 pilnuje treści modelu
  (`JSONDecodeError`), zad. 09 składa je z jawnym `if tekst is None: return None`.
  Każda warstwa ma własny kontrakt `None` i własny test — a zad. 09 ma trzy
  testy: sukces, awaria warstwy 1, awaria warstwy 2.
- Zad. 03/04 na `removeprefix`/`removesuffix` zamiast ręcznego cięcia slice'ami
  — i oba mają test „bez prefiksu / bez sufiksu", czyli sprawdzasz też,
  że funkcja **nie psuje** czystego wejścia.
- Zad. 02: `", ".join(f'"{pole}": "..."' for pole in pola)` + potrójna klamra
  w f-stringu — najtrudniejsza składniowo część tematu, zrobiona czysto.
- Zad. 12: walidacja pól pętlą z wczesnym `return None`, po uprzednim
  sprawdzeniu `if wynik is None`. Kolejność jest ważna i jest poprawna —
  odwrotnie poleciałby `TypeError` przy `pole not in None`.
- `patch("requests.post")` w teście zad. 10 działa poprawnie, bo moduł robi
  `import requests` i sięga po `requests.post` dopiero w momencie wywołania.
  Gdyby w module było `from requests import post`, ten patch by nie zadziałał
  i trzeba by celować w `llm_structured_extraction.post`.
- `patch("llm_structured_extraction.zadanie_10_zapytaj_model")` w zad. 11/12 —
  patch tam, gdzie funkcja jest **używana**, nie tam, gdzie jest zdefiniowana.
- `is None` w każdym sprawdzeniu kontraktu, zero `== None`.
- Type hinty i docstringi Args/Returns kompletne we wszystkich trzech plikach,
  `Args: Brak.` w fixture'ach conftest, zero nieużywanych importów.

## Werdykt

**ZALICZONE — gotowe do dalej.** Pytest zielony, zero 🔴, zero 🟡.
Temat zamknięty i zacommitowany. Po tym temacie odblokowują się tematy 21+.
