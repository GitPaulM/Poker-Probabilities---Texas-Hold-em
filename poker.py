

# https://www.cardplayer.com/poker-tools/odds-calculator/texas-holdem

from operator import itemgetter
import random
import time
from itertools import combinations 
from random import shuffle
import numpy as np

#  Card class contains the attributes of each card.
#  the methods are really just to display some of the card attributes

class Card(object):
    """ A standard playing card """
    def __init__(self, number, name,rank,suit):
        self.number = number
        self.name = name
        self.rank = rank
        self.suit = suit

    def faceup(self):
        """ Provides the full card info"""
        print("Card number: " + str(self.number) + " Card Rank: " + str(self.rank) + " " + self.name.title() + " of " + str(self.suit).title())

    def faceonly(self):
        """ Provides the partial card info"""
        print(self.name.title() + " of " + str(self.suit).title())

# Card_Set is a collection/list of playing cards (above)
# Card_Set has a few methods including shuffling, cutting, and various deck displays


class Card_Set(object):
    """ Generic group of playing cards Decks to a hand """
    
    def __init__(self):
        self.Cards = []
        
    def create_standard_deck(self):
        self.Cards = []
        SuitList = ['Diamonds','Clubs','Hearts','Spades']
        NameList = ['Two','Three','Four','Five',"Six",'Seven','Eight','Nine','Ten','Jack','Queen','King','Ace']
        a = 0
        for  Suits in SuitList:
            for Names in NameList:
                number = a + 1
                rank = (a % 13) + 2
                self.Cards.append(Card(number,Names,rank,Suits))
                a = a+1
                
    def shuffle_cards(self):
        """ shuffles cards """
        shuffle(self)

    def fan_cards(self,title):
        """ Show all the cards """
        print("\n"+title+"\n")
        for cardindeck in self.Cards:
            cardindeck.faceup()
        print("\nCard Total: " + str(len(self.Cards)))

    def show_cards(self):
        """ Show all the cards with partial info """
        for cardindeck in self.Cards:
            cardindeck.faceonly()
        print('\n')
           
    def cut_the_cards(self):
        """randomly cut the cards"""
        num = len(self.Cards)
        cutlocation = random.randint(0,num)
        self.Cards = self.Cards + self.Cards[0:cutlocation]
        del self.Cards[0:cutlocation]

 
    def display(self):
        """ Display all the cards, showing card number and card """
        halfdeck = len(self.Cards)//2
        for a in range(0,halfdeck):
            print(str(self.Cards[a].number).rjust(2),(self.Cards[a].name + " of " + 
                    self.Cards[a].suit).ljust(24),str(self.Cards[a+halfdeck].number).rjust(2),
                  (self.Cards[a+halfdeck].name + " of " + self.Cards[a+halfdeck].suit).ljust(24))
            if (a == 12):
                print('\n')
        print('\n')
        
    def get_card_indices(self):
        """ Capture card indicess """    
        a = [x.number-1  for x in self.Cards]
        return(a)
    
    def get_card_ranks(self):
        """ Capture rank indices """    
        a = [x.rank  for x in self.Cards]
        return(a)
    
    def get_card_suits(self):
        """ Capture suits """    
        a = [x.suit  for x in self.Cards]
        return(a)

#This is a group of cards that includes best hand and otherdetail about the hand

class BestHand(object):

    def __init__(self):
        self.cards= []
        self.description = 'Not Calculated'
        self.hand_rank = 0
        self.score = 0 # for hand comparison
        self.found = False
        self.note = ''
        

    def show(self):
        """ Show all the cards of the deck, but only partial info """
        print("Found Flag: ",self.found)
        print("Description: ",self.description)
        print("Best Hand: ",self.cards)
        print("Hand Rank: ",self.hand_rank)
        print("Hand Score: ",self.score)
        print("Note: ",self.note)
        print("\n")
        
def score(cards,hand_rank):
    """ The score routine calculates a hand score so hand strength can be compared """
    card_ranks = [(x-1)%13+2 for x in cards]
    if len(card_ranks) == 4:
        card_ranks = card_ranks+[1]
    multiplier = [14**4,14**3,14**2,14**1,14**0]
    hand_score = hand_rank*(14**5) + np.dot(card_ranks,multiplier)
    return(hand_score)


