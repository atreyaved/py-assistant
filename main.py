# main.py

# Libraries
import datetime
import gtts

import os
import random

import playsound2
import PREFS

import subprocess
import sys

import pyjokes
import requests

import wikipedia
import random

import string
import pywhatkit

# Dependencies
import adventure
import json

import requests
import time

class Assistant:
	"""Assistant is a cool assistant"""

	def __init__(self):
		super(Assistant, self).__init__()

		self.prefs = PREFS.PREFS({"lang": "en"})
		self.translations = PREFS.ReadPREFSFile("translations")

		self.commands = {
			"wikipedia": self.translations["wikipedia"][self.prefs.file["lang"]],
			"date": self.translations["date"][self.prefs.file["lang"]],
			"guess_the_number": self.translations["guess_the_number"][self.prefs.file["lang"]],
			"adventure_game": self.translations["adventure_game"][self.prefs.file["lang"]],
			"joke": self.translations["joke"][self.prefs.file["lang"]],
			"hour": self.translations["hour"][self.prefs.file["lang"]],
			"note": self.translations["note"][self.prefs.file["lang"]],
			"quote": self.translations["quote"][self.prefs.file["lang"]],
			"language": self.translations["language"][self.prefs.file["lang"]],
			"supported_languages": self.translations["supported_languages"][self.prefs.file["lang"]],

			"help": self.translations["help"][self.prefs.file["lang"]],
			"exit": self.translations["exit"][self.prefs.file["lang"]]
		}

		self.supported_languages = {
			"es": ["spanish", "español", "sp", "es"],
			"en": ["english", "inglés", "ingles", "en"],
			"hd": ["hindi", "hd"],
			"jp": ["japanese", "jp", "japonés", "japones"]
		}

		self.ask()

	def ask(self):
		"""Here the commands
		"""
		self.talk(self.get_translation("ask"), print_text=False)
		text = input(self.get_translation("ask"))

		command = text.split()[0]
		args = text[len(command) + 1:]

		if command == "wikipedia" :
			self.search_wikipedia(args)

		elif command == "date":
			date = datetime.datetime.now().strftime('%d/%m/%Y')
			self.talk(date)

		elif  command == "guess_the_number":
			self.guess()

		elif command == "adventure_game":
			self.adventure()

		elif command == "joke":
			self.talk(pyjokes.get_joke())

		elif command == "hour":
			time = datetime.datetime.now().strftime('%I:%M %p')
			self.talk(time)

		elif command == "note":
			self.note(args)

		# elif command == "info":
			# self.info()

		elif command == "help":
			self.talk( "\n".join([f"{k}: {v}" for k, v in self.commands.items()]) )

		elif command == "exit":
			sys.exit()
			return

		elif command == "quote":
			self.quote()

		elif command == "supported_languages":
			self.talk(" - ".join([v[0] for k, v in self.supported_languages.items()]) )

		elif command == "language":
			self.change_language(args)
		elif command == "password":
			self.password()

		elif 'play' in command:
			self.play_youtube(args)

		elif 'talk' in command :
			self.talk("Well, thats what im here to do, to talk to you and help you with your needs")
		elif 'dance' in command:
			self.talk("ummm, soo, i cant really do that because, im a robot")
		elif '	'


		else:
			self.talk(self.get_translation("not_found"))

		self.ask()

	def search_wikipedia(self, search):
		results = wikipedia.summary(search, 3)
		self.talk(results)

	def get_translation(self, key):
		try:
			text = self.translations[key][self.prefs.file["lang"]]
		except:
			text = self.translations[key]["en"]

		return text

	def talk(self, text, save=False, lang=None, filename="temp", extension="mp3", print_text=True):

		lang = self.prefs.file["lang"] if lang == None else lang

		try:
			sound = gtts.gTTS(text, lang=lang)
		except:
			sound = gtts.gTTS(text, lang="en")

		sound.save(f'{filename}.{extension}')

		if print_text: print(text)

		playsound2.playsound(f"{filename}.{extension}")
		if not save: os.remove(f"{filename}.{extension}")

	def note(self, text, filename="", extension="txt"):

		currentdate = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
		filename =  currentdate + f".{extension}" if filename == "" else filename + f".{extension}"

		with open(filename, "w") as f: #what is the difference between this and f = open()
			f.write(text)

		try:
			platform = sys.platform

			if platform == "linux":
				subprocess.Popen(['gedit', filename])
			else:
				subprocess.Popen(["notepad.exe", filename])
		except IndexError:
			subprocess.Popen(["notepad.exe", filename])


		#subprocess.Popen(["notepad.exe", filename])
		#subprocess.Popen(['gedit', 'file_name'])
		NOTE_STRS = ["make a note", "filename this down", "remember this", "type this"]
		for phrase in NOTE_STRS :
				if phrase in text :
					speak("What would you like me to write down?")
					write_down = input ("->")
					note(write_down)
					speak("Done!")

	def quote(self):
		url = 'https://api.quotable.io/random'
		request = requests.get(url)

		info = request.json()
		quote = info['content']
		author = info["author"]

		self.talk(f"«{quote}» -{author}")

	def guess(self, number_to_guess=None):
		if number_to_guess == None: self.talk("<- Guess a number between 0 and 100 ->")

		number_to_guess = random.randint(0, 101) if number_to_guess == None else number_to_guess

		number = int(input("Enter a number: "))

		if number > number_to_guess:
			self.talk("Wrong, try a smaller number.")
			self.guess(number_to_guess=number_to_guess)

		elif number < number_to_guess:
			self.talk("Wrong, try a bigger number.")
			self.guess(number_to_guess=number_to_guess)

		elif number == number_to_guess:
			self.talk("Congratulations, you have won.")
			choice = input("Do you want to play again? (y/n): ").lower()

			if choice == "y" or choice == "yes":
				self.guess()
			else:
				self.ask()
		else:
			self.talk("Please, try again")
			self.guess(number_to_guess=number_to_guess)

	def info(self):
		self.talk("Enter your information: ")

		self.talk("Name", print_text=False)
		name = input("\tName: ")
		self.prefs.WritePrefs(name, {})

		self.talk("Nickname", print_text=False)
		nickname = input("\tNickname: ")
		self.prefs.WritePrefs(f"{name}/nickname", nickname)

		self.talk("Age", print_text=False)
		age = input("\tAge: ")
		self.prefs.WritePrefs(f"{name}/age", age)

		self.talk("Discord", print_text=False)
		discord = input("\tDiscord: ")
		self.prefs.WritePrefs(f"{name}/discord", discord)

	def change_language(self, lang):
		languages = []

		for k, v in self.supported_languages.items():
			if lang in v:
				languages.append(k)

		if len(languages) == 0:
			self.talk(self.get_translation("not_lang"))
			return
		elif len(languages) > 1:
			self.talk(self.get_translation("not_understood"))
			return

		self.prefs.WritePrefs("lang", languages[0])

	def adventure(self):
		adventure.start()

	def password(self):
		lower = string.ascii_lowercase
		upper = string.ascii_uppercase
		num = string.digits
		all = lower + upper + num
		temp = random.sample(all,10)
		random_password = "".join(temp)
		self.talk("Here is your highly secure password")
		print(random_password)

	def play_youtube(self, 	video):
		self.talk('playing ' + video)
		pywhatkit.playonyt(video)



# Elsa#2561
# https://github.com/atreyaved
# Pronouns: she

# ᑎᗩᑕᖇᗴᝪᑌᔑᗞᗩᗯᑎ596#9360
# https://github.com/NacreousDawn596
# Pronouns: he

# patitotective#0217
# https://github.com/Patitotective
# Pronouns: he


def main():
	assistant = Assistant()

if __name__ == "__main__":
	main()
