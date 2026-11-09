//! Allocation-free byte-token counting; no Python interpreter dependency.

pub fn count_ascii_tokens(input: &[u8]) -> u64 {
    let mut count = 0;
    let mut inside = false;
    for &value in input {
        let separator = value == b' ' || (b'\t'..=b'\r').contains(&value);
        if !separator && !inside {
            count += 1;
        }
        inside = !separator;
    }
    count
}

#[no_mangle]
pub extern "C" fn sorust_abi_version() -> u32 {
    1
}

/// Count tokens into caller-owned output; 0=success, 1=invalid argument.
///
/// # Safety
/// For nonzero length, input must address length readable bytes in one live
/// allocation. Output must address an aligned writable u64, disjoint from input.
/// Neither allocation may be concurrently mutated. Null input is allowed only
/// for length zero. Non-null pointer validity remains the caller's obligation.
#[no_mangle]
pub unsafe extern "C" fn sorust_count_ascii_tokens_v1(
    input: *const u8,
    length: usize,
    output: *mut u64,
) -> i32 {
    if output.is_null() || (length > 0 && input.is_null()) || length > isize::MAX as usize {
        return 1;
    }
    let bytes = if length == 0 { &[] } else { unsafe { std::slice::from_raw_parts(input, length) } };
    unsafe { output.write(count_ascii_tokens(bytes)); }
    0
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn boundaries() {
        for (bytes, expected) in [(b"".as_slice(), 0), (b"a b\tc\nd", 4),
            (b" \t\n\r\x0b\x0c ", 0), (b"\0\xff\xc2\xa0", 1)] {
            assert_eq!(count_ascii_tokens(bytes), expected);
        }
    }

    #[test]
    fn ffi_invalid_and_empty() {
        let mut output = 99;
        unsafe {
            assert_eq!(sorust_count_ascii_tokens_v1(std::ptr::null(), 1, &mut output), 1);
            assert_eq!(output, 99);
            assert_eq!(sorust_count_ascii_tokens_v1(std::ptr::null(), 0, std::ptr::null_mut()), 1);
            assert_eq!(sorust_count_ascii_tokens_v1(std::ptr::null(), 0, &mut output), 0);
            assert_eq!(output, 0);
        }
    }
}
