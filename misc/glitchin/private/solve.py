from PIL import Image
import brotli

def parse_ihdr(raw):
	width = int.from_bytes(raw[0:4], byteorder='big')
	height = int.from_bytes(raw[4:8], byteorder='big')
	bps = raw[8]
	color_type = raw[9]
	compression_method = raw[10]
	filter_method = raw[11]
	interlace_method = raw[12]

	return {
		"Width": width,
		"Height": height,
		"Bits per sample": bps,
		"Color type": color_type,
		"Compresion method (!)": compression_method,
		"Filter method": filter_method,
		"Interlace method": interlace_method
	}


def display_ihdr(ihdr):
	for key, value in ihdr.items():
		print(f"\t{key}: {value}")


def parse_text(raw):
	keyword = ""
	i = 0
	for c in raw:
		i += 1
		if not c: # Stop at NULL byte
			break
		keyword += chr(c)
	print(f"\t{keyword}: {raw[i:]}")

	binary = ''.join('0' if b == 1 else '1' for b in raw[i+15:])
	decoded = ''.join(chr(int(binary[i:i + 8], 2)) for i in range(0, len(binary), 8))
	print(f"\tDecoded trailing data: {decoded}")


def paeth_predictor(a, b, c):
	p = a + b - c
	pa = abs(p - a)
	pb = abs(p - b)
	pc = abs(p - c)
	
	if pa <= pb and pa <= pc:
		return a
	elif pb <= pc:
		return b
	else:
		return c


def parse_idat(ihdr, raw):
	pixels = []
	decompressed = brotli.decompress(raw)
	# spp = Sample per pixel
	if ihdr["Color type"] == 0: # Grayscale
		spp = 1
	elif ihdr["Color type"] == 2: # RGB
		spp = 3
	elif ihdr["Color type"] == 3: # PLTE
		spp = 1
	elif ihdr["Color type"] == 4: # Grayscale + Alpha
		spp = 2
	elif ihdr["Color type"] == 6: # RGBA
		spp = 4

	scanline_length = (ihdr["Width"] * spp * ihdr["Bits per sample"]) // 8

	for i in range(0, len(decompressed), scanline_length+1):
		scanline = decompressed[i:i+scanline_length+1]
		filter_type = scanline[0]
		scanline = list(scanline[1:])

		if filter_type == 0: # No filter
			pass
		elif filter_type == 1: # Sub filter
			for x in range(3, len(scanline)):
				scanline[x] = (scanline[x] + scanline[x - 3]) % 256
		elif filter_type == 2: # Up filter
			for x in range(0, len(scanline)):
				scanline[x] = (scanline[x] + previous_scanline[x]) % 256
		elif filter_type == 3: # Average filter
			for x in range(len(scanline)):
				left = scanline[x - 3] if x >= 3 else 0
				up = previous_scanline[x]
				scanline[x] = (scanline[x] + ((left + up) // 2)) % 256
		elif filter_type == 4: # Paeth filter
			for x in range(len(scanline)):
				left = scanline[x - 3] if x >= 3 else 0
				up = previous_scanline[x]
				up_left = previous_scanline[x - 3] if x >= 3 else 0
				scanline[x] = (scanline[x] + paeth_predictor(left, up, up_left)) % 256

		previous_scanline = scanline

		for x in range(0, len(scanline), 3):
			pixels.append(tuple(scanline[x:x+3]))

	return pixels


def render_image(ihdr, pixels):
	img = Image.new("RGB", (ihdr["Width"], ihdr["Height"]))
	img.putdata(pixels)
	img.show()


def main():
	ihdr = {}
	pixels = []
	with open("out.png", "rb") as f:
		print(f"Signature: {f.read(8)}")

		chunk_type = b''
		while chunk_type != b"IEND":
			chunk_length = int.from_bytes(f.read(4), byteorder='big')
			chunk_type = f.read(4)
			chunk_content = f.read(chunk_length)
			f.read(4) # CRC do not care

			print(f"{chunk_type.decode()} ({chunk_length})")

			if chunk_type == b"IHDR":
				ihdr = parse_ihdr(chunk_content)
				display_ihdr(ihdr)
			elif chunk_type == b"tEXt":
				parse_text(chunk_content)
			elif chunk_type == b"IDAT":
				pixels = parse_idat(ihdr, chunk_content)

	render_image(ihdr, pixels)


if __name__ == "__main__":
	main()