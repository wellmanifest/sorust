---
{
  "schema": "wellmanifest.docs/document/v1",
  "id": "sorust-binary-standard",
  "kind": "information",
  "version": 3,
  "title": "Sorust 0.1: standard dwóch artefaktów",
  "status": "draft",
  "owner": "wellmanifest/sorust",
  "scope": "repository",
  "created": "2026-11-09",
  "updated": "2026-11-09",
  "review_after": "2027-02-09",
  "source_revision": "16e3f1e907fa406277cc4bd27931ebedc1339c43",
  "affected_repositories": [
    "wellmanifest/sorust"
  ],
  "evidence": [
    "repo://wellmanifest/sorust/src/sorust/backend.py",
    "repo://wellmanifest/sorust/tests/test_build.py",
    "repo://wellmanifest/sorust/crates/sorust-kernel/src/lib.rs",
    "https://github.com/wellmanifest/sorust",
    "receipt:sorust-initial-ref-plan.7e901cfd9781e8596e6a56da24744b400052a82a42880e1a9f2f9a916ca85045",
    "https://github.com/subactor/onedev-agent/blob/8ac2658e3fcd7d2df3375a8ece8bbe775329da9b/packages/diagit-control/onedev_diagit_control/initial_ref.py"
  ]
}
---

# Sorust 0.1: standard dwóch artefaktów

<!-- docs:section purpose -->
## Purpose

Sorust dostarcza wspólny kontrakt budowania dla bibliotek Wellmanifest `nl-*`: pozostały Python jako importowalne rozszerzenia oraz wydzielone, atomowe jądra Rust. Wersja 0.1 jest implementacją lokalną, bez publikacji w rejestrze i bez migracji istniejących repozytoriów.

<!-- docs:section scope -->
## Scope

HOME: `wellmanifest/sorust`, pakiet standardu i implementacja referencyjna. Każdy konsument zachowuje swoją semantykę, testy i odpowiedzialność. Standard nie zastępuje `wellmanifest/python`, `reuse` ani chronionego procesu publikacji.

<!-- docs:section evidence -->
## Evidence

Źródło implementacji: commit `fcfe82128748e23dc711b5d79ae776e8198a6306`. Testy budują wheel także z sdist, instalują go w osobnym venv, sprawdzają rozszerzenie, ABI, sumy kontrolne oraz klientów C, Rust i Python. Wynik: 21 testów pytest i dwa testy Cargo; wheel zbudowano również z sdist. Klient C używa dołączonego nagłówka. Odrzucono brakujące i zmodyfikowane artefakty oraz niezgodne ABI. Backend sprawdzono także w obcym pakiecie.



Pomiar lokalny na Linux x86_64 / CPython 3.13, Cython 3.3.1 i rustc 1.97.1: dla 155648 bajtów mediana pięciu serii po dziesięć wywołań wyniosła Python 19.90 ms, compiled-python 3.00 ms, Rust 0.214 ms, czyli około 93× względem referencyjnego Pythona. To mikrobenchmark funkcji, bez przypięcia CPU; nie mierzy całych procesów `nl-*` ani wielu małych wywołań. Digest źródeł build: `f3636ae9a13ca90806b054b528a558b6db6e449d1dd1d54ec9705d2d7c0f869a`.

Lokalne wyniki dystrybucji: `dist/sorust-0.1.0-cp313-cp313-linux_x86_64.whl` i `dist/sorust-0.1.0.tar.gz`. Testy i dokładne konfiguracje klientów: `tests/test_build.py`. Pełne wyniki maszynowe pozostają w prywatnych receiptach.

<!-- docs:section content -->
## Content

