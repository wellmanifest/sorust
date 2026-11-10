---
{
  "schema": "wellmanifest.docs/document/v1",
  "id": "sorust-binary-standard",
  "kind": "information",
  "version": 10,
  "title": "Sorust 0.1: standard dwóch artefaktów",
  "status": "implemented",
  "owner": "wellmanifest/sorust",
  "scope": "repository",
  "created": "2026-11-09",
  "updated": "2026-11-10",
  "review_after": "2027-02-09",
  "source_revision": "38b30c63dbead064c9a8b85da260907e0c181abb",
  "affected_repositories": [
    "wellmanifest/sorust"
  ],
  "evidence": [
    "repo://wellmanifest/sorust/src/sorust/backend.py",
    "repo://wellmanifest/sorust/tests/test_build.py",
    "repo://wellmanifest/sorust/crates/sorust-kernel/src/lib.rs",
    "https://github.com/wellmanifest/sorust",
    "receipt:sorust-initial-ref-plan.7e901cfd9781e8596e6a56da24744b400052a82a42880e1a9f2f9a916ca85045",
    "https://github.com/subactor/onedev-agent/pull/934",
    "https://github.com/subactor/onedev-agent/pull/935",
    "https://github.com/subactor/validator-agent/actions/runs/42702186932",
    "receipt:initial-ref-accepted-f6be13bd4201f3ddb46a433f",
    "https://github.com/wellmanifest/sorust/blob/ccfdcdcbe3f712950da3ae2672a8ed912626d752/src/sorust/__init__.py",
    "https://github.com/wellmanifest/sorust/blob/ccfdcdcbe3f712950da3ae2672a8ed912626d752/tests/test_build.py",
    "https://github.com/wellmanifest/sorust/blob/d6917eb2c4097ac364a4e51bbebefcb9ac134b56/src/sorust/__init__.py",
    "https://github.com/wellmanifest/sorust/blob/d6917eb2c4097ac364a4e51bbebefcb9ac134b56/src/sorust/_compat.py",
    "https://github.com/wellmanifest/sorust/blob/d6917eb2c4097ac364a4e51bbebefcb9ac134b56/tests/test_build.py",
    "https://github.com/wellmanifest/sorust/blob/1fe08ce952c78506befaa2bee73691e7eb4bfaf2/src/sorust/backend.py",
    "https://github.com/wellmanifest/sorust/blob/1fe08ce952c78506befaa2bee73691e7eb4bfaf2/tests/test_build.py",
    "https://github.com/wellmanifest/sorust/blob/29420b36642880671111b0e05b2a8998c02f23b3/tests/test_build.py",
    "https://github.com/wellmanifest/sorust/blob/ec05144a7aa582fc646a61b4ff78aafefb08b443/src/sorust/__init__.py",
    "https://github.com/wellmanifest/sorust/blob/ec05144a7aa582fc646a61b4ff78aafefb08b443/src/sorust/__main__.py",
    "https://github.com/wellmanifest/sorust/blob/ec05144a7aa582fc646a61b4ff78aafefb08b443/tests/test_build.py",
    "https://github.com/wellmanifest/sorust/blob/38b30c63dbead064c9a8b85da260907e0c181abb/src/sorust/__init__.py",
    "https://github.com/wellmanifest/sorust/blob/38b30c63dbead064c9a8b85da260907e0c181abb/src/sorust/_compat.py",
    "https://github.com/wellmanifest/sorust/blob/38b30c63dbead064c9a8b85da260907e0c181abb/crates/sorust-kernel/src/lib.rs",
    "https://github.com/wellmanifest/sorust/blob/38b30c63dbead064c9a8b85da260907e0c181abb/include/sorust.h",
    "https://github.com/wellmanifest/sorust/blob/38b30c63dbead064c9a8b85da260907e0c181abb/tests/test_build.py",
    "https://github.com/wellmanifest/sorust/blob/38b30c63dbead064c9a8b85da260907e0c181abb/tests/benchmark_count_many.py",
    "receipt:sorust.batch-baseline.069cf83",
    "receipt:sorust.paired-batch.38b30c6",
    "https://doc.rust-lang.org/std/slice/fn.from_raw_parts.html",
    "https://doc.rust-lang.org/std/ptr/fn.write.html"
  ]
}
---

