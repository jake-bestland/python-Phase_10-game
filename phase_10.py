"""
Phase 10 game
"""
from typing import Optional

import random
import arcade
from player_class import Player

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
## might not need rest
PHASE_PILE_3 = 8
PHASE_PILE_4 = 9
PHASE_PILE_5 = 10
PHASE_PILE_6 = 11
PHASE_PILE_7 = 12
PHASE_PILE_8 = 13

# List of phases that require 1 or 2 mat piles
PHASE_1_MATS = [4, 5, 6, 8]
PHASE_2_MATS = [1, 2, 3, 7, 9, 10]


class Card(arcade.Sprite):
    """ Card sprite """

    def __init__(self, suit=0, value=0, scale=1):
        """ Card constructor """

        # Attributes for suit and value
        self.suit = suit
        self.value = value

        # Image to use for the sprite when face up
        self.image_file_name = f"./images/{CARD_SUITS[self.suit]}_cards/{CARD_SUITS[self.suit]}{(self.value + 1):0>2}.png"
        self.is_face_up = False
        super().__init__(FACE_DOWN_IMAGE, scale, hit_box_algorithm="None")

    def __lt__(self, other):
        """checks if card is less than other card by it's value."""
        t1 = f"{self.value:0>2}"
        t2 = f"{other.value:0>2}"
        return t1 < t2

    def get_value(self):
        """returns card value"""
        return f"{self.value:0>2}"  # check if need (self.value + 1)
    
    def get_color(self):
        """returns the color of card"""
        return self.suit

    def face_down(self):
        """ Turn card face-down """
        self.texture = arcade.load_texture(FACE_DOWN_IMAGE)
        self.is_face_up = False

    def face_up(self):
        """ Turn card face-up """
        self.texture = arcade.load_texture(self.image_file_name)
        self.is_face_up = True

    @property
    def is_face_down(self):
        """ Is this card face down? """
        return not self.is_face_up

