Poker Probabilities - Texas Hold-em 

There are a few files in this repository that support calculating the best 5 card poker hand from a group of 5 or 7 cards.

The Volume Testing notebook is a test that goes thru an entire deck to count the number of hands in a deck that fall into a particular category (e.g. Full House)
It relays on hand specific functions in the poker.py library.   The results are then compared to Wikipedia poker probabilities to confirm accuracy.  This is just one
of several ways to test the validity of the library.

The Unit Testing notebook, provides insight into the hand ranking calculations and associated hand scoring.  It also does a test of the scores to provide confidence in the accuracy of the score ranking formula.

The Headsup match notebook leverages the poker.py library and calculates the winning probabilities associated with two players playng a hand of Texas Hold-em.
