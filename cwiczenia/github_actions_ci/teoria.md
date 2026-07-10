# GitHub Actions i CI — teoria

## 1. Co to jest CI i po co komu to?

Wyobraź sobie fabrykę słoików z dżemem. Na końcu taśmy stoi kontroler
jakości, który KAŻDY słoik sprawdza tak samo: czy zakrętka dokręcona,
czy etykieta prosta, czy dżem nie kwaśny. Nie sprawdza „co drugi, jak ma
humor" — każdy, zawsze, według tej samej listy.

**CI (Continuous Integration, ciągła integracja)** to taki kontroler
jakości dla kodu. Za każdym razem, gdy wysyłasz kod do repozytorium
(robisz `git push`), automat uruchamia Twoje testy pytest i mówi:
✅ zielono (wszystko działa) albo ❌ czerwono (coś zepsułeś).

Dlaczego to ważne? Bo Ty na swoim komputerze możesz zapomnieć uruchomić
testy. Automat nie zapomina nigdy. Znasz już pytest z poprzednich
tematów — CI to po prostu ktoś, kto odpala za Ciebie `pytest` po każdym
pushu.

**GitHub Actions** to wbudowany w GitHuba system CI. Nie instalujesz
nic — GitHub sam wypożycza Ci na chwilę komputer (świeżutki, pusty
Linux), wykonuje na nim Twoje polecenia i po wszystkim go kasuje.

### Typowe błędy początkujących
- Myślenie, że CI „naprawia" kod. Nie — CI tylko SPRAWDZA i raportuje.
  Naprawiasz Ty.
- Zdziwienie, że na maszynie CI nie ma pandas/pytest. To PUSTY komputer —
  wszystko trzeba na nim zainstalować od zera, za każdym razem.

## 2. Gdzie mieszka przepis dla automatu — plik workflow

GitHub Actions szuka instrukcji w JEDNYM konkretnym miejscu repozytorium:

```
twoje-repo/
└── .github/
    └── workflows/
        └── ci.yml
```

- `.github` — folder z kropką na początku (jak `.gitignore`); kropka
  w świecie Linuksa oznacza „plik/folder ukryty, konfiguracyjny".
- `workflows` — w środku mogą leżeć różne przepisy (np. jeden odpala
  testy, drugi publikuje paczkę).
- `ci.yml` — nazwa pliku jest dowolna, ale rozszerzenie musi być
  `.yml` lub `.yaml`.

Taki jeden plik-przepis nazywa się **workflow** (przepływ pracy).
Skąd ta sztywna ścieżka? GitHub musi wiedzieć, gdzie szukać — umówiono
się na `.github/workflows/` i tego się nie zmienia.

### Typowe błędy początkujących
- Literówka w nazwie folderu: `workflow` (bez `s`) albo `.githubs` —
  GitHub wtedy po prostu NIC nie uruchomi, bez żadnego błędu.
- Wrzucenie pliku do głównego folderu repo zamiast do
  `.github/workflows/`.

## 3. YAML — czyli słownik Pythona zapisany inaczej

Workflow pisze się w formacie **YAML**. Dobra wiadomość: YAML to
w gruncie rzeczy słownik Pythona, tylko zapisany wcięciami zamiast
klamrami. Porównaj:

```python
przepis = {
    "name": "CI",
    "on": {"push": {"branches": ["main"]}},
}
```

To samo w YAML:

```yaml
name: CI
on:
  push:
    branches:
      - main
```

Zasady tłumaczenia:
- `klucz: wartość` w YAML = para klucz-wartość w słowniku,
- wcięcie (2 spacje) = wejście o poziom głębiej (zagnieżdżony słownik),
- linia zaczynająca się od `- ` = element listy
  (`branches: [- main]` → `{"branches": ["main"]}`).

To jest NAJWAŻNIEJSZA myśl tego tematu: **każdy workflow YAML da się
zbudować w Pythonie jako słownik, a potem zamienić na tekst YAML**.
Dokładnie to będziesz robić w zadaniach — budować słowniki-przepisy
i tłumaczyć je na YAML.

### Typowe błędy początkujących
- Tabulatory zamiast spacji — YAML zabrania tabów, wcinaj SPACJAMI.
- Brak spacji po dwukropku: `name:CI` to błąd, musi być `name: CI`.
- Nierówne wcięcia (raz 2 spacje, raz 3) — YAML się wywraca.

## 4. Budowa workflow — trzy piętra: on, jobs, steps