| Reguła | Wymaganie |
| --- | --- |
| SORUST-001 | Konsument MUSI jawnie wskazać moduły `.py` do kompilacji i wersję backendu w `build-system.requires`; sama zależność runtime nie uruchamia kompilacji. |
| SORUST-002 | Każdy atomowy komponent budowany backendem MUSI dać rozszerzenie CPython oraz Rust `cdylib`. Wheel MUSI mieć tag interpretera i platformy; wybrane moduły `.py` nie są pakowane obok ich rozszerzeń. |
| SORUST-003 | Współdzielenie binarki Rust MUSI używać wersjonowanego ABI C: jawne rozmiary liczb, długości buforów, własność pamięci, kody błędów i funkcja wersji ABI. Panika nie może przekroczyć FFI. |
| SORUST-004 | Wheel MUSI zawierać `sorust-artifacts.json`: ścieżki, SHA-256 obu rodzajów binarek, ABI, SOABI Pythona, platformę, wersję rustc oraz digest źródeł. Nagłówki z `include/*.h` są pakowane i hashowane. |
| SORUST-005 | Produkcja MUSI jawnie używać natywnego backendu. Brak, rozbieżna suma albo niezgodna wersja ABI zatrzymuje wywołanie; nie ma cichego powrotu do źródłowego Pythona. |
| SORUST-006 | Zmiana jądra MUSI przejść testy różnicowe względem zaakceptowanej semantyki oraz pomiar reprezentatywnych rozmiarów. Migracja kolejnych bottlenecków wymaga profilowania. |
| SORUST-007 | Jedno jądro ma jednego właściciela, własną wersję i jedną odpowiedzialność. Konsumenci MUSZĄ reużywać dystrybucję zamiast kopiować implementację. |
| SORUST-008 | Budowanie Rust używa `--release --locked --offline`. Sdist MUSI zawierać źródła, Cargo.lock i konfigurację backendu; zależności Cargo należy wcześniej dostarczyć do cache lub vendor. |

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

Walidacja obejmuje Linux x86_64 i CPython 3.13. Repozytorium `wellmanifest/sorust` istnieje na GitHubie i ma skonfigurowany origin, lecz nadal nie ma żadnej zdalnej gałęzi. Hook odrzucił pierwsze wypchnięcie `main` kodem GOV-PUSH-001. PR i merge czekają na chronioną inicjalizację pierwszej referencji; hooków nie wyłączono. Profil Validatora dopuszcza repo i wymaga `governance / enforce` oraz `governance / remote lifecycle`, ale konfiguracja nie stanowi dowodu ich wykonania. Pełna adopcja chronionej bramy Docs nie jest skonfigurowana; układ, metadane i indeks kontroluje się lokalnie. Zarządzany checkpoint v2 działa po dodaniu origin. Brak canary manylinux, macOS, Windows, innych interpreterów oraz porównania na rzeczywistych zadaniach `nl-*`. Suma kontrolna wykrywa drift, nie uwierzytelnia wydawcy; zaufanie do wheel-a wymaga oddzielnej proweniencji. Ładowanie i import są buforowane w procesie. Cython nie gwarantuje przyspieszenia dowolnego kodu Python ani obsługi każdej dynamicznej konstrukcji. Nie deklarujemy bitowej odtwarzalności między hostami.

<!-- docs:section next_actions -->
## Next Actions

Właściciele konsumentów wybierają bottleneck na podstawie profilu, dodają testy zgodności i adoptują wydany pakiet zgodnie z instrukcją adopcji powyżej. Zmiany ABI wymagają nowego numeru ABI i jawnej migracji. Chroniona publikacja i macierz platform pozostają oddzielnymi krokami przed szeroką adopcją.


Chroniona inicjalizacja musi opublikować wyłącznie bazę governance `ea1bf67895e4ca2abda99d44fc8a538b01470350`, z pełną allowlistą 138 plików. Plan `initial-ref-aa50fb9513cfd8d684c0d3d8` ma digest `7e901cfd9781e8596e6a56da24744b400052a82a42880e1a9f2f9a916ca85045`. Brakuje świeżego jednorazowego grant-binding od niezależnego issuera oraz uruchomienia chronionego Publishera. Po niezależnej walidacji początkowej referencji należy wysłać gałąź ticket-001, otworzyć PR i uzyskać zatwierdzenie oraz merge Validatora. Plan jest propozycją, nie grantem ani zgodą na bezpośrednią zmianę main.


Ustalona przyczyna niedostępności grantu: opublikowany issuer OneDev w rewizji `8ac2658e3fcd7d2df3375a8ece8bbe775329da9b` sprawdza `remote.private == true` oraz obecność skonsumowanego, natywnego potwierdzenia bootstrapu Validatora. Publiczny Sorust utworzony bez tego kontrolera nie spełnia tych warunków. Nie wystarczy ponowić tego samego planu ani dopisać pozytywnego potwierdzenia.

Zależność właścicielska `subactor/onedev-agent / PLF-22278` została utworzona w lokalnym backlogu przez allocator Planfile. Dotyczy dopuszczenia ograniczonej ścieżki dla dokładnie tego istniejącego, publicznego i pustego repozytorium; zachowuje ochronę prywatnego bootstrapu. Nie zmieniono runtime ani jego uprawnień. Wznowienie publikacji Sorust wymaga niezależnego opublikowania i wdrożenia tej ścieżki, a następnie rzeczywistego grantu i walidacji początkowej referencji.
