# This is a python program that was created as more of a project
# Very basically it was to determine the win / lose / tie percentages
# for two heads up texas hold-em players.
# It is extremely slow but was not really meant for public consumption
# Just dabbling in python and needed a project

import operator
import random
from random import shuffle

# Deck is a collection of playing card classes.
# Deck has a few methods including shuffling, cutting, and various deck displays

class Deck(object):
    """ Standard deck """
    def __init__(self):
        self.hh = []

    def shuffledeck(self):
        """ shuffles deck """
        shuffle(self.hh)

    def fandeck(self):
        """ Show all the cards of the deck """
        for cardindeck in self.hh:
            cardindeck.faceup()
        print("\nCards in deck: " + str(len(self.hh)))

    def showcards(self):
        """ Show all the cards of the deck, but only partial info """
        for cardindeck in self.hh:
            cardindeck.faceonly()
        print '\n'

    def cutthedeck(self):
        """randomly cut the deck"""
        self.cutlocation = random.randint(0,52)
        self.hh = self.hh + self.hh[0:self.cutlocation]
        del self.hh[0:self.cutlocation]

    def sortit(self):
         """ sort by rank"""
         self.hh.sort(key=operator.attrgetter('rank'))

    def showselect(self):
        """ Show all the cards of the deck for the user to choose """
        print '\n'
        halfdeck = len(self.hh)/2
        for a in range(0,halfdeck):
            pad = ""
            padno = len(str(self.hh[a].number) + " " +  self.hh[a].name + " of " + self.hh[a].suit)
            for b in range(0,26 - padno):
                pad = pad + " "
            print(str(self.hh[a].number) + " " +  self.hh[a].name + " of " +self.hh[a].suit  + pad + str(self.hh[a + halfdeck].number)+ " " + self.hh[a+halfdeck].name + " of " + self.hh[a+halfdeck].suit)
            if a == 12:
                print '\n'
        print '\n'

# card class contains the attributes of ear card.
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

class BestHand(object):
    """ This is a group of cards that includes best hand and some additional attributes"""
    # It was used qute extensiveliy during testing to capture information compare to compare
    def __init__(self):
#         super().__init__()
        self.bh=[]
        self.found = 0
        self.flushflag = 0
        self.straightflag = 0
        self.straightflushflag = 0
        self.acelow = 0
        self.level= 0
        self.leveldescription = 'TBD'
        self.note = 'None so far'

    def showbestinfo(self):
        """ Show all the cards of the deck, but only partial info """
#        for cardindeck in self.bh:
#            cardindeck.faceup()
        print "Showing Best Info\n"
        print 'Found Flag ' + str(self.found)
        print 'FlushFlag '+ str(self.flushflag)
        print 'StraightFlag ' + str(self.straightflag)
        print 'StraightFlushFlag ' + str(self.straightflushflag)
        print 'Level ' + str(self.level)
        print 'Description ' + self.leveldescription
        print 'number of cards in best ' + str(len(self.bh))
        print 'Ace low ' + str(self.acelow)
        print 'process note ' + self.note + "\n"


    def showbestcardsonly(self):
        """ show the best hand cards only """
        for everycard in self.bh:
            everycard.faceonly()
        print '\n'


def sumranks(hand):
    """ sum of the ranks for a deck of cards, likely for a straight test """
    handlength = len(hand.hh)
    y = 0
    for z in range(0,handlength):
        y = y +  hand.hh[z].rank
#    print y
    return y


# this works but was not used in the code.  I was going to use this but went a different direction.
# kept this obsolete code out just to continue to violate any Python zen rules and maybe I'll use it later
def rankrun(hand):
    """ go thru ordered ranks and see the longest rank and the number of runs that exceed 1"""
    runmaxlength = 1
    currlength = 1
    runnumber = 0
    priorcardrank = hand.hh[0].rank
    looplength = len(hand.hh)
    for x in range(1,looplength):
        print "Entered loop -- Card number:  " + str(x) + " Prior card rank: " + str(priorcardrank)
        if hand.hh[x].rank == priorcardrank:
            print "Current rank "+ str(hand.hh[x].rank)
            currlength = currlength + 1
            print str(currlength)
            if currlength > runmaxlength:
                runmaxlength = currlength
                print str(runmaxlength)
            if currlength == 2:
                runnumber = runnumber + 1
                print(runnumber)
        else:
            print 'Else'
            currlength = 1
        priorcardrank = hand.hh[x].rank