Kompletny minimalny workflow wygląda tak:

```yaml
name: CI
on:
  push:
    branches:
      - main
jobs:
  testy:
    runs-on: ubuntu-latest
    steps:
      - name: Pobierz kod
        uses: actions/checkout@v4
      - name: Uruchom testy
        run: pytest
```

Rozbierzmy go linijka po linijce, jak przepis kulinarny:

**`name: CI`** — nazwa całego przepisu. Wyświetla się na GitHubie
w zakładce Actions. Czysto opisowa, dla ludzi.

**`on:`** — WYZWALACZ, czyli „kiedy automat ma ruszyć". To jak czujnik
ruchu przy lampie: lampa (workflow) zapala się, gdy czujnik (`on`)
coś wykryje.

**`push:`** pod `on:` — konkretny czujnik: „gdy ktoś wypchnie kod".

**`branches: [- main]`** — zawężenie: tylko push na gałąź `main`.
Bez tego workflow ruszałby przy pushu na KAŻDĄ gałąź.

Jako słownik Pythona ten wyzwalacz to:

```python
trigger = {"push": {"branches": ["main"]}}
```

**`jobs:`** — słownik ZADAŃ do wykonania. Jeden workflow może mieć
wiele jobów (np. osobno testy, osobno budowanie paczki) i domyślnie
biegną RÓWNOLEGLE — jak kilku kucharzy w jednej kuchni, każdy przy
swoim stanowisku.

**`testy:`** — to KLUCZ w słowniku `jobs`, czyli nazwa joba. Wymyślasz
ją sam (bez spacji i polskich znaków).

**`runs-on: ubuntu-latest`** — na jakim komputerze job ma się wykonać.
`ubuntu-latest` = „wypożycz mi najnowszy Linux Ubuntu". To najtańsza
i najczęstsza opcja.

**`steps:`** — LISTA kroków wewnątrz joba. Kroki (w odróżnieniu od
jobów) wykonują się PO KOLEI, jeden po drugim — jak kroki przepisu:
najpierw rozgrzej piekarnik, potem włóż ciasto. Każdy krok w YAML
zaczyna się od `- ` (bo to element listy).

Jako słownik Pythona job to:

```python
job = {
    "runs-on": "ubuntu-latest",
    "steps": [krok_pierwszy, krok_drugi],
}
```

### Typowe błędy początkujących
- Mylenie jobów z krokami: joby = równolegle, kroki = po kolei.
- `runs_on` z podkreślnikiem — klucze YAML w Actions używają
  myślników: `runs-on`.
- Zapominanie, że `steps` to LISTA (każdy krok od `- `),
  a `jobs` to SŁOWNIK (klucz = nazwa joba).

## 5. Dwa rodzaje kroków: run i uses

Każdy krok robi jedną z dwóch rzeczy:

**`run:`** — wykonaj polecenie w terminalu, dokładnie takie, jakie
sam wpisałbyś ręcznie:

```yaml
- name: Uruchom testy
  run: pytest cwiczenia/slowniki -v
```

Jako słownik: `{"name": "Uruchom testy", "run": "pytest cwiczenia/slowniki -v"}`.

**`uses:`** — użyj GOTOWEJ akcji z wypożyczalni. Akcja to
przygotowany przez kogoś klocek (jak robot kuchenny: nie budujesz
miksera od zera, wypożyczasz gotowy). Format:
`autor/nazwa@wersja`:

```yaml
- name: Pobierz kod
  uses: actions/checkout@v4
```

`actions` = autor (oficjalne konto GitHuba), `checkout` = nazwa akcji,
`@v4` = wersja 4. Wersję ZAWSZE podajesz — bez niej akcja mogłaby się
kiedyś zmienić pod Tobą bez ostrzeżenia.

`name:` w kroku jest opcjonalny opisowy podpis (widoczny w logach),
ale w tym kursie dajemy go zawsze — czytelne logi to połowa sukcesu
przy debugowaniu CI.

### Dwie akcje, które musisz znać

**`actions/checkout@v4`** — pobiera Twój kod z repozytorium na
wypożyczony komputer. Pamiętaj: maszyna CI startuje PUSTA — bez tego
kroku na komputerze NIE MA Twojego kodu i `pytest` nie miałby czego
testować. Dlatego checkout jest prawie zawsze PIERWSZYM krokiem.

**`actions/setup-python@v5`** — instaluje Pythona w wybranej wersji.
Ta akcja przyjmuje PARAMETR — a parametry dla `uses` podaje się
w kluczu `with:`:

