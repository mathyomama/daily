#!/usr/bin/env python
# -*- code: utf-8 -*-

import sys
import re

class Decompressor(object):

	def __init__(self, fileName):
		self.fileName = fileName
		self.decompressedText = self.solve()
	
	def solve(self):
		with open(self.fileName) as openedFile:
			numberPattern = re.compile(r'(?P<number>\d+)(?P<symbol>[!^])?')
			wordCount = int(openedFile.readline())
			wordsWithData = map(self.stripper, openedFile.readlines())
			decompressedList = []
			space, end = False, False
			for data in wordsWithData[wordCount:]:
				steps = data.split(' ')
				for chunk in steps:
					testMatch = numberPattern.match(chunk)
					if testMatch:
						if space:
							decompressedList.append(' ')
						else:
							space = True
						symbol = testMatch.group('symbol')
						if symbol == '^':
							decompressedList.append(wordsWithData[int(testMatch.group('number'))].capitalize())
						elif symbol == '!':
							decompressedList.append(wordsWithData[int(testMatch.group('number'))].upper())
						else:
							decompressedList.append(wordsWithData[int(testMatch.group('number'))])
					elif chunk in 'Rr':
						decompressedList.append('\n')
						space = False
					elif chunk in 'Ee':
						end = True
						break
					else:
						if chunk in '.,?!;:':
							decompressedList.append(chunk)
						elif chunk in '-':
							decompressedList.append(chunk)
							space = False
				if end:
					break

		return ''.join(decompressedList)

	@staticmethod
	def stripper(string):
		return string.strip('\n')

def main():
	daFile = sys.argv[1]
	decomp = Decompressor(daFile)
	print decomp.decompressedText
	with open("answer.txt", "w") as answer:
		answer.write(decomp.decompressedText)

if __name__ == "__main__":
	sys.exit(main())
