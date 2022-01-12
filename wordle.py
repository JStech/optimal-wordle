#!/usr/bin/env python
import random

class Wordle:
    @staticmethod
    def eval_guess(guess, word):
        n = len(word)

        outcome = [0]*n
        used = [False]*n
        for i in range(n):
            if guess[i] == word[i]:
                outcome[i] = 2
                used[i] = True
        for i in range(n):
            for j in range(n):
                if guess[i] == word[j] and not used[j]:
                    outcome[i] = 1
                    used[j] = True

        return outcome

    def __init__(self, wordlist, n=5):
        self.n=n
        self.words=list(filter(lambda w: len(w)==self.n and w.isalpha(), (w.rstrip().upper() for w in wordlist)))
        print("Wordle started with {} {}-letter words".format(len(self.words), self.n))
        self.turn=0
        self.word=None

    def new_game(self):
        self.word=random.choice(self.words)
        self.turn=0

    def guess(self, guess):
        self.turn += 1

        if guess not in self.words:
            return "Invalid guess--not in wordlist. Lose your turn. Turn {}.".format(self.turn)

        outcome = self.eval_guess(guess, self.word)

        ret_string = ('  ' + ''.join(' .O'[o] for o in outcome) + ' turn {}'.format(self.turn))
        if outcome == [2]*self.n:
            ret_string += "\n    Congrats, you win!"
            self.new_game()
        return ret_string

    def interactive(self):
        self.new_game()
        while True:
            guess = input("? ").upper()
            if guess == 'I GIVE UP':
                print("The word was", self.word)
                break
            print(self.guess(guess))


if __name__ == "__main__":
    import sys
    with open(sys.argv[1]) as wordfile:
        words = [w for w in wordfile]
    wordle = Wordle(words)
    wordle.interactive()
