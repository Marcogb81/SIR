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
    facts: list(tuple(int, str, int)), a list of facts, listed as (thing1, relationship, thing2)
    logic: constant dict, regex -> function, defining what to do in each regex match.
    """
    # defines the logical types

    def __init__(self):
        self.debug = False
        self.facts = []
        # We use a tuple of pairs because order matters
        self.logic = (
             ( "(every|any|an|a) (.*) is (a|an) (.*)",   lambda g: self.AddFact(g,"1s3|3S1")),
             ( "(.*) is (a|an) (.*)",                    lambda g: self.AddFact(g,"0m2|2M0")),
             ( "(.*) is (.*)",                           lambda g: self.AddFact(g,"0e1|1e0")),
             
             ( "(every|any|an|a) (.*) owns (a|an) (.*)", lambda g: self.AddFact(g,"1p3|3P1")),
             ( "(.*) owns (a|an) (.*)",                  lambda g: self.AddFact(g,"0p2|2P0")),
             ( "(.*) owns (.*)",                         lambda g: self.AddFact(g,"0p1|1P0")),
             
             ( "is (every|an|a) (.*) (a|an) (.*)",       lambda g: self.GetPath(g,"1e*s*e*3")),
             ( "is (.*) (a|an) (.*)",                    lambda g: self.GetPath(g,"0e*ms*e*2")),

             ( "does (every|an|a) (.*) own (a|an) (.*)", lambda g: self.GetPath(g,"1e*ms*ps*e*3")),
             ( "does any (.*) own (a|an) (.*)",          lambda g: self.GetPath(g,"0S*Me*ps*e*2")),
             ( "does (.*) own (a|an) (.*)",              lambda g: self.GetPath(g,"0e*ms*ps*e*2")),
             ( "quit",                                   lambda g: sys.exit()          ),
        )

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
            if self.debug : print "Added relationship: ", fact
            self.facts.append(fact)

    def parseString(self, string):
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

    def GetPath(self, grp, rule):
        """Searches for a link between two ideas, say 'dog' and 'animal'."""
        # Gets the relationship query
        pattern = rule[1:-1]
        start = grp[int(rule[0])]
        stop = grp[int(rule[-1])]
        ans = []
        p = self._path(pattern, start, stop, ans=ans)
        if self.debug: 
            detail = "%s %s" % (pattern,ans)
        else:
            detail = ""
        if ans: 
            print "  Yes ", detail
        else: 
            print "  Not sure ", detail

    def _path(self, pat, start, end, before=set(), ans=[], sofar="", indent=" "):
        """Helper static method that gets a pattern and runs a DFS to find it.

        Args:
            pat: str, the pattern we're searching for
            start: str, starting word
            end: str, ending word
            before: dict, list of visited nodes
            ans: list(str), the list of relationships to reach the target

        Puts the resulting answer in ans, a list
        """
        # gets already visited nodes
        visited = set()
        visited = visited | before

        # debugging info is tracked in indent
        if self.debug : print indent,"path - ",start," to ",end
        # loop through dem facts
        for fact in self.facts:
            # Checks hash table for visited
            # Checks whether the fact has anything to do with a
            (a, relationship, b) = fact

            if fact in visited or a != start:
                continue
            # checks that the relationship is a valid one
            # for what we're asking   
            matches = self.matchesSoFar(pat, sofar+relationship)
            if matches > 0:
                visited.add((a, relationship, b))
                #if we find the end
                if b == end and matches == 2:
                    ans.append(sofar+relationship)

                else:
                    # keep searching from new point
                    self._path(pat, b, end, visited, ans, sofar+relationship, indent+"  ")

    def matchesSoFar(self, pattern, b):
        """
        Checks that b matches at least some substring of pattern
        Returns 
            0 for no match
            1 for partial match(matches some substring) 
            2 for complete match(matches entire string).

        This checks that things like "A dog is a man is a dog" won't happen.
        """
        ans = 2
        while pattern:
            if re.match("^%s$"%pattern, b) : return ans
            if pattern[-1] == '*': 
                pattern = pattern[:-2]
            else: 
                pattern = pattern[:-1]
            ans = 1
        return 0




def main():
    siri = SIR()
    siri.debug = True
    while True:
        sent = raw_input(">>")
        siri.parseString(sent)




if __name__ == '__main__':
    main()
        