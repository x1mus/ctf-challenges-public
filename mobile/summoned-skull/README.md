# Summoned Skull

## Category
Mobile

## Estimated difficulty
Medium

## Description
A kivy app using a Cython module to perform the main encoding scheme. The encoding scheme is a permutation of the letters followed by a permutation of the bits for each letter. The contestant can solve the challenge by reverse engineering the Cython module (or by interacting with it as a black box if he manages to import the module with Python).

## Scenario
You already beat Yugi's weakest monster? That's impressive. However, you will not be able to knock out the next one. This time, the battle will occur in a more native environment! Your fate is sealed.

## Write-up
The app doesnt change that much from the previous one. You also have to decompile the main python bytecode to get the entrypoint. However, one small change appears. The `encode` function is imported and used on the user's input. Here is the `pycdc` decompilation.
```py
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
import subprocess

from encode import encode

class ActivityLayout(GridLayout):
	password = ObjectProperty(None)
	result = ObjectProperty(None)

	def submit(self):
		flag = self.password.text
		if SummonedSkull().check(flag):
			self.result.text = "Good job! Here's your flag:\nCSC{" + flag + "}"
		else:
			self.result.text = "Wrong password :("
		self.password.text = ""


class SummonedSkull(App):
	encoded = [117, 36, 113, 36, 215, 49, 177, 228, 102, 117, 52, 215, 179, 49, 97, 179, 215, 177, 228, 113, 241, 54, 161, 51, 215, 164, 36, 35, 96, 51, 179, 241, 52, 52, 117, 116, 51, 53, 229, 215, 229, 215, 36, 49, 55, 103, 227, 99, 215, 215, 54, 36, 99, 179, 118, 102, 102, 117, 49, 35, 103, 116]

	def build(self):
		return ActivityLayout()

	def check(self, message):
		if len(message) != 62:
			return False

		encoded_message = encode(message)
		
		for a, b in zip(self.encoded, encoded_message):
			if a != b:
				return False

		return True

if __name__ == "__main__":
	SummonedSkull().run()
```

### Finding the native library
The only problem now is that the `encode` package is not present next to the main source code. However, we can inspect the recipe that has been used to build the package:
```py
# File: setup.pyc (Python 3.11)
from distutils.core import setup
from distutils.extension import Extension
extensions = [
	Extension('encode', [
		'encode.c'], language = 'c')]
setup(name = 'encode', ext_modules = extensions)


# File: __init__.pyc (Python 3.11)
from pythonforandroid.recipe import CythonRecipe, IncludedFilesBehaviour

class EncodeRecipe(CythonRecipe, IncludedFilesBehaviour):
	version = '1.0'
	name = 'encode'
	depends = [
		('genericndkbuild', 'sdl2'),
		'setuptools']
	site_package_name = 'encode'
	url = None
	src_filename = 'src'

recipe = EncodeRecipe()
```

It is pretty hard to make the correct google research based only on this to find the location of the package. However, we can browse the directories of the application. The `lib` folder always seems interesting.
```bash
$ ls -lrt
total 31020
-rwxrwx--- 1 root vboxsf  3275912 Jul  7 03:05 libcrypto1.1.so
-rwxrwx--- 1 root vboxsf    71896 Jul  7 03:05 libffi.so
-rwxrwx--- 1 root vboxsf    15832 Jul  7 03:05 libmain.so
-rwxrwx--- 1 root vboxsf 12363974 Jul  7 03:05 libpybundle.so
-rwxrwx--- 1 root vboxsf  5296592 Jul  7 03:05 libpython3.11.so
-rwxrwx--- 1 root vboxsf   773160 Jul  7 03:05 libSDL2_image.so
-rwxrwx--- 1 root vboxsf   486696 Jul  7 03:05 libSDL2_mixer.so
-rwxrwx--- 1 root vboxsf  2932600 Jul  7 03:05 libSDL2.so
-rwxrwx--- 1 root vboxsf  4413880 Jul  7 03:05 libSDL2_ttf.so
-rwxrwx--- 1 root vboxsf  1329264 Jul  7 03:05 libsqlite3.so
-rwxrwx--- 1 root vboxsf   788656 Jul  7 03:05 libssl1.1.so
```

