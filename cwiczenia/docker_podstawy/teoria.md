# Docker — podstawy (teoria)

Ten plik zawiera CAŁĄ wiedzę potrzebną do zadań z `docker_podstawy.py`,
TODO w `conftest.py` i testów w `test_docker_podstawy.py`. Nie musisz
szukać niczego poza tym plikiem.

Ważna uwaga na start: w tym temacie NIE uruchamiamy Dockera. Uczymy się
jego języka — piszemy funkcje Pythona, które BUDUJĄ treść Dockerfile,
polecenia `docker build` / `docker run` i konfigurację docker-compose.
Dzięki temu wszystko testujesz pytestem, bez instalowania czegokolwiek.
To jak nauka pisania przepisów kulinarnych: nie musisz mieć piekarnika,
żeby nauczyć się poprawnie zapisać przepis.

---

## 1. Co to jest Docker?

### Co to jest?
Wyobraź sobie, że ugotowałeś zupę u siebie w kuchni i chcesz, żeby
kolega ugotował IDENTYCZNĄ u siebie. Możesz mu podyktować przepis przez
telefon — ale u niego jest inna kuchenka, inne garnki, brakuje przypraw.
Zupa wyjdzie inna albo nie wyjdzie wcale.

Docker rozwiązuje to tak: pakujesz do jednego pudełka CAŁĄ kuchnię —
garnek, kuchenkę, przyprawy i zupę. Kolega dostaje pudełko, otwiera je
i wszystko działa u niego dokładnie tak samo jak u ciebie.

W świecie programowania: twój program potrzebuje konkretnej wersji
Pythona, konkretnych bibliotek (np. `requests`), czasem przeglądarki.
Docker pakuje to wszystko razem, żeby program działał tak samo na
każdym komputerze — twoim, kolegi i na serwerze w chmurze.

### Skąd się wzięło?
Z wiecznego problemu "u mnie działa". Programista pisał kod na swoim
komputerze, wysyłał na serwer — i tam kod nie działał, bo serwer miał
inną wersję Pythona albo brakowało biblioteki. Docker (2013 r.) zamknął
program razem z jego otoczeniem, więc "u mnie działa" = "działa wszędzie".

### Dlaczego tak musi być?
Bo program to nie tylko twój plik `.py`. To także interpreter Pythona,
biblioteki, system operacyjny pod spodem. Jeśli którakolwiek warstwa
się różni — program może się zachować inaczej. Jedyny pewny sposób to
zabrać wszystkie warstwy ze sobą.

---

## 2. Obraz i kontener — dwa najważniejsze słowa

### Co to jest?
- **Obraz (image)** — przepis + spakowane składniki. Plik "zamrożony",
  nic się w nim nie dzieje. Jak płyta z grą na półce.
- **Kontener (container)** — URUCHOMIONY obraz. Jak gra, w którą właśnie
  grasz. Z jednego obrazu możesz uruchomić wiele kontenerów naraz —
  tak jak z jednej płyty może grać kilka osób na różnych konsolach.

### Skąd się wzięło?
Nazwa "kontener" pochodzi od kontenerów morskich: statek nie musi
wiedzieć, co jest w środku (banany? telewizory?), bo każdy kontener ma
ten sam kształt i tak samo się go przenosi dźwigiem. Docker robi to samo
z programami: serwer nie musi wiedzieć, co jest w środku kontenera —
uruchamia każdy tak samo.

### Dlaczego tak musi być?
Rozdzielenie "przepisu" (obraz) od "gotowania" (kontener) pozwala
zbudować obraz RAZ, a potem uruchamiać go setki razy — szybko i zawsze
z identycznym efektem.

### Typowe błędy początkujących
- Mylenie obrazu z kontenerem: obraz się BUDUJE (`docker build`),
  kontener się URUCHAMIA (`docker run`).