def FindBunch(handlist, Number, Void):
        """ Given a list and a number find the biggest rank of size number not equal to Void"""
        # So if number = 2 and and void = 3, I'm looking for a pair in the list that is not deuces
        ListLength = len(handlist)
        for k in range(0, ListLength - Number + 1):
            if (Void <> handlist[ListLength - Number  - k].rank) & (handlist[ListLength - Number  - k].rank == handlist[ListLength - k - 1].rank):
                return ListLength - Number - k
        return ListLength + 1000

def BestAvailable(handlist,Number, Void1, Void2):
        """Find the best number of cards not voided """
        # Looking for cards that that don't match certain criteria
        # Can be used if I have identified 2 pair and need the best remaining card
        ListLength = len(handlist)
        Found = 0
        BestAvail = []

        for k in range(0, ListLength):
            index = ListLength - k - 1
            if (Void1 <> handlist[index].rank) & (Void2 <> handlist[index].rank):
                BestAvail.append(index)
                Found = Found + 1
                if Found == Number:
                    return BestAvail
        return BestAvail



def straights(hand):
    """ Determine if we have 5 consecutive ranks """
    """ Do the natural straights first and then do ace low """
    NoDups = BestHand()
    NoDups.bh = hand.hh[:]
    crds = len(NoDups.bh)

    # Lets remove duplicate ranks temporarily
    go = True
    index = 0
    while go:
        if NoDups.bh[index].rank == NoDups.bh[index+1].rank:
            del NoDups.bh[index+1]
            crds = crds - 1
            if (index + 1) == crds:
                go = False
        else:
            index = index + 1
            if (index + 1) == crds:
                go = False

    UniqueRanks = len(NoDups.bh)

    if UniqueRanks <= 4:
        NoDups.note = 'No straights found'
        NoDups.bh = hand.hh[:]
        return NoDups
    else:
        for j in range (0, UniqueRanks-4):
            if NoDups.level <> 5:
                endcard = UniqueRanks - j - 1
                if NoDups.bh[endcard].rank - NoDups.bh[endcard - 4].rank == 4:
                    NoDups.leveldescription = "Straight: " + NoDups.bh[endcard].name + " high"
                    NoDups.straightflag = 1
                    NoDups.bh = NoDups.bh[endcard-4:endcard+1]
                    NoDups.level = 5
                    NoDups.found = 1

         # Edge case: Ace low straight check

        if NoDups.straightflag == 0:
            if (NoDups.bh[UniqueRanks - 1].rank == 14) & (NoDups.bh[3].rank == 5):
                NoDups.acelow = 1
                del NoDups.bh[4: UniqueRanks - 1]
                NoDups.bh = NoDups.bh[4:5] + NoDups.bh[0:4]
                NoDups.leveldescription = "Ace low straight"
                NoDups.level = 5
                NoDups.found = 1
                NoDups.straightflag = 1

    return NoDups

def flushes(hand):
    """ first loop through the cards and aggregate them in buckets to see if there are flushes"""
    # D = diamonds ...
    Best = BestHand()
    Best.bh = hand.hh

    D = Deck()
    C = Deck()
    H = Deck()
    S = Deck()
    Evalcard = Card(1,"start",1,"all")
    for x in range(0,len(hand.hh)):
        Evalcard = hand.hh[x]
        if Evalcard.suit == "Hearts":
            H.hh.append(Evalcard)
        if hand.hh[x].suit == "Spades":
            S.hh.append(Evalcard)
        if hand.hh[x].suit == "Clubs":
            C.hh.append(Evalcard)
        if hand.hh[x].suit == "Diamonds":
            D.hh.append(Evalcard)

    if len(D.hh) >= 5:
        Best.flushflag = 1
        Best.bh =   D.hh
        Best.note = "We have at least a DIAMOND flush"
    if len(H.hh) >= 5:
        Best.flushflag = 1
        Best.bh = H.hh
        Best.note = "We have at least a HEART flush"
    if len(C.hh) >= 5:
        Best.flushflag = 1
        Best.bh = C.hh
        Best.note = "We have at least a CLUBS flush"
    if len(S.hh) >= 5:
        Best.flushflag = 1
        Best.bh = S.hh
        Best.note = "We have at least a SPADES flush"
    if Best.flushflag == 1:
        Best.level = 4

    return Best

