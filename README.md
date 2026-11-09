# Sorust

Biblioteka Python i standard Wellmanifest dla kompilowanych modułów Python oraz współdzielonych, atomowych jąder Rust. Wersja 0.1 jest lokalnym prototypem; pakiet nie został opublikowany w PyPI.

Jedno budowanie tworzy platformowy wheel z dwoma rodzajami artefaktów:

- `_compat.<SOABI>.so`: wybrany moduł Python skompilowany przez Cython.
- `_native/libsorust_kernel.so`: samodzielne jądro Rust z ABI C v1, nagłówkiem i sumami kontrolnymi.

Cargo produkuje również `.rlib` do użycia ze zgodnym toolchainem. Wheel pozwala instalować gotowe binarki bez kompilatorów u konsumenta. Kolejne bottlenecki powinny mieć własne, małe dystrybucje zamiast kopii kodu w projektach `nl-*`.

```bash
python -m pip install '.[build,test]'
python -m build
python -m pip install dist/sorust-0.1.0-*.whl
```

Budowanie wymaga Pythona >=3.11 z nagłówkami, kompilatora C, Cargo i rustc. Cargo działa z `--locked --offline`; pierwsze jądro nie ma zewnętrznych zależności Rust.

```python
from sorust import count_ascii_tokens, verify_artifacts

assert count_ascii_tokens(b"one two\tthree") == 3
assert count_ascii_tokens(b"one two", backend="compiled-python") == 2
manifest = verify_artifacts()
```

To licznik tokenów bajtowych rozdzielonych białymi znakami ASCII, nie tokenizer modelu LLM. Domyślna ścieżka wykonuje Rust; brak lub uszkodzenie binarki kończy się błędem.

[Standard, instrukcja adopcji i wyniki walidacji](docs/information/sorust-binary-standard.md).

Sama zależność runtime `sorust` nie kompiluje konsumenta. Do wytwarzania jego własnych artefaktów służy jawny backend `sorust.backend` opisany w instrukcji adopcji.

W repozytorium stosuj checkout `.venv` i zatwierdzony runtime `wellman run`; testy wymagają jawnego `WELLMANIFEST_BASE_SHA` przy braku zdalnej gałęzi bazowej. Zweryfikowano Linux x86_64 / CPython 3.13. Pozostałe platformy i protected CI wymagają osobnej walidacji.
