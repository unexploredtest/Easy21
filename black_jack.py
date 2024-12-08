import random

from enum import Enum

SUIT_COUNT = 4
CARD_COUNT = 13


class CardSuit(Enum):
    HEART   = 1
    DIAMOND = 2
    SPADE   = 3
    CLUB    = 4


class CardNumber(Enum):
    TWO   = 1
    THREE = 2
    FOUR  = 3
    FIVE  = 4
    SIX   = 5
    SEVEN = 6
    EIGHT = 7
    NINE  = 8
    TEN   = 9
    JACK  = 10
    QUEEN = 11
    KING  = 12
    ACE   = 13

class Card:
    def __init__(self, suit, number):
        self.suit = suit
        self.number = number

    def __str__(self):
        card_suit = None
        card_number = None
        
        if(self.suit == CardSuit.HEART):
            card_suit = "heart"
        elif(self.suit == CardSuit.DIAMOND):
            card_suit = "diamond"
        elif(self.suit == CardSuit.SPADE):
            card_suit = "spade"
        elif(self.suit == CardSuit.CLUB):
            card_suit = "club"

        if(self.number == CardNumber.TWO):
            card_number = "2"
        elif(self.number == CardNumber.THREE):
            card_number = "3"
        elif(self.number == CardNumber.FOUR):
            card_number = "4"
        elif(self.number == CardNumber.FIVE):
            card_number = "5"
        elif(self.number == CardNumber.SIX):
            card_number = "6"
        elif(self.number == CardNumber.SEVEN):
            card_number = "7"
        elif(self.number == CardNumber.EIGHT):
            card_number = "8"
        elif(self.number == CardNumber.NINE):
            card_number = "9"
        elif(self.number == CardNumber.TEN):
            card_number = "10"
        elif(self.number == CardNumber.JACK):
            card_number = "jack"
        elif(self.number == CardNumber.QUEEN):
            card_number = "queen"
        elif(self.number == CardNumber.KING):
            card_number = "king"
        elif(self.number == CardNumber.ACE):
            card_number = "ace"

        return f"{card_number} {card_suit}"

    def __repr__(self):
        return self.__str__()

def get_all_cards():
    all_cards = []
    for i in range(1, SUIT_COUNT+1):
        suit = CardSuit(i)
        for j in range(1, CARD_COUNT+1):
            number = CardNumber(j)
            new_card = Card(suit, number)
            all_cards.append(new_card)

    return all_cards


def get_cards_sum(cards):
    has_ace = False
    cards_sum = 0
    for card in cards:
        if(card.number == CardNumber.JACK or card.number == CardNumber.QUEEN or card.number == CardNumber.KING):
            cards_sum += 10
        elif(card.number == CardNumber.ACE):
            cards_sum   += 1
            has_ace = True
        else:
            cards_sum += card.number.value + 1

    if(has_ace and cards_sum <= 11):
        cards_sum += 10

    return cards_sum

def has_activated_ace(cards):
    has_ace = False
    cards_sum = 0
    for card in cards:
        if(card.number == CardNumber.JACK or card.number == CardNumber.QUEEN or card.number == CardNumber.KING):
            cards_sum += 10
        elif(card.number == CardNumber.ACE):
            cards_sum   += 1
            has_ace = True
        else:
            cards_sum += card.number.value + 1

    if(has_ace and cards_sum <= 11):
        return True

    return False



# https://stackoverflow.com/questions/3791400/how-can-you-select-a-random-element-from-a-list-and-have-it-be-removed
# this will choose one and remove it
def choose_and_remove(items):
    # pick an item index
    if items:
        index = random.randrange( len(items) )
        return items.pop(index)
    # nothing left!
    return None



class BlackJack:
    def __init__(self):
        self.cards = None
        self.player_cards = None
        self.dealer_cards = None

        self.is_finished = False
        # self.result = None
        
        self.reset()

    # actions: "take", "stick"
    # Return results: "unfinished", "draw", "win", "def"
    # Note that the results are from the player's pov
    def step(self, action):
        if(action == "stick"):
            self.is_finished = True
            if(get_cards_sum(self.player_cards) < 11):
                return "def"
            
            while(get_cards_sum(self.dealer_cards) < get_cards_sum(self.player_cards)):
                self.dealer_cards.append(choose_and_remove(self.cards))

            if(get_cards_sum(self.dealer_cards) == get_cards_sum(self.player_cards)):
                return "draw"
            elif(self.is_dealer_cooked()):
                return "win"
            else:
                return "def"

        elif(action == "take"):
            self.player_cards.append(choose_and_remove(self.cards))
            if(self.is_player_cooked()):
                self.is_finished = True
                return "def"
            else:
                return "unfinished"

        

    def is_dealer_cooked(self):
        if(get_cards_sum(self.dealer_cards) > 21):
            return True
        else:
            return False

    def is_player_cooked(self):
        if(get_cards_sum(self.player_cards) > 21):
            return True
        else:
            return False

    def reset(self):
        self.cards = get_all_cards()
        self.player_cards = []
        self.dealer_cards = []

        self.is_finished = False

        for i in range(2):
            self.player_cards.append(choose_and_remove(self.cards))

        self.dealer_cards.append(choose_and_remove(self.cards))

    def get_player_sum(self):
        return get_cards_sum(self.player_cards)

    def player_has_ace(self):
        for card in self.player_cards:
            if(card.number == CardNumber.ACE):
                return True
        return False

    def player_has_activated_ace(self):
        return has_activated_ace(self.player_cards)

    def get_dealer_sum(self):
        return get_cards_sum(self.dealer_cards)

    def dealer_has_ace(self):
        for card in self.dealer_cards:
            if(card.number == CardNumber.ACE):
                return True
        return False

    def dealer_has_activated_ace(self):
        return has_activated_ace(self.dealer_cards)

    def get_state(self):
        player_sum = self.get_player_sum()
        player_has_ace = self.player_has_activated_ace()
        # player_has_ace = self.player_has_ace()
        
        dealer_sum = self.get_dealer_sum()
        # dealer_has_ace = self.dealer_has_activated_ace()
        # dealer_has_ace = black_jack.dealer_has_ace()

        return (player_sum, player_has_ace, dealer_sum)

    @staticmethod
    def make_state(player_sum, player_has_ace, dealer_sum):
        return (player_sum, player_has_ace, dealer_sum)

    # state: (player_sum, player_has_ace, dealer_sum, dealer_has_ace)
    # return: A binary represantion of the state:
    # XXXXX(player_sum)X(player_has_ace)XXXX(dealer_sum)X(action)
    # action: 1(take), 0(stick)
    # For now no ace
    @staticmethod
    def get_bin_rep(state, action):
        action_num = 1 if action == "take" else 0
        bin_rep = 0
        player_sum = state[0]
        player_has_ace = state[1]
        dealer_sum = state[2]

        bin_rep = (player_sum << 4+1+1) + (player_has_ace << 4+1) + (dealer_sum << 1) + action_num
        return bin_rep


def cli():
    game = BlackJack()
    print("Dealer's card: ", str(game.dealer_cards))
    
    last_result = None
    
    while(not game.is_finished):
        print("------------------")
        print("Your current cards: ", str(game.player_cards))
        action = input("Choose action(stick/take): ")
        last_result = game.step(action)

    print("------------------")
    print("Your current cards: ", str(game.player_cards))
    print("Dealer's cards: ", str(game.dealer_cards))
    print("Final result: " + last_result)


if __name__ == "__main__":
    cli()


