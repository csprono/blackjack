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
    def __init__(self, deck, balance):
        self.balance = balance
        self.hand = []
        self.bust = False
        self.stand = False
        self.blackjack = False
        self.score = 0
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
    def reset(self):
        self.hand = []
        self.bust = False
        self.stand = False
        self.blackjack = False
        self.score = 0

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

#init deck
deck = deck(6)
deck.shuffle()

#init players
player1 = player(deck, 10000)
dealer = player(deck, 0)

# #player bet
# print("Players balance:", player1.balance)
# bet = bet(player1)

#deal cards
while len(dealer.hand) != 2:
    player1.hand.append(deck.draw())
    dealer.hand.append(deck.draw())
dealer_up = dealer.hand[1]
dealer_down = dealer.hand[0]
print(dealer_up.value)

#blackjack check (face value 10 or 1)
if dealer_up.value == 1 or dealer_up == 10:
    #insurance check
    if dealer_up == 1:
        #offer insurance (2 to 1 side bet)
        insurance_check = input("Do you want insurance? (y/n)")
        if insurance_check == 'y':
            insurance_bet = insurance(player1)
    dealer.blackjack = (dealer.update_score == 21)
    if insurance and dealer.blackjack:
        player1.balance += (insurance_bet * 2)

#player blackjack check

#player turn loop
while player1.stand == False and player1.blackjack == False:
    print("Dealers's hand:", dealer.hand[0])
    print("Player's hand:", player1.hand)
    move = input("Hit, Stand, Double or Split: ")
    #stand
    if move == 's':
        player1.stand = True
    #hit
    elif move == 'h':
        player1.hand.append(deck.draw())
        player1.score = player1.update_score()
    #double
    #elif move == 'd': 
    #split
    #elif move == 'sp':
    
    #check if bust
    if player1.score > 21:
        player1.bust = True
        print("BUST")
        player1.stand = True
    elif len(player1.hand) == 5 and player1.bust == False:
        player1.stand = True

#dealer turn cycle
while dealer.stand == False and dealer.blackjack == False:
    if dealer.score <= player1.score or player1.bust == False:
        if dealer.score < 17:
            dealer.hand.append(deck.draw())
            dealer.score = dealer.update_score()
        else:
            stand = True
    elif dealer.score > 21:
        dealer.bust = True
        stand = True
    else:
        stand = True


#reset players
dealer.reset()
player1.reset()