- Myślenie, że zmiana w działającym kontenerze zmienia obraz — nie.
  Kontener po skasowaniu znika razem ze zmianami; obraz zostaje taki,
  jaki był.

---

## 3. Dockerfile — przepis na obraz

### Co to jest?
Dockerfile to zwykły plik tekstowy o nazwie dokładnie `Dockerfile`
(bez rozszerzenia), w którym linijka po linijce piszesz, jak zbudować
obraz. Każda linia to jedna INSTRUKCJA: słowo pisane WIELKIMI LITERAMI
plus argumenty. Docker czyta plik od góry do dołu i wykonuje instrukcje
po kolei — jak przepis: "weź garnek, wlej wodę, zagotuj".

Przykładowy kompletny Dockerfile (dla aplikacji w Pythonie):

```dockerfile
FROM python:3.12-slim
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
CMD ["python", "app.py"]
```

Teraz każda instrukcja osobno.

---

### 3.1. FROM — na czym budujemy

```dockerfile
FROM python:3.12-slim
```

**Co to jest?** Pierwsza instrukcja każdego Dockerfile. Mówi: "zacznij
od gotowego obrazu bazowego". Nie budujesz kuchni od zera — bierzesz
gotową kuchnię z zamontowaną kuchenką i dokładasz tylko swoje rzeczy.

**Składnia linijka po linijce:**
- `FROM` — słowo kluczowe instrukcji,
- `python` — nazwa obrazu bazowego (tu: oficjalny obraz z Pythonem),
- `:` — dwukropek oddziela nazwę od taga,
- `3.12-slim` — **tag**, czyli konkretna wersja obrazu. `slim` znaczy
  "odchudzony" — mniejszy obraz bez zbędnych dodatków.

Cała linia to zawsze wzór: `FROM nazwa:tag`.

**Skąd się wzięło?** Ludzie budowali w kółko te same podstawy (system +
Python). Ktoś zrobił to raz dobrze, opublikował w internetowej
bibliotece obrazów (Docker Hub) — i teraz wszyscy zaczynają od `FROM`.

**Dlaczego tak musi być?** Bez punktu startowego Docker nie wiedziałby,
jaki system i jakie narzędzia są w środku. `FROM` zawsze musi być
pierwsze — nie można dokładać składników do garnka, którego nie ma.

**Typowe błędy początkujących:**
- Pominięcie taga (`FROM python`) — Docker weźmie wtedy tag `latest`
  ("najnowszy"), który jutro może być INNĄ wersją niż dziś. Zawsze
  podawaj konkretny tag.
- Literówka w tagu (np. `3.12slim` bez myślnika) — obraz nie istnieje,
  budowanie się wywali.

---

### 3.2. COPY — wkładamy nasze pliki

```dockerfile
COPY requirements.txt .
```

**Co to jest?** Kopiuje plik z TWOJEGO komputera do środka obrazu.

**Składnia linijka po linijce:**
- `COPY` — słowo kluczowe,
- `requirements.txt` — **źródło**: plik na twoim komputerze (ścieżka
  względem folderu, w którym budujesz),
- `.` — **cel**: dokąd wkleić w obrazie. Kropka znaczy "do bieżącego
  folderu w obrazie" (znasz kropkę jako bieżący folder z tematu 4
  o pathlib).

Wzór: `COPY źródło cel` — źródło i cel oddzielone JEDNĄ spacją.

**Skąd się wzięło?** Obraz to zamknięte pudełko — nie widzi plików na
twoim dysku. Trzeba je jawnie włożyć do środka, dokładnie tak jak
pakując paczkę wkładasz do niej rzeczy.

**Dlaczego tak musi być?** Gdyby obraz widział cały twój dysk, nie
byłby przenośny — u kolegi twojego dysku nie ma. W obrazie może być
tylko to, co jawnie skopiowano.