user = Player("user", True)
lcomp = Player("lcomp")
mcomp = Player("mcomp")
rcomp = Player("rcomp")
class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Sprite list with all the cards, no matter what pile they are in.
        self.card_list: Optional[arcade.SpriteList] = None

        arcade.set_background_color(arcade.color.AMAZON)

        # List of cards we are dragging with the mouse
        self.held_cards = None

        # Original location of cards we are dragging with the mouse in case
        # they have to go back.
        self.held_cards_original_position = None

        # Sprite list with all the mats tha cards lay on.
        self.pile_mat_list = None

        # Create a list of lists, each holds a pile of cards.
        self.piles = None

        # Create players.
        # user = Player("user", True)
        # lcomp = Player("lcomp")
        # mcomp = Player("mcomp")
        # rcomp = Player("rcomp")

        # self.phase_list = None

        # # Keep track of phase
        # self.phase = phase
        # self.user_phase = 1
        # self.lcomp_phase = 4
        # self.mcomp_phase = 1
        # self.rcomp_phase = 4

        # # Keep track of score
        # self.score = score
        # self.user_score = 0
        # self.lcomp_score = 0
        # self.mcomp_score = 0
        # self.rcomp_score = 0

        # # Keep track of turn
        # self.user_turn = True
        # self.lcomp_turn = False
        # self.mcomp_turn = False
        # self.rcomp_turn = False

        # # Check if phase has been completed
        # self.user_phase_complete = False
        # self.lcomp_phase_complete = False
        # self.mcomp_phase_complete = False
        # self.r_comp_phase_complete = False


    # def add_score(self, player):
    #     """at end of round, add the point total for each card remaining in hand to total score."""
    #     self.player = player
    #     for card in player.hand:
    #         if card in CARD_VALUES[:9]:
    #             player.score += 5
    #         elif card in CARD_VALUES[10:12]:
    #             player.score += 10
    #         elif card == CARD_VALUES[13]:
    #             player.score += 15
    #         else:
    #             player.score += 25    

    def create_phase_mats(self, pile_x, phase):
        """ creates the play/phase piles for each player = user, lcomp, mcomp, or rcomp
        either one or two piles based on which phase they are on """
        self.pile_x = pile_x
        self.phase = phase
        # create phase mats for user
        if self.pile_x == USER_HAND_X:
            # one phase mat
            if self.phase in PHASE_1_MATS:
                pile = arcade.SpriteSolidColor(PHASE_1_MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.BLUE)
                pile.position = self.pile_x, BOTTOM_PHASE_Y
                self.pile_mat_list.append(pile)
            # two phase mats
            elif self.phase in PHASE_2_MATS:
                for i in range(2):
                    pile = arcade.SpriteSolidColor(PHASE_2_MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.YELLOW)
                    pile.position = (self.pile_x - .034 * HAND_MAT_WIDTH - PHASE_2_MAT_WIDTH / 2) + i * PHASE_2_X_SPACING, BOTTOM_PHASE_Y
                    self.pile_mat_list.append(pile)
        # create phase mats for the 3 computers
        else:
            # One phase mat
            if self.phase in PHASE_1_MATS:
                pile = arcade.SpriteSolidColor(PHASE_1_MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.BLUE)
                pile.position = self.pile_x, TOP_PHASE_Y
                self.pile_mat_list.append(pile)
            # Two phase mats
            elif self.phase in PHASE_2_MATS:
                for i in range(2):
                    pile = arcade.SpriteSolidColor(PHASE_2_MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.YELLOW)
                    pile.position = (self.pile_x - .034 * HAND_MAT_WIDTH - PHASE_2_MAT_WIDTH / 2) + i * PHASE_2_X_SPACING, TOP_PHASE_Y
                    self.pile_mat_list.append(pile)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """

        # List of cards we are dragging with the mouse
        self.held_cards = []

        # Original location of cards we are dragging with the mouse in case
        # they have to go back.
        self.held_cards_original_position = []

        # ---  Create the mats the cards go on.

        # Sprite list with all the mats tha cards lay on.
        self.pile_mat_list: arcade.SpriteList = arcade.SpriteList()

        # Create the mats for the DECK face down and face up piles
        pile = arcade.SpriteSolidColor(DECK_MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
        pile.position = DECK_X, DECK_Y
        self.pile_mat_list.append(pile)

        pile = arcade.SpriteSolidColor(DECK_MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
        pile.position = DECK_X + DECK_X_SPACING, DECK_Y
        self.pile_mat_list.append(pile)

        # Create the USER hand pile
        pile = arcade.SpriteSolidColor(HAND_MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
        pile.position = USER_HAND_X, BOTTOM_Y
        self.pile_mat_list.append(pile)

        # Create the COMP hand piles
        for i in range(3):
            pile = arcade.SpriteSolidColor(HAND_MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.RED)
            pile.position = COMP_HAND_X + i * HAND_X_SPACING, COMP_HAND_Y
            self.pile_mat_list.append(pile)

        # Create the Phase piles
        self.create_phase_mats(USER_HAND_X, user.phase)
        self.create_phase_mats(LCOMP_PHASE_X, lcomp.phase)
        self.create_phase_mats(MCOMP_PHASE_X, mcomp.phase)
        self.create_phase_mats(RCOMP_PHASE_X, rcomp.phase)

        # assign phase piles to players
        user.determine_phase_piles(self.pile_mat_list)
        lcomp.determine_phase_piles(self.pile_mat_list)
        mcomp.determine_phase_piles(self.pile_mat_list)
        rcomp.determine_phase_piles(self.pile_mat_list)
        
        # --- Create, shuffle, and deal the cards

        # Sprite list with all the cards, no matter what pile they are in.
        self.card_list = arcade.SpriteList()

        # Create 2 of every numbered card
        for i in range(2):
            for card_suit in range(4):
                for card_value in range(0, 12):
                    card = Card(card_suit, card_value, CARD_SCALE)
                    card.position = DECK_X, DECK_Y
                    self.card_list.append(card)
        # Create 8 wild cards
        for i in range(8):
            wild_card = Card(4, 12, CARD_SCALE)
            wild_card.position = DECK_X, DECK_Y         
            self.card_list.append(wild_card)
        # Create 4 skip cards
        for i in range(4):
            skip_card = Card(4, 13, CARD_SCALE)
            skip_card.position = DECK_X, DECK_Y 
            self.card_list.append(skip_card)

        # Shuffle the cards
        for pos1 in range(len(self.card_list)):
            pos2 = random.randrange(len(self.card_list))
            self.card_list.swap(pos1, pos2)

        # Create a list of lists, each holds a pile of cards.
        self.piles = [[] for _ in range(PILE_COUNT)]

        # Put all the cards in the DECK face-down pile
        for card in self.card_list:
            self.piles[DECK_FACE_DOWN_PILE].append(card)

        # - Pull from that pile into the user and comp hand piles, comp hands face-down, user hand face-up
        # deal to USER hand
        # Deal proper number of cards for that pile
        for j in range(10):
            # Pop the card off the deck we are dealing from and turn face-up
            card = self.piles[DECK_FACE_DOWN_PILE].pop()
            card.face_up()
            # Put in the proper pile
            if len(self.piles[USER_HAND_PILE]) > 0:
                # Move cards to proper position
                top_card = self.piles[USER_HAND_PILE][-1]
                self.piles[USER_HAND_PILE].append(card)
                card.position = top_card.center_x + CARD_HORIZONTAL_OFFSET, \
                                            top_card.center_y
            # Are there no cards in the user pile?
            else:
                self.piles[USER_HAND_PILE].append(card)
                # Move cards to proper position
                card.position = USER_HAND_X - (CARD_HORIZONTAL_OFFSET * 9) / 2, BOTTOM_Y
            # Sort cards in pile
            # self.pull_to_top(card)
            self.sort_pile(USER_HAND_PILE)
            
        # loop to deal to each COMP hand pile
        for pile_no in range(LCOMP_HAND_PILE, RCOMP_HAND_PILE + 1):
            # Deal proper number of cards for that pile
            for j in range(10):
                # Pop the card off the deck we are dealing from
                card = self.piles[DECK_FACE_DOWN_PILE].pop()
                #### --- Card face up for debugging purposes, # keep face down for game --- ###
                card.face_up()
                # Put in the proper pile
                if len(self.piles[pile_no]) > 0:
                    # Move cards to proper position
                    top_card = self.piles[pile_no][-1]
                    self.piles[pile_no].append(card)
                    card.position = top_card.center_x + CARD_HORIZONTAL_OFFSET, \
                                            top_card.center_y
                # Are there no cards in the comp pile?
                else:
                    self.piles[pile_no].append(card)
                        # Move cards to proper position
                    card.position = self.pile_mat_list[pile_no].center_x - (CARD_HORIZONTAL_OFFSET * 9) / 2, \
                                            self.pile_mat_list[pile_no].center_y
                # Sort cards in pile
                # self.pull_to_top(card)
                self.sort_pile(pile_no)
                

        # Flip over top card from main deck to face-up/ discard pile
        card = self.piles[DECK_FACE_DOWN_PILE].pop()
        card.face_up()
        self.piles[DECK_FACE_UP_PILE].append(card)
        card.position = self.pile_mat_list[DECK_FACE_UP_PILE].position   

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        self.clear()

        # Draw the mats the cards go on to
        self.pile_mat_list.draw()

        # Draw the cards
        self.card_list.draw()

    def pull_to_top(self, card: arcade.Sprite):
        """ Pull card to top of rendering order (last to render, looks on-top) """

        # Remove, and append to the end
        self.card_list.remove(card)
        self.card_list.append(card)

    def on_key_press(self, symbol: int, modifiers: int):
        """ User presses key """
        if symbol == arcade.key.R:
            # Restart
            self.setup()

    def on_mouse_press(self, x, y, button, key_modifiers):
        """ Called when the user presses a mouse button. """

        # Get list of cards we've clicked on
        cards = arcade.get_sprites_at_point((x, y), self.card_list)

        # Have we clicked on a card?
        if len(cards) > 0:

            # Figure out what pile the card is in
            pile_index = self.get_pile_for_card(cards[-1])

            # Are we clicking on the main deck?
            if pile_index == DECK_FACE_DOWN_PILE:
                # Get top card
                card = self.piles[DECK_FACE_DOWN_PILE][-1]
                # Flip face up
                card.face_up()
                # Move card position to discard/face-up pile
                card.position = self.pile_mat_list[USER_HAND_PILE].position
                # Remove card from face down pile
                self.piles[DECK_FACE_DOWN_PILE].remove(card)
                # Move card to face up list
                self.piles[USER_HAND_PILE].append(card)
                # Put on top draw-order wise
                # self.pull_to_top(card)
                self.sort_pile(USER_HAND_PILE)

            else:
                # All other cases, grab the face-up card we are clicking on
                self.held_cards = [cards[-1]]
                # Save the position
                self.held_cards_original_position = [self.held_cards[0].position]

        else:

            # Click on a mat instead of a card?
            mats = arcade.get_sprites_at_point((x, y), self.pile_mat_list)

            if len(mats) > 0:
                mat = mats[0]
                mat_index = self.pile_mat_list.index(mat)

                # Is it our turned over flip mat? and no cards on it?
                if mat_index == DECK_FACE_DOWN_PILE and len(self.piles[DECK_FACE_DOWN_PILE]) == 0:
                    # Flip the deck back over so we can restart
                    temp_list = self.piles[DECK_FACE_UP_PILE].copy()
                    for card in reversed(temp_list):
                        card.face_down()
                        self.piles[DECK_FACE_UP_PILE].remove(card)
                        self.piles[DECK_FACE_DOWN_PILE].append(card)
                        card.position = self.pile_mat_list[DECK_FACE_DOWN_PILE].position
                    # flip over top card
                    card = self.piles[DECK_FACE_DOWN_PILE].pop()
                    card.face_up()
                    self.piles[DECK_FACE_UP_PILE].append(card)
                    card.position = self.pile_mat_list[DECK_FACE_UP_PILE].position                    

            # --- add buttons here? ---
    
    def sort_pile(self, pile):
        """sorts cards in pile by value from low to high"""
        # Make a copy of pile to be sorted and clear the original
        temp_pile = self.piles[pile].copy()
        self.piles[pile].clear()
        # Sort cards in the temporary pile
        temp_pile.sort(reverse=True)
        # Get the index of the pile
        pile_mat_index = self.pile_mat_list[pile]
        # Loop for every card in pile
        for x in range(len(temp_pile)):
            # Pop card off of temp pile
            card = temp_pile.pop()
            # Put card back into original pile
            if len(self.piles[pile]) > 0:
                # Move cards to proper position
                top_card = self.piles[pile][-1]
                self.piles[pile].append(card)
                card.position = top_card.center_x + CARD_HORIZONTAL_OFFSET, \
                                            top_card.center_y
            else:
                # Add the first card to original pile and put in proper position
                self.piles[pile].append(card)
                # proper position if mat is either a players HAND or is a single phase mat (one bigger phase mat)
                if pile_mat_index.width == PHASE_1_MAT_WIDTH or pile_mat_index.width == HAND_MAT_WIDTH:
                    card.position = pile_mat_index.center_x - (CARD_HORIZONTAL_OFFSET * 9) / 2, \
                                            pile_mat_index.center_y
                # proper position if mat is a double phase mat (smaller mat)
                else:
                    card.position = pile_mat_index.center_x - (CARD_HORIZONTAL_OFFSET * 4) / 2, \
                                            pile_mat_index.center_y
            # Put on top in order added
            self.pull_to_top(card)
    
    def remove_card_from_pile(self, card):
        """ Remove card from whatever pile it was in. """
        for pile in self.piles:
            if card in pile and pile == self.piles[DECK_FACE_UP_PILE]:
                pile.remove(card)
                break
            elif card in pile:
                pile.remove(card)
                self.sort_pile(self.piles.index(pile))
            
    def get_pile_for_card(self, card):
        """ What pile is this card in? """
        for index, pile in enumerate(self.piles):
            if card in pile:
                return index

    def move_card_to_new_pile(self, card, pile_index):
        """ Move the card to a new pile """
        self.remove_card_from_pile(card)
        self.piles[pile_index].append(card)
        if pile_index != DECK_FACE_UP_PILE:
            self.sort_pile(pile_index)

    ### this will be more for future AI code to check phase piles for each comp
    def determine_phase_piles(self):  ## don't need as new func, just add code to setup?
        if self.user_phase in PHASE_1_MATS:  ## - play pile func?
            self.user_phase_pile = self.pile_mat_list[PHASE_PILE_1]
            last_user_pile = PHASE_PILE_1
        elif self.user_phase in PHASE_2_MATS:
            self.user_phase_pile_b = self.pile_mat_list[PHASE_PILE_1]
            self.user_phase_pile = self.pile_mat_list[PHASE_PILE_2]
            last_user_pile = PHASE_PILE_2

        if self.lcomp_phase in PHASE_1_MATS:
            self.lcomp_phase_pile = self.pile_mat_list[last_user_pile + 1]
            last_lcomp_pile = last_user_pile + 1
        elif self.lcomp_phase in PHASE_2_MATS:
            self.lcomp_phase_pile_b = self.pile_mat_list[last_user_pile + 1]
            self.lcomp_phase_pile = self.pile_mat_list[last_user_pile + 2]
            last_lcomp_pile = last_user_pile + 2

        if self.mcomp_phase in PHASE_1_MATS:
            self.mcomp_phase_pile = self.pile_mat_list[last_lcomp_pile + 1]
            last_mcomp_pile = last_lcomp_pile + 1
        elif self.mcomp_phase in PHASE_2_MATS:
            self.mcomp_phase_pile_b = self.pile_mat_list[last_lcomp_pile + 1]
            self.mcomp_phase_pile = self.pile_mat_list[last_lcomp_pile + 2] 
            last_mcomp_pile = last_lcomp_pile + 2

        if self.rcomp_phase in PHASE_1_MATS:
            self.rcomp_phase_pile = self.pile_mat_list[last_mcomp_pile + 1]
        elif self.rcomp_phase in PHASE_2_MATS:
            self.rcomp_phase_pile_b = self.pile_mat_list[last_mcomp_pile + 1]
            self.rcomp_phase_pile = self.pile_mat_list[last_mcomp_pile + 2]


    def check_set(self, amount, pile):#, complete=False):  # elim complete?
        """check to see if cards in phase pile meets the phase requirement for a set.
        amount = number of cards with same value needed to complete phase
        pile = the list of cards in the phase pile being checked
        returns bool"""
        self.amount = amount
        self.pile = pile
        # self.complete = complete # elim complete?
        # get first card value other than wild or skip
        while True:
            n = 0
            card_1 = self.pile[n]
            if card_1.getsuit() == "black":
                n += 1
            else:
                break
        # create an empty result list for acceptable cards and bad list for invalid cards
        res = []
        bad = []
        for card in self.pile:
            if card.get_value() == "wild":
                self.amount -= 1
            elif card.get_value() == card_1.get_value():   ### need to add if card != value it's false, return to hand
                    res.append(card)
            else:
                bad.append(card)
        return len(res) >= self.amount and len(bad) == 0
        # if len(res) >= self.amount and len(bad) == 0:  # take out of for loop?
        #     # self.complete = True   ### maybe change to a phase check = True (from a phase check func?)  ### maybe return player_phase_complete = True, and remove complete parameter
        #     # hit_on_set = True  --for future 'hitting' func
        #     return True
        # else:
        #     # self.complete = False
        #     return False

        ### if phase == 1:
        ### if check_set(3, phase pile 1) and check_set(3, phase pile 2):
                ###phase 1 = True. or self.user_phase_complete = True, self.user_phase +1

        ### if check_set(3, phase pile 1, True) and check_set(3, phase pile 2, True):
                ###phase 1 = True. or self.user_phase_complete = True, self.user_phase +1
    
    def check_color(self, amount, pile):#, complete=False):
        """ checks to see if all cards in pile has same color. returns bool.  """
        self.amount = amount
        self.pile = pile
        # self.complete = complete
        # get first card color, other than wild
        while True:
            n = 0
            card_1 = self.pile[n]
            if card_1.getsuit() == "black":
                n += 1
                continue
            else:
                break
        # create an empty result list for acceptable cards and bad list for invalid cards
        res = []
        bad = []
        for card in self.pile:
            # if card == Card("black", "wild", CARD_SCALE):
            #     self.amount -= 1
            if card.get_value() == "wild":
                self.amount -= 1
            elif card.get_suit() == card_1.get_suit():   ### need to add if card != suit it's false, return to hand
                    res.append(card)
            else:
                bad.append(card)
        if len(res) >= self.amount and len(bad) == 0:
            # self.complete = True   ### maybe change to a phase check = True (from a phase check func?)
            # hit_on_color = True  --for future 'hitting' func
            return True
        else:
            # self.complete = False
            return False

    def check_run(self, amount, pile):#, complete=False):
        self.amount = amount
        self.pile = pile
        # self.complete = complete
        # create an empty result list for acceptable cards and bad list for invalid cards        
        res = []
        bad = []
        for card in self.pile:  ### need to change value of wild card when adding into run.
            if len(res) > 0:
                start_card = res[0]
                prev_card = res[-1]
                if card.getvalue() == "skip":
                    bad.append(card)
                elif prev_card.getvalue() == "wild": #and len(res) == 1:
                    res.append(card)
                ### change below to -- elif: card.getvalue().isdigit() --- change else: to return False/put cards back (because of skip)
                elif card.getvalue() == "wild" or int(card.getvalue()) == (int(prev_card.getvalue()) + 1):
                        res.append(card)
                else:
                    bad.append(card)
            else:
                if card.getvalue() == "skip":
                    bad.append(card)
                else:
                    res.append(card)
        if len(res) >= self.amount and len(bad) == 0:
            # hit_on_run = True  --for future 'hitting' func
            return True
        else:
            return False

    def check_phase_complete(self, phase): # for user  # ex: check_phase_complete(self.user_phase)
        self.phase = phase
        if self.phase in PHASE_1_MATS:
            phase_pile = self.pile_mat_list[PHASE_PILE_1]
        elif self.phase in PHASE_2_MATS:
            phase_pile_b = self.pile_mat_list[PHASE_PILE_1]
            phase_pile = self.pile_mat_list[PHASE_PILE_2]

        if self.phase == 1:
            if self.check_set(3, phase_pile_b) and self.check_set(3, phase_pile):
                # self.phase_complete = True
                # self.phase += 1  -- maybe put at round end? if check_phase_complete = True, self.phase += 1
                # hit_on_set = True  -- phase_pile_b.hit_on_set() phase_pile.hit_on_set()
                return True
            else:
                # self.phase_complete = False
                return False

        elif self.phase == 2:
            if (self.check_set(3, phase_pile) and self.check_run(4, phase_pile_b)) or (self.check_set(3, phase_pile_b) and self.check_run(4, phase_pile)):
                self.phase_complete = True
            else:
                self.phase_complete = False

        elif self.phase == 3:
            if (self.check_set(4, phase_pile) and self.check_run(4, phase_pile_b)) or (self.check_set(4, phase_pile_b) and self.check_run(4, phase_pile)):
                self.phase_complete = True
            else:
                self.phase_complete = False

        elif self.phase == 4:
            if self.check_run(7, phase_pile):
                self.phase_complete = True
            else:
                self.phase_complete = False

        elif self.phase == 5:
            if self.check_run(8, phase_pile):
                self.phase_complete = True
            else:
                self.phase_complete = False

        elif self.phase == 6:
            if self.check_run(9, phase_pile):
                self.phase_complete = True
            else:
                self.phase_complete = False

        elif self.phase == 7:
            if self.check_set(4, phase_pile_b) and self.check_set(4, phase_pile):
                self.phase_complete = True
            else:
                self.phase_complete = False

        elif self.phase == 8:
            if self.check_color(7, phase_pile):
                self.phase_complete = True
            else:
                self.phase_complete = False

        elif self.phase == 9:
            if (self.check_set(5, phase_pile) and self.check_set(2, phase_pile_b)) or (self.check_set(5, phase_pile_b) and self.check_set(2, phase_pile)):
                self.phase_complete = True
            else:
                self.phase_complete = False

        elif self.phase == 10:
            if (self.check_set(5, phase_pile) and self.check_set(3, phase_pile_b)) or (self.check_set(5, phase_pile_b) and self.check_set(3, phase_pile)):
                self.phase_complete = True
            else:
                self.phase_complete = False


    
    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        """ Called when the user presses a mouse button. """

        # If we don't have any cards, who cares
        if len(self.held_cards) == 0:
            return

        # Find the closest pile, in case we are in contact with more than one
        pile, distance = arcade.get_closest_sprite(self.held_cards[0], self.pile_mat_list)
        reset_position = True

        # See if we are in contact with the closest pile
        if arcade.check_for_collision(self.held_cards[0], pile):

            # What pile is it?
            pile_index = self.pile_mat_list.index(pile)

            #  Is it the same pile we came from?
            if pile_index == self.get_pile_for_card(self.held_cards[0]):
                # If so, who cares. We'll just reset our position.
                pass

            # Is it on a hand pile?
            elif USER_HAND_PILE <= pile_index <= RCOMP_HAND_PILE:
                # Are there already cards there?
                if len(self.piles[pile_index]) > 0:
                    # Move cards to proper position
                    top_card = self.piles[pile_index][-1]
                    for dropped_card in self.held_cards:
                        dropped_card.position = top_card.center_x + CARD_HORIZONTAL_OFFSET, \
                                                top_card.center_y
                else:
                    # Are there no cards in the USER hand pile?
                    for dropped_card in self.held_cards:
                        # Move cards to proper position
                        dropped_card.position = pile.center_x - (CARD_HORIZONTAL_OFFSET * 9) / 2, \
                                                pile.center_y
                # Sort pile by card value
                self.sort_pile(pile_index)
                for card in self.held_cards:
                    # Cards are in the right position, but we need to move them to the right list
                    self.move_card_to_new_pile(card, pile_index)
                
                # Success, don't reset position of cards
                reset_position = False

            # Release on phase pile?
            elif PHASE_PILE_1 <= pile_index <= PHASE_PILE_8:
                if len(self.piles[pile_index]) > 0:
                    # Move cards to proper position
                    top_card = self.piles[pile_index][-1]
                    for dropped_card in self.held_cards:
                        dropped_card.face_up()
                        dropped_card.position = top_card.center_x + CARD_HORIZONTAL_OFFSET, \
                                                top_card.center_y
                else:
                    # Are there no cards in the phase pile?
                    for dropped_card in self.held_cards:
                        dropped_card.face_up()
                        # Move cards to proper position
                        # If 1 bigger phase pile
                        if pile.width == PHASE_1_MAT_WIDTH:
                            dropped_card.position = pile.center_x - (CARD_HORIZONTAL_OFFSET * 9) / 2, \
                                                pile.center_y
                        # If 2 smaller phase piles
                        else:
                            dropped_card.position = pile.center_x - (CARD_HORIZONTAL_OFFSET * 4) / 2, \
                                                pile.center_y

                # Sort pile by value
                self.sort_pile(pile_index)
                # Move card to card list
                for card in self.held_cards:
                    self.move_card_to_new_pile(card, pile_index)

                
                reset_position = False

            # Release on discard pile
            elif pile_index == DECK_FACE_UP_PILE:
                if len(self.piles[pile_index]) > 0:
                    top_card = self.piles[pile_index][-1]
                    for dropped_card in self.held_cards:
                        dropped_card.face_up()
                        dropped_card.position = top_card.position
                else:
                    for dropped_card in self.held_cards:
                        dropped_card.face_up()
                        dropped_card.position = pile.position
                self.pull_to_top(self.held_cards[-1])
                for card in self.held_cards:
                    self.move_card_to_new_pile(card, pile_index)
                
                reset_position = False
                # add change to turn flag
            

        if reset_position:
            # Where-ever we were dropped, it wasn't valid. Reset the each card's position
            # to its original spot.
            for pile_index, card in enumerate(self.held_cards):
                card.position = self.held_cards_original_position[pile_index]

        # We are no longer holding cards
        self.held_cards = []

    
    
    
    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """ User moves mouse """

        # If we are holding cards, move them with the mouse
        for card in self.held_cards:
            card.center_x += dx
            card.center_y += dy
            


def main():
    """ Main function """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()