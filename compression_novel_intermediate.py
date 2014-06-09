#!/usr/bin/env python
# -*- code: utf-8 -*-

import sys
import re

class Compressor(object):

	def __init__(self, fileName):
		self.fileName = fileName
		self.textList = []
		self.dataList = []
		self.compressedFormat = self.compress()
	
	def compress(self):
		#wordPattern = re.compile(r'(?P<pred>\b|[-])(?P<word>[A-Za-z][a-z]*)(?P<symbol>[.,?!;:]\b|[-])')
		#chunkPattern = re.compile(r'^(?P<alpha>[A-Za-z][a-z]*)(?P<symbol>[.,?!;:]?)$')
		wordPattern = re.compile(r'^(\w+)$')
		splitter = re.compile(r'(\W+)')
		symbolPattern = re.compile(r'^([.,?!;:])( |\n)$|^(-)$')
		with open(self.fileName) as openedFile:
			text = openedFile.readlines()
			length = 0
			for line in text:
				wordList = splitter.split(line)
				for chunk in wordList:
					wordMatch = wordPattern.match(chunk)
					symbolMatch = symbolPattern.match(chunk)
					if wordMatch:
						alpha = wordMatch.group(0)
						dataChunk = []
						test = alpha.lower()
						if test in self.textList:
							dataChunk.append(str(self.textList.index(test)))
							dataChunk.append(self.capTest(alpha))
						else:
							self.textList.append(test)
							dataChunk.append(str(length))
							dataChunk.append(self.capTest(alpha))
							length += 1
						self.dataList.append(''.join(dataChunk))
					elif symbolMatch:
						symbol = symbolMatch.group(1)
						self.dataList.append(symbol)
					elif chunk == ' ' or chunk == '':
						pass
					else:
						raise TypeError("There is something wrong with the text, {}, and can not be compressed.".format(chunk))
				self.dataList.append('R')
			self.dataList.append('E')

		return '\n'.join((str(length), '\n'.join(self.textList), ' '.join(self.dataList)))
	
	@staticmethod
	def capTest(string):
		if isinstance(string, str):
			capPattern = re.compile(r'^((?P<head>[A-Z])|(?P<small>[a-z]))((?P<tail>[A-Z]*(?=[A-Z]*))|(?P<other>[a-z]*))$')
			daMatch = capPattern.match(string)
			if daMatch:
				if daMatch.group('head'):
					if daMatch.group('tail'):
						return '!'
					else:
						return '^'
				else:
					return ''
			else:
				raise ValueError("Not a suitable string.")
		else:
			raise TypeError("Wrong type, needs string")
	
	def writeTo(self, fileName):
		with open(fileName, 'w') as openedFile:
			openedFile.write(self.compressedFormat)

def main():
	comp = Compressor(sys.argv[1])
	print comp.compressedFormat
	comp.writeTo("answer.txt")

if __name__ == "__main__":
	sys.exit(main())