**Typowe błędy początkujących:**
- Zapomnienie celu (`COPY app.py`) — instrukcja wymaga DWÓCH części.
- Kopiowanie wszystkiego (`COPY . .`) zamiast konkretnych plików —
  do obrazu trafiają śmieci (foldery testów, pliki tymczasowe).
  W naszych zadaniach kopiujemy konkretne pliki.

---

### 3.3. RUN — wykonaj polecenie podczas BUDOWANIA

```dockerfile
RUN pip install -r requirements.txt
```

**Co to jest?** Wykonuje polecenie W TRAKCIE budowania obrazu i zapisuje
efekt w obrazie. Tu: instaluje biblioteki, żeby były już gotowe, gdy
ktoś uruchomi kontener.

**Składnia:** `RUN` + polecenie dokładnie takie, jakie wpisałbyś
w terminalu.

Gdy poleceń jest kilka, łączy się je w JEDNĄ instrukcję RUN operatorem
`&&`:

```dockerfile
RUN pip install --upgrade pip && pip install -r requirements.txt
```

`&&` znaczy: "wykonaj drugie polecenie TYLKO jeśli pierwsze się udało".
Polecenia rozdziela się ` && ` (spacja, dwa ampersandy, spacja).

**Skąd się wzięło?** Każda instrukcja w Dockerfile tworzy osobną
"warstwę" obrazu (jak warstwy tortu). Im mniej warstw, tym mniejszy
i szybszy obraz — dlatego kilka poleceń skleja się w jeden RUN.

**Dlaczego tak musi być?** Instalacja bibliotek trwa. Lepiej zrobić ją
RAZ przy budowaniu, niż przy każdym uruchomieniu kontenera.

**Typowe błędy początkujących:**
- Mylenie RUN z CMD (o CMD za chwilę): RUN dzieje się przy BUDOWANIU,
  CMD przy URUCHOMIENIU kontenera.
- Sklejanie poleceń bez spacji wokół `&&` (`polecenie1&&polecenie2`) —
  bywa źle interpretowane; zawsze ` && `.

---

### 3.4. CMD — co ma się stać po STARCIE kontenera

```dockerfile
CMD ["python", "app.py"]
```

**Co to jest?** Ostatnia instrukcja przepisu: "gdy ktoś uruchomi
kontener, wykonaj TO". Obraz może mieć tylko jedno CMD.

**Składnia linijka po linijce:**
- `CMD` — słowo kluczowe,
- `["python", "app.py"]` — polecenie zapisane jako LISTA w formacie
  JSON: każdy kawałek polecenia (program i każdy argument) to osobny
  napis w cudzysłowach PODWÓJNYCH, kawałki oddzielone przecinkiem
  i spacją, całość w nawiasach kwadratowych.

Ta forma nazywa się **forma exec**. Istnieje też forma bez nawiasów
(`CMD python app.py`, tzw. forma shell), ale forma exec jest zalecana —
polecenie trafia do systemu dokładnie tak, jak je zapisałeś, bez
pośrednika, który mógłby coś przekręcić.

**Skąd się wzięło?** Format `["python", "app.py"]` to dokładnie JSON —
znasz go z tematu 7. Dlatego w Pythonie taką linię buduje się przez
`json.dumps` (przypomnienie w sekcji 8), a nie sklejanie napisów ręcznie.

**Dlaczego tak musi być?** JSON wymaga cudzysłowów podwójnych i ma
ścisłe reguły przecinków — ręczne sklejanie łatwo psuje format,
`json.dumps` nigdy.

**Typowe błędy początkujących:**
- Cudzysłowy pojedyncze w liście (`CMD ['python', 'app.py']`) — to NIE
  jest poprawny JSON, Docker potraktuje linię inaczej niż myślisz.
- RUN na starcie zamiast CMD: `RUN python app.py` uruchomiłoby program
  podczas BUDOWANIA obrazu (i budowanie by "wisiało"), a nie przy
  starcie kontenera.

---

## 4. docker build — budujemy obraz z przepisu

