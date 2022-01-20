#!/usr/bin/env python
import wordle
from collections import defaultdict
from math import log
from multiprocessing import Pool

def guess_distribution(words, guess):
    distribution = defaultdict(int)
    for word in words:
        distribution[tuple(wordle.Wordle.eval_guess(guess, word))] += 1
    return distribution

class ValueFunction:
    def __init__(self, wordlist):
        self.wordlist = wordlist

    def __call__(self, guess):
        value = 0
        for word in self.wordlist:
            value += sum(s**2 for s in wordle.Wordle.eval_guess(guess, word))
        return (guess, value)

if __name__ == "__main__":
    import sys
    print("opening words")
    with open(sys.argv[1]) as wordfile:
        words = [w for w in wordfile]
    print("created wordlist")
    for n in range(2, 6):
        w = wordle.Wordle(words, n)

        with Pool(4) as p:
            values = p.map(ValueFunction(w.words), w.words)

        with open('values_4_1_{}.txt'.format(n), 'w') as out_file:
            for word, value in values:
                print(word, value, file=out_file)

        print('Best first guess: ', max(values, key=lambda x: x[1]))
        print('Worst first guess:', min(values, key=lambda x: x[1]))
