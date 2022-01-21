from collections import Counter
from nltk.corpus import words
import numpy as np
import random
import string
import itertools

WORDS = words.words()

LETDIST = {
    i: "".join(WORDS).count(i) / len("".join(WORDS)) for i in string.ascii_lowercase
}


class WordHunter:
    def __init__(self, letters=None, mode="hunt"):

        # if letters is none create 16 random
        self.letters = (
            letters
            if letters is not None
            else "".join(
                random.choices(
                    string.ascii_lowercase, weights=(i for i in LETDIST.values()), k=16
                )
            )
        )

        self.mode = mode

        # mode seperation
        if self.mode == "hunt":
            # random weighted letterMatrix for word finding

            self.letterMatrix = np.array(list(self.letters)).reshape((4, 4))

            print(self.letterMatrix)

            # for regex and anagram operations

            # needed to narrow down
            self.words = self.getWords()

        elif self.mode == "anagram":

            print(self.letters)

            # only uses isAnagram function to create list
            self.words = sorted(
                list(filter(lambda x: self.isAnagram(x) and len(x) > 2, WORDS)), key=len
            )

        print(self.words)

    # function to figure out if a word can be made from a list of chars given
    def isAnagram(self, word):

        # create counters for comparison
        letterMatrixCounter = Counter(self.letters)
        wordCounter = Counter(word)

        if False in [let in self.letters for let in wordCounter]:
            return False

        # format letterMatrixCounter in terms of wordCounter keys
        letterMatrixCounter = {i: letterMatrixCounter[i] for i in wordCounter}

        # generate list of values for comparison
        comparisonList = [
            letterMatrixCounter[key] - wordCounter[key] for key in wordCounter
        ]

        return True if min(comparisonList) > -1 else False

    def isTraversable(self, word):

        # create a list of all possible moves from one position to the next in a 4x4 matrix
        possibleMoves = list(itertools.product((-1, 0, 1), (-1, 0, 1)))
        # remove self as possible next location
        possibleMoves.remove((0, 0))
        possibleMoves = {
            (i, j): [
                (i + k[0], j + k[1])
                for k in possibleMoves
                if 4 > i + k[0] > -1 and 4 > j + k[1] > -1
            ]
            for i in range(4)
            for j in range(4)
        }

        # figure out where the start of the word is
        startRow, startCol = np.where(self.letterMatrix == word[0])
        startIndicies = [(startRow[i], startCol[i]) for i in range(len(startRow))]

        def depthFirst(curIndex, restOfWord, visited=set()):

            # state variable for setting after validation of base condition
            isWord = False

            # base case, if it has gotten to end of word succesfully
            if restOfWord == "":
                return True

            # setup
            visited.add(curIndex)
            target = restOfWord[0]

            # for each of the possible moves, if that move matches the target, recur
            for move in possibleMoves[curIndex]:

                if move in visited:
                    continue

                if self.letterMatrix[move[0]][move[1]] == target:

                    # if depth first returns a truth value, break the loop and return value of isWord
                    if depthFirst(move, restOfWord[1:], visited) is True:

                        isWord = True
                        break

            return isWord

        # different indicies will have different results so it is ran in a for loop
        for start in startIndicies:
          
            if depthFirst(start, word[1:]) is True:
                return True

        # return False if depth first never evalueates to true
        return False

    def getWords(self):

        # filter words based on truth value of anagram and if its length is greater than 2
        wordList = list(filter(lambda x: self.isAnagram(x) and len(x) > 2, WORDS))

        # up until this point, only been filtering to reduce weight of computation
        wordList = list(filter(self.isTraversable, wordList))

        # sort list by length
        wordList = sorted(wordList, key=len)

        return wordList


if __name__ == "__main__":
    letters = input(": ")
    wordHunter = WordHunter()