```
docker build -t moja-apka:1.0 .
```

**Co to jest?** Polecenie terminala, które czyta Dockerfile i buduje
obraz.

**Składnia kawałek po kawałku:**
- `docker build` — program `docker`, podpolecenie `build` ("zbuduj"),
- `-t moja-apka:1.0` — flaga `-t` (od "tag") nadaje obrazowi nazwę
  i wersję we wzorze `nazwa:tag` — tym samym wzorze co w FROM. Bez
  nazwy obraz dostałby losowy identyfikator i trudno byłoby go znaleźć,
- `.` — **kontekst budowania**: folder, w którym Docker ma szukać
  Dockerfile i plików do COPY. Kropka = folder bieżący.

Wzór: `docker build -t nazwa:tag kontekst`.

**Skąd się wzięło?** Flagi jednoliterowe z myślnikiem (`-t`) to stara
konwencja poleceń terminala — krótkie przełączniki zmieniające
zachowanie programu.

**Dlaczego tak musi być?** Docker musi wiedzieć: JAK nazwać wynik (`-t`)
i GDZIE szukać składników (kontekst). `COPY requirements.txt .` znajdzie
plik właśnie względem kontekstu.

**Typowe błędy początkujących:**
- Zapomnienie kropki na końcu — `docker build -t moja-apka:1.0` kończy
  się błędem, bo brakuje kontekstu.
- Budowanie z innego folderu niż projekt — COPY nie znajdzie plików.

---

## 5. docker run — uruchamiamy kontener

```
docker run -d --name moj-kontener -p 8000:80 moja-apka:1.0
```

**Co to jest?** Polecenie, które z obrazu tworzy i startuje kontener.

**Składnia kawałek po kawałku:**
- `docker run` — "uruchom kontener",
- `-d` — od "detached" ("odczepiony"): kontener działa w tle, a ty
  odzyskujesz terminal. Bez `-d` terminal byłby zajęty, dopóki kontener
  się nie zatrzyma,
- `--name moj-kontener` — nadaje kontenerowi nazwę. Flagi wielolitrowe
  mają DWA myślniki (`--name`), jednoliterowe jeden (`-d`, `-p`, `-t`) —
  to ta sama konwencja terminala co przy build,
- `-p 8000:80` — mapowanie portów (wyjaśnienie niżej),
- `moja-apka:1.0` — obraz do uruchomienia, ZAWSZE na końcu polecenia.

Wzór: `docker run -d --name nazwa -p mapowanie obraz`.

### Mapowanie portów `8000:80`

**Co to jest?** Port to numerowane "drzwi" komputera, przez które
programy rozmawiają przez sieć (przy `requests` w temacie 11
korzystałeś z portów nie wiedząc o tym — adres `https://...` domyślnie
używa portu 443). Kontener jest zamkniętym pudełkiem — jego drzwi są
W ŚRODKU pudełka. Mapowanie `8000:80` mówi: "kto zapuka do drzwi 8000
MOJEGO komputera, tego przekieruj do drzwi 80 W KONTENERZE".

Wzór zawsze: `port_hosta:port_kontenera` — dwie liczby rozdzielone
dwukropkiem. **Host** to twój komputer (ten, który "gości" kontener).

**Dlaczego tak musi być?** Bez mapowania program w kontenerze byłby
niedostępny z zewnątrz — pudełko szczelnie zamknięte.

**Typowe błędy początkujących:**
- Odwrócenie kolejności: wzór to host:kontener, nie odwrotnie.
- Podanie jednej liczby (`-p 8000`) albo liter (`-p abc:80`) — mapowanie
  musi mieć DWIE liczby i dwukropek. W zadaniu 07 napiszesz funkcję,
  która to sprawdza i dla złego mapowania zwraca None (znany ci kontrakt
  None z tematu 1).

---

## 6. docker-compose — kilka kontenerów jednym plikiem