# Sorust 0.1: standard dwóch artefaktów

<!-- docs:section purpose -->
## Purpose

Sorust dostarcza wspólny kontrakt budowania dla bibliotek Wellmanifest `nl-*`: pozostały Python jako importowalne rozszerzenia oraz wydzielone, atomowe jądra Rust. Wersja 0.1 jest zbudowaną i przetestowaną implementacją referencyjną. Publikacja źródeł przechodzi chroniony PR; wydanie w rejestrze i migracje konsumentów pozostają osobnymi zadaniami.

<!-- docs:section scope -->
## Scope

HOME: `wellmanifest/sorust`, pakiet standardu i implementacja referencyjna. Każdy konsument zachowuje swoją semantykę, testy i odpowiedzialność. Standard nie zastępuje `wellmanifest/python`, `reuse` ani chronionego procesu publikacji.

<!-- docs:section evidence -->
## Evidence

Źródło implementacji: commit `fcfe82128748e23dc711b5d79ae776e8198a6306`. Testy budują wheel także z sdist, instalują go w osobnym venv, sprawdzają rozszerzenie, ABI, sumy kontrolne oraz klientów C, Rust i Python. Wynik pierwotnej walidacji: 21 testów pytest i dwa testy Cargo; wheel zbudowano również z sdist. Klient C używa dołączonego nagłówka. Odrzucono brakujące i zmodyfikowane artefakty oraz niezgodne ABI. Backend sprawdzono także w obcym pakiecie.



Pomiar lokalny na Linux x86_64 / CPython 3.13, Cython 3.3.1 i rustc 1.97.1: dla 155648 bajtów mediana pięciu serii po dziesięć wywołań wyniosła Python 19.90 ms, compiled-python 3.00 ms, Rust 0.214 ms, czyli około 93× względem referencyjnego Pythona. To mikrobenchmark funkcji, bez przypięcia CPU; nie mierzy całych procesów `nl-*` ani wielu małych wywołań. Digest źródeł build: `f3636ae9a13ca90806b054b528a558b6db6e449d1dd1d54ec9705d2d7c0f869a`.

Lokalne wyniki dystrybucji: `dist/sorust-0.1.0-cp313-cp313-linux_x86_64.whl` i `dist/sorust-0.1.0.tar.gz`. Testy i dokładne konfiguracje klientów: `tests/test_build.py`. Pełne wyniki maszynowe pozostają w prywatnych receiptach.

Korekta wiązania importu w źródle `ccfdcdcbe3f712950da3ae2672a8ed912626d752`: na bazie `4d3d97226fc8b29fb84ea8b61f42443d86cc2faa` odtworzono import `_compat.so` pominiętego w manifeście, mimo poprawnych sum pliku `listed_copy.so`. Runtime sprawdza teraz przed importem, czy wybrany natywny loader wskazuje plik wymieniony w zweryfikowanych wpisach `python-extension`, i porównuje pochodzenie zaimportowanego modułu. Cztery przypadki testu `test_compiled_import_requires_manifest_bound_native_module` zakończyły się PASS: nieujęta binarka, źródło `.py`, brak rozszerzenia i wcześniej zaimportowana nieujęta binarka. Test źródła potwierdza brak wykonania kodu `.py` przed odrzuceniem. Pełny zestaw walidacji korekty: 25 testów pytest PASS (47,32 s) oraz 2 testy Cargo PASS. Schemat manifestu i ABI C v1 pozostają zgodne.

Korekta bufora w źródle `d6917eb2c4097ac364a4e51bbebefcb9ac134b56`: na bazie `f6b9829ed488e0fc34b6b4c47130abc836d01d7e` stub Python zarejestrował długość 1024 dla rzeczywistego bufora 7 bajtów podklasy `bytes`; funkcji natywnej nie uruchamiano z tą długością. Zwykła podklasa dawała też Rust=2 i TypeError w compiled-python. Runtime i wzorzec Python normalizują teraz podklasy przez eksportowany bufor do niezmiennych `bytes`. Metody `__len__`, `__iter__`, `__bytes__` nie wyznaczają danych ani długości FFI. Zwykłe `bytes` zachowują ten sam obiekt bez dodatkowej kopii w adapterze. Siedem nowych testów zakończyło się PASS: bezpieczny stub nadmiernej długości, zachowanie tożsamości zwykłych bajtów oraz pięć wariantów zgodności wzorca, Rust i compiled-python. Test natywny nadpisanej długości używa wartości 0, aby również na błędnej bazie nie wykonywać odczytu poza buforem. Pełna walidacja korekty: 32 testy pytest PASS (17,51 s) i 2 testy Cargo PASS; ABI C i algorytm Rust zachowano.

