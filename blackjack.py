#Author: Dileesh Chandra Bikkasani
#11/01/16
import random
import os

clear_terminal = lambda : os.system('clear')

stringlist = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

bmap = { 'A' : 11,
         'K' : 10,
         'Q' : 10,
         "J" : 10,
         '10': 10,
         '9' : 9,
         '8' : 8,
         '7' : 7,
         '6' : 6,
         '5' : 5,
         '4' : 4,
         '3' : 3,
         '2' : 2
         }

class Account(object):

    def __init__(self, bank=100, cards=[]):
        self.bank = bank
        self.cards = cards

    def increase_bank(self, amount):
        self.bank += amount

    def decrease_bank(self, amount):
        self.bank -= amount


class Player(Account):
    def deal(self):
        self.cards = []
        self.cards.append(stringlist[random.randrange(0,13)])
        self.cards.append(stringlist[random.randrange(0,13)])
        if card_sum(self.cards) == 21:
            return 'Blackjack!'
        else:
            return self.cards

    def draw(self):
        self.cards.append(stringlist[random.randrange(0,13)])
        self.sum = card_sum(self.cards)
        if self.sum == 21:
            return 'Blackjack!'
        elif self.sum > 21:
            return 'Busted!'
        else:
            return self.cards

class Dealer(Account):

    def __init__(self, bank=100000, cards=[]):
        self.bank = bank
        self.cards_d = cards

    def deal(self):
        self.cards_d = []
        self.cards_d.append(stringlist[random.randrange(0,13)])
        self.cards_d.append(stringlist[random.randrange(0,13)])
        return self.cards_d

    def draw(self):
        self.cards_d.append(stringlist[random.randrange(0,13)])
        self.sum = card_sum(self.cards_d)
        if self.sum == 21:
            return 'Blackjack!'
        elif self.sum > 21:
            return 'Busted!'
        else:
            return self.cards_d

def card_sum(hand):
    total = 0
    for card in hand:
        total += bmap[card]
    return total

def play_again():
    print "\nYour bank roll is: {}".format(player.bank)
    decision = raw_input("Do you want to play again? (y/n): ")
    if decision.lower().startswith('y'):
        game()

def play_round(p_hand, d_hand, bet):
    clear_terminal()
    if 'Blackjack!' in p_hand:
        print p_hand
        player.increase_bank(bet*2)
        play_again()
    elif 'Busted!' in p_hand:
        print 'You busted.'
        play_again()
    else:
        print "Dealer: ['{}', '??']".format( d_hand[0] )
        print 'Sum: ', bmap[d_hand[0]]
        print '\n\nYou: ', p_hand
        print 'Sum: ', card_sum(p_hand)
        make_move(p_hand, d_hand, bet)

def stand(p, d, bet):
    if card_sum(p) > card_sum(d):
        d = dealer.draw()
        if 'Busted' in d: # dealer busted --> WIN
            print 'Dealer busted!'
            player.increase_bank(bet*2)
            play_again()
        elif 'Blackjack' in d: # dealer has blackjack
            print 'dealer has blackjack'
            play_again()
        elif card_sum(p) < card_sum(d) <= 21: # Dealer drew and has higher sum
            print 'Dealer hand: {} {}'.format(d, card_sum(d))
            print 'Dealer won.'
            play_again()
        elif card_sum(p) == card_sum(d): # both have equal hands --> PUSH
            print 'Dealer hand: {} {}'.format(d, card_sum(d))
            print 'Push'
            player.increase_bank(bet)
            play_again()
        else: # Dealer drew but is still lower --> WIN
            print 'Dealer hand: {} {}'.format(d, card_sum(d))
            print 'You won!'
            player.increase_bank(bet*2)
            play_again()
    elif card_sum(p) < card_sum(d) <= 21: # Dealer has higher hand without draw
        print 'Dealer hand: {} {}'.format(d, card_sum(d))
        print 'Dealer won.'
        play_again()
    elif card_sum(p) == card_sum(d): # both have equal hands --> PUSH
        print 'Dealer hand: {} {}'.format(d, card_sum(d))
        print 'Push'
        player.increase_bank(bet)
        play_again()

def draw(p, d, bet):
    p_hand = player.draw()
    d_hand = d
    play_round(p_hand, d_hand, bet)

def make_move(p, d, bet):
    if p[0] == p[1]:
        print '\n1) draw 2) stand \t3) split'
        choice = int(raw_input("Input number: "))
    elif d[0] == 'A' or d[1] == 'A':
        print '\n1) draw 2) stand \t4) insurance'
        choice = int(raw_input("Input number: "))
    else:
        print '\n1) draw 2) stand'
        choice = int(raw_input("Input number: "))

    if choice == 1:
        draw(p, d, bet)
    elif choice == 2:
        stand(p, d, bet)

def start_game(bet):
    global dealer
    dealer = Dealer()
    p_hand = player.deal()
    d_hand = dealer.deal()

    play_round(p_hand, d_hand, bet)

def game():
    clear_terminal()
    print 'Your current bankroll is: ', player.bank
    if player.bank > 0:
        print '\nMin bet: 10 | Max bet: 100\n'
        bet = int(raw_input('What is your bet?: '))

        player.decrease_bank(bet)
        print '\nYou have {} left in your bank. Good luck!'.format(player.bank)

        decision = raw_input("To start, type 'deal': ")
        if decision.lower().startswith('d'):
            start_game(bet)
    else:
        print 'Game over.'

def create_player(money):
    global player
    player = Player(money)

    game()

def start():
    print 'Welcome to this Blackjack Game!\n'
    while True:
        try:
            money = int(raw_input('What is your buy-in?: '))
        except:
            print 'Please enter an integer'
        else:
            create_player(money)
            break

start()