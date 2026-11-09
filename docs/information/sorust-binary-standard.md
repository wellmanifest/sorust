---
{
  "schema": "wellmanifest.docs/document/v1",
  "id": "sorust-binary-standard",
  "kind": "information",
  "version": 6,
  "title": "Sorust 0.1: standard dwóch artefaktów",
  "status": "implemented",
  "owner": "wellmanifest/sorust",
  "scope": "repository",
  "created": "2026-11-09",
  "updated": "2026-11-09",
  "review_after": "2027-02-09",
  "source_revision": "d6917eb2c4097ac364a4e51bbebefcb9ac134b56",
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
    "https://github.com/wellmanifest/sorust/blob/d6917eb2c4097ac364a4e51bbebefcb9ac134b56/tests/test_build.py"
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
| SORUST-008 | Budowanie Rust używa `--release --locked --offline`. Sdist MUSI zawierać źródła, Cargo.lock i konfigurację backendu; zależności Cargo należy wcześniej dostarczyć do cache lub vendor. |
| SORUST-009 | Adapter Python MUSI przekazać do ABI C długość rzeczywistego, niezmiennego bufora. Podklasy `bytes` w `count_ascii_tokens` normalizuje się z bufora przed obiema implementacjami; zwykłe `bytes` zachowują ścieżkę bez dodatkowej kopii w adapterze. |

Pierwsze jądro `sorust-kernel` liczy tokeny bajtowe oddzielone dokładnie przez spację i bajty 9–13. Pozostałe bajty, w tym NUL i UTF-8, są nieprzezroczyste. To nie jest tokenizer modelu LLM.

`count_ascii_tokens(data: bytes, backend="rust")` używa Rust. `backend="compiled-python"` jawnie wybiera rozszerzenie Cython. Obie ścieżki mają identyczną semantykę; wzorzec `.py` pozostaje w źródłach i sdist.

Rust generuje również `.rlib` dla klientów używających zgodnego kompilatora i strategii panic. To opcjonalny wynik Cargo, nie przenośne ABI ani zawartość wheel-a. Współdzielenie między językami odbywa się przez `cdylib` i dołączony nagłówek.

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

Pierwsza implementacja została niezależnie scalona przez [PR1](https://github.com/wellmanifest/sorust/pull/1) jako `4d3d97226fc8b29fb84ea8b61f42443d86cc2faa`. Korekta ticket-002 podlega własnym bramom i niezależnemu zatwierdzeniu aktualnego HEAD przed scaleniem. Przygotowane wheel i sdist pozostają lokalnymi artefaktami do późniejszego, osobno autoryzowanego wydania.
