"""
Phase 10 Constants
"""

# Screen title and size
SCREEN_WIDTH = 1360
SCREEN_HEIGHT = 850
SCREEN_TITLE = "Phase 10"

# Constants for sizing
CARD_SCALE = 0.66

# How big are the cards?
CARD_WIDTH = 140 * CARD_SCALE
CARD_HEIGHT = 190 * CARD_SCALE

# How big is the mat we'll place the card on?
MAT_PERCENT_OVERSIZE = 1.05
MAT_HEIGHT = int(CARD_HEIGHT * MAT_PERCENT_OVERSIZE)
DECK_MAT_WIDTH = int(CARD_WIDTH * MAT_PERCENT_OVERSIZE)
HAND_MAT_WIDTH = int(SCREEN_WIDTH * .3)
PHASE_1_MAT_WIDTH = int(HAND_MAT_WIDTH * .9)
PHASE_2_MAT_WIDTH = int(HAND_MAT_WIDTH * .45)

# How much space do we leave as a gap between the mats?
# Done as a percent of the mat size.
VERTICAL_MARGIN_PERCENT = 0.10
HORIZONTAL_MARGIN_PERCENT = 0.10

# The X,Y of the deck and discard pile (2 piles)
DECK_Y = SCREEN_HEIGHT / 2 - MAT_HEIGHT *.005
DECK_X = SCREEN_WIDTH / 2 - DECK_MAT_WIDTH * .5

# How far apart each pile goes
HAND_X_SPACING = HAND_MAT_WIDTH + HAND_MAT_WIDTH * .0825
PHASE_2_X_SPACING = HAND_MAT_WIDTH * .0034 + HAND_MAT_WIDTH /2
DECK_X_SPACING = DECK_MAT_WIDTH + DECK_MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT

# The X,Y of the USER hand (1 piles)
USER_HAND_X = SCREEN_WIDTH / 2
BOTTOM_Y = MAT_HEIGHT / 2 + MAT_HEIGHT * VERTICAL_MARGIN_PERCENT

#The Y of the USER phase pile (1-2 piles)
BOTTOM_PHASE_Y = BOTTOM_Y + MAT_HEIGHT + MAT_HEIGHT * VERTICAL_MARGIN_PERCENT

# The X,Y of Comp hands
COMP_HAND_Y = SCREEN_HEIGHT - MAT_HEIGHT / 2 - MAT_HEIGHT * VERTICAL_MARGIN_PERCENT
COMP_HAND_X = HAND_MAT_WIDTH / 2 + HAND_MAT_WIDTH * .0825

# The Y of Comp phase piles
TOP_PHASE_Y = COMP_HAND_Y - MAT_HEIGHT - MAT_HEIGHT * VERTICAL_MARGIN_PERCENT

# The X of Comp phase piles
LCOMP_PHASE_X = COMP_HAND_X
MCOMP_PHASE_X = COMP_HAND_X + HAND_X_SPACING
RCOMP_PHASE_X = COMP_HAND_X + HAND_X_SPACING * 2

# Card constants
CARD_VALUES = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "wild", "skip"]
CARD_SUITS = ["blue", "green", "red", "yellow", "black"]

# If we fan out cards stacked on each other, how far apart to fan them?
CARD_HORIZONTAL_OFFSET = CARD_WIDTH * CARD_SCALE * 0.4

# Face down image
FACE_DOWN_IMAGE = "./images/card_back.png"

# Constants that represent "what pile is what" for the game
PILE_COUNT = 14
DECK_FACE_DOWN_PILE = 0
DECK_FACE_UP_PILE = 1
USER_HAND_PILE = 2
LCOMP_HAND_PILE = 3
MCOMP_HAND_PILE = 4
RCOMP_HAND_PILE = 5
PHASE_PILE_1 = 6
PHASE_PILE_2 = 7
PHASE_PILE_3 = 8
PHASE_PILE_4 = 9
PHASE_PILE_5 = 10
PHASE_PILE_6 = 11
PHASE_PILE_7 = 12
PHASE_PILE_8 = 13

# List of phases that require 1 or 2 mat piles
PHASE_1_MATS = [4, 5, 6, 8]
PHASE_2_MATS = [1, 2, 3, 7, 9, 10]