**Co to jest?** Gdy projekt potrzebuje kilku kontenerów naraz (np.
aplikacja + baza danych) albo jednego kontenera z długą konfiguracją,
zamiast wpisywać długie `docker run` za każdym razem — opisujesz
wszystko RAZ w pliku `docker-compose.yml`, a potem uruchamiasz jednym
poleceniem `docker compose up`.

Plik wygląda tak:

```yaml
services:
  aplikacja:
    image: moja-apka:1.0
    ports:
      - "8000:80"
    volumes:
      - "./dane:/app/dane"
```

**Składnia linijka po linijce:**
- `services:` — nagłówek sekcji z listą usług. **Usługa (service)** to
  jeden kontener z konfiguracją,
- `aplikacja:` — nazwa usługi (wymyślasz sam),
- `image: moja-apka:1.0` — z jakiego obrazu uruchomić (to samo, co
  ostatni argument `docker run`),
- `ports:` — lista mapowań portów; każda pozycja listy zaczyna się od
  `- ` i jest napisem w takim samym wzorze `host:kontener` jak przy
  `-p`,
- `volumes:` — lista **wolumenów** (wyjaśnienie niżej).

Ten format pliku to **YAML** — sposób zapisu danych oparty na wcięciach.
Kluczowa obserwacja: struktura YAML to dokładnie zagnieżdżone słowniki
i listy, które znasz z tematów 2-3 i 7. Powyższy plik odpowiada
słownikowi Pythona:

```python
{
    "services": {
        "aplikacja": {
            "image": "moja-apka:1.0",
            "ports": ["8000:80"],
            "volumes": ["./dane:/app/dane"],
        }
    }
}
```

W zadaniach 09, 10 i 13 budujesz właśnie takie słowniki. W prawdziwym
projekcie zamieniłaby je na plik YAML gotowa biblioteka — my zostajemy
przy słownikach, bo to one są istotą konfiguracji.

**Skąd się wzięło?** Docker Compose powstał, bo ręczne uruchamianie
kilku kontenerów z długimi flagami było męczące i podatne na literówki.
Plik można trzymać w repozytorium — konfiguracja jest udokumentowana.

### Wolumen `./dane:/app/dane`

**Co to jest?** Kontener po skasowaniu ZNIKA razem ze wszystkim, co
zapisał w środku (pamiętasz z sekcji 2). Wolumen to "okno" między
folderem na twoim komputerze a folderem w kontenerze: co kontener
zapisze w `/app/dane`, ląduje NAPRAWDĘ w `./dane` u ciebie —
i przeżywa skasowanie kontenera.

Wzór jak przy portach: `folder_hosta:folder_kontenera`, rozdzielone
dwukropkiem. `./dane` znaczy "folder dane obok pliku compose"
(kropka-ukośnik = bieżący folder, znane z pathlib w temacie 4).

**Dlaczego tak musi być?** Twój scraper z tematu 12 zapisuje wyniki do
CSV. Gdyby zapisał je w kontenerze bez wolumenu — zniknęłyby razem
z kontenerem. Wolumen wynosi wyniki na zewnątrz.

**Typowe błędy początkujących:**
- Wpisywanie kluczy `ports:`/`volumes:` z PUSTĄ listą — jeśli usługa
  nie mapuje portów, klucza w ogóle nie powinno być w konfiguracji.
  W zadaniu 09 dodajesz te klucze do słownika tylko wtedy, gdy listy
  nie są puste.
- Odwrócenie stron dwukropka (kontener:host zamiast host:kontener).

---

## 7. Zazębienie — twoje projekty w kontenerze

Ostatnie zadania (11-13) łączą Dockera z tym, co już umiesz:

