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

/// Count contiguous byte segments in one call; 0=success, 1=invalid argument.
/// Invalid lengths/counts leave every output unchanged.
///
/// # Safety
/// For an in-range nonzero count, lengths must address count initialized,
/// aligned usize values, and output must address count aligned writable u64
/// slots (which may be uninitialized). Nonzero length requires one live,
/// initialized readable byte allocation. Output is disjoint from both inputs;
/// inputs remain immutable and output is exclusively borrowed for this call.
/// Non-null pointer validity remains the caller's obligation.
#[no_mangle]
pub unsafe extern "C" fn sorust_count_ascii_tokens_many_v1(
    input: *const u8,
    length: usize,
    lengths: *const usize,
    count: usize,
    output: *mut u64,
) -> i32 {
    if count == 0 {
        return if length == 0 { 0 } else { 1 };
    }
    if lengths.is_null() || output.is_null() || (length > 0 && input.is_null())
        || length > isize::MAX as usize
        || count > isize::MAX as usize / std::mem::size_of::<usize>()
        || count > isize::MAX as usize / std::mem::size_of::<u64>()
    {
        return 1;
    }
    let sizes = unsafe { std::slice::from_raw_parts(lengths, count) };
    let mut total = 0usize;
    for &size in sizes {
        total = match total.checked_add(size) {
            Some(value) => value,
            None => return 1,
        };
    }
    if total != length {
        return 1;
    }
    let bytes = if length == 0 { &[] } else { unsafe { std::slice::from_raw_parts(input, length) } };
    let mut offset = 0;
    for (index, &size) in sizes.iter().enumerate() {
        let end = offset + size;
        let value = count_ascii_tokens(&bytes[offset..end]);
        unsafe { output.add(index).write(value); }
        offset = end;
    }
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

    #[test]
    fn many_boundaries_and_uninitialized_output() {
        let input = b"a b\0\xff";
        let lengths = [1, 0, 2, 2];
        let mut output = std::mem::MaybeUninit::<[u64; 4]>::uninit();
        unsafe {
            assert_eq!(sorust_count_ascii_tokens_many_v1(input.as_ptr(), input.len(),
                lengths.as_ptr(), lengths.len(), output.as_mut_ptr().cast()), 0);
            assert_eq!(output.assume_init(), [1, 0, 1, 1]);
            assert_eq!(sorust_count_ascii_tokens_many_v1(std::ptr::null(), 0,
                std::ptr::null(), 0, std::ptr::null_mut()), 0);
            let lengths = [0, 0];
            let mut empty_output = [99, 99];
            assert_eq!(sorust_count_ascii_tokens_many_v1(std::ptr::null(), 0,
                lengths.as_ptr(), 2, empty_output.as_mut_ptr()), 0);
            assert_eq!(empty_output, [0, 0]);
        }
    }

    #[test]
    fn many_invalid_arguments_preserve_output() {
        let input = b"ab";
        let lengths = [1, 1];
        let mut output = [99, 99];
        unsafe {
            assert_eq!(sorust_count_ascii_tokens_many_v1(std::ptr::null(), 2,
                lengths.as_ptr(), 2, output.as_mut_ptr()), 1);
            assert_eq!(sorust_count_ascii_tokens_many_v1(input.as_ptr(), 2,
                std::ptr::null(), 2, output.as_mut_ptr()), 1);
            assert_eq!(sorust_count_ascii_tokens_many_v1(input.as_ptr(), 2,
                lengths.as_ptr(), 2, std::ptr::null_mut()), 1);
            assert_eq!(sorust_count_ascii_tokens_many_v1(input.as_ptr(), 1,
                lengths.as_ptr(), 2, output.as_mut_ptr()), 1);
            assert_eq!(sorust_count_ascii_tokens_many_v1(input.as_ptr(), 2,
                lengths.as_ptr(), 0, output.as_mut_ptr()), 1);
            assert_eq!(output, [99, 99]);
        }
    }

    #[test]
    fn many_rejects_sum_overflow_and_size_limits() {
        let lengths = [usize::MAX, 1];
        let mut output = [99, 99];
        unsafe {
            assert_eq!(sorust_count_ascii_tokens_many_v1(std::ptr::null(), 0,
                lengths.as_ptr(), 2, output.as_mut_ptr()), 1);
            assert_eq!(sorust_count_ascii_tokens_many_v1(std::ptr::null(), 0,
                std::ptr::null(), usize::MAX, output.as_mut_ptr()), 1);
            assert_eq!(output, [99, 99]);
        }
    }
}
