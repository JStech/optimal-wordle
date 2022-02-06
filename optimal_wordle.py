#!/usr/bin/env python
import wordle
from collections import defaultdict
from math import log
from multiprocessing import Pool

def guess_distribution(solution_words, guess):
    distribution = defaultdict(int)
    for solution in solution_words:
        distribution[tuple(wordle.Wordle.eval_guess(guess, solution))] += 1
    return distribution

def entropy(distribution):
    n = sum(distribution.values())
    entropy = 0.
    for outcome in distribution:
        p = distribution[outcome]/n
        entropy += -p * log(p)
    return entropy

class EntropyFunction:
    def __init__(self, solution_word_list):
        self.solution_word_list = solution_word_list
        self.solution_word_list = list(filter(lambda w: w.isalpha(), (w.rstrip().upper() for w in solution_word_list)))

    def __call__(self, guess):
        return entropy(guess_distribution(self.solution_word_list, guess))

if __name__ == "__main__":
    import sys
    with open(sys.argv[1]) as wordfile:
        words = [w for w in wordfile]
    if len(sys.argv) > 2:
        with open(sys.argv[2]) as wordfile:
            solution_words = [w for w in wordfile]
    else:
        solution_words = words

    for n in range(2, 6):
        w = wordle.Wordle(words, n)
        if len(w.words) == 0: continue

        with Pool(4) as p:
            entropies = p.map(EntropyFunction(solution_words), w.words)

        word_entropy = dict()
        with open('entropy_wordle_solutions_{}.txt'.format(n), 'w') as out_file:
            for word, H in zip(w.words, entropies):
                word_entropy[word] = H
                print(word, H, file=out_file)

        print('Best first guess: ', max(word_entropy, key=word_entropy.get))
        print('Worst first guess:', min(word_entropy, key=word_entropy.get))