**Zadanie 11 — API w kontenerze.** Aplikację z `requests` (temat 11 —
tam nauczyłeś się pobierać dane z API) pakujesz w obraz: baza
`python:3.12-slim`, skopiowanie `requirements.txt`, instalacja
bibliotek, skopiowanie pliku aplikacji, CMD uruchamiające Pythona.
To dokładnie przykład z sekcji 3 — teraz złożysz go funkcjami.

**Zadanie 12 — Chrome w kontenerze.** Z tematu 17 znasz obiekt Options
Selenium i dodawanie do niego flag przeglądarki metodą `add_argument` —
tu tylko przypominam, nie tłumaczę od nowa. Nowość: w kontenerze Chrome
potrzebuje dwóch dodatkowych flag, których na zwykłym komputerze nie
używałeś:

- `--no-sandbox` — Chrome normalnie zamyka każdą stronę w "piaskownicy"
  (izolowanym pokoju zabaw) dla bezpieczeństwa. Do zbudowania
  piaskownicy potrzebuje uprawnień systemowych, których w kontenerze
  NIE MA — bez tej flagi Chrome w kontenerze w ogóle nie wystartuje.
- `--disable-gpu` — Chrome próbuje rysować strony kartą graficzną,
  a kontener karty graficznej nie ma. Flaga każe rysować procesorem.

Do tego znana ci flaga `--headless=new` (tryb bez okna) — w kontenerze
i tak nie ma ekranu, więc na serwerach CI (maszynach automatycznie
uruchamiających testy) używa się jej zawsze. W zadaniu 12 budujesz
listę tych flag: dwie obowiązkowe zawsze, headless warunkowo.

**Zadanie 13 — compose dla scrapera.** Scraper z tematu 12 zapisuje
wyniki do CSV. Budujesz konfigurację compose: usługa `scraper`
z obrazem i wolumenem wynoszącym folder wyników na zewnątrz kontenera.

---

## 8. Narzędzia Pythona w tym temacie

### 8.1. json.dumps — przypomnienie z tematu 7

`json.dumps(obiekt)` zamienia obiekt Pythona na NAPIS w formacie JSON.
Nowe zastosowanie: forma exec instrukcji CMD to dokładnie JSON, więc:

```python
import json

czesci = ["python", "app.py"]
print(json.dumps(czesci))   # ["python", "app.py"]
```

`json.dumps` sam wstawia cudzysłowy podwójne, przecinki i nawiasy —
dokładnie tak, jak wymaga Docker. Linia CMD to sklejenie napisu `"CMD "`
z wynikiem `json.dumps`.

**Typowe błędy początkujących:** użycie `str(czesci)` zamiast
`json.dumps(czesci)` — `str` da `['python', 'app.py']` z pojedynczymi
cudzysłowami, czyli NIE-JSON.

### 8.2. split(":") i sprawdzanie liczb — isdigit

Do sprawdzenia mapowania `"8000:80"` potrzebujesz dwóch narzędzi.

`napis.split(":")` — tnie napis na LISTĘ kawałków w miejscach
dwukropka (split znasz z pracy z plikami tekstowymi; tu tylko inny
separator):

```python
"8000:80".split(":")    # ["8000", "80"]
"8000".split(":")       # ["8000"]  — jeden kawałek, bo nie było ":"
"a:b:c".split(":")      # ["a", "b", "c"]  — trzy kawałki
```

Poprawne mapowanie po pocięciu ma DOKŁADNIE 2 kawałki — sprawdzisz to
przez `len(kawalki) != 2`.

`napis.isdigit()` — NOWA metoda napisu. **Co to jest?** Zwraca True,
gdy napis jest niepusty i składa się z SAMYCH cyfr:

```python
"8000".isdigit()    # True
"80a0".isdigit()    # False — jest litera
"".isdigit()        # False — pusty napis to nie liczba
```