def allflushes(hand):
    """ If a flush is found, get the best cards and assign a rank"""
    # Rank 1 is the best level:  straight flush
    Best5 = BestHand()
    Best5 = flushes(hand)
    FlushCards = 0

    # Check and see if the flush is also a straight

    if Best5.flushflag == 1:
        FlushCards = len(Best5.bh)
        for j in range (0, FlushCards-4):
            if Best5.level <> 1:
                endcard = FlushCards - j - 1
                if Best5.bh[endcard].rank - Best5.bh[endcard - 4].rank == 4:
                    Best5.leveldescription = "Straight Flush: "
                    if Best5.bh[endcard].rank == 14:
                        Best5.leveldescription = "Royal Flush"
                    else:
                        Best5.leveldescription = Best5.leveldescription + Best5.bh[endcard].name + " high"
                    Best5.straightflushflag = 1
                    Best5.bh = Best5.bh[endcard-4:endcard+1]
                    Best5.level = 1
                    Best5.found = 1

         # Edge Case:  Ace low straight flush Check

        if Best5.straightflushflag == 0:
            if (Best5.bh[FlushCards - 1].rank == 14) & (Best5.bh[3].rank == 5):
                Best5.acelow = 1
                del Best5.bh[4: FlushCards - 2]
                Best5.bh = Best5.bh[4:5] + Best5.bh[0:4]
                Best5.straightflushflag = 1
                Best5.leveldescription = "Straight Flush: Ace Low"
                Best5.level = 1
                Best5.found = 1

    # If is not a straight flush, but it is a flush, get the top 5 cards of the same suit

    if (Best5.straightflushflag == 0) & (FlushCards >= 5):
        Best5.bh = Best5.bh[FlushCards-5:FlushCards]
        Best5.level = 4
        Best5.found = 1
        Best5.leveldescription = Best5.bh[endcard].suit + ' Flush: ' +  Best5.bh[endcard].name + " high"

    return Best5

def FourOfAKind(hand):
    """ Determine if there are 4 common ranks """

    Best5 = BestHand()
    Best5.bh = hand.hh[:]
    BestRemaining = []
    DummyCode = 1000

# Calculate to see if there is 4 of a kind.
    Temp4 = FindBunch(hand.hh,4,DummyCode)
    if Temp4 < DummyCode:
        BestRemaining = BestAvailable(hand.hh,1,hand.hh[Temp4].rank,hand.hh[Temp4].rank)
        Top = BestRemaining[0]
        Best5.bh = Best5.bh[Top:Top+1] + Best5.bh[Temp4:Temp4+4]
        Best5.level = 2
        Best5.found = 1
        Best5.leveldescription = '4 of a kind: ' +  Best5.bh[2].name + 's with a '+ Best5.bh[0].name + ' kicker'
    else:
      Best5.NOTE = "Not a 4K"

    return Best5


def FullHouseAnd3kind(hand):
    """ See if there is 3 of a kind and is so we either have a full house or 3 of a kind (3K)"""
    Threekind = False
    DummyCode = 1000
    Best5 = BestHand()
    Best5.bh = hand.hh[:]
    BestRemaining = []
    # See if there is a three of the same rank
    Temp3 = FindBunch(hand.hh,3,DummyCode)

    if Temp3 < DummyCode:
        Temp2 = FindBunch(hand.hh,2,hand.hh[Temp3].rank)
        if Temp2 < DummyCode:
            Best5.bh = Best5.bh[Temp2:Temp2+2]+Best5.bh[Temp3:Temp3+3]
            Best5.level = 3
            Best5.found = 1
            Best5.leveldescription = 'Full House: ' +  Best5.bh[4].name + 's ' + 'full of '+  Best5.bh[0].name + 's '
        else:
            BestRemaining = BestAvailable(hand.hh,2,hand.hh[Temp3].rank,hand.hh[Temp3].rank)
            Top = BestRemaining[0]
            Next = BestRemaining[1]
            Best5.bh = Best5.bh[Next:Next+1]+Best5.bh[Top:Top+1]+Best5.bh[Temp3:Temp3+3]
            Best5.level = 6
            Best5.found = 1
            Best5.leveldescription = '3 of a kind : ' +  Best5.bh[4].name + 's'

    return Best5