```yaml
- name: Ustaw Pythona
  uses: actions/setup-python@v5
  with:
    python-version: "3.13"
```

Jako słownik:

```python
krok = {
    "name": "Ustaw Pythona",
    "uses": "actions/setup-python@v5",
    "with": {"python-version": "3.13"},
}
```

`with` = „z takimi ustawieniami". Wersję Pythona podaje się jako TEKST
(`"3.13"` w cudzysłowie) — bez cudzysłowu YAML uznałby `3.10` za
liczbę 3.1 i uciąłby zero!

### Typowe błędy początkujących
- Krok z `run` I `uses` naraz — krok robi jedną rzecz: albo polecenie,
  albo gotowa akcja.
- Brak `actions/checkout` na początku — potem zdziwienie, że
  „pytest nie widzi plików".
- `python-version: 3.10` bez cudzysłowu → CI instaluje Pythona 3.1.

## 6. Pełny przepis: pytest w CI

Składamy klocki. Znasz pytest z poprzednich tematów — tu nic nowego,
po prostu automat wykonuje te same polecenia, które Ty wpisujesz
ręcznie:

```yaml
name: CI
on:
  push:
    branches:
      - main
jobs:
  testy:
    runs-on: ubuntu-latest
    steps:
      - name: Pobierz kod
        uses: actions/checkout@v4
      - name: Ustaw Pythona
        uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      - name: Zainstaluj zaleznosci
        run: pip install pytest
      - name: Uruchom testy
        run: pytest cwiczenia/openpyxl_formatowanie -v
```

Kolejność kroków jest logiczna i NIE wolno jej mieszać:
1. pobierz kod (bez kodu nie ma czego testować),
2. zainstaluj Pythona (bez Pythona nie ma pip),
3. zainstaluj pytest (pusty komputer!),
4. uruchom testy.

## 7. Job w kontenerze Dockera

Znasz już obrazy Dockera z tematu `docker_podstawy` — tu tylko jedno
zdanie przypomnienia: obraz to zamrożony, gotowy system z zainstalowanym
oprogramowaniem. GitHub Actions umie uruchomić job W ŚRODKU takiego
obrazu — dodajesz do joba klucz `container:`:

```yaml
jobs:
  testy:
    runs-on: ubuntu-latest
    container: python:3.13-slim
    steps:
      - name: Pobierz kod
        uses: actions/checkout@v4
      - name: Zainstaluj zaleznosci
        run: pip install pytest
      - name: Uruchom testy
        run: pytest cwiczenia/slowniki -v
```

Zauważ: zniknął krok `setup-python` — obraz `python:3.13-slim` MA już
Pythona w środku, więc instalowanie go drugi raz byłoby martwym krokiem.
`runs-on` nadal jest potrzebny (kontener musi na czymś stać).

### Typowe błędy początkujących
- Zostawienie `setup-python` w jobie z kontenerem pythonowym —
  działa, ale to zbędny krok (martwy kod w wersji CI).
- Zapomnienie `runs-on` — kontener nie lewituje, potrzebuje maszyny.

## 8. Badge — naklejka jakości w README

**Badge** to mały obrazek-naklejka w README pokazujący status ostatniego
przebiegu CI: zielony „passing" albo czerwony „failing". Jak naklejka
„Kontrola jakości: OK" na słoiku — od razu widać, czy projekt zdrowy.

GitHub sam generuje taki obrazek pod przewidywalnym adresem:

```
https://github.com/UZYTKOWNIK/REPO/actions/workflows/PLIK.yml/badge.svg
```

W README (plik Markdown) obrazek wstawia się składnią:

```markdown
![CI](https://github.com/looki/python-exercises/actions/workflows/ci.yml/badge.svg)
```

Rozbiór składni Markdown: `!` = „to obrazek", `[CI]` = tekst
zastępczy (gdy obrazek się nie wczyta), `(...)` = adres obrazka.

### Typowe błędy początkujących
- Zgubienie `!` na początku — bez niego powstaje link, nie obrazek.
- Adres z nazwą WORKFLOW zamiast nazwą PLIKU — w adresie badge jest
  nazwa pliku (`ci.yml`), nie `name:` z wnętrza pliku.

## 9. PyYAML — tłumacz słownik ↔ YAML w Pythonie

W zadaniach budujesz workflow jako słowniki Pythona. Żeby zamienić je
na tekst YAML (i z powrotem), użyjesz biblioteki **PyYAML**. To nowa
biblioteka — zainstaluj ją:

```
pip install pyyaml
```

Import (uwaga, importuje się jako `yaml`, nie `pyyaml`):

```python
import yaml
```

### Słownik → tekst YAML: yaml.safe_dump

```python
import yaml

workflow = {"name": "CI", "on": {"push": {"branches": ["main"]}}}
tekst = yaml.safe_dump(workflow, sort_keys=False, allow_unicode=True)
```

Linijka po linijce:
- `yaml.safe_dump(...)` — funkcja „zrzuć słownik do tekstu YAML".
  Zwraca `str`. Przedrostek `safe_` znaczy „bezpieczna wersja" —
  obsługuje tylko zwykłe typy (słowniki, listy, teksty, liczby)
  i tego się trzymaj.
- `sort_keys=False` — BEZ tego PyYAML posortuje klucze alfabetycznie
  i `name` wylądowałby pod `jobs`. Workflow czyta się z góry na dół
  (name → on → jobs), więc kolejność wstawiania chcemy zachować.
- `allow_unicode=True` — pozwala na polskie znaki w wartościach
  (bez tego „ą" zostałoby zapisane jako dziwny kod `ą`).

### Tekst YAML → słownik: yaml.safe_load

```python
import yaml

tekst = "name: CI\non:\n  push:\n    branches:\n      - main\n"
workflow = yaml.safe_load(tekst)
```

- `yaml.safe_load(tekst)` — funkcja „wczytaj tekst YAML do słownika".
  Zwraca `dict` (albo listę, jeśli YAML był listą). To lustrzane
  odbicie `safe_dump`.

Pułapka, o której MUSISZ wiedzieć: klucz `on` w YAML to słowo
specjalne (YAML traktuje `on`/`off` jak `True`/`False`). Gdy PyYAML
wczytuje plik workflow, klucz `on:` może zamienić się w `True`.
W zadaniach tego kursu unikamy problemu, bo budujemy słowniki
w Pythonie (tam `"on"` to zwykły tekst) — ale gdy kiedyś wczytasz
cudzy plik workflow i zamiast klucza `"on"` zobaczysz `True`, już
wiesz dlaczego.

### Typowe błędy początkujących
- `import pyyaml` → `ModuleNotFoundError`. Paczka nazywa się pyyaml,
  ale moduł to `yaml`.
- Użycie `yaml.dump`/`yaml.load` zamiast wersji `safe_` — niebezpieczne
  (`load` potrafi wykonać kod zaszyty w pliku!). ZAWSZE `safe_`.
- Zapomnienie `sort_keys=False` → klucze alfabetycznie → `jobs` przed
  `name` — działa, ale nieczytelnie.

## 10. pathlib — dopisek: tworzenie folderów i zapis tekstu

`Path` znasz z tematu `import_try_except_pathlib`. Tu dochodzą trzy
drobiazgi:

```python
from pathlib import Path

sciezka = Path("moje_repo") / ".github" / "workflows"
sciezka.mkdir(parents=True, exist_ok=True)
plik = sciezka / "ci.yml"
plik.write_text("name: CI\n", encoding="utf-8")
zawartosc = plik.read_text(encoding="utf-8")
```

- `/` między Pathami skleja ścieżkę (znasz to już — przypomnienie).
- `.mkdir(parents=True, exist_ok=True)` — utwórz folder.
  `parents=True` = „utwórz też brakujących rodziców" (folder `.github`
  i w nim `workflows` za jednym zamachem — bez tego błąd, gdy rodzica
  nie ma). `exist_ok=True` = „nie krzycz, jeśli folder już istnieje"
  (bez tego drugi zapis rzuciłby `FileExistsError`).
- `.write_text(tekst, encoding="utf-8")` — zapisz tekst do pliku
  (otwiera, pisze, zamyka — wszystko w jednej metodzie).
- `.read_text(encoding="utf-8")` — odczytaj cały plik jako jeden `str`.
- `.exists()` — czy plik/folder istnieje (zwraca `True`/`False`).

`encoding="utf-8"` podajemy ZAWSZE — Windows domyślnie użyłby innego
kodowania i polskie znaki by się posypały.

### Typowe błędy początkujących
- `mkdir()` bez `parents=True` przy zagnieżdżonej ścieżce →
  `FileNotFoundError`.
- `mkdir()` bez `exist_ok=True` przy powtórnym uruchomieniu →
  `FileExistsError`.
