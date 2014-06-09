#!/usr/bin/env python
# -*- code: utf-8 -*-

import sys
import random
import re

wordDict = dict()
with open("enable1.txt") as openedFile:
	for line in openedFile:
		word = line.strip()
		length = len(word)
		if length < 4:
			continue
		try:
			word = line.strip()
			wordDict[len(word)].append(word)
		except KeyError:
			wordDict[len(word)] = [word]

class Mastermind(object):
	"""
	This is the Mastermind game class.
	When using the class, either the difficulty can be set to an integer and the other attributes calculated from that 
	or the difficulty can be set to None and the word length and number of guesses can be set manually. So if difficulty
	is set to anything other than None, then the wordLength and guesses are superfluous. The object will first have it's
	difficulty, wordLength, and guesses set, and then the set method will pick out the word to guess. The dictionary of
	words is created from a file "enable1.txt" which is read when this module is loaded.
	"""

	_words = wordDict
	
	def __init__(self, wordLength=6, guesses=10, difficulty=None):
		self._difficulty = difficulty
		if self._difficulty is not None:
			self._wordLength, self._guesses = self.calculateFromDifficulty()
		else:
			self._wordLength, self._guesses = wordLength, guesses
		self._word = self.chooseRandomWord()
		self._attemptsLeft = self.guesses
		self._lastResult = "_"*self._wordLength

	@property
	def difficulty(self):
		"""This is the difficulty set at the initialization of the instance"""
		return self._difficulty

	@property
	def wordLength(self):
		"""This is the length of the word chosen to guess"""
		return self._wordLength

	@property
	def guesses(self):
		"""This the number of guesses set at the initialization of the instance"""
		return self._guesses

	@property
	def word(self):
		"""This is the word to guess."""
		return self._word

	@property
	def attemptsLeft(self):
		"""This is the number of attempts left."""
		return self._attemptsLeft

	@property
	def lastResult(self):
		"""This is the last result of the guess; the initial value is a string of underscores signifying the blank
		letters."""
		return self._lastResult

	def calculateFromDifficulty(self):
		if self._difficulty is not None:
			wordLength, guesses = 3 + self._difficulty, 10
			return wordLength, guesses

	def chooseRandomWord(self):
		return random.choice(self._words[self._wordLength])

	def guess(self, word):
		"""
		This takes a word and checks the length against the wordLength attribute and if it doesn't match, then returns
		None. If the word passes, then it is checked for matches. Matches in letter and position will appear with that
		letter in the string while matches in letter will but not position will have an asterisk in that position. The
		rest of the positions will be underscores, meaning no match or similarity. E.g.
		correct word	= soapy
		guess word		= sands
		result			= s*___
		The second 's' won't match because the first 's' is in the right spot and there are no more 's's to match.

		This method will return a dictionary with a status of the guess and the result of the guess. The statuses could
		be
		'LETTERS'		= not enough letters given
		'WINNER'		= the correct word was found
		'DONE'			= the last guess was used and the user didn't win
		'AGAIN'			= there are more attempts
		'OUT'			= there are no more attempts left and you should stop guessing
		"""
		status, result = None, None
		if len(word) != self._wordLength or re.match(r'^[a-zA-Z]*$', word) is None:
			#status = "There weren't enough letters, you gave me {0} out of {1}.".format(len(word), self._wordLength)
			status = 'LETTERS'
		elif self._attemptsLeft > 0:
			self._attemptsLeft -= 1
			result = self.checkMatch(word.lower())
			self._lastResult = result
			if result == self._word:
				#status = "You are a winner."
				status = 'WINNER'
			elif self._attemptsLeft == 0:
				#status = "That was your last attempt I'm afraid."
				status = 'DONE'
			else:
				#status = "You have {0} attempts left.".format(self._attemptsLeft)
				status = 'AGAIN'
		else:
			#status = "You have no more attempt. Sorry. :("
			status = 'OUT'
		return {
			'status': status,
			'result': result
			}
	
	def checkMatch(self, guessWord):
		"""
		This checks the word and returns the result which is a string indicating where correct letter are located and
		where letters in the word are located but not in the right position.
		"""
		matches = [] # indices for matches in character and position
		similars = [] # indices for matches in character but different position
		counted = [] # indices for the letters which have been accounted for in the correct word
		for index, letter in enumerate(guessWord):
			if letter == self._word[index]:
				matches.append(index)
				counted.append(index)
				continue
		for index, letter in enumerate(guessWord):
			for i in xrange(self.wordLength):
				if i == index:
					continue
				elif letter == self._word[i] and i not in counted:
					similars.append(index)
					counted.append(i)
					break
		result = ''.join([guessWord[i] if i in matches else '*' if i in similars else '_' for i in xrange(self.wordLength)])
		return result