Korekta wejścia blokady w źródle `1fe08ce952c78506befaa2bee73691e7eb4bfaf2`: baza `b0e9c9c13ce1e72476ce851b557189655e59dda3` akceptowała dowiązanie `Cargo.lock` poza projekt, a zmiana wyłącznie kontrolowanego pliku docelowego zmieniała digest źródeł. Odtworzenie nie uruchamiało Cargo ani skryptów budowania. Backend stosuje teraz istniejącą kontrolę zwykłego pliku, dowiązań i położenia także do `Cargo.lock`. Odrzuca dowiązania zarówno zewnętrzne, jak i wewnętrzne; zachowuje komunikat dla brakującej blokady. Trzy regresje zakończyły się PASS przez konfigurację i rzeczywiste wejście PEP 517 sdist, przed generowaniem C przez Cython i bez utworzenia sdist. Kontrola dotyczy jawnego wejścia blokady; nie stanowi ogólnego sandboxa Cargo. Pełna walidacja korekty: 35 testów pytest PASS (29,54 s) i 2 testy Cargo PASS; zwykłe pliki blokady zachowują dotychczasowy sposób budowania.

Rozszerzenie walidacji konsumenta w źródle `29420b36642880671111b0e05b2a8998c02f23b3`: rzeczywisty test obcej dystrybucji obejmuje teraz pojedynczy moduł oraz dwa moduły, w tym zagnieżdżony. Każdy wariant buduje sdist i wheel, sprawdza brak źródeł wybranych do kompilacji, zachowanie niewybranego modułu, wszystkie sumy binarek i nagłówka, a następnie uruchamia zainstalowane rozszerzenia oraz ABI obcego jądra Rust. Każdy wheel instaluje się ponownie, aby pip nie pozostawił poprzedniego wariantu o tej samej wersji. Pełna walidacja: 36 testów pytest PASS (32,45 s) i 2 testy Cargo PASS. Backend, runtime, ABI i zależności nie zmieniły się.

Osobny lokalny canary na bazie `23e6adcf2ed09803b552ad229bc0dc87cf2409eb` potwierdził rzeczywiste izolowane PEP 517: sdist → wheel z lokalnego wheelhouse przy `PIP_NO_INDEX=1`, dwa rozszerzenia Python (jedno zagnieżdżone), jedno Rust cdylib, selekcję źródeł i sumy binarek/nagłówka. Wheelhouse przygotowano wcześniej z Sorust 0.1.0, setuptools 84.2.1, wheel 0.48.0, Cython 3.3.1, build 1.6.1, packaging 26.3 i pyproject_hooks 1.3.3. Nowy venv konsumenta zawierał własny wheel bez Sorust, Cython i build; oba rozszerzenia oraz klient C linkujący zainstalowane jądro przeszły testy. Receipt: `receipt:sorust.isolated-adoption.23e6adc`; surowe logi i fixture są prywatne. To lokalny canary, nie zadeklarowana chroniona brama CI ani próba innych platform. Trwały test pytest używa `--no-isolation` z przygotowanymi zależnościami; oba rodzaje dowodów pozostają rozdzielone.