A lot of libraries are present. The easiest way of finding the most important one is to issue the `file` command
```bash
$ file *              
libcrypto1.1.so:  ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, stripped
libffi.so:        ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, stripped
libmain.so:       ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, BuildID[sha1]=4d16f36ef1ac54490486b094cddb940c15419109, stripped
libpybundle.so:   gzip compressed data, was "libpybundle.so", max compression, original size modulo 2^32 25794560
libpython3.11.so: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, stripped
libSDL2_image.so: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, BuildID[sha1]=a95744d506add2eaf01b1ca00a49d572a5a831f4, stripped
libSDL2_mixer.so: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, BuildID[sha1]=bf14e59c8c4f807050a4efd79230e1a2f62ecde3, stripped
libSDL2.so:       ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, BuildID[sha1]=4b64b13a2089bbf1bd080782b73bfaa97ff48f0f, stripped
libSDL2_ttf.so:   ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, BuildID[sha1]=b4378fb498b4761af720376236012aad1c158502, stripped
libsqlite3.so:    ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, BuildID[sha1]=72e20cc63d576839b3ffebe173ecfc325e063955, stripped
libssl1.1.so:     ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, stripped
```

One library stands out: `libpybundle.so`. It seems to be a GZIP file and not an actual library [(doing some research on the filename now gives some more information)](https://kivy.org/doc/stable/guide/licensing.html#android). Let's uncompress everything:
```bash
tar xvf libpybundle.so
```

This will create a `_python_bundle` folder where every modules and site-packages lies. If you look closely, you will find the `encode.so` file at `_python_bundle/site-packages/encode.so`. Hoorah! We have the package.

### Reversing the package
By launching ghidra, we can quickly find the only function containing code and rename it to `encode`. Here's the decompilation of the function:
```c
long encode(undefined8 param_1,undefined8 param_2) {
	byte bVar1;
	int iVar2;
	uint uVar3;
	long lVar4;
	undefined8 uVar5;
	ulong uVar6;
	long lVar7;
	ulong uVar8;
	ulong local_28;
	long local_20;
	
	lVar4 = 0;
	iVar2 = _PyArg_ParseTuple_SizeT(param_2,&DAT_001006af,&local_20,&local_28);
	if (iVar2 != 0) {
		lVar4 = PyList_New(local_28);
	if (lVar4 == 0) {
		lVar4 = 0;
	}
	else if (0 < (long)local_28) {
		uVar8 = 2;
		lVar7 = 0;
		do {
			if ((uVar8 | local_28) >> 0x20 == 0) {
				uVar6 = (uVar8 & 0xffffffff) % (local_28 & 0xffffffff);
			}
			else {
				uVar6 = (long)uVar8 % (long)local_28;
			}
			bVar1 = *(byte *)(local_20 + uVar6);
			uVar3 = (uint)bVar1;
			uVar5 = PyLong_FromLong(
				(bVar1 & 1) << 6 ^ bVar1 & 2 ^ (
					(uVar3 & 8) << 4 | bVar1 >> 2 & 4 | uVar3 & 0x20 | (bVar1 >> 6 & 1) + (uint)(bVar1 >> 7) * 8
				) + (uVar3 & 4) * 4
			);
			PyList_SetItem(lVar4,lVar7,uVar5);
			lVar7 = lVar7 + 1;
			uVar8 = uVar8 + 0x4f;
		} while (lVar7 < (long)local_28);
	}
	}
	return lVar4;
}
```

Let's use the lazy way and ask ChatGPT to provide a simplification of the most important part of the code. Moreover, we will ask it to translate it to python:
```python
def manipulate_user_input(user_input):
	buffer = []
	u_var6 = 2
	l_var5 = 0
	_length = len(user_input)

	while l_var5 < _length:
		u_var4 = u_var6 % _length
		b_var1 = user_input[u_var4]
		
		manipulated_value = ((b_var1 & 1) << 6) ^ (b_var1 & 2) ^ \
							((b_var1 & 8) << 4) | \
							((b_var1 >> 2) & 4) | \
							(b_var1 & 0x20) | \
							(((b_var1 >> 6) & 1) + ((b_var1 >> 7) * 8)) + \
							((b_var1 & 4) * 4)
		
		buffer.append(manipulated_value)
		
		l_var5 += 1
		u_var6 += 79  # 0x4f in hexadecimal

	return buffer

# Example usage:
user_input = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  # Replace this with the actual input array
result = manipulate_user_input(user_input)
print(result)
```
This is way better to analyze:
1. The user input is probably a string and not an integer array
2. u_var4 is actually an index to a character of the user's input. Renamed it `idx`
3. If we calculate the index for the 4 first occurences of the loop, we have something like this (for length=10)
	1. `idx = 2 % length # 2`
	2. `idx = (2+79) % length # 1`
	3. `idx = (2+79+79) % length # 0`
	4. `idx = (2+79+79+79) % length # 9`
	5. We see a common pattern that could be written as `idx = (2+79*i) % length`
	6. Just for clarity, this formula creates a 1-to-1 mapping for each different `i`, therefore this index calculation is "just" a permutation of the letter in the user's input and this can be reconstructed (Note: Only true because the multiplier is a prime number).
4. If the input is a string, we need to get the ascii value of each character before processing it

Refactoring this part of the code looks like this:
```py
def encode(message):
	buffer = []

	for i in range(len(message)):
		idx = ((i*79) + 2) % len(message)
		c = ord(message[idx])
		manipulated_value = ((c & 1) << 6) ^ (c & 2) ^ \
							((c & 8) << 4) | \
							((c >> 2) & 4) | \
							(c & 0x20) | \
							(((c >> 6) & 1) + ((c >> 7) * 8)) + \
							((c & 4) * 4)
		buffer.append(manipulated_value)

	return buffer

print(encode("my_user_input"))
```

Now we could try to understand how all the binary operations work but this would be a bit too much for this challenge. So let's go a tiny bit more dynamic and create a mapping for each of the 256 potential input values. (`ord()` returns a value between 0 and 255). Here's the script to get the mapping: (Note: If the input is 57, the output will be 228. This means that regarding the encoded message if we find the value 228, the decoded value would be 57).
```py
mapping = [0]*256
for c in range(256):
	manipulated_value = ((c & 1) << 6) ^ (c & 2) ^ \
						((c & 8) << 4) | \
						((c >> 2) & 4) | \
						(c & 0x20) | \
						(((c >> 6) & 1) + ((c >> 7) * 8)) + \
						((c & 4) * 4)
	mapping[manipulated_value] = c

print(mapping)
# Output:
# [0, 64, 2, 66, 16, 80, 18, 82, 128, 192, 130, 194, 144, 208, 146, 210, 4, 68, 6, 70, 20, 84, 22, 86, 132, 196, 134, 198, 148, 212, 150, 214, 32, 96, 34, 98, 48, 112, 50, 114, 160, 224, 162, 226, 176, 240, 178, 242, 36, 100, 38, 102, 52, 116, 54, 118, 164, 228, 166, 230, 180, 244, 182, 246, 1, 65, 3, 67, 17, 81, 19, 83, 129, 193, 131, 195, 145, 209, 147, 211, 5, 69, 7, 71, 21, 85, 23, 87, 133, 197, 135, 199, 149, 213, 151, 215, 33, 97, 35, 99, 49, 113, 51, 115, 161, 225, 163, 227, 177, 241, 179, 243, 37, 101, 39, 103, 53, 117, 55, 119, 165, 229, 167, 231, 181, 245, 183, 247, 8, 72, 10, 74, 24, 88, 26, 90, 136, 200, 138, 202, 152, 216, 154, 218, 12, 76, 14, 78, 28, 92, 30, 94, 140, 204, 142, 206, 156, 220, 158, 222, 40, 104, 42, 106, 56, 120, 58, 122, 168, 232, 170, 234, 184, 248, 186, 250, 44, 108, 46, 110, 60, 124, 62, 126, 172, 236, 174, 238, 188, 252, 190, 254, 9, 73, 11, 75, 25, 89, 27, 91, 137, 201, 139, 203, 153, 217, 155, 219, 13, 77, 15, 79, 29, 93, 31, 95, 141, 205, 143, 207, 157, 221, 159, 223, 41, 105, 43, 107, 57, 121, 59, 123, 169, 233, 171, 235, 185, 249, 187, 251, 45, 109, 47, 111, 61, 125, 63, 127, 173, 237, 175, 239, 189, 253, 191, 255]
```

Now that we have the mapping for each of the values, we can also create a mapping for the order of the letters! For this we need the length of the password which is 62 (as described in the main.pyc file).
```py
order = [0]*62
for i in range(62):
	idx = ((i*79) + 2) % 62
	order[idx] = i

print(order)
# Output:
# [40, 51, 0, 11, 22, 33, 44, 55, 4, 15, 26, 37, 48, 59, 8, 19, 30, 41, 52, 1, 12, 23, 34, 45, 56, 5, 16, 27, 38, 49, 60, 9, 20, 31, 42, 53, 2, 13, 24, 35, 46, 57, 6, 17, 28, 39, 50, 61, 10, 21, 32, 43, 54, 3, 14, 25, 36, 47, 58, 7, 18, 29]
```

Everything is now ready to get the flag!
```py
encoded = [117, 36, 113, 36, 215, 49, 177, 228, 102, 117, 52, 215, 179, 49, 97, 179, 215, 177, 228, 113, 241, 54, 161, 51, 215, 164, 36, 35, 96, 51, 179, 241, 52, 52, 117, 116, 51, 53, 229, 215, 229, 215, 36, 49, 55, 103, 227, 99, 215, 215, 54, 36, 99, 179, 118, 102, 102, 117, 49, 35, 103, 116]
order = [40, 51, 0, 11, 22, 33, 44, 55, 4, 15, 26, 37, 48, 59, 8, 19, 30, 41, 52, 1, 12, 23, 34, 45, 56, 5, 16, 27, 38, 49, 60, 9, 20, 31, 42, 53, 2, 13, 24, 35, 46, 57, 6, 17, 28, 39, 50, 61, 10, 21, 32, 43, 54, 3, 14, 25, 36, 47, 58, 7, 18, 29]
mapping = [0, 64, 2, 66, 16, 80, 18, 82, 128, 192, 130, 194, 144, 208, 146, 210, 4, 68, 6, 70, 20, 84, 22, 86, 132, 196, 134, 198, 148, 212, 150, 214, 32, 96, 34, 98, 48, 112, 50, 114, 160, 224, 162, 226, 176, 240, 178, 242, 36, 100, 38, 102, 52, 116, 54, 118, 164, 228, 166, 230, 180, 244, 182, 246, 1, 65, 3, 67, 17, 81, 19, 83, 129, 193, 131, 195, 145, 209, 147, 211, 5, 69, 7, 71, 21, 85, 23, 87, 133, 197, 135, 199, 149, 213, 151, 215, 33, 97, 35, 99, 49, 113, 51, 115, 161, 225, 163, 227, 177, 241, 179, 243, 37, 101, 39, 103, 53, 117, 55, 119, 165, 229, 167, 231, 181, 245, 183, 247, 8, 72, 10, 74, 24, 88, 26, 90, 136, 200, 138, 202, 152, 216, 154, 218, 12, 76, 14, 78, 28, 92, 30, 94, 140, 204, 142, 206, 156, 220, 158, 222, 40, 104, 42, 106, 56, 120, 58, 122, 168, 232, 170, 234, 184, 248, 186, 250, 44, 108, 46, 110, 60, 124, 62, 126, 172, 236, 174, 238, 188, 252, 190, 254, 9, 73, 11, 75, 25, 89, 27, 91, 137, 201, 139, 203, 153, 217, 155, 219, 13, 77, 15, 79, 29, 93, 31, 95, 141, 205, 143, 207, 157, 221, 159, 223, 41, 105, 43, 107, 57, 121, 59, 123, 169, 233, 171, 235, 185, 249, 187, 251, 45, 109, 47, 111, 61, 125, 63, 127, 173, 237, 175, 239, 189, 253, 191, 255]

print("".join([chr(mapping[encoded[i]]) for i in order]))
# output: y0u_h4v3_n0t_b3en_c0nfus3d_by_summ0ned_5kull!_65464d70a8fcd99f
```

## Flag
`CSC{y0u_h4v3_n0t_b3en_c0nfus3d_by_summ0ned_5kull!_65464d70a8fcd99f}`

## Creator
Maximilien Laenen

## Creator bio
Former CSCBE participant, mainly interested in mobile applications and reverse engineering. I hope you will ~~hate~~ like my challenges! 👀