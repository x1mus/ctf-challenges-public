# Dark Magician

## Category
Mobile

## Estimated difficulty
Hard

## Description
A kivy app using a Cython module to perform an unscrambling of the source code using ASTs and then execute it. The module takes the `check.python` file, unscrambles it and loads the defined functions dynamically. The scrambling just permutes lines of code around and also permutes the original encoded list. The contestant can solve the challenge by dumping the memory of the running application using `fridump` to retrieve the unscrambled code. The other approach would be to reverse engineer the ASTs scrambler to understand/patch and retrieve the unscrambled code.

## Scenario
So... you are dump enough to face Yugi's favorite monster. However, he still got some tricks up his sleeve.

## Write-up
The app doesnt change that much from the previous ones. You also have to decompile the main python bytecode to get the entrypoint. However, one small change appears (again). No encoding is done from this file. Everything is done inside the `magic` native library where we call `__init__()` and `magic()` Here is the `pycdc` decompilation.
```py
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
import subprocess

from magic import Magician


class ActivityLayout(GridLayout):
	password = ObjectProperty(None)
	result = ObjectProperty(None)

	def submit(self):
		flag = self.password.text
		if DarkMagician().check(flag):
			self.result.text = "Good job! Here's your flag:\nCSC{" + flag + "}"
		else:
			self.result.text = "Wrong password :("
		self.password.text = ""


class DarkMagician(App):
	def __init__(self):
		super(DarkMagician, self).__init__()
		self.magician = Magician()

	def build(self):
		return ActivityLayout()

	def check(self, message):
		return self.magician.magic(message)

if __name__ == "__main__":
	DarkMagician().run()
```

Another important file that is available just next to the `main` file is `check.python`.
```py
# This code has been scrambled using some dark magic o.O
def check(message):
	return True
	for (i, letter) in enumerate(message):
		searchme = (searchme - 702) % 256
		searchme = (searchme << 4 | searchme >> 4) % 256
		searchme = (searchme << 5 | searchme >> 3) % 256
		searchme = (searchme + 979) % 256
		searchme = (searchme + 219) % 256
		searchme = (searchme ^ 637) % 256
		searchme = (searchme >> 1 | searchme << 7) % 256
		searchme = searchme * 569 % 256
		searchme = searchme * 277 % 256
		searchme = (searchme >> 6 | searchme << 2) % 256
		searchme = searchme * 43 % 256
		searchme = (searchme + 689) % 256
		searchme = searchme * 139 % 256
		searchme = searchme * 13 % 256
		searchme = (searchme >> 5 | searchme << 3) % 256
		searchme = (searchme + 322) % 256
		searchme = searchme * 229 % 256
		searchme = (searchme ^ 219) % 256
		searchme = searchme * 31 % 256
		searchme = (searchme ^ 547) % 256
		searchme = (searchme >> 3 | searchme << 5) % 256
		searchme = (searchme << 1 | searchme >> 7) % 256
		searchme = (searchme + 419) % 256
		searchme = (searchme + 273) % 256
		searchme = searchme * 193 % 256
		searchme = (searchme >> 4 | searchme << 4) % 256
		searchme = (searchme << 7 | searchme >> 1) % 256
		searchme = (searchme - 22) % 256
		searchme = (searchme ^ 270) % 256
		searchme = (searchme >> 3 | searchme << 5) % 256
		searchme = (searchme + 668) % 256
		searchme = (searchme >> 3 | searchme << 5) % 256
		searchme = searchme * 241 % 256
		searchme = (searchme >> 2 | searchme << 6) % 256
		searchme = (searchme ^ 356) % 256
		searchme = (searchme << 7 | searchme >> 1) % 256
		searchme = searchme * 313 % 256
		searchme = (searchme << 3 | searchme >> 5) % 256
		searchme = (searchme >> 6 | searchme << 2) % 256
		searchme = (searchme - 103) % 256
		searchme = (searchme + 220) % 256
		searchme = searchme * 761 % 256
		searchme = (searchme >> 4 | searchme << 4) % 256
		searchme = (searchme ^ 356) % 256
		searchme = (searchme << 2 | searchme >> 6) % 256
		searchme = (searchme ^ 193) % 256
		searchme = searchme * 53 % 256
		searchme = (searchme >> 2 | searchme << 6) % 256
		searchme = (searchme + 203) % 256
		if searchme != encoded[i]:
			return False
		searchme = searchme * 29 % 256
		searchme = (searchme + 499) % 256
		searchme = ord(letter)
		searchme = searchme * 31 % 256
		searchme = (searchme >> 2 | searchme << 6) % 256
		searchme = searchme * 809 % 256
		searchme = searchme * 487 % 256
		searchme = searchme * 977 % 256
		searchme = searchme * 661 % 256
		searchme = (searchme + 184) % 256
		searchme = (searchme >> 4 | searchme << 4) % 256
		searchme = (searchme << 2 | searchme >> 6) % 256
		searchme = (searchme << 6 | searchme >> 2) % 256
		searchme = (searchme + 713) % 256
		searchme = (searchme ^ 103) % 256
		searchme = (searchme ^ 111) % 256
		searchme = (searchme + 929) % 256
		searchme = (searchme + 628) % 256
		searchme = searchme * 947 % 256
		searchme = searchme * 29 % 256
		searchme = (searchme + 61) % 256
		searchme = (searchme ^ 240) % 256
		searchme = (searchme >> 6 | searchme << 2) % 256
		searchme = (searchme ^ 535) % 256
		searchme = (searchme << 3 | searchme >> 5) % 256
		searchme = (searchme >> 4 | searchme << 4) % 256
		searchme = (searchme << 4 | searchme >> 4) % 256
		searchme = (searchme >> 6 | searchme << 2) % 256
		searchme = searchme * 349 % 256
		searchme = (searchme + 268) % 256
		searchme = (searchme + 391) % 256
		searchme = (searchme ^ 116) % 256
		searchme = searchme * 61 % 256
		searchme = (searchme ^ 818) % 256
		searchme = (searchme + 657) % 256
		searchme = (searchme + 134) % 256
		searchme = (searchme >> 5 | searchme << 3) % 256
		searchme = searchme * 47 % 256
		searchme = (searchme >> 3 | searchme << 5) % 256
		searchme = (searchme >> 6 | searchme << 2) % 256
		searchme = searchme * 149 % 256
		searchme = (searchme >> 1 | searchme << 7) % 256
		searchme = searchme * 179 % 256
		searchme = (searchme - 93) % 256
		searchme = searchme * 83 % 256
		searchme = (searchme + 53) % 256
		searchme = searchme * 59 % 256
		searchme = (searchme >> 3 | searchme << 5) % 256
		searchme = (searchme - 470) % 256
		searchme = (searchme << 2 | searchme >> 6) % 256
		searchme = (searchme << 4 | searchme >> 4) % 256
		searchme = (searchme - 321) % 256
	if len(message) != len(encoded):
		return False
	encoded = [243, 227, 164, 92, 8, 243, 87, 243, 128, 142, 28, 24, 243, 24, 12, 156, 132, 11, 252, 12, 128, 253, 219, 87, 88, 88, 217, 132, 88, 8, 101, 11, 161, 127, 243, 79, 253, 23, 176, 142, 243, 11, 164, 243, 144, 12, 65, 87, 143, 90, 243, 123, 196, 176, 211, 8, 243]
```

