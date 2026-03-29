import zlib, brotli

def change_idat_compression(content):
	content = zlib.decompress(content)
	content = brotli.compress(content)
	return content

with open("final.png", "rb") as f:
	with open("glitchin.png", "wb") as of:
		of.write(f.read(8)) # PNG Signature
		chunk = ""
		while chunk != b"IEND":
			length = f.read(4)
			chunk = f.read(4)
			content = f.read(int.from_bytes(length, byteorder='big'))
			crc = f.read(4)

			if chunk.decode() == "IDAT":
				content = change_idat_compression(content)
				length = len(content).to_bytes(4, byteorder='big') # Compute new length
				crc = (zlib.crc32(chunk+content)).to_bytes(4, byteorder='big') # Compute new CRC
			
			of.write(length + chunk + content + crc)