- Zapis bez `encoding="utf-8"` — u Ciebie działa, u kogoś innego krzaki.

## 11. Teoria testowa

### Po co jest conftest.py i co robi sys.path.insert

Gdy pytest uruchamia `test_github_actions_ci.py`, ten plik robi
`from github_actions_ci import ...`. Python szuka modułów tylko
w miejscach zapisanych na liście `sys.path` — a folderu tematu na tej
liście NIE MA (pytest bywa uruchamiany z głównego folderu repo).
Dlatego w `conftest.py` (plik, który pytest wczytuje AUTOMATYCZNIE
przed testami, zawsze pierwszy) dopisujemy folder tematu na początek
tej listy:

```python
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
```

- `os.path.abspath(__file__)` — pełna ścieżka do samego conftest.py,
- `os.path.dirname(...)` — utnij nazwę pliku, zostaw folder,
- `sys.path.insert(0, ...)` — wstaw ten folder na POCZĄTEK listy
  poszukiwań (indeks 0 = pierwsza pozycja, żeby wygrał z innymi).

### Schemat 3 pytań — zanim napiszesz jakikolwiek test

Każdy test zaczyna się od odpowiedzi na trzy pytania (wpisujesz je
w docstring testu):

1. **Co testuję?** — którą funkcję i które jej zachowanie.
2. **Co udaję?** — czego nie chcę robić naprawdę (np. prawdziwego
   GitHuba) i czym to zastępuję (np. folderem tymczasowym).
3. **Co sprawdzam?** — jaki konkretnie assert kończy test.

### Schemat: przygotuj → podmień → wywołaj → sprawdź

Każde CIAŁO testu ma cztery fazy (czasem faza „podmień" jest pusta):

1. **przygotuj** — zbuduj dane wejściowe,
2. **podmień** — zastąp prawdziwe zasoby udawanymi,
3. **wywołaj** — uruchom testowaną funkcję,
4. **sprawdź** — assert na wyniku.

Przykład z INNEJ dziedziny niż ten temat (funkcja licząca średnią ocen
ucznia z pliku):

```python
def test_srednia_ocen_liczy_poprawnie(tmp_path: Path) -> None:
    """Co testuje: czy srednia z ocen 4 i 6 to 5.0.
    Co udaje: prawdziwy dziennik — zastepuje go plikiem w tmp_path.
    Co sprawdzam: wynik == 5.0.
    """
    plik = tmp_path / "oceny.txt"                # przygotuj
    plik.write_text("4\n6\n", encoding="utf-8")  # podmień
    wynik = srednia_ocen(str(plik))              # wywołaj
    assert wynik == 5.0                          # sprawdź
```

### tmp_path — folder tymczasowy od pytest (przypomnienie)

Używałeś już `tmp_path` w poprzednich tematach, więc krótko: to
fixture wbudowana w pytest. Wpisujesz `tmp_path: Path` jako parametr
testu, a pytest przed testem tworzy ŚWIEŻY, PUSTY folder tymczasowy
i podaje Ci jego ścieżkę jako obiekt `Path`. Po teście sam sprząta.
Dzięki temu testy zapisujące pliki nie śmiecą w repo i nie zależą od
siebie nawzajem. W tym temacie `tmp_path` udaje folder repozytorium,
w którym funkcje mają utworzyć `.github/workflows/`.

### Fixture własna (przypomnienie jednym akapitem)

Fixture to funkcja z dekoratorem `@pytest.fixture`, której WYNIK pytest
wstrzykuje do testu przez parametr o tej samej nazwie. Budujesz w niej
dane wielokrotnego użytku (u nas: przykładowy słownik workflow), żeby
nie kopiować tego samego kodu do dziesięciu testów.

### Typowe błędy początkujących
- Assert „że nie wybuchło" — test bez asserta zawsze przechodzi
  i nic nie sprawdza.
- Zapisywanie plików testowych w prawdziwym repo zamiast w `tmp_path`.
- Docstring obiecuje dwa sprawdzenia, a w kodzie jest jeden assert —
  test kłamie o swoim pokryciu.

## 12. Co dalej

W zadaniach zbudujesz z klocków (słowników) kompletny generator
workflow: od pojedynczego wyzwalacza, przez kroki i joby, po zapis
pliku YAML w `.github/workflows/`, badge do README i — na koniec —
gotowy workflow odpalający pytest na testach z ukończonych tematów,
także w wariancie z kontenerem Dockera.