Eksport binarek w źródle `ec05144a7aa582fc646a61b4ff78aafefb08b443`: dodano `export_artifacts` i CLI `python -m sorust export` dla plików wskazanych w manifeście v1. 16 nowych testów przeszło (7,31 s): rzeczywista instalacja API/CLI, dokładne bajty i sumy eksportu, załadowanie rozszerzenia w czystym venv bez Sorust/Cython, klient C linkujący wyeksportowane Rust cdylib, odmowa nadpisania ośmiu wariantów istniejącego celu, brak wyjścia dla uszkodzonego/brakującego/uciekającego źródła i powtórzonej ścieżki, ponowne sprawdzenie snapshotu oraz brak manifestu po kontrolowanym błędzie kopiowania. Istniejące testy obcych konsumentów sprawdzają również eksport pakietów pojedynczych i zagnieżdżonych przez API. Pełna walidacja: 52 testy pytest PASS (19,33 s) i 2 testy Cargo PASS. Osobny lokalny canary CLI `--package-dir` wyeksportował rzeczywisty obcy pakiet z dwoma rozszerzeniami i zgodnymi sumami; receipt `receipt:sorust.foreign-export.ec05144`. Nie dodano zależności runtime ani zmian algorytmu i ABI.

Liczenie wsadowe w źródle `38b30c63dbead064c9a8b85da260907e0c181abb`: profil zainstalowanej bazy `069cf837755284b0a622ec25cc3b9a36bebe5dfd` wykazał koszt wielu przejść FFI. Dla 256 buforów po 3 B mediana dziewięciu rozgrzanych serii wyniosła Rust-scalar 290,42 µs i Python-reference 74,63 µs; dla 64 B Rust-scalar 345,74 µs. Receipt: `receipt:sorust.batch-baseline.069cf83`. Dodano `count_ascii_tokens_many` oraz addytywny symbol C `sorust_count_ascii_tokens_many_v1`; Rust otrzymuje połączone bajty i długości segmentów w jednym wywołaniu. Wariant compiled-python i referencja zachowują tę samą semantykę. Stare wywołanie skalarne ABI v1 pozostaje zgodne.

Walidacja źródła: 29 testów celowanych PASS (11,21 s), pełne 71 testów pytest PASS (33,90 s) i 5 testów Cargo PASS. Obejmuje losowe/NUL/UTF-8/puste dane, generatory i podklasy bytes, weryfikację importu obu API przed załadowaniem, brak opcjonalnego symbolu w starej bibliotece ABI v1, niezgodne długości i przepełnienia bez częściowego zapisu, C-klienta z niezainicjalizowaną tablicą wyników oraz eksport samodzielnego modułu Python z funkcją wsadową.

Pomiar publicznych adapterów w minimalnych venv (Linux x86_64, CPython 3.13.12, rustc 1.97.1, Cython 3.3.1): ta sama procedura uruchomiona dla starego wheel-a przed i po kandydacie, po dziewięć rozgrzanych serii, bez przypięcia CPU. Wariant Rust-many wlicza normalizację, łączenie bajtów, tablice ctypes i utworzenie listy wyników. Poniżej mediany dla 256 buforów w kandydacie z jednego wheel-a:

| Bajty/bufor | Rust-scalar, µs/paczka | Rust-many, µs/paczka | Przyspieszenie |
| --- | --- | --- | --- |
| 3 | 596,87 | 159,06 | 3,75× |
| 64 | 362,03 | 116,92 | 3,10× |
| 4096 | 910,02 | 786,72 | 1,16× |

Cel ≥2× dla 256 × 64 B został osiągnięty. Receipt `receipt:sorust.paired-batch.38b30c6` wiąże dokładny wheel, środowiska i próbki; kod odtwarzający: `tests/benchmark_count_many.py`. Czasy skalarne zmieniały się między seriami; cel porównano z pętlą skalarną tego samego wheel-a. To mikrobenchmark powtarzanych buforów, bez dowodu przyspieszenia rzeczywistych procesów `nl-*` ani gwarancji wyniku dla dowolnej paczki. Wcześniejsza seria z przygotowanego venv dała 3,84× dla 64 B; surowe wyniki obu serii pozostają prywatne.

<!-- docs:section content -->
## Content

