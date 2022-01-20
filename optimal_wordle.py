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

def entropy(distribution):
    n = sum(distribution.values())
    entropy = 0.
    for outcome in distribution:
        p = distribution[outcome]/n
        entropy += -p * log(p)
    return entropy

class EntropyFunction:
    def __init__(self, wordlist):
        self.wordlist = wordlist

    def __call__(self, guess):
        return entropy(guess_distribution(self.wordlist, guess))

if __name__ == "__main__":
    import sys
    print("opening words")
    with open(sys.argv[1]) as wordfile:
        words = [w for w in wordfile]
    print("created wordlist")
    for n in range(2, 6):
        w = wordle.Wordle(words, n)
        if len(w.words) == 0: continue

        with Pool(4) as p:
            entropies = p.map(EntropyFunction(w.words), w.words)

        word_entropy = dict()
        with open('entropy_{}.txt'.format(n), 'w') as out_file:
            for word, H in zip(w.words, entropies):
                word_entropy[word] = H
                print(word, H, file=out_file)

        print('Best first guess: ', max(word_entropy, key=word_entropy.get))
        print('Worst first guess:', min(word_entropy, key=word_entropy.get))
