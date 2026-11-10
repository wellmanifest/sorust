#ifndef SORUST_H
#define SORUST_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
uint32_t sorust_abi_version(void);
/* 0=success, 1=invalid argument. Input is borrowed for this call only.
 * Nonzero length requires readable input; output requires aligned writable
 * storage disjoint from input. Null input is valid for length zero only.
 * Neither buffer may be mutated concurrently. No allocation crosses the ABI. */
int32_t sorust_count_ascii_tokens_v1(const uint8_t *input, size_t length, uint64_t *output);
/* Additive ABI v1 batch entry. Input contains count adjacent segments whose
 * lengths sum exactly to length. count=0 requires length=0; all pointers may
 * then be NULL. Otherwise lengths/output address count aligned elements;
 * input may be NULL only for length=0. Output storage may be uninitialized
 * and must be disjoint from both immutable input regions, exclusively writable
 * for the call. Invalid lengths/counts return 1 without modifying output.
 * Non-null pointer validity remains the caller's obligation. */
int32_t sorust_count_ascii_tokens_many_v1(const uint8_t *input, size_t length,
                                        const size_t *lengths, size_t count, uint64_t *output);
#ifdef __cplusplus
}
#endif
#endif
