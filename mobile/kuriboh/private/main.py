from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty


class ActivityLayout(GridLayout):
	password = ObjectProperty(None)
	result = ObjectProperty(None)

	def submit(self):
		flag = self.password.text
		if Kuriboh().check(flag):
			self.result.text = "Good job! Here's your flag:\nCSC{" + flag + "}"
		else:
			self.result.text = "Wrong password :("
		self.password.text = ""


class Kuriboh(App):
	encoded = [139, 149, 146, 209, 130, 208, 136, 191, 209, 213, 191, 150, 211, 146, 153, 191, 131, 149, 148, 211, 193, 193, 193, 191, 209, 130, 217, 132, 129, 217, 131, 134, 215, 132, 213, 130, 215, 134, 209, 133]

	def build(self):
		return ActivityLayout()

	def check(self, message):
		if len(message) != len(self.encoded):
			return False
		
		for a,b in zip(self.encoded, message):
			if a ^ ord(b) != 224:
				return False
		
		return True

if __name__ == "__main__":
	Kuriboh().run()