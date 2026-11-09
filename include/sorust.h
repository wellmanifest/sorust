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
#ifdef __cplusplus
}
#endif
#endif
