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
		# CSC{y0u_h4v3_n0t_b3en_c0nfus3d_by_summ0ned_5kull!_65464d70a8fcd99f}
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