This file contains multiple useful information:
1. The comment: "# This code has been scrambled using some dark magic o.O"
2. The code itself. The lines appears to be moved around
3. The encoded flag as we used to have in the `main.py` file
4. A lot of repetitive operation looking like `x = x <op> <const> % 256`
5. The variable name `searchme`

From this point we could try to reorder by hand the function to make it more viable and "normal" looking such as this:
```py
# This code has been scrambled using some dark magic o.O
def check(message):
	encoded = [243, 227, 164, 92, 8, 243, 87, 243, 128, 142, 28, 24, 243, 24, 12, 156, 132, 11, 252, 12, 128, 253, 219, 87, 88, 88, 217, 132, 88, 8, 101, 11, 161, 127, 243, 79, 253, 23, 176, 142, 243, 11, 164, 243, 144, 12, 65, 87, 143, 90, 243, 123, 196, 176, 211, 8, 243]
	
	if len(message) != len(encoded):
		return False
	
	for (i, letter) in enumerate(message):
		searchme = ord(letter)
		searchme = (searchme - 702) % 256
		searchme = (searchme << 4 | searchme >> 4) % 256
		searchme = (searchme << 5 | searchme >> 3) % 256
		# Operations cropped for clarity
		searchme = (searchme >> 3 | searchme << 5) % 256
		searchme = (searchme - 470) % 256
		searchme = (searchme << 2 | searchme >> 6) % 256
		searchme = (searchme << 4 | searchme >> 4) % 256
		searchme = (searchme - 321) % 256
		if searchme != encoded[i]:
			return False
	
	return True
```

Doing this will however lead to nowhere since the order of the operations are not correct and bruteforcing the order is in theory not possible (100 operations so 100! possibilities). Maybe we will get lucky with the native library as for the previous challenge.

