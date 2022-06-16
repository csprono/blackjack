import itertools, random

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
    def __init__(self, deck, balance):
        self.balance = balance
        self.hand = []
        self.bust = False
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
        return total

def bet(player1):
    min_bet = 500
    bet = 0
    bet_check = False
    while bet_check == False:
        try:
            bet = int(input("Place your bet: "))
        except:
            print("ERROR: Input invalid")
            continue
        if bet >= min_bet: 
            if player1.balance >= bet:
                player1.balance -= bet
                bet_check = True
            else:
                print("ERROR: Not enough balance")
        else:
            print(f"ERROR: Min bet is {min_bet}")
    return bet

def insurance(player1):
    insurance_bet = 0
    insurance_check = True
    while insurance_check == False:
        try:
            insurance_bet = int(input("Place your insurance bet: "))
        except:
            print("ERROR: Input invalid")
            continue
        if player1.balance >= bet:
            player1.balance -= bet
            insurance_check = True
        else:
            print("ERROR: Not enough balance")
    return insurance_bet

deck = deck(6)
deck.shuffle()

player1 = player(deck, 10000)
dealer = player(deck, 0)

print("Players balance:", player1.balance)
bet = bet(player1)

while len(dealer.hand) != 2:
    player1.hand.append(deck.draw())
    dealer.hand.append(deck.draw())

player1_score = player1.update_score()
dealer_score = dealer.update_score()
dealer_up = dealer.hand[1]

if dealer_up == 10 or dealer_up == 1:
    if dealer_up == 1:
        insurance_check = input("Do you want to make an insurance bet (y/n): ")
        if insurance_check == 'y':
            insurance_bet = insurance(player1)
            if dealer.hand[0] in [10, 'J', 'Q', 'K']:
                dealer.balance += insurance_bet * 2


stand = False
while stand == False:
    print("Dealers's hand:", dealer.hand[0])
    print("Player's hand:", player1.hand)
    move = input("Hit or Stand: ")
    if move == 's':
        stand = True
    elif move == 'h':
        player1.hand.append(deck.draw())
        player1_score = player1.update_score()
    #elif move == 'd': 

    if player1_score > 21:
        player1.bust = True
        print("BUST")
        stand = True
    elif len(player1.hand) == 5 and player1.bust == False:
        stand = True

stand = False
while stand == False:
    if dealer_score <= player1_score or player1.bust == False:
        if dealer_score < 17:
            dealer.hand.append(deck.draw())
            dealer_score = dealer.update_score()
        else:
            stand = True
    elif dealer_score > 21:
        dealer.bust = True
        stand = True
    else:
        stand = True

print("Dealers's hand:", dealer.hand)
print('d score', dealer_score)
print("Player's hand:", player1.hand)
print('p score', player1_score)

if player1.bust == True:
    print("LOSE")
elif dealer.bust == True:
    print("WIN")
else:
    if len(player1.hand) == 5 and player1.bust == False:
        print("WIN")
        player1.balance += (bet * (3/2))
    elif player1_score < dealer_score:
        print("LOSE")
    elif player1_score > dealer_score or dealer.bust:
        print("WIN")
        player1.balance += (bet * (3/2))
    elif player1_score == dealer_score:
        print("PUSH")
        player1.balance += bet    

player1.bust = False
player1.hand = []
dealer.bust = False
dealer.hand = []
bet = 0
print("Balance:", player1.balance)