#!/usr/bin/env python
import random

class Wordle:
    def __init__(self, wordlist, n=5):
        self.words=list(filter(lambda w: len(w)==5 and w.isalpha(), (w.rstrip().upper() for w in wordlist)))
        self.n=5
        self.turn=0
        self.word=None

    def new_game(self):
        self.word=random.choice(self.words)
        self.turn=0


    def guess(self, guess):
        self.turn += 1

        if guess not in self.words:
            return "Invalid guess--not in wordlist. Lose your turn. Turn {}.".format(self.turn)

        outcome = [0]*self.n
        for i in range(self.n):
            if guess[i] == self.word[i]:
                outcome[i] = 2
            elif guess[i] in self.word:
                outcome[i] = 1

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
                exit()
            print(self.guess(guess))


if __name__ == "__main__":
    import sys
    with open(sys.argv[1]) as wordfile:
        words = [w for w in wordfile]
    wordle = Wordle(words)
    wordle.interactive()