| Reguła | Wymaganie |
| --- | --- |
| SORUST-001 | Konsument MUSI jawnie wskazać moduły `.py` do kompilacji i wersję backendu w `build-system.requires`; sama zależność runtime nie uruchamia kompilacji. |
| SORUST-002 | Każdy atomowy komponent budowany backendem MUSI dać rozszerzenie CPython oraz Rust `cdylib`. Wheel MUSI mieć tag interpretera i platformy; wybrane moduły `.py` nie są pakowane obok ich rozszerzeń. |
| SORUST-003 | Współdzielenie binarki Rust MUSI używać wersjonowanego ABI C: jawne rozmiary liczb, długości buforów, własność pamięci, kody błędów i funkcja wersji ABI. Panika nie może przekroczyć FFI. |
| SORUST-004 | Wheel MUSI zawierać `sorust-artifacts.json`: ścieżki, SHA-256 obu rodzajów binarek, ABI, SOABI Pythona, platformę, wersję rustc oraz digest źródeł. Nagłówki z `include/*.h` są pakowane i hashowane. |
| SORUST-005 | Produkcja MUSI jawnie używać natywnego backendu. Wybrane do importu rozszerzenie CPython MUSI odpowiadać zweryfikowanemu wpisowi `python-extension` przed jego załadowaniem; brak, nieujęty plik, źródło `.py`, rozbieżna suma lub ABI zatrzymują wywołanie. |
| SORUST-006 | Zmiana jądra MUSI przejść testy różnicowe względem zaakceptowanej semantyki oraz pomiar reprezentatywnych rozmiarów. Migracja kolejnych bottlenecków wymaga profilowania. |
| SORUST-007 | Jedno jądro ma jednego właściciela, własną wersję i jedną odpowiedzialność. Konsumenci MUSZĄ reużywać dystrybucję zamiast kopiować implementację. |
| SORUST-008 | Budowanie Rust używa `--release --locked --offline`. Sdist MUSI zawierać źródła, Cargo.lock i konfigurację backendu. `Cargo.lock` MUSI być zwykłym plikiem projektu, bez dowiązań także do innych plików wewnętrznych; zależności Cargo należy wcześniej dostarczyć do cache lub vendor. |
| SORUST-009 | Adapter Python MUSI przekazać do ABI C długość rzeczywistego, niezmiennego bufora. Podklasy `bytes` w `count_ascii_tokens` normalizuje się z bufora przed obiema implementacjami; zwykłe `bytes` zachowują ścieżkę bez dodatkowej kopii w adapterze. |
| SORUST-010 | Eksport plików z manifestu MUSI zweryfikować źródła przed utworzeniem nowego celu, zachować względne ścieżki i sumy oraz zapisać manifest po plikach. Nie wolno ponownie używać istniejącego katalogu, pliku ani dowiązania jako celu eksportu. |
| SORUST-011 | Wsad MUSI zachować kolejność i semantykę każdego bufora oraz odrzucić niespójne długości, przepełnienie sumy, zbyt duże rozmiary tablic i niedozwolone NULL przed zapisem wyników. Ważność i rozłączność pozostałych wskaźników należą do obowiązków klienta C. |

Pierwsze jądro `sorust-kernel` liczy tokeny bajtowe oddzielone dokładnie przez spację i bajty 9–13. Pozostałe bajty, w tym NUL i UTF-8, są nieprzezroczyste. To nie jest tokenizer modelu LLM.

`count_ascii_tokens(data: bytes, backend="rust")` używa Rust. `backend="compiled-python"` jawnie wybiera rozszerzenie Cython. Obie ścieżki mają identyczną semantykę; wzorzec `.py` pozostaje w źródłach i sdist.

Rust generuje również `.rlib` dla klientów używających zgodnego kompilatora i strategii panic. To opcjonalny wynik Cargo, nie przenośne ABI ani zawartość wheel-a. Współdzielenie między językami odbywa się przez `cdylib` i dołączony nagłówek.

### Wiele buforów w jednym wywołaniu

```python
from sorust import count_ascii_tokens_many
assert count_ascii_tokens_many([b"one two", b"three", b""]) == [2, 1, 0]
assert count_ascii_tokens_many([b"a", b"b"], backend="compiled-python") == [1, 1]
```

API przyjmuje iterable obiektów `bytes`, zachowuje kolejność i zwraca `list[int]`; pusta paczka daje `[]`, z wymaganymi artefaktami natywnymi także w tym przypadku. Podklasy bytes normalizuje się przez ich rzeczywisty bufor. Elementy innych typów powodują `TypeError`, nieznany backend — `ValueError`, brak/uszkodzenie wymaganej binarki lub brak nowego symbolu/metody — `NativeArtifactError`. Nie wykonuje się zastępczej pętli skalarnej przy braku obsługi wsadów.