class Phase(object):

	_phrases = (
			"What did you say?",
			"How is that even funny?",
			"nechfnshfaufsdn, I can type random gibberish, too.",
			"Y U NO ANSUR RITE.",
			"Think before you type.",
			)
	
	def start(self):
		print "This phase of the game hasn't been written, sorry about that. We will restart the game."
		return 'beginning'

	def wut(self):
		print random.choice(self._phrases)

class Beginning(Phase):
	
	def start(self):
		print "Welcome to the game."
		tries = 4
		while tries > 0:
			action = raw_input("Do you want to play Mastermind? (y/n)\n> ")
			if action == "y":
				return 'setup',
			elif action == "n":
				return 'exit',
			else:
				tries -= 1
				print "That isn't a valid answer. You have {0} more tries/try to answer correctly.".format(tries)
		print "You couldn't give a 'y' or 'n' so..."
		return 'exit',

class Setup(Phase):

	def start(self):
		wordLength, guesses, difficulty = None, None, None
		difficultyDefault = 3
		tries = 5
		while tries > 0:
			difficulty = None
			choice = int(raw_input("Would you rather choose the difficulty (1) or set the word length and number of guesses manually (2). Pick 1 or 2 accordingly.\n> "))
			if choice == 1:
				difficulty = int(raw_input("What difficulty do you want? (easiest 1-12 hardest)\n> "))
				if difficulty in range(1, 13):
					self.difficultySet(difficulty)
					break
				else:
					tries -= 1
					self.tryAgain(tries, difficultyDefault)
					continue
				if tries == 0:
					self.difficultySet(difficulty)
					difficulty = difficultyDefault # default
			elif choice == 2:
				wordLength = raw_input("What word length do you want? (4 - 15 characters)\n. ")
				if wordLength not in range(4, 16):
					tries -= 1
					self.tryAgain(tries, difficultyDefault)
					continue
				guesses = raw_input("How many guesses do you want? (More than 0)\n> ")
				if not isinstance(guesses, int) or guesses < 0:
					tries -= 1
					self.tryAgain(tries, difficultyDefault)
					continue
				print "The word length has been set to {0} and the number of guesses has been set to {1}.".format(wordLength, guesses)
				break
			else:
				self.wut()
				self.tryAgain(tries, difficultyDefault)
			if tries == 0:
				difficulty = difficultyDefault
				self.difficultySet(difficulty)

		game = Mastermind(wordLength=wordLength, guesses=guesses, difficulty=difficulty)
		return 'game', game

	def tryAgain(self, tries, diff):
		print "This isn't a valid answer. You have {0} more tries/try to answer correctly. Otherwise it will be set to the default difficulty, {1}.".format(tries, diff)
	
	def difficultySet(self, diff):
		print "The difficulty has been set to {0}.".format(diff)