### The native library
To find the native library, just proceed as for the previous challenge (`libpybundle.so`, etc.). However, when the native library has been found and imported in Ghidra. You will soon realize that it is not simple to reverse the algorithm. The algorithm is based on ASTs and then converted automatically to Cython to make the reversing of the library harder (maybe even impossible in the timeframe of the challenge). A potential solution to still use reverse engineering would therefore be to understand the global logic and try to patch the binary to make it return the unscrambled code instead of executing it.

### Going dynamic
When reverse engineering is not enough, going dynamic might be the best approach. By deduction or by analyzing the library, we can make some educated guesses:
1. The `magic.Magician().__init__()` method probably unscrambles the code and saves it
2. The `magic.Magician().magic()` method probably executes the unscrambled code when we submit our input

If the code is being unscrambled and saved then it must be loaded in memory! (Moreover, the `dump` keyword in the scenario is not a typo).

### Dumping memory
To dump the memory of an android application, we can use `fridump`. This tool is based on `frida` and allows us to dump most of the memory related to an application. (Note: Sometimes optimisation, stack variability, ... might provide different memory dump so trying multiple times is definitely recommended if you do not find anything interesting on the first try).

```console
$ python3 fridump.py -U 'Dark Magician' 

        ______    _     _
        |  ___|  (_)   | |
        | |_ _ __ _  __| |_   _ _ __ ___  _ __
        |  _| '__| |/ _` | | | | '_ ` _ \| '_ \
        | | | |  | | (_| | |_| | | | | | | |_) |
        \_| |_|  |_|\__,_|\__,_|_| |_| |_| .__/
                                         | |
                                         |_|
        
