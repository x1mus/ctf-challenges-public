# Glitchin'

## Category
Misc

## Estimated difficulty
Medium

## Description
A PNG where the standard *deflate* compression algorithm has been replaced by the *Brotli* alrogithm. A few hints are given along the way.

## Scenario
Just intercepted a suspicious PNG file from a compromised server. The file appears corrupted. It won't open in any standard image viewer.

Rumor has it that the file contains a hidden flag. Your task is to analyze, repair, and extract the hidden information.

## Write-up
The contestant is provided with a PNG file that seems to be corrupted.

### Reconnaissance
By using various tools such as `exiftool`, `pngcheck` or anything else we can quickly figure out that:
1. The `compr_method` field doesn't follow the PNG specification. Indeed the value here is *2*, whereas only *0* is defined.
```bash
┌──(kali㉿kali)-[~/Desktop]
└─$ pngcheck glitchin.png 
glitchin.png  invalid IHDR compression method (2)
ERROR: glitchin.png
```
2. A few private chunks are defined and only contains comments: `wEBb`, `cORe`, `rOOt`, `bYTe`, `nULl`, `sKId`
3. The comments themselves, mainly point to the RFC and others either give false indication or very vague hints

### Fixing the PNG
Going further and fixing the file manually by removing the non-standard chunks and putting the compression method back to 0, will provide a new error message:
```bash
└─$ pngcheck -vv glitchin.png
File: glitchin.png (1927767 bytes)
  chunk IHDR at offset 0x0000c, length 13
    1600 x 900 image, 24-bit RGB, non-interlaced
  chunk IDAT at offset 0x00025, length 1927710
    zlib: compression header fails checksum

    zlib: oops! cant initialize (error = -2)
    row filters (0 none, 1 sub, 2 up, 3 avg, 4 paeth):
     
    zlib: inflate error = -2 (stream error)
ERRORS DETECTED in glitchin.png
```

This error tells us that the data within the **IDAT** chunk is not a valid zlib compressed data. This is already 2 hints towards the compression of the file. Knowing that the `compr_method` is supposed to indicate the compression that has been used, we can deduce that the PNG file uses another one. Now we need to find which one.

### Brotli?
A working approach but probably not very efficient now, would be to try every possible compression method that exists until we get a valid PNG file. However, there is a simpler approach to this challenge. The compression algorithm name is hidden within the non-standard private chunks. By playing around with the chunk names, we can find the correct algorithm.
```py
wEBb, cORe, rOOt, bYTe, nULl, sKId # Original
webb, core, root, byte, null, skid # Lowercase
# Lets try to do some combinations
wcrbns # First letters
eooyuk # Second letters
brotli # Third letters
beteld # Last letters
```
The third letters seems a bit more interesting: `brotli`. Its a compression algorithm created by Google! (They do really like Google...)

The easiest solution path now is to decompress the content of the IDAT chunk with brotli and compress it again with zlib to have a valid PNG file.

## Flag
`CSC{br0tl1_f0r_th3_w1n!_b8332f3f}`

## Creator
Maximilien Laenen

## Creator bio
Former CSCBE participant, mainly interested in mobile applications and reverse engineering. I hope you will ~~hate~~ like my challenges! 👀