class Game(Phase):

	def __init__(self, mm):#mm should be an instance of the Mastermind class
		self.mm = mm#Mastermind(wordLength=wordLength, guesses=guesses, difficulty=difficulty)

	def start(self):
		print "Guess the {0} letter word in {1} attempts. Each letter is from the English alphabet.".format(self.mm.wordLength, self.mm.guesses)
		self.printOptions()
		while True:
			action = self.ask()#raw_input("What would you like to do?\n> ")
			if action == 'g':
				guess = raw_input("What is your guess? ({0} letters)\n> ".format(self.mm.wordLength))
				answer = self.mm.guess(guess)
				s = answer['status']
				r = answer['result']
				if s == 'WINNER':
					self.printResult(guess, r)
					print "Congratulations, you won."
					return 'ending',
				elif s == 'AGAIN':
					self.printResult(guess, r)
					print "You have {0} attempts left.".format(self.mm.attemptsLeft)
				elif s == 'DONE':
					print "It seems like you are all out of attempts. Better luck next time."
					self.reveal()
					return 'ending',
				elif s == 'LETTERS':
					print "You have given too many/not enough letters or an incorrect character. Please try again."
				elif s == 'OUT':
					print "Somehow you made it to this point in the program. There might be an error."
					self.reveal()
					return 'ending',
			elif action == 'n':
				self.printAttemptsLeft()
			elif action == 'l':
				self.printLastResult()
			elif action == 'h':
				self.printOptions()
			elif action == 'r':
				tries = 4
				while tries > 0:
					restart = raw_input("Are you sure you want to restart?(y/n)\n> ")
					if restart == 'y':
						return 'beginning',
					elif restart == 'n':
						break
					else:
						self.wut()
						print "Yes or no!?"
						tries -= 1
				print "You couldn't make a decision so I will help you out and say 'no'."
			elif action == 'q':
				tries = 4
				while tries > 0:
					quit = raw_input("Are you sure you want to quit?(y/n)\n> ")
					if quit == 'y':
						return 'exit',
					elif quit == 'n':
						break
					else:
						self.wut()
						print "Yes or no!?"
						tries -= 1
				print "You couldn't make a decision so I will help you out and say 'no'."
			elif action == 'cheat':
				self.reveal()
			else:
				self.wut()
				self.printOptions()
			print "\n--------"
	
	def ask(self):
		return raw_input("What would you like to do?\n> ")

	def printOptions(self):
		print "There are a few options. In order to use the options type the character and press enter."
		print "The options are"
		print "g\tguess the word"
		print "n\tlook up the number of attempts left"
		print "l\tlook at the results of the last guess"
		print "h\tprint this list of options"
		print "r\t restart the game with a new word"
		print "q\tquit the game"

	def printAttemptsLeft(self):
		print "You have {0} attempts left.".format(self.mm.attemptsLeft)
	
	def printResult(self, guess, result):
		print "You guessed"
		self.spaceLetters(guess)
		print "The result is"
		self.spaceLetters(result)
	
	def printLastResult(self):
		print "Your last result was"
		self.spaceLetters(self.mm.lastResult)
	
	def reveal(self):
		print "The answer to the game is"
		self.spaceLetters(self.mm.word)
		print "What do you think?"
	
	@staticmethod
	def spaceLetters(string):
		print
		for letter in string:
			print letter,
		print "\n"

class Ending(Phase):
	
	def start(self):
		tries = 4
		while tries > 0:
			action = raw_input("Would you like to play again.(y/n)\n> ")
			if action == 'y':
				return 'beginning',
			elif action == 'n':
				return 'exit',
			else:
				tries -= 1
				self.wut()
				print "Try again."
		if tries <= 0:
			print "I am going to exit for you."
			return 'exit',

class Exit(Phase):

	def start(self):
		print "Thank you for playing and have a nice day."
		sys.exit(0)

class Gameplay(object):
	
	phases = {
			'beginning': Beginning,
			'setup': Setup,
			'game': Game,
			'ending': Ending,
			'exit': Exit
			}

	def __init__(self):
		self.openingPhase = 'beginning'
	
	def nextPhase(self, phaseName, *args, **kwargs):
		return self.phases.get(phaseName)(*args, **kwargs)
	
	def startPlaying(self):
		return self.nextPhase(self.openingPhase)

class Engine(object):
	
	def __init__(self, gameplay):
		self.gameplay = gameplay
		print "Loaded the game"
	
	def play(self):
		currentPhase = self.gameplay.startPlaying()
		while True:
			print "\n--------------------"
			nextPhaseArgs = currentPhase.start()
			currentPhase = self.gameplay.nextPhase(*nextPhaseArgs)

def main():
	theGameplay = Gameplay()
	theGame = Engine(theGameplay)
	theGame.play()

if __name__ == "__main__":
	sys.exit(main())