Adapter materializuje iterable, łączy bajty do jednego bufora i tworzy tablice długości/wyników. Koszt tych alokacji i kopii jest wliczony w pomiary; wielkość paczki należy dobrać do pamięci i profilu konsumenta. Każdy segment liczy się osobno, także bez separatora na granicy. Wariant compiled-python sprawdza manifest i natywny loader raz dla całej paczki, zachowując dotychczasowe sprawdzanie każdego wywołania skalarnego.

W ABI C pozostaje wersja 1; dodatkowa deklaracja to:

```c
int32_t sorust_count_ascii_tokens_many_v1(const uint8_t *input, size_t length,
    const size_t *lengths, size_t count, uint64_t *output);
```

`count` długości musi sumować się dokładnie do `length`. Dla `count=0` wymagane jest `length=0`, a wszystkie wskaźniki mogą być NULL. Dla dodatniej liczby elementów tablice długości i wyników są nie-NULL i odpowiednio wyrównane; `input` może być NULL wyłącznie dla `length=0`. Pamięć wyjściowa jest wyłącznie zapisywalna na czas wywołania i rozłączna z niezmiennymi danymi i długościami. Może być niezainicjalizowana: implementacja używa surowego zapisu, zgodnie z [kontraktem ptr::write](https://doc.rust-lang.org/std/ptr/fn.write.html). Każdy odczytywany region pozostaje w jednej żywej alokacji, zgodnie z [wymaganiami slice::from_raw_parts](https://doc.rust-lang.org/std/slice/fn.from_raw_parts.html). Rozmiary tablic i sumy są sprawdzane przed zapisami, status 1 pozostawia wyniki bez zmian. Nienullowe wskaźniki nadal muszą wskazywać poprawną pamięć; ABI nie potrafi potwierdzić dowolnej ważności adresu. Starszy klient skalarny może używać nowej biblioteki; nowa funkcja wsadowa jawnie odrzuca starszą bibliotekę bez tego symbolu.

Benchmark po zainstalowaniu konkretnego wheel-a w venv:

```bash
python -I tests/benchmark_count_many.py --output batch-benchmark.json
```

W pracy nad repozytorium polecenie uruchamia się przez zatwierdzony `wellman run`, a wynik zapisuje pod prywatnym `.subactor/receipts/`. Benchmark zapisuje próbki, digest skryptu, manifest binarek i wersje środowiska; progów czasowych nie egzekwuje niedeterministyczny test pytest w CI.

### Eksport do współdzielenia binarek

Po zainstalowaniu wheel-a można uzyskać osobny katalog z rozszerzeniami CPython, Rust cdylib, nagłówkami i manifestem:

```bash
python -m sorust export ./sorust-bundle
```

```python
from sorust import export_artifacts, verify_artifacts
bundle = export_artifacts("./sorust-bundle-api")
manifest = verify_artifacts(bundle)
```

Obcy pakiet z manifestem `sorust.artifacts/v1` można wskazać przez `python -m sorust export ./component-bundle --package-dir /sciezka/do/pakietu` albo `export_artifacts("./component-bundle", package_dir="/sciezka/do/pakietu")`. Ścieżka źródłowa oznacza katalog zawierający `sorust-artifacts.json`, nie całe repozytorium. Eksport nie uruchamia kompilatorów ani nie ładuje kopiowanego kodu natywnego.

Rodzic celu musi istnieć, a sam cel musi być nowy. API zwraca bezwzględny `Path`, CLI wypisuje go na stdout. API zgłasza `NativeArtifactError` dla niepoprawnego źródła lub snapshotu, `FileExistsError` dla istniejącego celu i `OSError` dla błędów zapisu. CLI kończy takie błędy kodem 1; błędy składni argumentów obsługuje argparse. Puste katalogi, pliki i dowiązania również nie są nadpisywane. Kopiuje się tylko wpisy `artifacts` i `headers`; nie kopiuje się adapterów `.py`, danych pakietu ani opcjonalnego `.rlib`.

Manifest zachowuje dane o ABI, platformie, SOABI i źródłach. Snapshot bajtów sprawdza się ponownie przed utworzeniem wyjścia; manifest zapisuje się po plikach. Przerwany zapis może pozostawić częściowy katalog, którego nie należy używać bez udanej weryfikacji. To nie jest atomowa publikacja całego katalogu ani gwarancja trwałości po awarii systemu. Klient C korzysta z wyeksportowanego `_native/sorust.h` i `_native/libsorust_kernel.so`. Rozszerzenie Python wymaga zgodnego CPython/ABI; gotowy wheel pozostaje standardową drogą instalacji pełnego adaptera Python.

### Adopcja konsumenta

Dla istniejącego jądra wystarcza zależność runtime:

```toml
[project]
dependencies = ["sorust>=0.1.0,<0.2"]
```

```python
from sorust import count_ascii_tokens
count = count_ascii_tokens(prompt.encode("utf-8"))
```

Aby produkować własne dwa artefakty, konfiguracja konsumenta zawiera:

```toml
[build-system]
requires = ["sorust[build]==0.1.0", "setuptools>=77", "wheel>=0.45", "Cython>=3,<4"]
build-backend = "sorust.backend"

[tool.setuptools.packages.find]
where = ["src"]

[tool.sorust]
python-modules = ["nl_component._legacy"]
rust-manifest = "crates/nl-kernel/Cargo.toml"
rust-library = "nl_kernel"
artifact-package = "nl_component"
abi-version = 1
```

Standardowe pola `[project]` konsumenta pozostają wymagane przez setuptools. Nie dodawać `backend-path`: backend pochodzi z zależności, nie z lokalnej kopii Sorust. Własna dystrybucja MUSI dostarczyć adapter do swojego ABI; runtime `sorust.count_ascii_tokens` obsługuje wyłącznie jądro Sorust.

W crate ustawić `crate-type = ["cdylib", "rlib"]`, umieścić wersjonowane `extern "C"` i Cargo.lock. `MANIFEST.in` konsumenta musi zawierać:

```text
recursive-include crates *.toml *.lock *.rs
recursive-include include *.h
```

`python-modules` przyjmuje również kilka modułów, w tym zagnieżdżone, np. `["nl_component._legacy", "nl_component.nested._fast"]`. Wheel zawiera ich rozszerzenia i jedno jądro Rust. Usuwa się tylko źródła jawnie wybrane do kompilacji; niewybrane moduły pozostają zwykłym Pythonem. Pakiet nadal dostarcza własne pliki `__init__.py` lub deklaruje właściwą strukturę namespace.

Budować przez `python -m build`, z dostępnym kompilatorem C, nagłówkami CPython, Cargo i rustc. Zależności Cargo muszą być obecne lokalnie. Wybrane moduły `.py` muszą znajdować się pod `src/` i należeć do `artifact-package`; ABI v1 jest jedyną przyjmowaną wersją konfiguracji.

Sorust nie został opublikowany w PyPI. Do lokalnej adopcji najpierw zbudować wheel Sorust i dostarczyć go builderowi przez lokalny wheelhouse (`pip --find-links /sciezka/do/dist`), lub zainstalować wheel i zależności build w izolowanym venv, a następnie użyć `python -m build --no-isolation`.

Konsumenci gotowego wheel-a nie potrzebują Rust ani Cython. Klient C korzysta z `_native/sorust.h` i `_native/libsorust_kernel.so`; klient Rust może użyć tego samego ABI C albo `.rlib` z dokładnie zgodnego toolchaina. `.rlib` z profilu release wymaga `panic=abort` u klienta.


<!-- docs:section limitations -->
## Limitations

Walidacja obejmuje Linux x86_64 i CPython 3.13. Chroniony Publisher opublikował wyłącznie seed governance `ea1bf67895e4ca2abda99d44fc8a538b01470350` na `main`. Niezależny Validator w uruchomieniu [42702186932](https://github.com/subactor/validator-agent/actions/runs/42702186932) potwierdził wszystkie 138 plików, dokładny zestaw refów i digest drzewa. Receipt `receipt:initial-ref-accepted-f6be13bd4201f3ddb46a433f` ma wynik `accepted`; źródło workflow: `9c964d217274233ef9e4ec5f3113859498f8b045`.

Sam etap walidacji zakończył się sukcesem. Cały workflow ma wynik `failure`, ponieważ GitHub odrzucił zapis obu attestation dla prywatnego repozytorium w obecnym planie organizacji. Dowód odebrano z uwierzytelnionego, niezmiennego artefaktu GitHub nr `13713060849`; SHA-256 archiwum `4e0b004a1d5c550bd770cba099285d994e1bf6dba1f2f400e9d0fc36fde2fa1f` zgadza się z metadanymi API. To transport artefaktu workflow; podpisana attestation nie jest dostępna. Chroniony Validator zachowuje odpowiedzialność za niezależną decyzję o scaleniu PR implementacji.

Profil przeglądu Sorust wymaga `governance / enforce` i `governance / remote lifecycle`. Ich wykonanie oraz zatwierdzenie muszą dotyczyć aktualnego HEAD PR. Pełna adopcja chronionej bramy Docs nie jest skonfigurowana; układ, metadane i indeks kontroluje się lokalnie. Brak canary manylinux, macOS, Windows, innych interpreterów oraz porównania na rzeczywistych zadaniach `nl-*`. Suma kontrolna wykrywa drift, nie uwierzytelnia wydawcy; zaufanie do wheel-a wymaga oddzielnej proweniencji. Ładowanie i import są buforowane w procesie. Cython nie gwarantuje przyspieszenia dowolnego kodu Python ani obsługi każdej dynamicznej konstrukcji. Nie deklarujemy bitowej odtwarzalności między hostami.

<!-- docs:section next_actions -->
## Next Actions

Właściciele konsumentów wybierają bottleneck na podstawie profilu, dodają testy zgodności i adoptują wydany pakiet zgodnie z instrukcją adopcji powyżej. Zmiany ABI wymagają nowego numeru ABI i jawnej migracji. Chroniona publikacja i macierz platform pozostają oddzielnymi krokami przed szeroką adopcją.


Ścieżka dla istniejącego publicznego repozytorium została niezależnie opublikowana w kontrolerze przez [PR934](https://github.com/subactor/onedev-agent/pull/934), merge `a0dfebf0d2826c59bf0759adad64736e7dccad6a`, i dokładną politykę [PR935](https://github.com/subactor/onedev-agent/pull/935), merge `b40bc32a5b5a2a7f54996f2b0d6bb1e67a62bec4`. Zasady prywatnego bootstrapu zachowano. Kontroler sprawdził bajty obu modułów względem zatwierdzonego źródła, wystawił jednorazowy grant dla planu `7e901cfd9781e8596e6a56da24744b400052a82a42880e1a9f2f9a916ca85045`, a Publisher odczytał wynik publikacji. Właścicielska zależność to `subactor/onedev-agent / PLF-22278`.

Pierwsza implementacja została niezależnie scalona przez [PR1](https://github.com/wellmanifest/sorust/pull/1) jako `4d3d97226fc8b29fb84ea8b61f42443d86cc2faa`. Korekty importu i bufora zostały niezależnie scalone w [PR2](https://github.com/wellmanifest/sorust/pull/2) jako `f6b9829ed488e0fc34b6b4c47130abc836d01d7e` i [PR3](https://github.com/wellmanifest/sorust/pull/3) jako `b0e9c9c13ce1e72476ce851b557189655e59dda3`. Korektę Cargo.lock scalono przez [PR4](https://github.com/wellmanifest/sorust/pull/4) jako `23e6adcf2ed09803b552ad229bc0dc87cf2409eb`. Walidację wielu modułów scalono przez [PR5](https://github.com/wellmanifest/sorust/pull/5) jako `37c7389400d26ec504e4156a381e6c8dda2c47bf`. Eksport binarek scalono przez [PR6](https://github.com/wellmanifest/sorust/pull/6) jako `069cf837755284b0a622ec25cc3b9a36bebe5dfd`. Każda następna zmiana, w tym wsady w ticket-007, wymaga własnych bram i niezależnego zatwierdzenia aktualnego HEAD przed scaleniem. Przygotowane wheel i sdist pozostają lokalnymi artefaktami do późniejszego, osobno autoryzowanego wydania.
