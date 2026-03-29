// Build with: cl ransomware.c aes.c sha256.c /Fe:ransomware.exe
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "aes.h"
#include "sha256.h"

#define XOR_KEY 0x5A
const uint8_t obfuscated_password[] = {
	0xa, 0x28, 0x69, 0x29, 0x29, 0x7a, 0x7d, 0x1c, 0x7d, 0x7a, 0x2e, 0x6a, 0x7a, 0x33, 0x34, 0x2e, 0x69, 0x28, 0x3b, 0x39, 0x2e, 0x74, 0x74, 0x74
};
#define OBFUSCATED_LEN (sizeof(obfuscated_password))

void decode_password(char *out) {
	for (size_t i = 0; i < OBFUSCATED_LEN; i++) {
			out[i] = obfuscated_password[i] ^ XOR_KEY;
	}
	out[OBFUSCATED_LEN] = '\0';
}

void derive_key_iv(const char *password, uint8_t *key, uint8_t *iv) {
		uint8_t hash[32];
		sha256_easy_hash(password, strlen(password), hash);
		memcpy(key, hash, 32);
		memcpy(iv, hash + 16, 16);
}

int main() {
	char user_password[128];
	char expected_password[64];

	// Decode known password
	decode_password(expected_password);

	// Request password from user
	printf("Please send 1 BTC to this address to retrieve the decryption password: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa\n\n");
	printf("Decryption password: ");
	fgets(user_password, 128, stdin);
	user_password[strcspn(user_password, "\r\n")] = 0;
	if (strcmp(user_password, expected_password) != 0) { // "Pr3ss 'F' t0 int3ract..."
		fprintf(stderr, "Incorrect password.\n");
		return 1;
	}

	// Retrieve "flag.txt" content
	FILE *f = fopen("flag.txt", "rb");
	if (!f) {
		perror("flag.txt not found");
		return 1;
	}
	fseek(f, 0, SEEK_END);
	long file_size = ftell(f);
	rewind(f);
	unsigned char *ciphertext = malloc(file_size);
	fread(ciphertext, 1, file_size, f);
	fclose(f);

	// Perform decryption
	uint8_t key[32], iv[16];
	derive_key_iv(user_password, key, iv);
	struct AES_ctx aes_ctx;
	AES_init_ctx(&aes_ctx, key);
	AES_init_ctx_iv(&aes_ctx, key, iv);
	AES_CBC_decrypt_buffer(&aes_ctx, ciphertext, file_size);

	// Write decrypted data back
	f = fopen("flag.txt", "wb");
	fwrite(ciphertext, 1, file_size, f);
	fclose(f);

	// Print success message
	printf("You paid the ransom. Files decrypted.\n");

	free(ciphertext);
	return 0;
}