**Skąd się wzięło?** Nazwa od "is digit" — "czy to cyfra". **Dlaczego
tak musi być?** `int("abc")` rzuciłoby wyjątek ValueError — `isdigit`
pozwala sprawdzić PRZED konwersją, bez try/except, i spokojnie zwrócić
None dla złych danych. **Typowe błędy początkujących:** wywołanie bez
nawiasów (`kawalek.isdigit` zamiast `kawalek.isdigit()`) — bez nawiasów
dostajesz obiekt metody, który w warunku zawsze jest "prawdziwy".

Po sprawdzeniu zamieniasz kawałki na liczby przez `int(kawalek)`.

### 8.3. Krotka (tuple) — para wartości jako wynik

**Co to jest?** Krotka to "lista, której nie można zmieniać", zapisywana
w nawiasach OKRĄGŁYCH: `(8000, 80)`. Spotkałeś ją przy `zip`
i `enumerate` w temacie 2 — teraz sam ją zwrócisz. Idealna na wynik
"para liczb: port hosta i port kontenera", bo para ma zawsze dokładnie
dwa elementy i nikt jej po drodze nie zmieni.

```python
para = (8000, 80)
para[0]    # 8000
para[1]    # 80
```

W teście porównuje się całe krotki wprost: `wynik == (8000, 80)`.

**Typowe błędy początkujących:** zwrócenie listy `[8000, 80]` zamiast
krotki — test `wynik == (8000, 80)` wtedy NIE przejdzie, bo lista
i krotka to różne typy.

### 8.4. Budowanie słownika warunkowo — `if lista:`

W zadaniu 09 klucz `"ports"` ma trafić do słownika TYLKO gdy lista
portów nie jest pusta. Wzorzec:

```python
konfiguracja = {"image": "moja-apka:1.0"}
porty = ["8000:80"]
if porty:
    konfiguracja["ports"] = porty
```

**Co robi `if porty:`?** W Pythonie pusta lista `[]` jest w warunku
traktowana jak False, a niepusta jak True. `if porty:` czyta się:
"jeśli lista porty COŚ zawiera". To zalecany przez PEP 8 zapis —
krótszy i czytelniejszy niż `if len(porty) > 0:` (oba działają tak
samo). Dodawanie klucza do istniejącego słownika
(`slownik["klucz"] = wartosc`) znasz z tematu 3.

**Typowe błędy początkujących:** `if porty is True:` — pusta lista to
NIE False (to osobny obiekt, który jedynie ZACHOWUJE SIĘ jak fałsz
w warunku), więc porównania z True/False tu nie działają. Piszemy po
prostu `if porty:`.

### 8.5. Sklejanie linii — "\n".join i " && ".join

`separator.join(lista_napisow)` skleja napisy z listy, wstawiając
separator MIĘDZY nie (join znasz z wcześniejszych tematów):

```python
" && ".join(["pip install -r requirements.txt", "pip list"])
# "pip install -r requirements.txt && pip list"

"\n".join(["FROM python:3.12-slim", "COPY app.py ."])
# "FROM python:3.12-slim\nCOPY app.py ."
```

`\n` to znak nowej linii — sklejenie linii przez `"\n".join` daje
wielolinijkowy tekst pliku, dokładnie to, czym jest Dockerfile.

**Typowe błędy początkujących:** doklejanie separatora na końcu
w pętli — `join` nie ma tego problemu, wstawia separator tylko
POMIĘDZY elementy.

### 8.6. Argument z wartością domyślną

W zadaniu 06 kontekst budowania ma domyślnie być kropką:

```python
def zbuduj_polecenie(nazwa: str, kontekst: str = ".") -> str:
```

`kontekst: str = "."` znaczy: jeśli wywołujący NIE poda kontekstu,
funkcja przyjmie `"."`. Wywołanie `zbuduj_polecenie("apka")` da
kontekst `"."`, a `zbuduj_polecenie("apka", "backend")` — `"backend"`.
PEP 8: przy adnotacji typu wokół `=` SĄ spacje (`kontekst: str = "."`).

---

## 9. Teoria testowa

