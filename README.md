### Phase_10
A rummy-type card game for my capstone project

This is currently an incompete game.  The game should eventually include a computer AI to play for the three other "computer" players.
Currently, the game is user-controlled for all four players.

### Requirements

All requirements are listed in the `requirements.txt` file.

### Python Version
Python 3.11.9

### Arcade Version
arcade 2.6.17

### Installation

To install, clone the repo into a new folder, set up and activate a virtual environment, then install the using the following commands:
```shell
$ git clone git@github.com:jake-bestland/Phase_10.git
$ cd Phase_10
$ python -m venv venv
$ source ./venv/bin/activate
$ pip install -r requirements.txt
```

To run the game, enter the following command into your teminal:
```shell
$ python phase_10.py
```


### Instructions
OBJECT:

To be the first player to complete all 10 Phases. In case of a tie, the player with the lowest score is the winner.

PLAY:

On your turn, draw one card, either from the top card from the draw pile or the top card from the discard pile.
End your turn by discarding any one of your cards onto the top of the discard pile.  During the play of the firsthand,
each player tries to complete Phase 1.  A Phase is a combination of cards.  Phases are made of sets, runs, cards of
one color, or a combination of sets and runs.
These are the 10 phases:
1. 2 sets of 3
2. 1 set of 3 + 1 run of 4
3. 1 set of 4 + 1 run of 4
4. 1 run of 7
5. 1 run of 8
6. 1 run of 9
7. 2 sets of 4
8. 7 cards of one color
9. 1 set of 5 + 1 set of 2
10. 1 set of 5 + 1 set of 3

Each player can make only one Phase during each hand.  Phases must be completed in order, from 1 to 10.

Definitions:
Sets - A set is made of two or more cards with the same number.
Runs - A run is made of four or more cards numbered in order

Wild cards:
a "Wild" card may be used in place of a number card, or may be used as any color, in order to complete a Phase

Skip cards - When played it will cause another player to lose a turn.
To use, drop the "Skip" card onto another players "hand".

Making a Phase:
If during your turn, you are able to make a Phase with the cards in your hand, lay the Phase down in the empty space(s) near your hand before discarding.
- You must have the whole Phase in hand before laying it down.
- You may lay down more than the minimun requirements of a Phase, but only if the additional cards can be directly added to the cards already in the Phase pile.

Hitting:
Hitting is the way to get rid of leftover cards after making a phase.  You may hit by putting a card directly on a Phase already laid down.
The card must properly fit with the cards already laid down.  Before you can make a hit, your own Phase must already be laid down. You may hit on your own cards,
another player's cards, or both.

Finishing a round:
The first player to get rid of all the cards in their hand, wins the round.  the winner of the round and any other players who also complete their Phase, will
advance to the next Phase.

Scoring:
The winner of the round scores zero.  All remaining players score points against them, for cards still in their hand, as follows:
- 5 points for each card numbered 1-9
- 10 points for each card numbered 10-12
- 15 points for each "Skip" card
- 25 points for each "Wild" card



# Fast forward/ Save place
The game can take some time to complete.  If you do not want to play the whole length of the game, you can change which phase each player starts on.
Or if you want to continue playing the game later, you can write down each players score and which Phase they're on and manually enter it before you start again.
(that feature can be added later - writing/reading file)
In the `phase_10.py` file, on lines 163-166 (where the players are created) you can change which phase each player starts on, and/or you can manually enter
their score (If you want to pick up where you left off).