def PairsAndLower(hand):
    """ Examine the sub matches within the cards and determine the remaining hands"""
    # at this point of the comparison we have either two pair or worse
    Twokind = False
    DummyCode = 1000
    Best5 = BestHand()
    Best5.bh = hand.hh[:]
    BestRemaining = []
    # Check for a pair
    Temp2 = FindBunch(hand.hh,2,DummyCode)

    # If one pair is found, let's see if there might be another
    if Temp2 < DummyCode:
        Temp1 = FindBunch(hand.hh,2,hand.hh[Temp2].rank)
        if Temp1 < DummyCode:
            # Two pair
            BestRemaining = BestAvailable(hand.hh,1,hand.hh[Temp2].rank,hand.hh[Temp1].rank)
            Top = BestRemaining[0]
            Best5.bh = Best5.bh[Top:Top+1]+Best5.bh[Temp1:Temp1+2]+Best5.bh[Temp2:Temp2+2]
            Best5.level = 7
            Best5.found = 1
            Best5.leveldescription = 'Two Pair: ' +  Best5.bh[4].name + 's ' + 'over '+  Best5.bh[1].name + 's ' + 'with a ' + Best5.bh[0].name + ' kicker'
        else:
            # Single Pair
            BestRemaining = BestAvailable(hand.hh,3,hand.hh[Temp2].rank,hand.hh[Temp2].rank)
            Top = BestRemaining[0]
            Next = BestRemaining[1]
            Smallest = BestRemaining[2]
            Best5.bh = Best5.bh[Smallest:Smallest+1]+Best5.bh[Next:Next+1]+Best5.bh[Top:Top+1]+Best5.bh[Temp2:Temp2+2]
            Best5.level = 8
            Best5.found = 1
            Best5.leveldescription = '1 pair : ' +  Best5.bh[4].name + 's'

    return Best5

def NoPair(hand):
    """ Get the 5 best cards as the last remaining choice """
    Best5 = BestHand()
    Best5.bh = hand.hh[2:7]
    Best5.level = 9
    Best5.found = 1
    Best5.leveldescription = 'No pair : ' +  Best5.bh[4].name + ' High'
    return Best5



def HandAnalysis(hand,printflag):
    """ Review some data related to the hand to help determine it's value """
    # This really goes thru the hands and begins to determine the top hand.
    # Printflag was used for debugging and can be removed
    Best5 = BestHand()
    Best5.hh = hand.hh
    if printflag == 1:
        print 'ENTERED HAND ANALYSIS'
    Best5 = allflushes(hand)
    if printflag == 1:
        print 'POST FLUSH ' + str(Best5.found)
    if (Best5.found == 1) & (printflag == 1):
        Best5.showbestinfo()
        Best5.showbestcardsonly()
    if Best5.found == 0:
        Best5 = straights(hand)
        if printflag == 1:
            print "POST STRAIGHT " + str(Best5.found)
        if (Best5.found == 1) & (printflag == 1):
            Best5.showbestinfo()
            Best5.showbestcardsonly()
    if Best5.found == 0:
        Best5 = FourOfAKind(hand)
        if printflag == 1:
            print 'POST 4 OF A KIND ' + str(Best5.found)
        if (Best5.found == 1) & (printflag == 1):
                Best5.showbestinfo()
                Best5.showbestcardsonly()
    if Best5.found == 0:
        Best5 = FullHouseAnd3kind(hand)
        if printflag == 1:
            print 'POST FULL HOUSE ' + str(Best5.found)
        if (Best5.found == 1) & (printflag == 1):
            Best5.showbestinfo()
            Best5.showbestcardsonly()
    if Best5.found == 0:
        Best5 = PairsAndLower(hand)
        if printflag == 1:
            print 'POST PAIRS AND LOWER ' + str(Best5.found)
        if (Best5.found == 1) & (printflag == 1):
            Best5.showbestinfo()
            Best5.showbestcardsonly()
    if Best5.found == 0:
        Best5 = NoPair(hand)
        if printflag == 1:
            print 'POST NO PAIR ' + str(Best5.found)
        if (Best5.found == 1) & (printflag == 1):
            Best5.showbestinfo()
            Best5.showbestcardsonly()

    return Best5