Current Directory: /home/x1mus/Desktop/shared/fridump
Output directory is set to: /home/x1mus/Desktop/shared/fridump/dump
Creating directory...
Starting Memory dump...
Progress: [#################################################-] 98.99% Complete
Finished!
```

This will create a `dump` directory containing a lot of information. Now comes the tricky part, locating the unscrambled code. Luckily, the creator of the challenge has been nice and provided a unique variable name for you to search (remember ?) `searchme`.
```console
$ grep searchme *
Binary file 0x734e48f000_dump.data matches
Binary file 0x7353202000_dump.data matches
Binary file 0x7353a87000_dump.data matches
Binary file 0x75565a8000_dump.data matches
Binary file 0x75565e8000_dump.data matches
Binary file 0x75665a4000_dump.data matches
Binary file 0x75665e4000_dump.data matches
```

Now that we know in which file we should be looking, we will use a combination of `strings` and `grep` to get the most interesting output. (Of course you will find also a lot of: garbage, incomplete code, scrambled code, ... but with a little bit of determination we can find the perfect output).
```console
$ strings 0x75565e8000_dump.data | grep searchme
        searchme = ord(letter)
        searchme = (searchme + 499) % 256
        searchme = (searchme >> 2 | searchme << 6) % 256
        # Operations cropped for clarity
        searchme = (searchme + 203) % 256
        searchme = (searchme >> 2 | searchme << 6) % 256
        searchme = searchme * 29 % 256
```

This looks very promising! The first instruction being `searchme = ord(letter)` which defines the variable. Lets now write a little script to get a mapping for each input:
```py
encoded = [101, 8, 161, 11, 243, 127, 253, 79, 176, 23, 243, 142, 164, 11, 144, 243, 65, 12, 143, 87, 243, 90, 196, 123, 211, 176, 243, 8, 243, 88, 164, 227, 8, 92, 87, 243, 128, 243, 28, 142, 243, 24, 12, 24, 132, 156, 252, 11, 128, 12, 219, 253, 88, 87, 217, 88, 132,]
mapping = [""]*256
for x in range(256):
    searchme = x
    searchme = (searchme + 499) % 256
    searchme = (searchme >> 2 | searchme << 6) % 256
    searchme = searchme * 31 % 256
    searchme = searchme * 487 % 256
    searchme = searchme * 809 % 256
    searchme = searchme * 661 % 256
    searchme = searchme * 977 % 256
    searchme = (searchme >> 4 | searchme << 4) % 256
    searchme = (searchme + 184) % 256
    searchme = (searchme << 6 | searchme >> 2) % 256
    searchme = (searchme << 2 | searchme >> 6) % 256
    searchme = (searchme ^ 103) % 256
    searchme = (searchme + 713) % 256
    searchme = (searchme + 929) % 256
    searchme = (searchme ^ 111) % 256
    searchme = searchme * 947 % 256
    searchme = (searchme + 628) % 256
    searchme = (searchme + 61) % 256
    searchme = searchme * 29 % 256
    searchme = (searchme >> 6 | searchme << 2) % 256
    searchme = (searchme ^ 240) % 256
    searchme = (searchme << 3 | searchme >> 5) % 256
    searchme = (searchme ^ 535) % 256
    searchme = (searchme << 4 | searchme >> 4) % 256
    searchme = (searchme >> 4 | searchme << 4) % 256
    searchme = searchme * 349 % 256
    searchme = (searchme >> 6 | searchme << 2) % 256
    searchme = (searchme + 391) % 256
    searchme = (searchme + 268) % 256
    searchme = searchme * 61 % 256
    searchme = (searchme ^ 116) % 256
    searchme = (searchme + 657) % 256
    searchme = (searchme ^ 818) % 256
    searchme = (searchme >> 5 | searchme << 3) % 256
    searchme = (searchme + 134) % 256
    searchme = (searchme >> 3 | searchme << 5) % 256
    searchme = searchme * 47 % 256
    searchme = searchme * 149 % 256
    searchme = (searchme >> 6 | searchme << 2) % 256
    searchme = searchme * 179 % 256
    searchme = (searchme >> 1 | searchme << 7) % 256
    searchme = searchme * 83 % 256
    searchme = (searchme - 93) % 256
    searchme = searchme * 59 % 256
    searchme = (searchme + 53) % 256
    searchme = (searchme - 470) % 256
    searchme = (searchme >> 3 | searchme << 5) % 256
    searchme = (searchme << 4 | searchme >> 4) % 256
    searchme = (searchme << 2 | searchme >> 6) % 256
    searchme = (searchme - 702) % 256
    searchme = (searchme - 321) % 256
    searchme = (searchme << 5 | searchme >> 3) % 256
    searchme = (searchme << 4 | searchme >> 4) % 256
    searchme = (searchme + 219) % 256
    searchme = (searchme + 979) % 256
    searchme = (searchme >> 1 | searchme << 7) % 256
    searchme = (searchme ^ 637) % 256
    searchme = searchme * 277 % 256
    searchme = searchme * 569 % 256
    searchme = searchme * 43 % 256
    searchme = (searchme >> 6 | searchme << 2) % 256
    searchme = searchme * 139 % 256
    searchme = (searchme + 689) % 256
    searchme = (searchme >> 5 | searchme << 3) % 256
    searchme = searchme * 13 % 256
    searchme = searchme * 229 % 256
    searchme = (searchme + 322) % 256
    searchme = searchme * 31 % 256
    searchme = (searchme ^ 219) % 256
    searchme = (searchme >> 3 | searchme << 5) % 256
    searchme = (searchme ^ 547) % 256
    searchme = (searchme + 419) % 256
    searchme = (searchme << 1 | searchme >> 7) % 256
    searchme = searchme * 193 % 256
    searchme = (searchme + 273) % 256
    searchme = (searchme << 7 | searchme >> 1) % 256
    searchme = (searchme >> 4 | searchme << 4) % 256
    searchme = (searchme ^ 270) % 256
    searchme = (searchme - 22) % 256
    searchme = (searchme + 668) % 256
    searchme = (searchme >> 3 | searchme << 5) % 256
    searchme = searchme * 241 % 256
    searchme = (searchme >> 3 | searchme << 5) % 256
    searchme = (searchme ^ 356) % 256
    searchme = (searchme >> 2 | searchme << 6) % 256
    searchme = searchme * 313 % 256
    searchme = (searchme << 7 | searchme >> 1) % 256
    searchme = (searchme >> 6 | searchme << 2) % 256
    searchme = (searchme << 3 | searchme >> 5) % 256
    searchme = (searchme + 220) % 256
    searchme = (searchme - 103) % 256
    searchme = (searchme >> 4 | searchme << 4) % 256
    searchme = searchme * 761 % 256
    searchme = (searchme << 2 | searchme >> 6) % 256
    searchme = (searchme ^ 356) % 256
    searchme = searchme * 53 % 256
    searchme = (searchme ^ 193) % 256
    searchme = (searchme + 203) % 256
    searchme = (searchme >> 2 | searchme << 6) % 256
    searchme = searchme * 29 % 256
    mapping[searchme] = x

for c in encoded:
    print(chr(mapping[c]), end="")
```

Be careful that you need to use the `encoded` list gathered from memory because it has also been scrambled. The output is the flag.

## Flag
`CSC{Yug1_l0v3s_th1S_c4rd_MAyb3_u_5houLd_7_it_242fa8174905de5f}`

## Creator
Maximilien Laenen

## Creator bio
Former CSCBE participant, mainly interested in mobile applications and reverse engineering. I hope you will ~~hate~~ like my challenges! 👀