### 9.1. Po co jest conftest.py i co robi sys.path.insert?

Gdy pytest uruchamia `test_docker_podstawy.py`, ten plik robi
`from docker_podstawy import ...`. Problem: Python szuka modułów tylko
w kilku znanych sobie miejscach (lista `sys.path`) — a folderu twojego
tematu na tej liście NIE MA. Bez pomocy import się wywali
(ModuleNotFoundError).

Ratunek to `conftest.py` — specjalny plik, który pytest znajduje
i wykonuje AUTOMATYCZNIE przed testami, bez importowania go przez
ciebie. Wstawiamy w nim folder tematu na początek listy miejsc
poszukiwań:

```python
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
```

Linijka po linijce:
- `__file__` — ścieżka do samego pliku conftest.py,
- `os.path.abspath(__file__)` — zamienia ją na pełną ścieżkę od
  początku dysku,
- `os.path.dirname(...)` — odcina nazwę pliku, zostaje sam folder,
- `sys.path.insert(0, ...)` — wstawia ten folder na POCZĄTEK listy
  (pozycja 0), więc Python zajrzy tu najpierw.

### 9.2. Schemat 3 pytań — zanim napiszesz jakikolwiek test

Do każdego testu odpowiadasz sobie na trzy pytania:

1. **Co testuję?** — którą funkcję i który jej obowiązek (jedno
   zachowanie na jeden test).
2. **Co udaję?** — czego test NIE robi naprawdę (sieć, pliki, czas)
   i czym to zastępuje. W tym temacie funkcje tylko budują napisy
   i słowniki, więc zwykle odpowiedź brzmi: "nic — czyste dane".
3. **Co sprawdzam?** — jaki konkretnie wynik uznaję za sukces (assert).

Docstring każdego testu w tym temacie ma te trzy odpowiedzi wypisane —
czytaj je PRZED wypełnianiem ciała.

### 9.3. Schemat przygotuj → podmień → wywołaj → sprawdź

Każde ciało testu układasz w cztery kroki (przykład celowo z INNEGO
tematu — funkcja budująca polecenie gita, żebyś nie miał gotowca):

```python
def test_buduje_polecenie_commit() -> None:
    """Co testuję: budowanie polecenia git commit z opisem.
    Co udaję: nic — funkcja tylko skleja napis.
    Co sprawdzam: wynik to dokładnie 'git commit -m "Add tests"'.
    """
    opis = "Add tests"                          # przygotuj
    # (podmień: nic do podmiany — czyste dane)  # podmień
    wynik = zbuduj_polecenie_commit(opis)       # wywołaj
    assert wynik == 'git commit -m "Add tests"' # sprawdź
```

- **przygotuj** — dane wejściowe,
- **podmień** — zastąp prawdziwe zależności atrapami (tu zwykle brak),
- **wywołaj** — JEDNO wywołanie testowanej funkcji,
- **sprawdź** — assert porównujący wynik z oczekiwaniem.

Przydatne formy asserta w tym temacie (wszystkie już znasz z poprzednich
tematów): `assert wynik == oczekiwane`, `assert wynik is None`,
`assert "COPY app.py ." in wynik` (czy napis zawiera fragment — `in` dla
napisów działa jak dla list), `assert "ports" not in wynik` (czy słownik
NIE ma klucza).

---

## 10. PEP 8 w tym temacie — szybka ściąga

- Dwie puste linie między funkcjami.
- Type hint na każdej funkcji, także testowej (`-> None`).
- Docstring z sekcjami Args/Returns; bez argumentów → w Args "Brak.".
- Porównania z None zawsze przez `is None`, nigdy `== None`.
- Importy: stdlib → third-party → local, grupy rozdzielone pustą linią
  (w tym temacie wystarczy stdlib: `json`).
- Kontrakt funkcji: jeden typ zwracany albo None — błąd sygnalizujemy
  przez None, nigdy napisem w stylu "błąd!".