# Create a deck instant and assign a suit and a name to each of the cards and append them to the deck

def getcurrentdeck():
    """ Build a new deck of cards """

    SuitList = ['Diamonds','Clubs','Hearts','Spades']
    NameList = ['Two','Three','Four','Five',"Six",'Seven','Eight','Nine','Ten','Jack','Queen','King','Ace']

    a = 0
    for  Suits in SuitList:
        for Names in NameList:
            number = a + 1
            rank = (a % 13) + 2
            Curr_Card = Card(number,Names,rank,Suits)
            CurrentDeck.hh.append(Curr_Card)
            a = a+1
    return CurrentDeck

def ShuffleCut(origprint,shuffle,shprint,cut,cutprint):
    """ Randomizing a Deck and Printing as requested """
    # Print (fan)# out the deck, shuffle it and re fan the deck, cut the deck and refan
    # Note this was used to help test.  For the simulation no need to shuffle and cut the deck
    if origprint == 1:
        print ("\nHere is the original deck\n")
        CurrentDeck.fandeck()

    if shuffle == 1:
        CurrentDeck.shuffledeck()
    if shprint == 1:
        print ("\nHere is the shuffled deck\n")
        CurrentDeck.fandeck()

    if cut == 1:
        CurrentDeck.cutthedeck()
    if cutprint == 1:
        print ("\nHere is the cut deck\n")
        CurrentDeck.fandeck()
    return CurrentDeck

def printouthands(hflag,tflag,bflag):
    """ Print out some of the hands and intermediate tables """

    if hflag == 1:
        print("\nHere is your Texas Hold-em Hand:")
        YourHand.showcards()
    if tflag == 1:
        print("Here is your opponent's Texas Hold-em Hand:")
        TheirHand.showcards()
    if bflag ==1:
        print("Here is the Board (Flop + Turn + River):")
        Board.showcards()

def Compare(visitor,home):
    """ Compare two opponents and determine winner """
    # Compare the hand levels and if the are the same
    # Compare card by card

    if (visitor.level > home.level):
        return 0
    if (visitor.level < home.level):
        return 1
    tie = 2
    for a in range (0,5):
        if (visitor.bh[4-a].rank < home.bh[4-a].rank):
            return 0
        if (visitor.bh[4-a].rank > home.bh[4-a].rank):
            return 1
    return tie

def createlist(N,r):
    """ Create simulation lists where each list corresponds to a unique group of 5 cards """
    # N = number of cards to choose from, r = number of cards to choose
    # Seed the list with the original cards chosen.  I was initialy just creating lists of lists
    # and decided to use the routine.  Could be done with tuples.
    combinations = []
    for a in range(0,N):
        combinations.append([a+1])
        # We will have to loop thru the cards one time less then the number of cards chosen.
        # the seeding is actually the first loop
    for rloop in range (0,r-1):
        currcombinations = len(combinations)
    # Pop card combinations off the stack 1 by 1
        for b in range(0,currcombinations):
       #start with a fresh array and put an combination in the array
            temp3 = []
            temp3 = combinations.pop(0)
            last = temp3[-1]
        # extend the combination to all possible for this iteration
            for c in range(last,N):
                tempz = temp3[:]
                tempz.append(c+1)
                combinations.append(tempz)

    return combinations

# MAIN program

# Some initializatons (it's a suit joke)

