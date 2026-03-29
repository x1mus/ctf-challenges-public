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
		# CSC{Yug1_l0v3s_th1S_c4rd_MAyb3_u_5houLd_7_it_242fa8174905de5f}
		return ActivityLayout()

	def check(self, message):
		return self.magician.magic(message)

if __name__ == "__main__":
	DarkMagician().run()