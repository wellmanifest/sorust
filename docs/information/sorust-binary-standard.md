---
{
  "schema": "wellmanifest.docs/document/v1",
  "id": "sorust-binary-standard",
  "kind": "information",
  "version": 21,
  "title": "Sorust 0.1: standard dwóch artefaktów",
  "status": "implemented",
  "owner": "wellmanifest/sorust",
  "created": "2026-11-09",
  "updated": "2026-11-10",
  "review_after": "2027-02-09",
  "source_revision": "82055601c3803ab16238112e5c3e645cf0e4385a",
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
    "https://doc.rust-lang.org/std/ptr/fn.write.html",
    "https://github.com/wellmanifest/sorust/blob/50293859eebd1c706c078a1d6fde0e453c29cc2c/src/sorust/__init__.py",
    "https://github.com/wellmanifest/sorust/blob/50293859eebd1c706c078a1d6fde0e453c29cc2c/tests/test_build.py",
    "https://github.com/wellmanifest/sorust/blob/50293859eebd1c706c078a1d6fde0e453c29cc2c/tests/benchmark_count_many.py",
    "receipt:sorust.stream-baseline.ef788e9",
    "receipt:sorust.stream-memory.5029385",
    "https://github.com/wellmanifest/sorust/pull/7",
    "https://github.com/wellmanifest/sorust/pull/8",
    "https://github.com/wellmanifest/sorust/blob/2d5f63baeb62394a4460894e649b6a80b548d9b7/src/sorust/backend.py",
    "https://github.com/wellmanifest/sorust/blob/2d5f63baeb62394a4460894e649b6a80b548d9b7/tests/test_build.py",
    "receipt:sorust.rebuild-baseline.b102941",
    "receipt:sorust.rebuild-validation.2d5f63b",
    "https://github.com/wellmanifest/sorust/blob/eefdb1cae1f8aa30343f416f2e78653db879e8f8/src/sorust/backend.py",
    "https://github.com/wellmanifest/sorust/blob/eefdb1cae1f8aa30343f416f2e78653db879e8f8/tests/test_build.py",
    "receipt:sorust.rebuild-skip-build.124c1b4",
    "receipt:sorust.rebuild-validation.eefdb1c",
    "https://github.com/wellmanifest/sorust/blob/7a87f03b6e15796081578af655e6e5e59fbf5f9f/tests/test_build.py",
    "receipt:sorust.package-init-baseline.bf83dc5",
    "receipt:sorust.package-init-targeted.7a87f03",
    "https://github.com/wellmanifest/sorust/pull/9",
    "receipt:sorust.package-init-validation.7a87f03",
    "https://github.com/wellmanifest/sorust/blob/db0851e278fd35ff894a5069daf439489512130b/src/sorust/__init__.py",
    "https://github.com/wellmanifest/sorust/blob/db0851e278fd35ff894a5069daf439489512130b/tests/test_build.py",
    "https://github.com/wellmanifest/sorust/blob/db0851e278fd35ff894a5069daf439489512130b/tests/benchmark_prepared_counter.py",
    "receipt:sorust.compiled-call-baseline.04e38d5",
    "receipt:sorust.prepared-counter-targeted.db0851e",
    "https://github.com/wellmanifest/sorust/pull/10",
    "receipt:sorust.prepared-counter-validation.db0851e",
    "receipt:sorust.prepared-counter-performance.db0851e",
    "https://github.com/wellmanifest/sorust/blob/f1e93f11bfba382cd55fd268d908047c5089387d/src/sorust/backend.py",
    "https://github.com/wellmanifest/sorust/blob/f1e93f11bfba382cd55fd268d908047c5089387d/tests/test_build.py",
    "receipt:sorust.build-script-baseline.ea3b05b",
    "https://doc.rust-lang.org/cargo/reference/manifest.html#the-build-field",
    "receipt:sorust.build-script-targeted.f1e93f1",
    "receipt:sorust.build-script-validation.f1e93f1",
    "https://github.com/wellmanifest/sorust/blob/9cd707bff4ab5c71d2e53f35eefd807467d6822f/tests/benchmark_nl_dsl_pilot.py",
    "https://github.com/wellmanifest/sorust/blob/9cd707bff4ab5c71d2e53f35eefd807467d6822f/tests/test_nl_dsl_pilot.py",
    "https://github.com/wellmanifest/nl-dsl-llm/blob/aa47c8752f1ea446208f6dfb7a018ad02e92250a/standard/nl_dsl_llm.py",
    "receipt:sorust.nl-dsl-build-baseline.16e802b",
    "receipt:sorust.nl-pilot-targeted.9cd707b",
    "receipt:sorust.nl-pilot-validation.9cd707b",
    "receipt:sorust.nl-pilot-practical.9cd707b",
    "https://github.com/wellmanifest/sorust/blob/7a2ce11ad410b0428acb04154c1fdc0668f518b4/src/sorust/backend.py",
    "https://github.com/wellmanifest/sorust/blob/7a2ce11ad410b0428acb04154c1fdc0668f518b4/src/sorust/__init__.py",
    "https://github.com/wellmanifest/sorust/blob/7a2ce11ad410b0428acb04154c1fdc0668f518b4/tests/test_resources.py",
    "receipt:sorust.resource-baseline.55bb710",
    "receipt:sorust.resources-targeted.7a2ce11",
    "receipt:sorust.resources-validation.7a2ce11",
    "receipt:sorust.resources-practical.7a2ce11",
    "receipt:sorust.resources-compatibility.7a2ce11",
    "https://github.com/wellmanifest/sorust/pull/14",
    "https://github.com/wellmanifest/sorust/blob/60b35e493443b0fd0153b27d4913fba0a8943cf6/src/sorust/backend.py",
    "https://github.com/wellmanifest/sorust/blob/60b35e493443b0fd0153b27d4913fba0a8943cf6/tests/test_prebuilt_component.py",
    "receipt:sorust.prebuilt-baseline.e78ce82",
    "receipt:sorust.prebuilt-targeted.60b35e4",
    "receipt:sorust.prebuilt-validation.60b35e4",
    "receipt:sorust.prebuilt-practical.60b35e4",
    "receipt:sorust.prebuilt-compatibility.60b35e4",
    "https://github.com/wellmanifest/sorust/pull/15",
    "https://github.com/wellmanifest/sorust/blob/5fe81a150284a81e3422855a9d8864d046648d0f/tests/benchmark_nl_dsl_pilot.py",
    "https://github.com/wellmanifest/sorust/blob/5fe81a150284a81e3422855a9d8864d046648d0f/tests/test_nl_dsl_pilot.py",
    "receipt:sorust.isolation-baseline.78c0f69",
    "https://github.com/wellmanifest/sorust/blob/4faed7fdd072ffffc4c32578ea2062848274d79f/tests/benchmark_nl_dsl_pilot.py",
    "https://github.com/wellmanifest/sorust/blob/4faed7fdd072ffffc4c32578ea2062848274d79f/tests/test_nl_dsl_pilot.py",
    "receipt:sorust.isolation-practical.4faed7f",
    "receipt:sorust.isolation-missing-cython.corrected",
    "receipt:sorust.isolation-pip-probe.5fe81a1",
    "receipt:sorust.isolation-validation.4faed7f",
    "receipt:sorust.isolation-default-regression.4faed7f",
    "receipt:sorust.isolation-unchanged-sdk.4faed7f",
    "https://github.com/wellmanifest/sorust/pull/16",
    "https://github.com/wellmanifest/sorust/blob/82055601c3803ab16238112e5c3e645cf0e4385a/src/sorust/__init__.py",
    "https://github.com/wellmanifest/sorust/blob/82055601c3803ab16238112e5c3e645cf0e4385a/tests/test_rust_components.py",
    "receipt:sorust.native-component-baseline.8de2464",
    "receipt:sorust.native-component-targeted.8205560",
    "receipt:sorust.native-component-validation.8205560",
    "receipt:sorust.native-component-practical.8205560",
    "receipt:sorust.native-component-compatibility.8205560"
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

Iterator ograniczający paczki w źródle `50293859eebd1c706c078a1d6fde0e453c29cc2c`: kontrolowany generator 4096 różnych buforów po 4096 B na zainstalowanej bazie `ef788e90d9dce61c559418416b8d49c4a8b6ca66` wymagał mediany 34050649 B alokacji Python w eager-many (receipt `receipt:sorust.stream-baseline.ef788e9`). Nowe `iter_ascii_token_counts` pobiera paczki i używa istniejącego API natywnego. 19 testów celowanych PASS (9,28 s), pełne 90 testów pytest PASS (76,64 s) i 5 testów Cargo PASS. Testy obejmują leniwe pobieranie, ograniczenie prefetcha, argumenty, błędy źródła i elementów, brak artefaktów nawet dla pustego źródła, zachowanie własności źródła oraz rzeczywistą zgodność Rust/compiled-python. Testy Cargo wykonano przed zmianą wyłącznie typów adaptera; kod Rust nie zmienił się.

Porównanie obu API z tego samego wheel-a kandydata w minimalnym venv, Linux x86_64 / CPython 3.13.12: trzy serie z rozgrzanym jądrem, 4096 × 4096 B, nowe `bytes(bytearray(payload))` przy każdym pobraniu, wyniki konsumowane przez `sum`, paczka iteratora 256. Każda seria daje checksum 8388608.

| API | Mediana szczytu alokacji Python, B | MiB |
| --- | --- | --- |
| `count_ascii_tokens_many` | 34050665 | 32,47 |
| `iter_ascii_token_counts` | 2140233 | 2,04 |

Iterator osiągnął 6,29% szczytu eager-many (spadek 93,71%), spełniając lokalny cel ≤10%. Receipt `receipt:sorust.stream-memory.5029385` wiąże źródło, dokładny wheel, digest skryptu, manifest i próbki. `tracemalloc` mierzy alokacje Python, nie RSS całego procesu. To generator kontrolowany, bez dowodu na rzeczywiste procesy `nl-*`, gwarancji stałej liczby bajtów ani celu czasowego. Pomiary czasu podczas śledzenia pamięci nie służą ocenie przyspieszenia. Wersja 11 uzupełnia historyczne ustalenia wersji 10; nie zmienia jądra Rust, ABI C ani obu istniejących API.

Korekta ponownego budowania w źródle `2d5f63baeb62394a4460894e649b6a80b548d9b7`: na bazie `b10294160915d5507e8a50ace6a78f2a9db7feeb` dwie budowy wheel-a w tym samym drzewie konsumenta ujawniły stary moduł natywny. Po zmianie `python-modules` z `legacy` na `fresh` i źródła legacy z wartości 10 na 11 drugi wheel zawierał zarówno aktualne `legacy.py`, jak i stare, niewymienione w nowym manifeście `legacy.so`. Rzeczywisty import po instalacji zwracał 10. Receipt: `receipt:sorust.rebuild-baseline.b102941`. To odtworzenie lokalnego błędu pakowania, bez migracji rzeczywistego konsumenta.

Backend tworzy teraz własny tymczasowy katalog dla każdego hooka `build_wheel`. Polecenia setuptools `build` i `bdist_wheel` kierują do niego odpowiednio `build_lib` i katalog instalacji wheel-a. Dzięki temu stare wyniki kompilacji oraz pliki pozostawione po przerwanym pakowaniu nie stają się zawartością nowej paczki. Katalog jest usuwany po wyjściu z hooka, również przy wyjątku. Cache kompilatorów Cython/Cargo i wcześniejsze katalogi build pozostają do ponownego użycia; nie wykonuje się ich czyszczenia. Hooki metadanych i sdist, runtime, Rust i ABI nie zmieniły się. Wersja 12 uzupełnia ustalenia wersji 11.

Walidacja korekty: pełne 92 testy pytest PASS (153,64 s) i 5 testów Cargo PASS. Dwa przypadki regresji budują dwukrotnie w tym samym drzewie konsumenta, zmieniają wybór modułu do kompilacji, a poprzednio kompilowany moduł odpowiednio zmieniają lub usuwają. Każdy przypadek dodatkowo zasiewa zawartość poprzedniego wheel-a w konwencjonalnym katalogu pakowania, odwzorowując przerwany starszy build. Sprawdzono brak starych rozszerzeń/źródeł, sumy bieżącego manifestu i rzeczywiste zachowanie po instalacji drugiego wheel-a. Zachowano testy pojedynczych/zagnieżdżonych modułów, sdist, eksportu i API scalar/many/stream. Receipt: `receipt:sorust.rebuild-validation.2d5f63b`.

Uzupełnienie w źródle `eefdb1cae1f8aa30343f416f2e78653db879e8f8`: kontrolowany hook wheel-a z opcją setuptools `--skip-build` na HEAD `124c1b4dc7e954eebf3b860ef57dd263f89db3d3` zakończył się kodem 0, tworząc archiwum zawierające wyłącznie cztery pliki dist-info, bez modułów i manifestu. Receipt: `receipt:sorust.rebuild-skip-build.124c1b4`. Świeży staging wymaga wykonania budowy; backend odrzuca teraz tę opcję jawnym `ValueError` przed pakowaniem. Wersja 13 zachowuje ustalenia wersji 12 i dodaje tę granicę kontraktu hooka; publiczne API runtime i ABI pozostają zgodne.

Końcowa walidacja źródła `eefdb1cae1f8aa30343f416f2e78653db879e8f8`: 93 testy pytest PASS (86,51 s), w tym oba przypadki przebudowy ze starą zawartością i rzeczywisty hook odrzucający `--skip-build` bez utworzenia wheel-a. 5 testów Cargo PASS dotyczy niezmienionego kodu Rust. Receipt: `receipt:sorust.rebuild-validation.eefdb1c`. Wcześniejszy wynik 92 testów powyżej odnosi się do historycznej rewizji korekty stagingu.

Walidacja inicjalizatorów pakietów w źródle `7a87f03b6e15796081578af655e6e5e59fbf5f9f`: odczytana baza `bf83dc5a5da2eae33d3c7a666679e8dd3a5223d9` już poprawnie kompiluje wybrany `__init__.py`, zachowując import względny, `__package__` i `__path__` (receipt `receipt:sorust.package-init-baseline.bf83dc5`). Nie odtworzono usterki runtime. Dodany trwały wariant konsumenta buduje sdist i wheel z czterema rozszerzeniami, w tym inicjalizatorami pakietu głównego i zagnieżdżonego, oraz jednym Rust cdylib. Test celowany PASS (16,05 s, 93 pozostałe pominięte) potwierdził brak wybranych źródeł `.py`, zachowanie niewybranego modułu Python w wheel-u, wszystkie sumy manifestu i nagłówka oraz semantykę pakietu po instalacji.

Ten sam eksport z czterema rozszerzeniami działa w nowym venv bez Sorust i Cython. Wyeksportowany pakiet nie zawiera `.py`; normalne importy CPython uruchamiają inicjalizatory i ich skompilowane zależności, zachowując ścieżki pakietów i importy względne. Test wykonuje również rzeczywiste wywołanie Rust C ABI z eksportowanego cdylib. Receipt `receipt:sorust.package-init-targeted.7a87f03` wiąże manifest i wynik. Backend, runtime, ABI i zależności pozostają bez zmian; wersja 14 uzupełnia instrukcję i dowody wersji 13, bez nowej deklaracji platformowej ani pomiaru przyspieszenia.

Pełna walidacja tej rewizji: 94 testy pytest PASS (83,87 s) oraz 5 testów Cargo PASS; receipt `receipt:sorust.package-init-validation.7a87f03`. Zakres obejmuje poprzednie regresje budowania, importów, eksportu i API scalar/many/stream oraz nowy wariant czterech rozszerzeń i samodzielnego Rust cdylib. W tej zmianie modyfikowano wyłącznie testy i dokumentację.

Przygotowany licznik w źródle `db0851e278fd35ff894a5069daf439489512130b`: profil zainstalowanej bazy `04e38d529532538ee9adbeb38b509bf95fc052e5` wykazał koszt powtarzanej weryfikacji i wyboru rozszerzenia dla małych danych. Dla 64 B mediana siedmiu rozgrzanych serii wyniosła 1,861 ms dla publicznego compiled-python i 0,378 µs dla już zweryfikowanej funkcji natywnej. Receipt: `receipt:sorust.compiled-call-baseline.04e38d5`. To mikrobenchmark bez przypięcia CPU, nie wynik procesów `nl-*`. Dodano jawną funkcję `prepare_ascii_token_counter`, zwracającą callable związany z natywnym wejściem. Weryfikacja i wybór następują podczas przygotowania, a kolejne wywołania nie czytają plików.

Dziesięć testów celowanych PASS (26,23 s) i 5 testów Cargo PASS. Pokrycie obejmuje brak artefaktów/wejścia, niepoprawny backend, tożsamość zwykłych bytes, długości rzeczywistego bufora podklas, utrzymanie uchwytu CDLL, status błędu FFI, losowe/NUL/UTF-8/puste dane oraz równoległe wywołania obu backendów. Test zmienia wyłącznie niemapowany nagłówek: przygotowany licznik zachowuje działające wiązanie, natomiast jawny audyt i nowe przygotowanie odrzucają drift. Istniejący scalar compiled-python nadal odrzuca taką zmianę przy kolejnym wywołaniu. Receipt: `receipt:sorust.prepared-counter-targeted.db0851e`. Testy nie modyfikują wykonywalnych, załadowanych binarek. Wersja 15 uzupełnia wersję 14; dotychczasowe API, jądro Rust, ABI i zależności pozostają zgodne.

Pełna walidacja źródła: 104 testy pytest PASS (201,57 s) i 5 testów Cargo PASS, receipt `receipt:sorust.prepared-counter-validation.db0851e`. Źródła istniejących funkcji scalar/many/stream, weryfikacji, eksportu i loaderów pozostają identyczne z bazą. Nowe przygotowanie nie zmienia ich dotychczasowego sprawdzania.

Porównanie publicznych API w jednym wheel-u, osobny minimalny venv na Linux x86_64 / CPython 3.13.12, siedem rozgrzanych serii. Poniżej mediany kolejnych wywołań compiled-python; przygotowanie licznika jest wyłączone z tych czasów:

| Bajty | Public scalar, µs | Prepared, µs | Stosunek czasów |
| --- | --- | --- | --- |
| 3 | 1973.34 | 0.389 | 5070.9× |
| 64 | 2235.74 | 0.350 | 6384.7× |
| 4096 | 1719.98 | 46.366 | 37.1× |

Cel ≥20× dla 64 B został osiągnięty (6384,7× w tym pomiarze). Porównywane API mają różny jawny moment audytu: public scalar ponawia sprawdzanie, prepared wykorzystuje wcześniej zweryfikowane wiązanie. To nie jest przyspieszenie tej samej polityki odczytu plików ani całego procesu `nl-*`. Mediana osobno mierzonego przygotowania po rozgrzaniu wyniosła 1,514 ms dla compiled-python i 1,238 ms dla Rust; zimnego ładowania nie mierzono. Rust dla 64 B dał 2,184 µs public i 2,143 µs prepared; nie deklaruje się nowego przyspieszenia dla Rust. Brak przypięcia CPU, małe powtarzane bufory i zmienność próbek ograniczają wniosek do tej lokalnej procedury. Receipt `receipt:sorust.prepared-counter-performance.db0851e` wiąże dokładny wheel, manifest, digest skryptu i wszystkie próbki. Pomiary wykonano po zakończeniu pełnego zestawu testów; próg nie jest bramą czasową CI.

Korekta odcisku skryptu Cargo w źródle `f1e93f11bfba382cd55fd268d908047c5089387d`: na bazie `ea3b05b39810b0add6b8d21e3fbd486d9432b96d` dwie budowy zmieniające wyłącznie `build.rs` dały różne biblioteki Rust i wynik funkcji 49 → 50, ale identyczny `source_sha256` (`88ab6ec654dfd6103fcdebdaf4e273376490bedc301de9cfc0e46304cbfe65f3`). Receipt `receipt:sorust.build-script-baseline.ea3b05b` wiąże oba wheel-e, skrypty i wynik osobnych procesów. Sumy samych artefaktów działały poprawnie; brak dotyczył zestawu źródeł manifestu. Wersja 16 zachowuje historyczne ustalenia wersji 15 i uzupełnia kontrakt źródeł.

Walidacja źródła: 17 testów celowanych PASS (211,26 s), pełny zestaw 121 testów pytest PASS (345,51 s) i 5 testów Cargo PASS. Testy domyślnego skryptu, jawnego `true`, własnej lokalizacji i ścieżki do współdzielonego pliku budują sdist → wheel dwukrotnie; zmiana wyłącznie skryptu zmienia odcisk, hash biblioteki i rzeczywisty wynik Rust. Osobne procesy ładują oddzielne pliki, bez zapisu do mapowanej biblioteki. Sprawdzane są obecność skryptu w sdist i sumy wszystkich artefaktów. Dalsze przypadki obejmują brak/wyłączenie skryptu, błędne typy, brak jawnego wejścia, katalog, ścieżki absolutne/wychodzące poza projekt i symlinki pliku/rodzica, z odmową przed utworzeniem `build`. Receipty: `receipt:sorust.build-script-targeted.f1e93f1`, `receipt:sorust.build-script-validation.f1e93f1`. Runtime, jądro, nagłówek i ABI zachowują bajty bazy; zmienił się backend budowania i testy.

Pilot deweloperski w źródle `9cd707bff4ab5c71d2e53f35eefd807467d6822f` rozszerza walidację backendu Sorust o rzeczywisty, niezmieniony moduł normatywny `standard/nl_dsl_llm.py` z przypiętego wejścia `wellmanifest/nl-dsl-llm@aa47c8752f1ea446208f6dfb7a018ad02e92250a`. Nie modyfikuje repozytorium konsumenta ani jego kanonicznej specyfikacji. Buduje lokalną dystrybucję próbną `sorust-nl-dsl-pilot==0.0.0` z nakładką PEP 517; nie stanowi migracji lub wydania właściwego projektu. Wersja 17 zachowuje historyczne ustalenia wersji 16.

Walidacja narzędzia: 19 testów pilota PASS (1,65 s), 121 niezmienionych regresji rdzenia Sorust PASS i 5 testów Cargo PASS. Pełne wywołanie pytest na `8af2e367d892d499330fc11b794db3754152d0e3` dało 138 PASS (501,89 s); późniejsze wzmocnienie powiązania wejściowego wheel-a z faktycznie reużytymi bajtami binarek pokrywa komplet 19 testów na `9cd707bff4ab5c71d2e53f35eefd807467d6822f`. Źródła i testy rdzenia pozostały identyczne. Łącznie pokryto 140 unikalnych aktualnych przypadków; nie oznaczamy tego jako pojedynczego przebiegu 140 testów na końcowym HEAD. Receipt `receipt:sorust.nl-pilot-validation.9cd707b` wiąże oba XML, rewizje i sprawdzenie niezmienności.

Końcowy pilot na checkout `b7731eae9cd88b50eb2ea3680e5cb7cc457a3ebe`, z identycznymi bajtami skryptu `9cd707b…`, przeszedł po 8 oryginalnych testów zgodności w każdym z trzech trybów. Zgodne są obserwacje parsera, serializacji i wyników mostka; hashe `.so` w wheel-u i eksporcie są identyczne. Działa wspólna wyeksportowana biblioteka Rust oraz osobny klient `.rlib` z wynikiem `3 3 0`. Obiecanego zasobu JSON brakuje w samym eksporcie binarek, a jawne dostarczenie przypiętego pliku przywraca działanie. Raport SHA-256 `cf44cbf094b34c5f0c350e2dfb3a89786c174267cbe25c5f21d2920dec6ff483`, receipt `receipt:sorust.nl-pilot-practical.9cd707b`, wiąże wejścia, binarki i pełne serie.

Pomiary pilota na Linux x86_64 / CPython 3.13.12: mediana siedmiu rozgrzanych serii po 1000 powtórzeń całego wskazanego korpusu, w µs na korpus. Wszystkie trzy procesy pracują w tym samym minimalnym venv, kolejno po zakończeniu testów i kompilacji tego zadania.

| Korpus | Źródło Python | Wheel `.so` | Eksport `.so` |
| --- | ---: | ---: | ---: |
| Parser, 15 wejść | 3253,33 | 3033,93 | 3171,53 |
| Parse → canonical, 5 poleceń | 25,57 | 24,22 | 31,60 |
| Mostek, 4 żądania w pamięci | 407,39 | 383,13 | 236,62 |

Ilorazy median source/wheel wynoszą odpowiednio 1,072×, 1,056× i 1,063×. Rozrzut jest duży: parser source 3071,70–5189,93 µs, wheel 1059,05–4900,61 µs; ten sam kod `.so` daje również różne wyniki wheel/export. Ten pomiar nie ustala wiarygodnej przewagi czasowej 6–7% ani przewagi eksportu. Potwierdza pakowanie i zgodność konkretnego modułu; zysku w produkcji nie zmierzono. W profilu 15000 wywołań parsera wystąpiło 471000 `re.search` i 465000 `re.escape`; samo przeniesienie otaczającego kodu do Cython nie usuwa tej pracy.

Dla tego samego zgodnego podzbioru krótkich wejść, w procesie wheel-a, Rust batch z UTF-8 i przygotowaniem buforów miał medianę 13,85 µs, a Python `split()` 3,33 µs — około 4,16× krócej po stronie Python. W pozostałych dwóch procesach narzut Rust wyniósł około 3,10× i 4,07×. To pomiar granicy wywołania na małych danych, nie samej pętli Rust ani długich buforów. Cztery próby separatorów Unicode dały Python=2 i Rust=1, z zachowaniem argumentu `status=OPEN` przez oryginalny parser. Pilot nie zmienia algorytmu konsumenta ani nie podstawia niezgodnej semantyki.

Zasoby paczki w źródle `7a2ce11ad410b0428acb04154c1fdc0668f518b4`: na bazie `55bb710930d9d83d31c9dd5d9a221872c813af08` kopia rzeczywistego wheel-a NL przyjmowała zmianę wyłącznie whitespace w `semantic-profile.json` bez błędu `verify_artifacts`, a eksport pomijał ten plik. To granica dotychczasowego formatu v1, który nie deklarował zasobów, bez obejścia hashowania binarek. Receipt `receipt:sorust.resource-baseline.55bb710` wiąże hashe przed/po i obserwacje. Wersja 18 dodaje jawne zasoby i format manifestu v2; historyczne pomiary oraz manualny tryb pilota z wersji 17 pozostają zapisane.

43 testy celowane PASS (74,18 s) i 5 testów Cargo PASS. Test dwukrotnie buduje sdist → wheel z czterema skompilowanymi modułami, bez deklaracji package-data i z `include-package-data=false`: JSON w katalogu głównym i binarny plik danych w podpakiecie trafiają do sdist, wheel-a i eksportu. Zmiana samego JSON-a zmienia odcisk źródeł i wynik skompilowanej funkcji. Eksport działa w nowym venv bez Sorust/Cython. Pozostałe przypadki obejmują niepoprawne/niekanoniczne/zastrzeżone ścieżki, brak pliku, symlinki pliku i rodzica, kolizje manifestu, checksum drift oraz ponowną kontrolę snapshotu przed utworzeniem wyjścia. Receipt: `receipt:sorust.resources-targeted.7a2ce11`.

Pełna walidacja źródła `7a2ce11…`: 183 testy pytest PASS (340,19 s) i 5 testów Cargo PASS, receipt `receipt:sorust.resources-validation.7a2ce11`. Poza dodaną obsługą metadanych/zasobów algorytmy natywne i ABI C pozostały bez zmian.

Rzeczywisty pilot `--manifest-resources` na checkout `b33a5c701b7a8d97a55d9519c2fc6850a8c782d3`, z kodem identycznym z `7a2ce11…`, zbudował oryginalny moduł NL z przypiętego commitu `aa47c8752f1ea446208f6dfb7a018ad02e92250a`. Nowy manifest v2 wskazuje `semantic-profile.json` o SHA-256 `7319797e7283808622da6e4afed1b34dc564c0c7a6a720084a68c60674cf2eda`. Plik dotarł do eksportu bez ręcznej kopii, import w minimalnym venv działa, a kontrolowana zmiana whitespace została odrzucona przez audyt. Po przywróceniu zatwierdzonych bajtów ponownie przeszły po 8 oryginalnych testów w trybach źródłowym, wheel i eksport (24 wykonania), z takimi samymi obserwacjami. Reużycie wspólnego Rust `.so` i istniejącego `.rlib` dało oczekiwane wyniki. Użyto `--number 10` wyłącznie do kontroli funkcjonalnej; nie wyprowadza się nowego wniosku czasowego. Raport SHA-256 `df3b92fb7146091a32854eb1456afae447d5850427512d59123663f169d87b26`, receipt `receipt:sorust.resources-practical.7a2ce11`.

Test rzeczywistego starszego czytnika odczytał kod runtime z wcześniej dostarczonego wheel-a bazy `55bb710` (SHA-256 wheel-a `a07007b64d575551e5a9a3ba67e8ee525dfdd0711abce95d99b2a7b7e843bc76`, kod runtime `b3f44e56206a823978423862a8dc3c83607113701377c66ea8dd0f587d8b181c`). Oba wywołania — weryfikacja i eksport paczki v2 — zakończyły się `NativeArtifactError: unsupported manifest or ABI`, bez utworzenia celu eksportu. Ten czytnik zaakceptował nową paczkę bez zasobów w v1, a nowy runtime zaakceptował rzeczywistą starszą paczkę v1. Receipt: `receipt:sorust.resources-compatibility.7a2ce11`.

Tryb komponentu zainstalowanego w źródle `60b35e493443b0fd0153b27d4913fba0a8943cf6`: baza `e78ce82c3100dfedf178cddaed0439ffbd38b687` odrzucała konfigurację i budowała Rust ponownie. Nowe 33 testy przeszły (45,28 s), pełne 216 testów pytest przeszło (251,67 s), 5 testów Cargo przeszło. Testy sprawdzają konfigurację, tożsamość, własność, drift, dowiązania, zmianę podczas audytu, snapshot i odcisk niezależny od ścieżki instalacji. Dwa rzeczywiste przepływy sdist → wheel, bez crate i lokalnych nagłówków, działają z blokującymi stubami `cargo`/`rustc`, dla konsumentów z zasobem i bez niego. Pakiet dawcy w testach metadanych zgłasza błąd przy próbie importu, a weryfikacja go nie importuje. Stary czytnik z dokładnej bazy v18 zweryfikował i wyeksportował oba rzeczywiście zbudowane warianty v1/v2 z addytywnym `rust_component`; nowy czytnik potwierdził wyniki. Receipty: `receipt:sorust.prebuilt-validation.60b35e4`, `receipt:sorust.prebuilt-compatibility.60b35e4`.

Próba `--prebuilt-rust --manifest-resources --number 10` na niezmienionych plikach NL z `aa47c8752f1ea446208f6dfb7a018ad02e92250a` dała zgodne wyniki i 8 oryginalnych funkcji conformance w każdym z trzech trybów, 24 wykonania łącznie. Podczas budowy sdist/wheel konsumenta stuby Rust zarejestrowały zero wywołań. Sdist nie zawiera crate, nagłówków dawcy ani binarek; manifest v2 wiąże zasób, jego drift jest odrzucany, a eksport nie wymaga ręcznego sidecara. Rust cdylib i nagłówek są identyczne z dawcą. Pin manifestu dawcy: `f85ef29bb5ffb3b0614220c0d4d84c2f86b569e4a001e8137263907c1b7faffb`; digest źródeł dawcy: `a798b61112fa7f8b3f1d138c3b659345a67ca138e64e6b8d1cdc32a28086c670`. Oddzielny klient istniejącego `.rlib` o SHA-256 `7905f052716c60e4c42c772549359c7fc46ab696e453db4f695e7641c5365170` zwrócił `[3, 3, 0]`. Receipt `receipt:sorust.prebuilt-practical.60b35e4` wiąże raport o SHA-256 `030fcd96e39bc54f6ea804feb9986769cfa95181776fc07a69123afa270ae23f`. Krótki przebieg potwierdza zgodność i reużycie; nie dowodzi przyspieszenia. Nie zmieniono algorytmu, ABI ani repozytorium konsumenta.

Izolowany pilot w źródle `4faed7fdd072ffffc4c32578ea2062848274d79f`: dotychczasowy pilot z bazy `78c0f69dcda83f60469bbddbbee65838f2339734` budował wyłącznie w przygotowanym środowisku. Pierwsza próba nowego trybu `5fe81a1` zbudowała oba artefakty, lecz trafnie odrzuciła deklarację braku wywołań Rust: pip ze świeżego venv pięciokrotnie odpytuje `rustc --version` przy tworzeniu user agent. Jądro nie było ponownie kompilowane. Poprawiony pilot udostępnia frontendowi prywatny PATH narzędzi C i sprawdza niedostępność Cargo/rustc, zamiast akceptować lub ukrywać te sondy. Receipt: `receipt:sorust.isolation-pip-probe.5fe81a1`.

Rzeczywista próba offline na tych samych plikach NL `aa47c8752f1ea446208f6dfb7a018ad02e92250a` przechodzi dwa izolowane środowiska PEP 517: sdist oraz wheel z sdist. Frontend `build 1.6.1` nie zawiera Sorust, Cython ani setuptools przed budową; Cargo i rustc nie są dostępne na jego PATH. Snapshot zawiera siedem istniejących wheel-i: Sorust 0.1.0, Cython 3.3.1, setuptools 84.2.1, wheel 0.48.0, build 1.6.1, packaging 26.3 i pyproject_hooks 1.3.3. SDK wejściowy ma SHA-256 `6616b6a73efce67e54a966f3f06b11e909a3bd7a93b28dfc0f0a57b2fbfff985`. Wyniki źródła, instalacji i eksportu są zgodne; 8 oryginalnych funkcji conformance przechodzi w każdym trybie, 24 wykonania łącznie. Biblioteka Rust, nagłówek i zasób konsumenta zachowują przypięte bajty. Sdist nie zawiera Rust, nagłówków dawcy ani binarek. Raport o SHA-256 `663f9476fe0b01689124f0b7a013e181c6ced88f5da7575179836758081ef660` wiąże pełen inwentarz wejść i dowody; receipt `receipt:sorust.isolation-practical.4faed7f`.

Oddzielny świeży przebieg z sześcioma wheel-ami, po usunięciu Cython, kończy się oczekiwanym błędem rozwiązywania zależności w izolowanym środowisku, mimo dostępności Cython w głównym venv. Nie powstaje wheel i nie są wywoływane narzędzia Rust. Receipt `receipt:sorust.isolation-missing-cython.corrected` wiąże obserwację braku pakietów/narzędzi frontendu i hash logu odmowy. To kontrola zależności lokalnych; nie rozszerza macierzy platform, nie migruje źródeł NL i nie stanowi pomiaru przyspieszenia. SDK, runtime, schematy manifestów i ABI nie zmieniają się w tej zmianie narzędzia.

Końcowa walidacja poprawionego źródła: 36 testów pilota PASS (17,20 s), pełne 233 testy pytest PASS (312,00 s) oraz 5 testów Cargo PASS dla niezmienionego jądra. Osobny domyślny przebieg bez izolacji przeszedł kolejne 24 wykonania oryginalnych testów zgodności; digest wyników semantycznych i wejściowy wheel SDK są identyczne z przebiegiem izolowanym. Receipt `receipt:sorust.isolation-validation.4faed7f` wiąże pełną końcową wersję testów; `receipt:sorust.isolation-default-regression.4faed7f` wiąże porównanie trybów. Runtime/backend/crate/konfiguracja budowania są identyczne z bazą, co sprawdzono względem Git i bajtów SDK (`receipt:sorust.isolation-unchanged-sdk.4faed7f`). Dlatego finalny wheel SDK i `.rlib` można reużyć bez ponownej kompilacji, a sdist zawiera aktualne narzędzie i dokumentację.

Samodzielny komponent Rust w źródle `82055601c3803ab16238112e5c3e645cf0e4385a`: baza `8de2464d896f336e3c27a35cc0001696416973ee` odrzucała weryfikację i eksport Rust-only przed utworzeniem wyjścia. Nowy format przechodzi 76 testów celowanych (25,66 s), pełne 273 testy pytest (276,20 s) i 5 testów Cargo. Testy obejmują dokładne pola i role, hashe, ścieżki, dowiązania metadanych/root/payloadu, duplikaty, drift, zgodność starych schematów oraz brak możliwości zastąpienia domyślnego SDK formatem Rust-only. Rzeczywisty Python-free wheel instaluje się jako osobna dystrybucja; metadata lookup bez importu pakietu, eksport oraz klient C ABI v1 przechodzą. Receipt: `receipt:sorust.native-component-validation.8205560`.

Próba na niezmienionym NL `aa47c8752f1ea446208f6dfb7a018ad02e92250a` użyła osobnego `sorust-kernel-component-pilot==0.0.0` jako zadeklarowanej zależności budowania. Wheel `py3-none-linux_x86_64` ma SHA-256 `b09433c55142f88570acaea958a34a88885f67c3f4c33a6735de9cba596553dd`, zawiera tylko Rust, nagłówek, manifest i metadane, a hash jego manifestu wynosi `ca4ebfd72a569b5490f9513a0dd7a9953a9134fdc7427c18f1b031e39b861369`. Zachowany digest źródeł SDK wynosi `b0a5dc235f76cc0b86357778c10919c55ff83b9cf17bbcd0ff5b6be6bc485ac0`. Osiem wheel-i trafia do prywatnego snapshotu; dystrybucja komponentu nie jest wcześniej zainstalowana we frontendzie. Izolowane sdist → wheel działa bez Cargo/rustc na PATH. Każdy z trzech trybów źródło/instalacja/eksport przechodzi 8 oryginalnych testów conformance, 24 wykonania łącznie; Rust i nagłówek są identyczne z wejściowym SDK. Raport ma SHA-256 `31eca23b9c48c3b12d7c72ff7640b5d607a280c3f6f18785b374463ee3902439`; receipt `receipt:sorust.native-component-practical.8205560`. To próba zgodności i reużycia z 10 iteracjami, bez nowego wniosku czasowego.

Rzeczywisty stary czytnik z bazy v20 odrzuca nowego dawcę w verify/export, pozostawiając brak celu. Ten sam czytnik poprawnie audytuje nowy SDK v1 oraz audytuje i eksportuje rzeczywisty wynik NL v2 z proweniencją nowego dawcy. Potwierdza to oddzielenie nowego formatu zależności od zachowanego kontraktu artefaktów konsumenta; receipt `receipt:sorust.native-component-compatibility.8205560`. Nie zmieniono jądra Rust, ABI, zależności ani źródeł konsumenta.

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
| SORUST-012 | Iterator MUSI zachować kolejność, pobierać co najwyżej `batch_size` elementów do bieżącej paczki i sprawdzić obsługę natywną przed pobraniem źródła. Nie wywołuje `close()` na źródle należącym do klienta. Błąd nieukończonej paczki nie udostępnia jej częściowych wyników. |
| SORUST-013 | Backend MUSI składać każdy wheel z aktualnych źródeł i konfiguracji w świeżym stagingu, oddzielonym od wcześniejszych katalogów biblioteki i pakowania. Wycofany z kompilacji moduł wraca jako bieżący Python, jeżeli jego źródło istnieje; usunięty moduł nie może przetrwać przez cache poprzedniej budowy. |
| SORUST-014 | Przygotowany licznik MUSI audytować artefakty podczas przygotowania i utrzymywać uchwyt biblioteki przez czas użycia. Kontrakt MUSI jawnie odróżniać ten audyt od kolejnych wywołań bez odczytu plików; audyt ani nowe przygotowanie nie stanowią hot reload kodu w procesie. |

Pierwsze jądro `sorust-kernel` liczy tokeny bajtowe oddzielone dokładnie przez spację i bajty 9–13. Pozostałe bajty, w tym NUL i UTF-8, są nieprzezroczyste. To nie jest tokenizer modelu LLM.

`count_ascii_tokens(data: bytes, backend="rust")` używa Rust. `backend="compiled-python"` jawnie wybiera rozszerzenie Cython. Obie ścieżki mają identyczną semantykę; wzorzec `.py` pozostaje w źródłach i sdist.

Rust generuje również `.rlib` dla klientów używających zgodnego kompilatora i strategii panic. To opcjonalny wynik Cargo, nie przenośne ABI ani zawartość wheel-a. Współdzielenie między językami odbywa się przez `cdylib` i dołączony nagłówek.

### Przygotowany licznik dla częstych wywołań

```python
from sorust import prepare_ascii_token_counter

count = prepare_ascii_token_counter(backend="compiled-python")
assert count(b"one two") == 2
assert count(b"") == 0
```

`prepare_ascii_token_counter(*, backend="rust") -> Callable[[bytes], int]` sprawdza backend i wymagane artefakty podczas przygotowania. Niepoprawny backend daje `ValueError`; brak/uszkodzenie pliku, niezgodne ABI albo brak wywoływalnego wejścia compiled-python — `NativeArtifactError`. Rust audytuje pliki również wtedy, gdy jądro zostało już zbuforowane w procesie. Loader compiled-python zachowuje dotychczasowe wiązanie do zweryfikowanej binarki przed importem.

Callable przechowuje natywne wejście oraz uchwyt CDLL dla Rust. Przyjmuje tylko `bytes`, odrzuca inne typy przez `TypeError`, normalizuje podklasy przez rzeczywisty bufor i nie kopiuje zwykłych bytes w adapterze. Każde wywołanie Rust ma własny wynik uint64; nie współdzieli bufora wyjściowego z innymi wywołaniami. Niezerowy status FFI daje `NativeArtifactError`.

Kolejne wywołania zachowują wiązanie i nie powtarzają sprawdzania plików. To jawny wybór dla wielokrotnych wywołań w workerze: licznik przygotowuje się raz, a koszt audytu ponosi podczas tworzenia. `verify_artifacts()` lub nowe przygotowanie wykrywa późniejszy drift plików. Loader CPython i CDLL nadal korzysta z pamięci podręcznej procesu; ponowny audyt nie przeładowuje wcześniej załadowanego kodu. Zmiana załadowanej binarki wymaga nowego procesu. Dotychczasowe funkcje scalar/many/stream zachowują swoje zasady sprawdzania; Rust już buforuje jądro i nie ma tu nowego celu przyspieszenia dla Rust.

Odtwarzalny benchmark publicznych API: `python -I tests/benchmark_prepared_counter.py --output .subactor/receipts/prepared-counter-benchmark.json`, w repozytorium przez zatwierdzony `wellman run`, po instalacji konkretnego wheel-a. Zapisuje siedem rozgrzanych serii, pełny manifest, digest skryptu, środowisko oraz osobny koszt przygotowania po rozgrzaniu. Ten koszt nie obejmuje zimnego ładowania i nie wchodzi do czasów kolejnych wywołań. Progów czasowych nie dodano do pytest ani chronionej bramy CI.

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

### Iterator o ograniczonej wielkości paczki

```python
from sorust import iter_ascii_token_counts

values = (value for value in [b"one two", b"three", b""])
assert list(iter_ascii_token_counts(values, batch_size=2)) == [2, 1, 0]
```

`iter_ascii_token_counts(inputs, *, batch_size=256, backend="rust")` zwraca `Generator[int, None, None]`, obsługujący `close()`. Konstrukcja sprawdza backend oraz wielkość paczki, lecz nie wywołuje nawet `iter(inputs)`. Wielkość używa protokołu indeksu całkowitego (`SupportsIndex`), wyklucza `bool` i musi należeć do `1..sys.maxsize`. Błędny typ daje `TypeError`, zakres lub backend — `ValueError`.

Pierwsze pobranie sprawdza natywną obsługę wsadów wybranego backendu na pustej paczce przed dotknięciem źródła. Puste źródło również wymaga działających artefaktów; brak obsługi nie powoduje zastępczego wykonania Python ani skalarnego. Rust i compiled-python zachowują semantykę oraz normalizację podklas bytes z `count_ascii_tokens_many`.

Iterator pobiera całą paczkę przed zwróceniem pierwszego wyniku tej paczki. Następna paczka jest pobierana dopiero po wydaniu wszystkich wyników poprzedniej. Wyjątek źródła lub niepoprawny element kończy iterator: poprawne wcześniejsze paczki mogły już wydać wyniki, ale błędna/nieukończona paczka nie wydaje żadnego. Kursor źródła może przy tym przesunąć się o całą paczkę. Zamknięcie wyników nie pobiera kolejnych danych i nie wywołuje `close()` na źródle; niewydane wyniki już pobranej paczki są porzucane. Klient zachowujący źródło może nadal go używać, a za jego zamknięcie odpowiada sam.

Ograniczenie dotyczy liczby elementów w paczce i ich łącznych bajtów. Duży pojedynczy bufor lub źródło buforujące dane samodzielnie nadal może wymagać dużo pamięci. Gwarancja nie obejmuje stałego limitu bajtów ani niezależnego zarządzania pamięcią producenta. Pomiar odtwarza się z zainstalowanym wheel-em przez zatwierdzony `wellman run` i polecenie `python -I tests/benchmark_count_many.py --memory --output .subactor/receipts/stream-memory-benchmark.json`; receipt i surowe próbki pozostają prywatne. Progów czasu/pamięci nie dodano do pytest jako niestabilnej bramy CI.

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

Obcy pakiet z manifestem `sorust.artifacts/v1`, `sorust.artifacts/v2` lub `sorust.rust-component/v1` można wskazać przez `python -m sorust export ./component-bundle --package-dir /sciezka/do/pakietu` albo `export_artifacts("./component-bundle", package_dir="/sciezka/do/pakietu")`. Ścieżka źródłowa oznacza katalog zawierający `sorust-artifacts.json`, nie całe repozytorium. Eksport nie uruchamia kompilatorów ani nie ładuje kopiowanego kodu natywnego.

Rodzic celu musi istnieć, a sam cel musi być nowy. API zwraca bezwzględny `Path`, CLI wypisuje go na stdout. API zgłasza `NativeArtifactError` dla niepoprawnego źródła lub snapshotu, `FileExistsError` dla istniejącego celu i `OSError` dla błędów zapisu. CLI kończy takie błędy kodem 1; błędy składni argumentów obsługuje argparse. Puste katalogi, pliki i dowiązania również nie są nadpisywane. Kopiuje się wpisy `artifacts`, `headers` i zadeklarowane `resources` w v2; pomija się niewymienione adaptery `.py`, dane pakietu i opcjonalne `.rlib`.

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

### Skrypt budowy Cargo i odcisk źródeł

Backend uwzględnia skrypt wybrany przez `[package].build` w `Cargo.toml`: brak pola wykrywa istniejący `build.rs` w katalogu crate, `true` wymaga tego pliku, niepusty względny ciąg wskazuje własny skrypt, a `false` wyłącza wybór. Domyślny plik, własną ścieżkę i wyłączenie opisuje [dokumentacja Cargo](https://doc.rust-lang.org/cargo/reference/manifest.html#the-build-field); zachowanie jawnego `true` zweryfikowano lokalnie z Cargo 1.97.1.

Wybrany skrypt musi być zwykłym plikiem wewnątrz projektu, bez symlinków w ścieżce. Sorust dopuszcza `../shared-build.rs`, jeżeli wynikowa ścieżka pozostaje w projekcie. Brak jawnie wskazanego pliku, ścieżka absolutna lub wychodząca poza projekt oraz niepoprawny typ powodują błąd konfiguracji przed Cython i Cargo. Ścieżkę po normalizacji oraz bajty wybranego skryptu dodaje się do `source_sha256` tylko wtedy, gdy pliku nie objęto już dotychczasowym zbiorem źródeł. Projekt bez skryptu zachowuje wcześniejszy odcisk; wyłączony `build.rs` w katalogu crate nie jest dodatkowym wejściem.

Konsument MUSI umieścić skrypt w sdist, także przy własnej nazwie lub lokalizacji. Powyższe `recursive-include crates *.rs` obejmuje testowane skrypty `.rs` pod `crates/`; inne lokalizacje lub rozszerzenia wymagają odpowiedniego wpisu konsumenta. Odcisk nadal obejmuje określony zbiór: pyproject, źródła Python, manifest i lockfile crate, jego `src/**/*.rs`, nagłówki, wybrany skrypt i jawnie zadeklarowane zasoby. Nie śledzi dowolnych plików odczytywanych przez skrypt, środowiska ani pełnego grafu zależności Cargo; nie stanowi deklaracji hermetycznej budowy. Schemat manifestu i ABI pozostają w wersji 1.

`python-modules` przyjmuje również kilka modułów, w tym zagnieżdżone, np. `["nl_component._legacy", "nl_component.nested._fast"]`. Wheel zawiera ich rozszerzenia i jedno jądro Rust. Usuwa się tylko źródła jawnie wybrane do kompilacji; niewybrane moduły pozostają zwykłym Pythonem. Pakiet zachowuje odpowiednie inicjalizatory lub właściwą strukturę namespace; jawnie wybrane `__init__.py` można również kompilować jak poniżej.

### Gotowy komponent Rust jako zależność budowania

Konfiguracja wymaga dokładnie jednego z `rust-manifest` albo `rust-component`. W drugim trybie konsument zachowuje zwykłe `python-modules`, `rust-library`, `artifact-package` i `abi-version`, usuwa `rust-manifest` oraz wskazuje już zainstalowaną dystrybucję:

```toml
[tool.sorust]
python-modules = ["nl_component.__init__", "nl_component._legacy"]
rust-library = "sorust_kernel"
artifact-package = "nl_component"
abi-version = 1

[tool.sorust.rust-component]
distribution = "sorust"
version = "0.1.0"
package = "sorust"
manifest-sha256 = "<dokładny SHA-256 bajtów sorust/sorust-artifacts.json>"
```

W miejsce opisu SHA wpisuje się 64 małe znaki hex. Dystrybucja dawcy musi być jawnie dostarczona przez `[build-system].requires` i frontend budowania; sam backend niczego nie pobiera ani nie instaluje. Gdy dawcą jest Sorust, może to być ten sam wheel, który dostarcza backend. Wersja 0.1.0 nie jest opublikowana w rejestrze: lokalny wheelhouse i pin dokładnych bajtów wheel-a muszą dostarczać implementację obsługującą tę opcję. Starszy backend odrzuca nową konfigurację.

Backend używa `importlib.metadata`, bez importu pakietu dawcy i bez ładowania Rust podczas budowy. Sprawdza nazwę i dokładną wersję dystrybucji, własność manifestu oraz wybranych plików według listy zainstalowanej dystrybucji, hash manifestu, wszystkie artefakty przez `verify_artifacts`, zgodność przypiętych bajtów z wynikiem audytu oraz pakiet, platformę, ABI i nazwę biblioteki. Odrzuca dowiązania w ścieżkach manifestu i kopiowanych plików, brak proweniencji kompilatora/źródeł, zadeklarowane zasoby dawcy oraz nagłówki poza bezpośrednim `_native/*.h`. Lokalne `include/*.h` konsumenta są niedozwolone w tym trybie.

Po audycie ponownie sprawdza hashe i tworzy snapshot wyłącznie Rust cdylib i nagłówków. Rozszerzenia Python dawcy podlegają audytowi, lecz nie są kopiowane ani wykonywane. Snapshot trafia do nowego wheel-a konsumenta; odcisk źródeł wiąże jego wejścia z bajtami przypiętego manifestu i snapshotu pod stałymi nazwami, bez ścieżki instalacji dawcy. Budowa konsumenta nie uruchamia `cargo` ani `rustc`; nadal potrzebuje Cython, kompilatora C i nagłówków CPython. Crate, `Cargo.lock` oraz lokalne nagłówki nie są potrzebne konsumentowi. Backend nie dodaje binarek dawcy do sdist: zawiera on źródła konsumenta i piny zależności. To nie jest filtr dowolnych binarek ręcznie dołączonych przez autora projektu.

Addytywne pole manifestu `rust_component` zapisuje `distribution`, `version`, `package`, `manifest_sha256` i `source_sha256` dawcy; pole `rustc` zachowuje jego kompilator. Jest to informacja o pochodzeniu, bez uwierzytelnienia wydawcy. Lista wymaganych plików i zasady ich audytu pozostają w istniejącym schemacie: v1 bez zasobów konsumenta, v2 z zasobami. Czytnik v18 nadal audytuje i eksportuje te manifesty. Wheel i eksport są samodzielne, z prywatnymi kopiami wspólnych bajtów; nie gwarantują jednej współdzielonej instancji w procesie.

Pin odnosi się do konkretnego zainstalowanego wheel-a i platformy. Sdist z takim pinem nie jest automatycznie przenośny między platformami ani wersjami CPython. Testowany zakres pozostaje Linux x86_64 / CPython 3.13. Zmiana dawcy wymaga jawnej aktualizacji pinów i ponownej walidacji konsumenta; powrót do `rust-manifest` zachowuje dotychczasową drogę budowania.

### Samodzielny komponent Rust

Manifest `sorust.rust-component/v1` opisuje osobnego dawcę biblioteki Rust. Jest przyjmowany przez `verify_artifacts(package_dir)` i eksport z jawnym `package_dir` / `--package-dir`; domyślny audyt i eksport własnego SDK Sorust nadal wymagają formatu dual v1/v2. Własne API SDK nie może w ten sposób utracić wymogu obu artefaktów. Nowy format nie zmienia schematów v1/v2 ani ABI C v1.

Manifest zawiera dokładnie osiem pól:

| Pole | Kontrakt |
| --- | --- |
| `schema` | `sorust.rust-component/v1` |
| `abi_version` | Liczba całkowita 1, z wykluczeniem boolean |
| `package` | Kanoniczna nazwa pakietu zgodna z konfiguracją `rust-component` |
| `platform` | Niepusta deklaracja platformy; backend wymaga zgodności z builderem |
| `rustc` | Niepusta informacja o kompilatorze źródłowego artefaktu |
| `source_sha256` | 64 małe znaki hex, digest zadeklarowanych źródeł producenta |
| `headers` | Lista wpisów z dokładnymi kluczami `path`, `sha256`, może być pusta |
| `artifacts` | Dokładnie jeden wpis `kind="rust-cdylib"` z `path` i `sha256` |

Biblioteka ma bezpośrednią, kanoniczną ścieżkę `_native/<plik>.so`, `.dylib` lub `.dll`; nagłówki `_native/<plik>.h`. Wpisy mają unikalne ścieżki i SHA-256 jako 64 małe znaki hex. Nie wolno dodawać `python_soabi`, rozszerzeń Python, `resources` ani nieznanych pól. Manifest i payload muszą być zwykłymi plikami, bez symlinków także w rodzicach. Audyt sprawdza zadeklarowane bajty; nie inwentaryzuje dowolnych niewymienionych plików i nie uwierzytelnia producenta.

Dotychczasowy descriptor `[tool.sorust.rust-component]` działa także dla takiego dawcy: nadal przypina nazwę dystrybucji, dokładną wersję, pakiet i hash manifestu. Backend odczytuje metadane bez importu pakietu, sprawdza własność manifestu/payloadu, platformę, nazwę biblioteki, ABI i snapshot. Rozszerzenia Python dawcy nie są już wymagane, gdy jego jawny format jest Rust-only. Konsument nadal buduje swoje rozszerzenia i emituje zwykły manifest v1/v2; `rust_component` wskazuje nowego dawcę. Starszy czytnik odrzuca nowy schemat przed eksportem. Budowa z nim wymaga SDK obsługującego ten format, z przypiętym źródłem lub dokładnym wheel-em.

Opcja pilota `--native-only-component`, razem z `--prebuilt-rust --build-wheelhouse ...`, pakuje wyłącznie zweryfikowane Rust cdylib i nagłówki wejściowego SDK przez istniejące `python -m wheel pack`. Wheel `sorust_kernel_component_pilot-0.0.0-py3-none-<platform>.whl` zawiera manifest, bibliotekę, nagłówki i standardowe metadane, bez źródeł ani rozszerzeń Python. Manifest zachowuje kompilator i digest źródeł pochodzący z wejściowego SDK; nie oznacza to nowej kompilacji jądra. Generator działa jako kontrolowany pilot repakowania gotowych bajtów, bez nowego profilu budowania komponentów Rust ze źródeł.

Wygenerowany wheel trafia do prywatnego snapshotu wheelhouse jako ósme wejście; nie wolno mu zastąpić pliku użytkownika. Projekt NL deklaruje go w `[build-system].requires`, a izolowany frontend instaluje go przed budową. Probe frontendu sprawdza uprzedni brak tej dystrybucji, a raport `rustComponentWheel` wiąże nazwę, tag, hash całego wheel-a, manifest i descriptor. Weryfikacja inwentarza dotyczy rzeczywistego generowanego wheel-a i potwierdza brak payloadu Python. Tag `py3-none` opisuje brak ABI CPython w tej paczce; nie jest dowodem testów na innych interpreterach, manylinux lub innych systemach. Zakres pomiaru pozostaje Linux x86_64 / CPython 3.13.

### Jawne zasoby danych i manifest v2

Konsument może dodać opcjonalne pole do swojej istniejącej tabeli `[tool.sorust]`:

```toml
resources = ["semantic-profile.json", "nested/vocabulary.bin"]
```

Ścieżki odnoszą się do `src/<artifact-package>/`, np. `src/standard/semantic-profile.json`. To jawne pliki, bez rozwijania globów ani automatycznego odkrywania pozostałej zawartości paczki. Mogą zawierać Unicode. Wymagane są unikalne, kanoniczne względne ścieżki POSIX do zwykłych plików, bez `..`, aliasów `./`/podwójnych separatorów, backslash, dwukropka, znaków kontrolnych i symlinków w ścieżce. Katalog `_native`, korzeń `sorust-artifacts.json` i jego podścieżki oraz rozszerzenia wykonywalnych modułów Python i dynamicznych bibliotek (`.py`, `.pyc`, `.pyo`, `.pyw`, `.so`, `.pyd`, `.dll`, `.dylib`) są zastrzeżone. Błąd wejścia zatrzymuje konfigurację przed Cython/Cargo.

Backend dołącza zasoby do listy źródeł sdist przez istniejący hook `build_ext.get_source_files` i jawnie kopiuje je do świeżego wheel-a. Nie trzeba dodawać dla nich `package-data`; test obejmuje także `include-package-data=false`. Celowe reguły wykluczania we własnym `MANIFEST.in` nie są nadpisywane. Wheel budowany ze sdist musi otrzymać wszystkie zadeklarowane wejścia; konfiguracja odrzuca brakujący plik. Nazwy projektowe i bajty zasobów są również częścią `source_sha256`.

| Paczka | Emitowany format | Odczyt przez bieżący runtime |
| --- | --- | --- |
| Brak `resources` lub pusta lista | `sorust.artifacts/v1`, bez pola zasobów | Dotychczasowy audyt i eksport binarek/nagłówków |
| Co najmniej jeden zadeklarowany zasób | `sorust.artifacts/v2`, lista `resources` | Audyt i eksport binarek, nagłówków oraz zadeklarowanych danych |

W v2 wymagane jest pole `resources` typu lista wpisów zawierających dokładnie `path` i `sha256`; ręcznie tworzony v2 może mieć listę pustą. ABI C pozostaje 1, a wymagania obu rodzajów artefaktów natywnych pozostają takie same. Bieżący czytnik obsługuje v1 i v2, odrzuca deklarację zasobów pod etykietą v1 oraz konflikty zasobów z innymi wpisami. Starszy czytnik Sorust znający tylko v1 odrzuca v2, dzięki czemu nie akceptuje częściowego audytu ani eksportu pomijającego zadeklarowane dane. W lokalnym, jeszcze niewydanym 0.1 wybiera się właściwy resource-aware wheel przez zatwierdzoną rewizję i hash; sama nazwa pliku wersji deweloperskiej nie potwierdza obsługi v2.

`verify_artifacts` sprawdza obecność, ścieżki i sumy zadeklarowanych zasobów. `export_artifacts` zachowuje podpis API, ponownie hashuje odczytane bajty snapshotu przed utworzeniem celu, kopiuje także dane i zapisuje manifest na końcu. Brak zasobu, zmiana sumy, symlink lub konflikt powodują odmowę. Dotychczasowe zasady nowego katalogu i braku atomowości całej operacji pozostają w mocy. Nie eksportuje się niezadeklarowanych plików. Sumy wykrywają drift, nie uwierzytelniają wydawcy; zwykły import samodzielnego `.so` nie uruchamia automatycznie audytora.

Pilot NL ma nowy opcjonalny przełącznik `--manifest-resources`. Ten tryb deklaruje oryginalny `semantic-profile.json`, wymaga formatu v2 i poprawnego importu bez ręcznego kopiowania pliku, kontrolowanie zmienia wyłącznie JSON w eksporcie, sprawdza odmowę audytu i przywraca zatwierdzone bajty. Następnie wykonuje oryginalne testy i porównanie trzech trybów. Do krótkiej kontroli funkcjonalnej można użyć `--number 10`; nie stanowi ona nowego pomiaru przyspieszenia. Bez przełącznika pozostaje historyczny tryb v1 z manualnym sidecarem.

### Powtarzalny pilot na module NL DSL

Narzędzie Sorust `tests/benchmark_nl_dsl_pilot.py` korzysta z lokalnego checkoutu konsumenta, dokładnego 40-znakowego SHA commitu oraz wcześniej zbudowanych wheel-a Sorust i `.rlib`. Czyta pliki z obiektów Git, dzięki czemu zmiany robocze konsumenta nie zmieniają wejścia i nie są nadpisywane. Nie utrzymuje kopii implementacji NL w źródłach Sorust. Przykład po przygotowaniu tych lokalnych artefaktów:

```sh
wellman run --root . --allow-primary-venv -- python -I tests/benchmark_nl_dsl_pilot.py \
  --consumer-root "$NL_DSL_CHECKOUT" \
  --revision aa47c8752f1ea446208f6dfb7a018ad02e92250a \
  --sorust-wheel "$SORUST_WHEEL" \
  --rust-rlib "$SORUST_RLIB" \
  --output .subactor/cache/nl-dsl-pilot \
  --number 1000
```

Zmienne wskazują odpowiednio lokalny checkout NL oraz istniejące pliki wheel i `.rlib`. Wyjście musi być nowym katalogiem pod `.subactor/cache` bieżącego checkoutu, bez symlinków; poprzedniego pomiaru nie nadpisuje się. W linked worktree jawnie dopuszcza się użycie venv jego zarejestrowanego primary. Kod runtime/backendu wheel-a musi odpowiadać bieżącemu źródłu Sorust; jego manifest i wszystkie bajty artefaktów muszą odpowiadać zainstalowanemu pakietowi użytemu do eksportu. Uszkodzony lub inny wheel nie może zostać oznaczony jako źródło reużytej biblioteki. Narzędzie nie pobiera zależności: build używa dostępnego środowiska, Cargo działa offline, a instalacja lokalnego wheel-a konsumenta ma `--no-index --no-deps`.

Pilot kompiluje oryginalny inicjalizator `standard` oraz moduł NL. Sprawdza trzy osobne procesy w minimalnym venv: oryginalny Python, zainstalowany wheel z rozszerzeniami oraz samodzielnie eksportowany pakiet. Venv nie zawiera Sorust ani Cython, a PATH workerów nie udostępnia kompilatorów. Wybrane testy zgodności pochodzą z tego samego przypiętego commitu i muszą być niepuste, bez argumentów/fixtures; żadnego nie pomija się milcząco. Porównuje się dane parsera, tekst kanoniczny i wyniki mostka z pominięciem losowego trace ID oraz czasu odpowiedzi. To sprawdzenie konkretnego modułu i korpusu, nie pełnej aplikacji gRPC/LLM ani ruchu produkcyjnego.

W domyślnym trybie v1 tego pilota eksport przenosi artefakty i nagłówki manifestu. Moduł NL potrzebuje również `semantic-profile.json`. Pilot najpierw wymaga rzeczywistego błędu importu bez tego zasobu, następnie dostarcza go jawnie jako plik danych konsumenta i sprawdza jego hash względem przypiętego wejścia przed pomiarem. Ten sidecar nie staje się automatycznie zasobem weryfikowanym przez `verify_artifacts`; jego pakowanie i integralność pozostają odpowiedzialnością konsumenta.

Wszystkie trzy tryby używają tej samej wyeksportowanej biblioteki Rust z wejściowego wheel-a Sorust, przez ABI C v1. Oddzielny klient Rust linkuje istniejące `.rlib` bez ponownej kompilacji jądra, z dokładnie zgodnym toolchainem i `panic=abort`. Raport wiąże hashe obu wejściowych binarek i wynik klienta. Domyślna budowa próbnego wheel-a korzysta z niezmienionych plików crate Sorust w prywatnej nakładce.

Opcja `--prebuilt-rust` używa zamiast tego przypiętego manifestu zainstalowanego wheel-a Sorust. Nakładka nie kopiuje crate ani nagłówków źródłowych; podczas budowy sdist i wheel-a polecenia `cargo` i `rustc` są zastąpione programami kończącymi się błędem i rejestrującymi każde wywołanie. Raport wymaga braku tych wywołań oraz identycznych bajtów biblioteki i nagłówków dawcy. Połączenie `--prebuilt-rust --manifest-resources` obejmuje również automatyczny eksport JSON konsumenta. Osobna obserwacja toolchaina i kompilacja klienta `.rlib` nadal używają Rust poza etapem budowania konsumenta; cały pilot wymaga tego toolchaina. Krótki przebieg `--number 10` służy zgodności, bez nowego wniosku o przyspieszeniu.

Raport `result.json` przechowuje rewizje, hashe źródeł/artefaktów/skryptu, wejścia, wyniki zgodności, loader, środowisko, siedem rozgrzanych serii czasu i profil parsera. Domyślnie seria ma 1000 powtórzeń całego korpusu. Czas FFI obejmuje UTF-8, łączenie buforów, tablice długości i własne wyjście; budowa, import i przygotowanie są poza czasem steady-state. `cProfile` nie rozkłada wnętrza Rust/Cython. Brak przypięcia CPU i współdzielony host ograniczają interpretację; raport nie wymusza przyspieszenia ani progu CI.

Licznik Rust zachowuje swój kontrakt separatorów bajtowych. Dla U+00A0, U+2003, U+001C oraz U+3000 Python `str.split()` rozpoznaje separator, natomiast licznik Sorust nie. Pilot wymaga wykazania tej różnicy oraz porównuje czas liczenia tylko na wejściach o zgodnej semantyce. Nie zastępuje licznikiem ASCII parsera Unicode lub estymatora tokenów modelu.

### Izolowana budowa z lokalnego wheelhouse

Do polecenia pilota powyżej można dodać `--prebuilt-rust --manifest-resources --build-wheelhouse /sciezka/do/wheels --number 10`. `--build-wheelhouse` wymaga `--prebuilt-rust`. Katalog wejściowy jest płaski i zawiera wyłącznie zwykłe pliki `.whl`, bez dowiązań w plikach lub katalogach nadrzędnych. Musi zawierać dokładne bajty wheel-a wskazanego przez `--sorust-wheel` oraz komplet lokalnych zależności frontendu i konfiguracji `[build-system]`. Pilot niczego nie pobiera do uzupełnienia wheelhouse.

Przed pip tworzy prywatny snapshot tych plików z inwentarzem nazw i SHA-256. Nie scala ani nie nadpisuje wcześniejszego snapshotu. Następnie tworzy nowy venv z pip, instaluje z tego snapshotu frontend `build` i jego zależności oraz sprawdza brak Sorust, Cython i setuptools w środowisku frontendu. Rzeczywiste `python -I -m build` działa bez `--no-isolation`, budując sdist, a następnie wheel z sdist; deklarowane zależności budowania instaluje w izolowanych środowiskach PEP 517. W tym trybie `PATH` frontendu zawiera wyłącznie prywatne aliasy wymaganych narzędzi C i binutils. Przed budową pilot sprawdza, że `cargo` i `rustc` są niedostępne. To omija również opcjonalne odpytywanie `rustc --version` przez pip. Dotychczasowy tryb bez izolacji nadal używa stubów odrzucających oba polecenia.

Odziedziczone ustawienia `PIP_*` są zastąpione: konfiguracja pip i cache wyłączone, indeks wyłączony, `find-links` wskazuje wyłącznie lokalny snapshot przez URI pliku, a pip przyjmuje tylko wheel-e. Brak lokalnej zależności kończy budowę błędem. To kontrolowany test wskazanych lokalnych pakietów i rozdzielenia zależności, bez deklaracji sandboxa sieciowego ani hermetyczności dowolnego kodu wykonywanego przez backend lub zależności. Hash wykrywa zmianę wejścia, nie uwierzytelnia jego wydawcy.

Raport otrzymuje `buildIsolation="pep517-offline"` i `isolatedBuildInputs` z inwentarzem snapshotu, wersją frontendu oraz sprawdzonym brakiem trzech pakietów i narzędzi Rust przed budową. Pole `buildRustToolPolicy` rozróżnia `unavailable-on-path`, `failure-stubs` i domyślne `available` przy budowie Rust ze źródeł. Domyślny przebieg zachowuje `--no-isolation`, zapisuje `buildIsolation="prepared-environment"` i nie przypisuje sobie dowodu izolowanej instalacji. Pozostałe kontrole źródła, manifestów, zasobów, semantyki i binarek działają tak samo w obu trybach. Osobny klient `.rlib` nadal wymaga Rust poza etapem budowania konsumenta.

### Skompilowane inicjalizatory pakietów

Inicjalizator wybiera się przez pełną nazwę zakończoną `.__init__`. Przykładowa lista w istniejącej tabeli `[tool.sorust]`:

```toml
python-modules = [
  "nl_component.__init__",
  "nl_component._legacy",
  "nl_component.nested.__init__",
  "nl_component.nested._fast",
]
```

W sprawdzonym wariancie `import nl_component` i `import nl_component.nested` korzystają z `__init__.<SOABI>.so`, zachowując `__package__`, `__path__` oraz importy względne do dwóch pozostałych rozszerzeń. Wybrane inicjalizatory `.py` są usuwane z wheel-a tak samo jak inne wybrane moduły. Niewybrane moduły nadal mogą być zwykłym Pythonem.

Aby importować pakiet bezpośrednio z eksportu, katalog docelowy powinien mieć jego nazwę, np. `./binary-packages/nl_component`, a jego rodzic powinien być dostępny na `sys.path`. Eksport musi zawierać skompilowane zależności importowane przez inicjalizatory. Nie kopiuje automatycznie niewybranych źródeł ani zależności zewnętrznych. Testowany przykład wybiera wszystkie cztery wymagane moduły, dzięki czemu sam pakiet w eksporcie zawiera wyłącznie binarki, nagłówek i manifest. Nadal wymaga zgodnego interpretera CPython i platformy.

Budować przez `python -m build`, z dostępnym kompilatorem C i nagłówkami CPython. Tryb `rust-manifest` wymaga również Cargo, rustc i lokalnie dostępnych zależności Cargo; tryb `rust-component` wymaga przypiętej, zainstalowanej dystrybucji. Wybrane moduły `.py` muszą znajdować się pod `src/` i należeć do `artifact-package`; ABI v1 jest jedyną przyjmowaną wersją konfiguracji.

### Ponowne budowanie konsumenta

Można ponownie budować wheel w tym samym drzewie źródeł po zmianie `python-modules` lub usunięciu dawnego modułu. Każde wywołanie `build_wheel` używa osobnego tymczasowego stagingu pod `build/`, obejmującego bibliotekę oraz etap instalacji przed utworzeniem archiwum. Do nowej paczki trafiają bieżące moduły i nowy manifest; stare rozszerzenie nie może przesłonić aktualnego źródła Python. Nie trzeba usuwać wcześniejszego `build/lib.*` ani `build/bdist.*` dla tego przepływu. Opcja wheel-a `--skip-build` jest nieobsługiwana: hook zgłasza `ValueError` i nie tworzy wheel-a z niepełną zawartością. Usuwa się tylko staging utworzony przez bieżące wywołanie; cache kompilatorów pozostaje współdzielony między kolejnymi budowami.

To rozdzielenie zawartości wheel-i, bez deklaracji izolacji procesu budowania, bezpiecznej równoległej budowy jednego drzewa ani obsługi dowolnych ręcznie dodanych binarek w źródłach. Wywołania w tym samym drzewie należy serializować. Standardowa izolacja zależności PEP 517 pozostaje odrębną właściwością frontendu.

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

Pierwsza implementacja została niezależnie scalona przez [PR1](https://github.com/wellmanifest/sorust/pull/1) jako `4d3d97226fc8b29fb84ea8b61f42443d86cc2faa`. Korekty importu i bufora zostały niezależnie scalone w [PR2](https://github.com/wellmanifest/sorust/pull/2) jako `f6b9829ed488e0fc34b6b4c47130abc836d01d7e` i [PR3](https://github.com/wellmanifest/sorust/pull/3) jako `b0e9c9c13ce1e72476ce851b557189655e59dda3`. Korektę Cargo.lock scalono przez [PR4](https://github.com/wellmanifest/sorust/pull/4) jako `23e6adcf2ed09803b552ad229bc0dc87cf2409eb`. Walidację wielu modułów scalono przez [PR5](https://github.com/wellmanifest/sorust/pull/5) jako `37c7389400d26ec504e4156a381e6c8dda2c47bf`. Eksport binarek scalono przez [PR6](https://github.com/wellmanifest/sorust/pull/6) jako `069cf837755284b0a622ec25cc3b9a36bebe5dfd`. Wsady scalono przez [PR7](https://github.com/wellmanifest/sorust/pull/7) jako `ef788e90d9dce61c559418416b8d49c4a8b6ca66`, po niezależnym zatwierdzeniu HEAD `9d3a6d2dcdcc25264b587b45f45315b18d6da9c4`. Iterator scalono przez [PR8](https://github.com/wellmanifest/sorust/pull/8) jako `b10294160915d5507e8a50ace6a78f2a9db7feeb`, po niezależnym zatwierdzeniu HEAD `2129599488fc1c004db7756290c5139584b84d3c`. Staging i odmowę pominięcia budowy scalono przez [PR9](https://github.com/wellmanifest/sorust/pull/9) jako `bf83dc5a5da2eae33d3c7a666679e8dd3a5223d9`, po niezależnym zatwierdzeniu HEAD `3c2e6bd15ba6e08f6f435c6780cd15a318ca5f36`. Walidację inicjalizatorów scalono przez [PR10](https://github.com/wellmanifest/sorust/pull/10) jako `04e38d529532538ee9adbeb38b509bf95fc052e5`, po niezależnym zatwierdzeniu HEAD `c8fef2e148d99419fc0c3dd8d7a2610f06c1faac`. Przygotowany licznik scalono przez [PR11](https://github.com/wellmanifest/sorust/pull/11) jako `ea3b05b39810b0add6b8d21e3fbd486d9432b96d`, po niezależnym zatwierdzeniu HEAD `b57267857a6ecfc10566e1d55e95aeaed4425dcf`. Odcisk skryptu Cargo scalono przez [PR12](https://github.com/wellmanifest/sorust/pull/12) jako `16e802b5d16fba5372fc4333a4ed05a6a9bb8e7f`, po niezależnym zatwierdzeniu HEAD `85892adc316c02803fbf4f6f6f892f583452a7d1`. Pilot scalono przez [PR13](https://github.com/wellmanifest/sorust/pull/13) jako `55bb710930d9d83d31c9dd5d9a221872c813af08`, po niezależnym zatwierdzeniu HEAD `c94eed2635e8e3c7509aa98221f68569702dc19d`. Zasoby scalono przez [PR14](https://github.com/wellmanifest/sorust/pull/14) jako `e78ce82c3100dfedf178cddaed0439ffbd38b687`, po niezależnym zatwierdzeniu HEAD `5b06d9c3fcbe7775276eb4eb0ebaa0afe4dc7779`. Komponent zainstalowany scalono przez [PR15](https://github.com/wellmanifest/sorust/pull/15) jako `78c0f69dcda83f60469bbddbbee65838f2339734`, po niezależnym zatwierdzeniu HEAD `fa11c5574aeca336dd700eacb2c9a0c520bb24f2`. Izolowany pilot scalono przez [PR16](https://github.com/wellmanifest/sorust/pull/16) jako `8de2464d896f336e3c27a35cc0001696416973ee`, po niezależnym zatwierdzeniu HEAD `91405c695758586a594a35bc02b09313e1a991f5`. Każda następna zmiana, w tym samodzielny komponent Rust w ticket-017, wymaga własnych bram i niezależnego zatwierdzenia aktualnego HEAD przed scaleniem. Przygotowane wheel i sdist pozostają lokalnymi artefaktami do późniejszego, osobno autoryzowanego wydania.
