"""Implementation of Semantic Information Retrieval AI.

This is a simple artificial intelligence that takes as inputs strings
of information. You can then ask it questions and it will try to answer them
based on context of previous knowledge.

Sample input/output:
? the cat has a collar
  I understand
? fluff is a cat
  I understand
? does fluff have a collar
  Not sure 
? every cat has a collar
  I understand
? does fluff have a collar
  Yes 
"""

__author__ = "jameswu"

import re, sys


class SIR(object):
	"""Semantic Information retrieval bot.

	For now, we'll just support a few basic types of information.
	Namely, logical statements like, "every __ has a ___" or
	"does ___ have a ___".

	Attributes:
	debug: bool, whether or not to print out results
	facts: list(str), a list of facts
	logic: constant dict, regex -> function, defining what to do in each regex match.
	"""
	# defines the logical types

	def __init__(self):
		self.debug = False
		self.facts = []
		self.logic = {
			# Factual statements. s=subset, S=superset 
			"(every|any|an|a) (.*) is (a|an) (.*)": (lambda g: self.AddFact(g, "1s3|3S1")) ,
			# m= member, M=membership in(the cat is an animal = that particular cat is an animal)
			"(.*) is (a|an) (.*)" : (lambda g: addFact(g,"0m2|2M0")),
			# e = equivalent to. (human is person, etc)
			"(.*) is (.*)" : (lambda g: addFact(g,"0e1|1e0")),
		}

	def AddFact(self, grp, logic):
		"""Adds a relationship between two things into the fact list.
		
		Args:
			grp: list(str), the grepped string after matching regex
			logic: str, the logic pattern behind it, "1s3|3S1"
		"""
		for pattern in logic.split("|"):
			# pattern is guaranteed to be a 3 char string
			assert len(pattern) == 3
			# e.g. "man, person"
			word1, word2 = grp[int(pattern[0])], grp[int(pattern[2])]
			# e.g. "s"(subset)
			relationship = pattern[1]
			fact = (word1, relationship, word2)
			if debug : print "Added relationship: ", fact
			facts.append(fact)

	def parseString(string):
		"""Parses a string of information."""
		# magic string parsing
		# substitutes any 2 spaces with one space, processes some string
		info = re.sub("  *"," ",string.strip().lower())

		for expr, action in self.logic:
			match = re.match(expr, info)
			if match:
				# if we found a match activate it
				action(match.groups())
				return

		print "I don't understand your sentence."



def main():
	siri = SIR()
	siri.debug = True
	while True:
		sent = raw_input(">>")
		siri.parseString(sent)




if __name__ == '__main__':
	main()
		