import datetime
import gtts

import os
import random

import playsound2
import PREFS

import subprocess
import sys

import pyjokes

import wikipedia

class Assistant:
	"""Assistant is a cool assistant"""

	def __init__(self):
		super(Assistant, self).__init__()

		default_prefs = {"lang": "en"}
		self.prefs = PREFS.PREFS(default_prefs)

		self.ask()

	def ask(self):
		"""Here the commands
		"""
		commands = {"wikipedia": "Searchs the given text in wikipedia", 
			"date": "Gives you the current date (dd/mm/yy)", 
			"guess_a_number": "Simple guess number game", 
			"joke": "Tells you a joke", 
			"hour": "Gives you the current hour", 
			"note": "Creates a file with the given text and open text editor", 
			"exit": "Exits the program"}

		text = input("What do you want to do: ")
		command = text.split()[0]
		args = text[len(command) + 1:]

		if command == "wikipedia" :
			self.search_wikipedia(args)

		elif command == "date":
			date = datetime.datetime.now().strftime('%d/%m/%Y')
			self.talk(date)
		
		elif "guess_a_number" in command:
			self.guess()

		elif command == "joke":
			self.talk(pyjokes.get_joke())

		elif command == "hour":
			time = datetime.datetime.now().strftime('%I:%M %p')
			self.talk(time)
		
		elif command == "note":
			self.note(args)		
		
		elif command == "help":
			self.talk( "\n".join([f"{k}: {v}" for k, v in commands.items()]) )

		elif command == "exit":
			sys.exit()
			return
		else:
			self.talk("Couldn't understand you, type help to see the available commands")
		
		self.ask()

	def search_wikipedia(self, search):
		results = wikipedia.summary(search, 3)
		self.talk(results)

	def talk(self, text, save=False, lang=None, filename="temp", extension="mp3"):

		lang = self.prefs.file["lang"]

		sound = gtts.gTTS(text, lang=lang)

		sound.save(f'{filename}.{extension}')
		
		print(text)

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


# Elsa#2561
# https://github.com/atreyaved
# Pronouns: he

# ᑎᗩᑕᖇᗴᝪᑌᔑᗞᗩᗯᑎ596#9360
# https://github.com/NacreousDawn596
# Pronouns: he

# patitotective#0217
# https://github.com/Patitotective
# Pronouns: she


def main():
	assistant = Assistant()

if __name__ == "__main__":
	main()
