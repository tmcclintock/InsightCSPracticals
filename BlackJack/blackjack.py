import numpy.random as npr
import numpy as np

class blackjackgame(object):
    def __init__(self):
        cards = np.zeros(52, dtype=int)
        for i in range(52):
            cards[i] = i//4 + 1
        self.cards = cards
        self.phand = []
        self.dhand = []
        self.ingame = False
        self.cmap = {1:"A", 11:"J", 12:"Q", 13:"K"}
        print("call my play_game() function to play BlackJack")

    def deal_card(self):
        if not self.ingame:
            print("You haven't started a game yet.")
            return
        i = npr.randint(0, len(self.cards))
        c = self.cards[i]
        self.cards = np.delete(self.cards, i)
        return c

    def _cards_to_str(self, cards):
        out = ""
        for c in cards:
            if c in self.cmap:
                out += self.cmap[c] + ", "
            else:
                out += str(c) + ", "
        return out[:-2]

    def _card_sum(self, cards):
        t = 0
        for c in cards:
            t += min(c, 10)
        return t
        
    def play_game(self):
        if self.ingame == True:
            print("You are already playing a game.")
        self.ingame = True

        #Deal all cards
        self.phand.append(self.deal_card())
        self.dhand.append(self.deal_card())
        self.phand.append(self.deal_card())
        self.dhand.append(self.deal_card())

        print(f"You show {self._card_sum(self.phand)}")
        print("With cards: " + self._cards_to_str(self.phand))

        #Check for ace cases
        if 1 in self.phand: #has an ace
            if self._card_sum(self.phand) == 11:
                print("You win with a natural!")
                self.reset()
                return
        
        print(f"Dealer shows {self._card_sum(self.dhand[1:])}")
        print("With cards: " + self._cards_to_str(self.dhand[1:]))
        print("and one card hidden")

        #Check for ace cases
        if 1 in self.dhand: #has an ace
            if self._card_sum(self.dhand) == 11:
                print("Dealer wins with a natural!")
                self.reset()
                return

        print("Call hit() or stay()")
        return

    def hit(self):
        if not self.ingame:
            print("You haven't started a game yet.")
            return

        self.phand.append(self.deal_card())
        print(f"You show {self._card_sum(self.phand)}")
        print("With cards: " + self._cards_to_str(self.phand))

        if self._card_sum(self.phand) > 21:
            print("Busted!")
            self.reset()
            return
        elif self._card_sum(self.phand) == 21:
            print("You win!")
            self.reset()
            return

        #Check for ace cases
        if 1 in self.phand: #has an ace
            if self._card_sum(self.phand) == 11:
                print("You win with the ace!")
                self.reset()
            elif self.phand == [1,1,1]:
                print("You win with three aces!")
                self.reset()

        print("Call hit() or stay()")
        return

    def stay(self):
        if not self.ingame:
            print("You haven't started a game yet.")
            return

        print("Dealer flips the hidden card")
        print(f"Dealer shows {self._card_sum(self.dhand)}")
        print("With cards: " + self._cards_to_str(self.dhand))

        while self._card_sum(self.dhand) < 17:
            print("Dealer hits")
            self.dhand.append(self.deal_card())

            if self._card_sum(self.dhand) > 21:
                print(f"Dealer busts with {self._card_sum(self.dhand)}! Congrats!")
                self.reset()
                return
            
            print(f"Dealer shows {self._card_sum(self.dhand)}")
            print("With cards: " + self._cards_to_str(self.dhand))

            #Check for ace cases
            if 1 in self.dhand: #has an ace
                if self._card_sum(self.dhand) == 11:
                    print("Dealer wins with the ace!")
                    self.reset()
                elif self.dhand == [1,1,1]:
                    print("Dealer wins with three aces!")
                    self.reset()

        if self._card_sum(self.dhand) < self._card_sum(self.phand):
            print("You win! Congrats!")
        elif self._card_sum(self.dhand) == self._card_sum(self.phand):
            print("You tie.")
        else:
            print("Dealer wins. Better luck next time!")
        self.reset()
        return

    def reset(self):
        self.phand = []
        self.dhand = []
        cards = np.zeros(52, dtype=int)
        for i in range(52):
            cards[i] = i//4 + 1
        self.cards = cards
        self.ingame = False
        return