CurrentDeck = Deck()
TempDeck = Deck()
TempCard = Card(0,'temp',0,'Hugo Boss')
FinalBest_y = BestHand()
FinalBest_t = BestHand()
taglist = []
YourHand = Deck()
TheirHand = Deck()
Board = Deck()
SevenCard_y = Deck()
SevenCard_t = Deck()
Wins = 0
Ties = 0
Losses = 0

# Build a deck of cards, or open a new deck if you like
CurrentDeck = getcurrentdeck()

# Disablined routine
# CurrentDeck = ShuffleCut(0,0,0,0,0)

CurrentDeck.showselect()

# Let user pick cards and place the cards in the respective hands
w = int(input("Enter your card number 1: "))
CurrentDeck.hh[w-1].faceonly()
x = int(input("Enter your card number 2: "))
CurrentDeck.hh[x-1].faceonly()
y = int(input("Enter the opponent's card number 1: "))
CurrentDeck.hh[y-1].faceonly()
z = int(input("Enter the opponent's card number 2: "))
CurrentDeck.hh[z-1].faceonly()

YourHand.hh.append(CurrentDeck.hh[w-1])
YourHand.hh.append(CurrentDeck.hh[x-1])
TheirHand.hh.append(CurrentDeck.hh[y-1])
TheirHand.hh.append(CurrentDeck.hh[z-1])

# Remove the selected cards from the deck and use the remaining deck to
# create the simulated boards (Flop + Turn + River)

removed = 0
a = 0
while removed < 4:
    if (CurrentDeck.hh[a].number == w)  or (CurrentDeck.hh[a].number == x) or (CurrentDeck.hh[a].number == y) or (CurrentDeck.hh[a].number == z):
        del CurrentDeck.hh[a]
        removed = removed + 1
    else:
        a = a + 1

# Display the two competing hands and begin the calculations which includes
# Creating all of the board combinations from the 52-4 = 48 cards and then
# compare the hands for the two opponents for each board

printouthands(1,1,0)

# Build the boards.  This is a hog of a routine
print "Creating a list of all possible boards.  Slow :( ................."

uniquetags = createlist(48,5)
iterations = len(uniquetags)
print str(iterations) + " Boards created\n"

# Begin hand compare
print "Compare the hands for each of the " + str(iterations) + " boards\n"

for a in range(0,iterations):
    if (a < 140001) & (a % 10000 == 0):
        print "Compared total: " + str(a)
    else:
        if ((a % 150000) == 0):
            print "Compared total: " + str(a)
    taglist = uniquetags[a]
    Board.hh = []

# For each board id (tag) create 7 cards for each player and sort it for process efficiency

    for t in range(0,5):
        CardNum = taglist[t] - 1
        TempCard = CurrentDeck.hh[CardNum]
        Board.hh.append(TempCard)
    SevenCard_y.hh = YourHand.hh + Board.hh
    SevenCard_t.hh = TheirHand.hh + Board.hh
    SevenCard_y.sortit()
    SevenCard_t.sortit()

    # Obsolete for the simulation printouthands(1,1,1)
    # Calculate the best hand for each player

    FinalBest_y = HandAnalysis(SevenCard_y,0)
    FinalBest_t = HandAnalysis(SevenCard_t,0)


    # Compare the hands for each player and tally the results
    result = Compare(FinalBest_t,FinalBest_y)
    resultlabels = ['Win','Loss','Tie']

# At this point of the program we can print the totals
# print 'Result: ' +resultlabels[result]+'\n'

    if result == 0:
        Wins = Wins + 1
    elif result == 1:
        Losses = Losses + 1
    else:
        Ties = Ties + 1

Totals = Wins + Ties + Losses

#  Print the final results

print "Compared total: " + str(iterations) + '\n'
print 'Wins ' + str(Wins)
print (Wins*100.0000)/Totals
print 'Losses ' + str(Losses)
print (Losses*100.0000)/Totals
print 'Ties ' + str(Ties)
print (Ties*100.0000)/Totals
print 'Totals ' + str(Totals)

    # print SevenCardy.hh[1].rank  Wilson (obsolete test code)
