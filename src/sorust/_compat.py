"""Reference semantics, compiled to an importable extension by Cython.

Token boundaries are exactly ASCII HT, LF, VT, FF, CR and space. UTF-8 bytes
are opaque; this is deliberately different from Unicode str.split().
"""


def count_ascii_tokens(data: bytes) -> int:
    if not isinstance(data, bytes):
        raise TypeError("data must be bytes")
    if type(data) is not bytes:
        data = memoryview(data).tobytes()
    count = 0
    inside = False
    for value in data:
        separator = value == 32 or 9 <= value <= 13
        if not separator and not inside:
            count += 1
        inside = not separator
    return count