""" Each of the hand functions below was built as a stand alone in order to accomodate 
    unit testing.   The input for each is a 5 to 7 list containg integers from 1 to 52 (cards
    in a deck. The output is the best hand if found.  """
        
def straight_flush(cards):
    BestSf = BestHand()
    l = len(cards)
    rank_labels = ['Two','Three','Four','Five',"Six",'Seven','Eight','Nine','Ten','Jack','Queen','King','Ace']    
    Suits = ["Diamond","Club","Heart","Spade"]
    Suit = Suits[(cards[0]-1)//13]
    if l >= 7:
        if cards[2]-cards[6] == 4:
            BestSf.found = True
            BestSf.cards = cards[2:7]
    if l >= 6:
        if cards[1]-cards[5] == 4:
            BestSf.found = True
            BestSf.cards = cards[1:6]
    if cards[0]-cards[4] == 4:
            BestSf.found = True
            BestSf.cards = cards[0:5]
    if BestSf.found == True:
        if (BestSf.cards[0]%13==0):
            BestSf.description = Suit+" Royal Flush"
            BestSf.hand_rank = 10
        else:
            BestSf.description = (Suit + " Straight Flush: " + 
                                  rank_labels[(BestSf.cards[0]-1)%13] + " Thru " +
                                  rank_labels[(BestSf.cards[4]-1)%13])
            BestSf.hand_rank = 9
        BestSf.score = score(BestSf.cards,BestSf.hand_rank)
        return(BestSf)

#Ace low edge case
    if ((cards[0]%13 == 0) & (cards[-4]%13 == 4) & (cards[-4]-cards[-1] == 3)):
        cards = [cards[0]] + cards[-4:]  
        BestSf.found = True
        BestSf.description = Suit+" Ace-Low Straight Flush"
        BestSf.cards = cards
        BestSf.hand_rank = 9
        BestSf.score = score(BestSf.cards[-4:],BestSf.hand_rank)
        BestSf.note = "Ace-Low"
            
    return(BestSf)


def four_of_a_kind(cards):
    Best4k = BestHand()
    rank_labels =['Two','Three','Four','Five',"Six",'Seven','Eight','Nine','Ten','Jack','Queen','King','Ace']
    kind = 4
    card_ranks = [(x-1)%13+2 for x in cards]
    card_detail = [list(i) for i in zip(cards,card_ranks)]
    frequency = [card_ranks.count(x) for x in range(15)]
    max_freq = max(frequency)
    if max_freq != kind:
        return(Best4k)
    card_detail= [card_detail[x]+[frequency[card_detail[x][1]]] for x in (range(len(card_detail)))]
    card_detail = sorted(card_detail, key=lambda x: (x[2], x[1], x[0]), reverse=True)
    top = card_detail[0:kind]
    bottom = sorted(card_detail[kind:], key=lambda x: (x[1], x[0]), reverse=True)
    card_detail=top+bottom
    
    Best4k.found = True
    Best4k.cards = [card_detail[x][0] for x in range(5)]
    Best4k.description = ("4 of a kind: " + rank_labels[card_detail[0][1]-2]
                         +"s with " + rank_labels[card_detail[4][1]-2])
    Best4k.hand_rank = 8
    Best4k.score = score(Best4k.cards,Best4k.hand_rank)
    return(Best4k)



def full_house(cards):
    BestFh = BestHand()
    rank_labels = ['Two','Three','Four','Five',"Six",'Seven','Eight','Nine','Ten','Jack','Queen','King','Ace']
    idx = 0
    card_ranks = [(x-1)%13+2 for x in cards]
    card_detail = [list(i) for i in zip(cards,card_ranks)]
    card_detail = sorted(card_detail, key=itemgetter(1,0),reverse=True)
    frequency = [card_ranks.count(x) for x in range(15)]
    freqtest = [x for x in frequency if x>=2]
    if len(freqtest) == 0:
        return(BestFh)
    if ((max(freqtest) != 3) or (len(freqtest)<2)):
        return(BestFh)
    card_detail= [card_detail[x]+[frequency[card_detail[x][1]]] for x in (range(len(card_detail)))]
    card_detail=sorted(card_detail, key=itemgetter(2,1,0),reverse=True)
    BestFh.found = True 
    BestFh.cards = [card_detail[x][0] for x in range(5)]
    BestFh.description = ("Full House: " + rank_labels[card_detail[0][1]-2]
                         +"s over " + rank_labels[card_detail[3][1]-2]+"s")
    BestFh.hand_rank = 7
    BestFh.score = score(BestFh.cards,BestFh.hand_rank)
    if frequency.count(3) == 2:
        BestFh.note = "Two 3 of a kind" 
    return(BestFh)


def flush(cards):
    BestF = BestHand()
    BestTest= BestHand()
    cards.sort(reverse=True)
    flushfound = False
    rank_labels = ['Two','Three','Four','Five',"Six",'Seven','Eight','Nine','Ten','Jack','Queen','King','Ace']
    diamonds = [x for x in cards if x >= 1  and x <= 13]
    clubs    = [x for x in cards if x >= 14 and x <= 26]
    hearts   = [x for x in cards if x >= 27 and x <= 39]
    spades   = [x for x in cards if x >= 40 and x <= 52]
    
    if len(diamonds) >= 5:
        flushfound = True
        BestF.description = ("Diamond Flush : " + rank_labels[(diamonds[0]-1)%13] + ", " +
                         rank_labels[(diamonds[1]-1)%13] + ", " +
                         rank_labels[(diamonds[2]-1)%13] + ", " + 
                         rank_labels[(diamonds[3]-1)%13] + ", " + 
                         rank_labels[(diamonds[4]-1)%13])        
        
        BestF.cards = diamonds
        BestF.hand_rank = 6
        BestF.score = score(BestF.cards[0:5],BestF.hand_rank)
    elif len(clubs) >= 5:
        flushfound = True
        BestF.description = ("Club Flush : " + rank_labels[(clubs[0]-1)%13] + ", " +
                         rank_labels[(clubs[1]-1)%13] + ", " +
                         rank_labels[(clubs[2]-1)%13] + ", " + 
                         rank_labels[(clubs[3]-1)%13] + ", " +
                         rank_labels[(clubs[4]-1)%13])                    
        BestF.cards = clubs
        BestF.hand_rank = 6
        BestF.score = score(BestF.cards[0:5],BestF.hand_rank)
    elif len(hearts) >= 5:
        flushfound = True
        BestF.description = ("Heart Flush : " + rank_labels[(hearts[0]-1)%13] + ", " +
                         rank_labels[(hearts[1]-1)%13] + ", " +
                         rank_labels[(hearts[2]-1)%13] + ", " + 
                         rank_labels[(hearts[3]-1)%13] + ", " + 
                         rank_labels[(hearts[4]-1)%13])    
        BestF.cards = hearts
        BestF.hand_rank = 6
        BestF.score = score(BestF.cards[0:5],BestF.hand_rank)
    elif len(spades) >= 5:  
        flushfound = True
        BestF.description = ("Spade Flush : " + rank_labels[(spades[0]-1)%13] + ", " +
                         rank_labels[(spades[1]-1)%13] + ", " +
                         rank_labels[(spades[2]-1)%13] + ", " + 
                         rank_labels[(spades[3]-1)%13] + ", " + 
                         rank_labels[(spades[4]-1)%13])    
        BestF.cards = spades
        BestF.hand_rank = 6
        BestF.score = score(BestF.cards[0:5],BestF.hand_rank)
    if flushfound == True:
        BestTest = straight_flush(BestF.cards)
        if BestTest.found:
            return(BestTest)
        BestF.cards = BestF.cards[0:5]
        BestF.found = flushfound
    return(BestF) 


def straight(cards):
    BestSt = BestHand()
    rank_labels = ['Two','Three','Four','Five',"Six",'Seven','Eight','Nine','Ten','Jack','Queen','King','Ace']
    idx = 0
    card_ranks = [(x-1)%13+2 for x in cards]
    card_detail = [list(i) for i in zip(cards,card_ranks)]
    card_detail=sorted(card_detail, key=itemgetter(1,0),reverse=True)    
    card_detail = [newcard for idx, newcard in enumerate(card_detail) 
               if newcard[1] not in [x[1] for x in card_detail[:idx]]]
    if len(card_detail) < 5:
        return(BestSt)
    l = len(card_detail)
    if l == 7:
        if card_detail[2][1]-card_detail[6][1] == 4:
            BestSt.found = True 
            BestSt.cards = [card_detail[x][0] for x in range(2,7)]
            BestSt.description = ("Straight: "+rank_labels[card_detail[2][1]-2]
                +" thru " + rank_labels[card_detail[6][1]-2])
            BestSt.hand_rank = 5
            BestSt.score = score(BestSt.cards,BestSt.hand_rank)
    if l >= 6:
        if card_detail[1][1]-card_detail[5][1] == 4:
            BestSt.found = True   
            BestSt.cards = [card_detail[x][0] for x in range(1,6)]
            BestSt.description = ("Straight: "+rank_labels[card_detail[1][1]-2]
                +" thru " + rank_labels[card_detail[5][1]-2])
            BestSt.hand_rank = 5
            BestSt.score = score(BestSt.cards,BestSt.hand_rank)        
    if card_detail[0][1]-card_detail[4][1] == 4:
            BestSt.found = True  
            BestSt.cards = [card_detail[x][0] for x in range(0,5)]
            BestSt.description = ("Straight: "+rank_labels[card_detail[0][1]-2]
                +" thru " + rank_labels[card_detail[4][1]-2])
            BestSt.hand_rank = 5
            BestSt.score = score(BestSt.cards,BestSt.hand_rank)         
    if BestSt.found == True:
        return(BestSt)

#Ace low edge case

    if ((card_detail[0][1] == 14) & (card_detail[-4][1] == 5) & (card_detail[-4][1]-card_detail[-1][1] == 3)):
        BestSt.found = True 
        BestSt.cards = [card_detail[0][0]] + [card_detail[x][0] for x in range(len(card_detail)-4,len(card_detail))]
        BestSt.description = ("Straight: "+rank_labels[card_detail[0][1]-2]
                            +" thru " + rank_labels[card_detail[-4][1]-2])
        BestSt.hand_rank = 5
        BestSt.score = score(BestSt.cards[-4:],BestSt.hand_rank)

        BestSt.note = "Ace-Low"
    return(BestSt)


def three_of_a_kind(cards):

    Best3k = BestHand()
    rank_labels = ['Two','Three','Four','Five',"Six",'Seven','Eight','Nine','Ten','Jack','Queen','King','Ace']
    kind = 3
    card_ranks = [(x-1)%13+2 for x in cards]
    card_detail = [list(i) for i in zip(cards,card_ranks)]
    frequency = [card_ranks.count(x) for x in range(15)]
    max_freq = max(frequency)
    if max_freq != kind:
        return(Best3k)
    card_detail= [card_detail[x]+[frequency[card_detail[x][1]]] for x in (range(len(card_detail)))]
    card_detail = sorted(card_detail, key=lambda x: (x[2], x[1], x[0]), reverse=True)
    top = card_detail[0:kind]
    bottom = sorted(card_detail[kind:], key=lambda x: (x[1], x[0]), reverse=True)
    card_detail=top+bottom
    
    Best3k.found = True
    Best3k.cards = [card_detail[x][0] for x in range(5)]
    Best3k.description = ("3 of a kind: " + rank_labels[card_detail[0][1]-2]
                          +"s with " + rank_labels[card_detail[3][1]-2]
                          +" and "+ rank_labels[card_detail[4][1]-2]) 
    Best3k.hand_rank = 4
    Best3k.score = score(Best3k.cards,Best3k.hand_rank)
    return(Best3k)



def two_pairs(cards):
    Best2p = BestHand()
    rank_labels = ['Two','Three','Four','Five',"Six",'Seven','Eight','Nine','Ten','Jack','Queen','King','Ace']
    kind = 2*2
    card_ranks = [(x-1)%13+2 for x in cards]
    card_detail = [list(i) for i in zip(cards,card_ranks)]
    frequency = [card_ranks.count(x) for x in range(15)]
    freqtest = [x for x in frequency if x>1]
    if len(freqtest) == 0:
        return(Best2p)
    if ((max(freqtest) != 2) or (len(freqtest)<2)):
        return(Best2p)
    card_detail= [card_detail[x]+[frequency[card_detail[x][1]]] for x in (range(len(card_detail)))]
    card_detail = sorted(card_detail, key=lambda x: (x[2], x[1], x[0]), reverse=True)
    top = card_detail[0:kind]
    bottom = sorted(card_detail[kind:], key=lambda x: (x[1], x[0]), reverse=True)
    card_detail=top+bottom
    
    Best2p.found = True 
    Best2p.cards = [card_detail[x][0] for x in range(5)]
    Best2p.description = ("2 Pair: " + rank_labels[card_detail[0][1]-2]
                         +"s over " + rank_labels[card_detail[2][1]-2] +"s with a "+
                         rank_labels[card_detail[4][1]-2])
    Best2p.hand_rank = 3
    Best2p.score = score(Best2p.cards,Best2p.hand_rank)
    if frequency.count(2) == 3:
        Best2p.note = "Three pair" 
    return(Best2p)



def one_pair(cards):
    Best1p = BestHand()
    rank_labels = ['Two','Three','Four','Five',"Six",'Seven','Eight','Nine','Ten','Jack','Queen','King','Ace']
    kind = 2
    card_ranks = [(x-1)%13+2 for x in cards]
    card_detail = [list(i) for i in zip(cards,card_ranks)]
    frequency = [card_ranks.count(x) for x in range(15)]
    max_freq = max(frequency)
    if max_freq != 2:
        return(Best1p)
    card_detail= [card_detail[x]+[frequency[card_detail[x][1]]] for x in (range(len(card_detail)))]
    card_detail = sorted(card_detail, key=lambda x: (x[2], x[1], x[0]), reverse=True)
    top = card_detail[0:kind]
    bottom = sorted(card_detail[kind:], key=lambda x: (x[1], x[0]), reverse=True)
    card_detail=top+bottom

    Best1p.found = True 
    Best1p.cards = [card_detail[x][0] for x in range(5)]
    Best1p.description = ("1 pair: " + rank_labels[card_detail[1][1]-2]
                          +"s with " + rank_labels[card_detail[2][1]-2]
                          +" and "+ rank_labels[card_detail[3][1]-2]
                          +" and "+ rank_labels[card_detail[4][1]-2])       
    Best1p.hand_rank = 2
    Best1p.score = score(Best1p.cards,Best1p.hand_rank)
    return(Best1p)


def no_pair(cards):
    BestNp = BestHand()
    kind = 0
    remaining = []
    rank_labels = ['Two','Three','Four','Five',"Six",'Seven','Eight','Nine','Ten','Jack','Queen','King','Ace']
    remaining_not_found = True
    idx = 0
    card_ranks = [(x-1)%13+2 for x in cards]
    card_detail = [list(i) for i in zip(cards,card_ranks)]
    if len(card_detail) < 5:
        return(BestNp)
    card_detail = sorted(card_detail[kind:], key=lambda x: (x[1], x[0]), reverse=True)
    BestNp.found = True 
    BestNp.cards = [card_detail[x][0] for x in range(5)]
    BestNp.description = ("No Pair: " + rank_labels[card_detail[0][1]-2] + ", " +
                         rank_labels[card_detail[1][1]-2] + ", " +
                         rank_labels[card_detail[2][1]-2] + ", " + 
                         rank_labels[card_detail[3][1]-2] + ", " + 
                         rank_labels[card_detail[4][1]-2])
     
    BestNp.hand_rank = 1
    BestNp.score = score(BestNp.cards,BestNp.hand_rank)
    return(BestNp)

""" This is the routine that waterfalls through the different hand type in search of the best hand category"""

def hand_ranking(cards):
    Best = BestHand()
    Best = flush(cards)
    if Best.found == False: 
        Best = four_of_a_kind(cards)
    if Best.found == False: 
        Best = full_house(cards)
    if Best.found == False: 
        Best = straight(cards)
    if Best.found == False: 
        Best = three_of_a_kind(cards)
    if Best.found == False: 
        Best = two_pairs(cards)
    if Best.found == False: 
        Best = one_pair(cards)
    if Best.found == False: 
        Best = no_pair(cards)
    return(Best)

