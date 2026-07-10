# conftest.py — pytest wykonuje ten plik automatycznie przed testami.
# Zadanie pliku: dopisać folder tematu do listy miejsc, w których Python
# szuka modułów, żeby test_docker_podstawy.py widział docker_podstawy.py
# (szczegóły: teoria.md, sekcja 9.1).

# TODO: zaimportuj os oraz sys (dwa osobne importy, stdlib)

# TODO: dodaj sys.path.insert wskazujący na folder tematu:
#   pozycja 0, a ścieżkę zbuduj z __file__ przez os.path.abspath
#   i os.path.dirname (kolejność jak w teoria.md, sekcja 9.1)
