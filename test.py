import itertools, random

#errors
class Error(Exception):
   """Base class for other exceptions"""
   pass
class RankError(Error):
    """Raised when input rank is not a valid card rank"""
    pass
class SuitError(Error):
   """Raised when input rank is not a valid card suit"""
   pass
class NoCardsError(Error):
    """Raised when deck does not have enough cards to deal"""
    pass

values = [1,2,3,4,5,6,7,8,9,10,'J','Q','K']
suits = ["♠", "♥", "♦", "♣"]

class card:
    def __init__(self, value, suit):
        if value not in values:
            raise RankError("Invalid value!")
        if suit not in suits:
            raise SuitError("Invalid suit!")
        self.suit = suit
        self.value = value
    def __repr__(self):
            return f"{self.value}{self.suit}"
    def calc_score(self):
        if self.value in ['J','Q','K']:
            return 10
        elif int(self.value) <= 10:
            return self.value      

class deck:
    def __init__(self, quantity):
        self.cards = quantity * [card(value,suit) for (value,suit) in itertools.product(values,suits)]

    def shuffle(self):
        self.shuffled_cards = random.shuffle(self.cards)
        
    def draw(self):
        dealt_card = self.cards[0]
        self.cards.pop(0)
        return dealt_card

class player:
    def __init__(self, balance):
        self.balance = balance
        self.hand = []
        self.bust = False
        self.stand = False
        self.blackjack = False
        self.score = []
        self.bet = []
        self.insurance_bet = 0
    def update_score(self):
        total = 0
        soft = False
        for card in self.hand:
            card_score = card.calc_score()
            if card_score == 1:
                soft = True    
            total += card_score
            if soft and total + 10 <= 21:
                total += 10
        self.score = total
        return self.score
    def reset(self):
        self.hand = []
        self.bust = False
        self.stand = False
        self.blackjack = False
        self.score = []
        self.bet = []
        self.insurance_bet = 0

deck = deck(6)
deck.shuffle()

player1 = player(10000)

player1.hand.append(deck.draw())
player1.hand.append(deck.draw())

#split
for i in range(len(player1.hand)):
    player1.hand.append([player1.hand[0]])
    player1.hand.pop(0)

