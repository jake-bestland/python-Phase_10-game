"""
Phase 10 game
"""
from typing import Optional

import random
import arcade
import webbrowser
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
DISCARD_PILE = 1
USER_HAND_PILE = 2
LCOMP_HAND_PILE = 3
MCOMP_HAND_PILE = 4
RCOMP_HAND_PILE = 5
PHASE_PILE_1 = 6
PHASE_PILE_2 = 7
LAST_PHASE_PILE = 13

# List of phases that require 1 or 2 mat piles
PHASE_1_MATS = [4, 5, 6, 8]
PHASE_2_MATS = [1, 2, 3, 7, 9, 10]


class Card(arcade.Sprite):
    """ Card sprite """

    def __init__(self, suit=0, value=0, scale=1, points=0):
        """ Card constructor """

        # Attributes for suit, value and points
        self.suit = suit
        self.value = value
        self.points = points

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
        """returns string of card value"""
        return f"{self.value:0>2}"
    
    def get_color(self):
        """returns a string of the color of card"""
        return self.suit

    def get_width(self):
        """returns the width of the card"""
        return self.width
    
    def change_value(self, new_value):
        """changes the value of the Card"""
        self.new_value = new_value
        self.value = self.new_value

    def change_width(self, new_width):
        """change width of the card.  done as a percentage."""
        self.new_width = new_width
        self.width = self.width * self.new_width

    def get_points(self):
        """returns the point value of the card based off of the value."""
        if self.value in range(0, 9):
            self.points = 5
        elif self.value in range(9, 12):
            self.points = 10
        elif self.value == 13:
            self.points = 15
        else:
            self.points += 25
        return self.points

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

# create players
user = Player("user", USER_HAND_PILE, 1, True)
lcomp = Player("lcomp", LCOMP_HAND_PILE, 1)
mcomp = Player("mcomp", MCOMP_HAND_PILE, 1)
rcomp = Player("rcomp", RCOMP_HAND_PILE, 1)

class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Sprite list with all the cards, no matter what pile they are in.
        self.card_list: Optional[arcade.SpriteList] = None

        arcade.set_background_color(arcade.color.DARK_GRAY)

        # List of cards we are dragging with the mouse
        self.held_cards = None

        # Original location of cards we are dragging with the mouse in case
        # they have to go back.
        self.held_cards_original_position = None

        # Sprite list with all the mats tha cards lay on.
        self.pile_mat_list = None

        # Create a list of lists, each holds a pile of cards.
        self.piles = None

        # Create list of Players
        self.player_list = None


    def create_phase_mats(self, pile_x, phase):
        """ creates the play/phase piles for each player = user, lcomp, mcomp, or rcomp.
        Player will have one or two piles based on which phase they are on """
        self.pile_x = pile_x
        self.phase = phase
        # create phase mats for user
        if self.pile_x == USER_HAND_X:
            # one phase mat
            if self.phase in PHASE_1_MATS:
                pile = arcade.SpriteSolidColor(PHASE_1_MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_SLATE_GRAY)
                pile.position = self.pile_x, BOTTOM_PHASE_Y
                self.pile_mat_list.append(pile)
            # two phase mats
            elif self.phase in PHASE_2_MATS:
                for i in range(2):
                    pile = arcade.SpriteSolidColor(PHASE_2_MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_SLATE_GRAY)
                    pile.position = (self.pile_x - .034 * HAND_MAT_WIDTH - PHASE_2_MAT_WIDTH / 2) + i * PHASE_2_X_SPACING, BOTTOM_PHASE_Y
                    self.pile_mat_list.append(pile)
        # create phase mats for the 3 computers
        else:
            # One phase mat
            if self.phase in PHASE_1_MATS:
                pile = arcade.SpriteSolidColor(PHASE_1_MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_SLATE_GRAY)
                pile.position = self.pile_x, TOP_PHASE_Y
                self.pile_mat_list.append(pile)
            # Two phase mats
            elif self.phase in PHASE_2_MATS:
                for i in range(2):
                    pile = arcade.SpriteSolidColor(PHASE_2_MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_SLATE_GRAY)
                    pile.position = (self.pile_x - .034 * HAND_MAT_WIDTH - PHASE_2_MAT_WIDTH / 2) + i * PHASE_2_X_SPACING, TOP_PHASE_Y
                    self.pile_mat_list.append(pile)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """

        # List of cards we are dragging with the mouse
        self.held_cards = []

        # Original location of cards we are dragging with the mouse in case
        # they have to go back.
        self.held_cards_original_position = []

        # List of Players
        self.player_list = []

        # Flags to check if someone has won
        self.game_over = False
        self.keep_playing = True

        # create list of players and counter
        self.player_list.append(user)
        self.player_list.append(lcomp)
        self.player_list.append(mcomp)
        self.player_list.append(rcomp)
        n = self.get_turn()

        # ---  Create the mats the cards go on.

        # Sprite list with all the mats tha cards lay on.
        self.pile_mat_list: arcade.SpriteList = arcade.SpriteList()

        # Create the mats for the DECK face down and face up piles
        pile = arcade.SpriteSolidColor(DECK_MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_SLATE_GRAY)
        pile.position = DECK_X, DECK_Y
        self.pile_mat_list.append(pile)

        pile = arcade.SpriteSolidColor(DECK_MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_SLATE_GRAY)
        pile.position = DECK_X + DECK_X_SPACING, DECK_Y
        self.pile_mat_list.append(pile)

        # Create the USER hand pile
        pile = arcade.SpriteSolidColor(HAND_MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.BLUE)
        pile.position = USER_HAND_X, BOTTOM_Y
        self.pile_mat_list.append(pile)

        # Create the 3 COMP hand piles
        pile = arcade.SpriteSolidColor(HAND_MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.GREEN)
        pile.position = COMP_HAND_X, COMP_HAND_Y
        self.pile_mat_list.append(pile)

        pile = arcade.SpriteSolidColor(HAND_MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.RED)
        pile.position = COMP_HAND_X + HAND_X_SPACING, COMP_HAND_Y
        self.pile_mat_list.append(pile)

        pile = arcade.SpriteSolidColor(HAND_MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.YELLOW)
        pile.position = COMP_HAND_X + 2 * HAND_X_SPACING, COMP_HAND_Y
        self.pile_mat_list.append(pile)


        # Create the Phase piles
        self.create_phase_mats(USER_HAND_X, user.phase)
        self.create_phase_mats(LCOMP_PHASE_X, lcomp.phase)
        self.create_phase_mats(MCOMP_PHASE_X, mcomp.phase)
        self.create_phase_mats(RCOMP_PHASE_X, rcomp.phase)

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

        # - Pull from that pile into the hand piles, cards will be face-up for whichever players turn it is. The other hands face-down

        # Deal 10 cards to USER hand
        for j in range(10):
            # Pop the card off the deck we are dealing from
            card = self.piles[DECK_FACE_DOWN_PILE].pop()
            # Put in the proper pile
            if len(self.piles[USER_HAND_PILE]) > 0:
                # Move cards to proper position
                top_card = self.piles[USER_HAND_PILE][-1]
                self.piles[USER_HAND_PILE].append(card)
                card.position = top_card.center_x + CARD_HORIZONTAL_OFFSET, \
                                            top_card.center_y
            # If no cards in the user pile
            else:
                self.piles[USER_HAND_PILE].append(card)
                # Move cards to proper position
                card.position = USER_HAND_X - (CARD_HORIZONTAL_OFFSET * 9) / 2, BOTTOM_Y
            # Sort cards in pile
            self.sort_pile(USER_HAND_PILE)
            
        # loop to deal to each COMP hand pile
        for pile_no in range(LCOMP_HAND_PILE, RCOMP_HAND_PILE + 1):
            # Deal proper number of cards for that pile
            for j in range(10):
                # Pop the card off the deck we are dealing from
                card = self.piles[DECK_FACE_DOWN_PILE].pop()
                # Put in the proper pile
                if len(self.piles[pile_no]) > 0:
                    # Move cards to proper position
                    top_card = self.piles[pile_no][-1]
                    self.piles[pile_no].append(card)
                    card.position = top_card.center_x + CARD_HORIZONTAL_OFFSET, \
                                            top_card.center_y
                # If no cards in the comp pile
                else:
                    self.piles[pile_no].append(card)
                    # Move cards to proper position
                    card.position = self.pile_mat_list[pile_no].center_x - (CARD_HORIZONTAL_OFFSET * 9) / 2, \
                                            self.pile_mat_list[pile_no].center_y
                # Sort cards in pile
                self.sort_pile(pile_no)

        # Flip over cards in hand for whose turn it is
        for card in self.piles[self.player_list[n].hand]:
            card.face_up()
        # Flip over top card from main deck to face-up/ discard pile
        card = self.piles[DECK_FACE_DOWN_PILE].pop()
        card.face_up()
        self.piles[DISCARD_PILE].append(card)
        card.position = self.pile_mat_list[DISCARD_PILE].position
        # if a skip card is flipped over, skip first player
        if card.get_value() == "13":
            self.end_turn(n)

        # assign phase piles to players
        user.determine_phase_piles(self.piles)
        lcomp.determine_phase_piles(self.piles, user.last_pile)
        mcomp.determine_phase_piles(self.piles, lcomp.last_pile)
        rcomp.determine_phase_piles(self.piles, mcomp.last_pile)

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        self.clear()

        # Draw the mats the cards go on to
        self.pile_mat_list.draw()

        # Draw the cards
        self.card_list.draw()

        # Draw text to draw/pickup card
        n = self.get_turn()
        draw_card_text = f"* Draw or pickup a card *"
        if self.player_list[n].turn and self.player_list[n].draw_card and self.game_over == False:
            arcade.draw_text(
                draw_card_text,
                DECK_X - 3 * DECK_MAT_WIDTH,
                DECK_Y,
                arcade.csscolor.BLACK,
                15
            )
        
        # Draw game over/ winner
        if self.game_over == True:
            if self.winner.name == "user":
                player_text = "Player 1"
            elif self.winner.name == "lcomp":
                player_text = "Player 2"
            elif self.winner.name == "mcomp":
                player_text = "Player 3"
            elif self.winner.name == "rcomp":
                player_text = "Player 4"
            arcade.draw_text(
                f"*{player_text} Wins!!*",
                DECK_X + 3 * DECK_MAT_WIDTH,
                DECK_Y,
                arcade.csscolor.BLACK,
                38
                )
            
            arcade.draw_text(
                "*GAME OVER!*",
                DECK_X - 5 * DECK_MAT_WIDTH,
                DECK_Y,
                arcade.csscolor.BLACK,
                38
            )
        
        # Draw box to put around hands showing where to play skip card
        # if self.held_cards[0].get_value() == "13":
        #     arcade.draw_texture_rectangle

        # Draw instructions
        instruction_text = """\
        Press * SPACE * for 
        complete instructions
        """
        arcade.draw_text(
            instruction_text,
            875,
            235,
            arcade.csscolor.BLACK,
            12,
            width=260,
            multiline=True
        )

        # Draw phase list # -- leave spaces after each line so that the width doesn't cut off anything unwanted for multiline
        phase_list_text = """\
          The phases are:              
          1. 2 sets of 3              
          2. 1 set of 3 + 1 run of 4  
          3. 1 set of 4 + 1 run of 4      
          4. 1 run of 7               
          5. 1 run of 8               
          6. 1 run of 9               
          7. 2 sets of 4              
          8. 7 cards of 1 color       
          9. 1 set of 5 + 1 set of 2  
        10. 1 set of 5 + 1 set of 3 
        """
        arcade.draw_text(
            phase_list_text,
            1040,
            265,
            arcade.csscolor.BLACK,
            15,
            width=290,
            bold=True,
            multiline=True
        )

        # Draw the scoreboard
        user_name_text = f"Player 1:"
        arcade.draw_text(
            user_name_text,
            10,
            265,
            arcade.csscolor.BLUE,
            20,
            bold=True
        )

        user_phase_text = f"Phase: {self.player_list[0].phase}    Score: {self.player_list[0].score}"
        arcade.draw_text(
            user_phase_text,
            10,
            240,
            arcade.csscolor.BLACK,
            15,
        )

        lcomp_name_text = f"Player: 2"
        arcade.draw_text(
            lcomp_name_text,
            10,
            190,
            arcade.csscolor.GREEN,
            20,
            bold=True
        )

        lcomp_phase_text = f"Phase: {self.player_list[1].phase}    Score: {self.player_list[1].score}"
        arcade.draw_text(
            lcomp_phase_text,
            10,
            165,
            arcade.csscolor.BLACK,
            15
        )

        mcomp_name_text = f"Player: 3"
        arcade.draw_text(
            mcomp_name_text,
            10,
            115,
            arcade.csscolor.RED,
            20,
            bold=True
        )
        
        mcomp_phase_text = f"Phase: {self.player_list[2].phase}    Score: {self.player_list[2].score}"
        arcade.draw_text(
            mcomp_phase_text,
            10,
            90,
            arcade.csscolor.BLACK,
            15
        )

        rcomp_name_text = f"Player: 4"
        arcade.draw_text(
            rcomp_name_text,
            10,
            40,
            arcade.csscolor.YELLOW,
            20,
            bold=True
        )

        rcomp_phase_text = f"Phase: {self.player_list[3].phase}    Score: {self.player_list[3].score}"
        arcade.draw_text(
            rcomp_phase_text,
            10,
            15,
            arcade.csscolor.BLACK,
            15
        )


    def pull_to_top(self, card: arcade.Sprite):
        """ Pull card to top of rendering order (last to render, looks on-top) """

        # Remove, and append to the end
        self.card_list.remove(card)
        self.card_list.append(card)


    def get_instructions(self):
        """Opens web browser and directs to a web page with detailed instructions"""
        info_url = "https://www.instructables.com/How-to-Play-Phase-10/"
        webbrowser.open(info_url)
    

    def on_key_press(self, symbol: int, modifiers: int):
        """ User presses key """
        # if symbol == arcade.key.R:
        #     # Restart
        #     self.setup()

        if symbol == arcade.key.SPACE:
            self.get_instructions()


    def on_mouse_press(self, x, y, button, key_modifiers):
        """ Called when the user presses a mouse button. """

        # Get list of cards we've clicked on
        cards = arcade.get_sprites_at_point((x, y), self.card_list)

        # Have we clicked on a card?
        if len(cards) > 0:

            # Figure out what pile the card is in
            pile_index = self.get_pile_for_card(cards[-1])

            # Figure out index of player whose turn it is
            n = self.get_turn()

            # draw card from the main deck
            if pile_index == DECK_FACE_DOWN_PILE:
                if self.player_list[n].draw_card:
                    self.player_list[n].draw_card_from_deck(self.piles, self.pile_mat_list, DECK_FACE_DOWN_PILE, self.player_list[n].hand)
                    self.sort_pile(self.player_list[n].hand)

                else:
                    pass

            # take previously discarded card instead of drawing from deck
            elif pile_index == DISCARD_PILE:
                card = self.piles[DISCARD_PILE][-1]
                if self.player_list[n].draw_card and card.get_value() != "13":
                    self.player_list[n].draw_card_from_deck(self.piles, self.pile_mat_list, DISCARD_PILE, self.player_list[n].hand)
                    self.sort_pile(self.player_list[n].hand)

                else:
                    pass

            ### remove ability to click on other hands if not their turn
            elif USER_HAND_PILE <= pile_index <= RCOMP_HAND_PILE and pile_index != self.player_list[n].hand:
                pass

            
            # When clicking on a phase pile
            elif PHASE_PILE_1 <= pile_index <= LAST_PHASE_PILE:
                if self.player_list[n].phase in PHASE_1_MATS:
                    # if current players phase pile
                    if pile_index == self.player_list[n].last_pile:
                        # If current player has not completed their phase
                        if self.player_list[n].complete == False:
                            # grab the face-up card we are clicking on
                            self.held_cards = [cards[-1]]
                            # Save the position
                            self.held_cards_original_position = [self.held_cards[0].position]
                        # if phase already complete, cards get locked in
                        else:
                            pass
                    else:
                        pass

                elif self.player_list[n].phase in PHASE_2_MATS:
                    # If current player is User
                    if n == 0:
                        # if user turn and not clicking on user phase piles
                        if pile_index == (self.player_list[n].last_pile - 1) or pile_index == self.player_list[n].last_pile:
                            if self.player_list[n].complete == False:
                                # grab the face-up card we are clicking on
                                self.held_cards = [cards[-1]]
                                # Save the position
                                self.held_cards_original_position = [self.held_cards[0].position]
                            # if phase already complete, cards get locked in
                            else:
                                pass
                        else:
                            pass
                    
                    # If current player is not User
                    else:
                        if pile_index == self.player_list[n - 1].last_pile + 1 or pile_index == self.player_list[n - 1].last_pile + 2:
                            if self.player_list[n].complete == False:
                                # grab the face-up card we are clicking on
                                self.held_cards = [cards[-1]]
                                # Save the position
                                self.held_cards_original_position = [self.held_cards[0].position]
                            # if phase complete, cards are locked in
                            else:
                                pass
                        else:
                            pass
            
            else:
                # All other cases, grab the face-up card we are clicking on
                self.held_cards = [cards[-1]]   ### maybe add, if self.held_cards is 'skip' highlight hand piles
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
                    temp_list = self.piles[DISCARD_PILE].copy()
                    for card in reversed(temp_list):
                        card.face_down()
                        self.piles[DISCARD_PILE].remove(card)
                        self.piles[DECK_FACE_DOWN_PILE].append(card)
                        card.position = self.pile_mat_list[DECK_FACE_DOWN_PILE].position
                    # flip over top card
                    card = self.piles[DECK_FACE_DOWN_PILE].pop()
                    card.face_up()
                    self.piles[DISCARD_PILE].append(card)
                    card.position = self.pile_mat_list[DISCARD_PILE].position                    

    
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
            if card in pile and pile == self.piles[DISCARD_PILE]:
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
        if pile_index != DISCARD_PILE:
            self.sort_pile(pile_index)
    
    def get_turn(self):
        """returns index of the player whose turn it is"""
        for index, player in enumerate(self.player_list):
            if player.turn == True:
                return index

    def get_player_for_phase_pile(self, pile_list, pile_index):
        """Returns the index of the player whose phase piles are being played on.
        Finds the 'owner' of the given phase pile."""
        self.pile_list = pile_list
        self.pile_index = pile_index
        for index, player in enumerate(self.player_list):
            if player.phase_pile == self.pile_list[pile_index]:
                return index
            elif player.phase_pile_b == self.pile_list[pile_index]:
                return index

    def end_turn(self, index):
        """Ends players turn, finds next player and flips over appropriate cards """
        self.index = index
        self.player_list[self.index].turn = False
        for card in self.piles[self.player_list[self.index].hand]:
            card.face_down()
        if self.index < 3:
            new_index = self.index + 1
        else:
            new_index = self.index - 3
        while True:
            if self.player_list[new_index].skipped == False:
                self.player_list[new_index].turn = True
                self.player_list[new_index].draw_card = True
                for card in self.piles[self.player_list[new_index].hand]:
                    card.face_up()
                break

            elif self.player_list[new_index].skipped == True:
                self.player_list[new_index].skipped = False
                if new_index < 3:
                    new_index += 1
                else:
                    new_index -= 3
                continue
        self.round_over()


    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        """ Called when the user presses a mouse button. """

        # If we don't have any cards, who cares
        if len(self.held_cards) == 0:
            return

        # Find the closest pile, in case we are in contact with more than one
        pile, distance = arcade.get_closest_sprite(self.held_cards[0], self.pile_mat_list)
        reset_position = True
        draw_pile = False

        # See if we are in contact with the closest pile
        if arcade.check_for_collision(self.held_cards[0], pile):

            # What pile is it?
            pile_index = self.pile_mat_list.index(pile)

            # Get index of the Player whose turn it is
            n = self.get_turn()

            # Get index of the Player for a given phase phase pile (which player's phase pile it is)
            p = self.get_player_for_phase_pile(self.piles, pile_index)

            #  Is it the same pile we came from?
            if pile_index == self.get_pile_for_card(self.held_cards[0]):
                # If so, who cares. We'll just reset our position.
                pass

            # If User hand 
            elif pile_index == USER_HAND_PILE:
                # If another player, other than user is dropping card
                if self.player_list[0].turn == False:
                    # Check if current player has drawn a card yet
                    if self.player_list[n].draw_card == False:
                        for dropped_card in self.held_cards:
                            # If card is a skip, skip user
                            if dropped_card.get_value() == "13":
                                self.player_list[0].skipped = True
                                if len(self.piles[DISCARD_PILE]) > 0:
                                    top_card = self.piles[DISCARD_PILE][-1]
                                    dropped_card.position = top_card.position
                                    self.move_card_to_new_pile(dropped_card, DISCARD_PILE)
                                    self.discard()
                                    self.sort_phase_pile()
                                    self.end_turn(n)
                                else:
                                    dropped_card.position = self.pile_mat_list[DISCARD_PILE].position
                                    self.move_card_to_new_pile(dropped_card, DISCARD_PILE)
                                    self.discard()
                                    self.sort_phase_pile()
                                    self.end_turn(n)
                            else:
                                draw_pile = True
                    else:
                        draw_pile = True
                # If the user is returning cards to their hand from their phase piles
                else:
                    if self.get_pile_for_card(self.held_cards[0]) == (self.player_list[0].last_pile -1) or self.get_pile_for_card(self.held_cards[0]) == self.player_list[0].last_pile:
                        for card in self.held_cards:
                            self.move_card_to_new_pile(card, pile_index)
                            self.sort_phase_pile()
                    
                    else:
                        draw_pile = True
                # reset card position if move was invalid
                reset_position = draw_pile

            # If Left comp hand
            elif pile_index == LCOMP_HAND_PILE:
                # If another player, other than Left comp, is dropping card.
                if self.player_list[1].turn == False:
                    # Check if current player has drawn a card yet
                    if self.player_list[n].draw_card == False:
                        for dropped_card in self.held_cards:
                            # If card is a skip, skip left comp
                            if dropped_card.get_value() == "13":
                                self.player_list[1].skipped = True
                                if len(self.piles[DISCARD_PILE]) > 0:
                                    top_card = self.piles[DISCARD_PILE][-1]
                                    dropped_card.position = top_card.position
                                    self.move_card_to_new_pile(dropped_card, DISCARD_PILE)
                                    self.discard()
                                    self.sort_phase_pile()
                                    self.end_turn(n)
                                else:
                                    dropped_card.position = self.pile_mat_list[DISCARD_PILE].position
                                    self.move_card_to_new_pile(dropped_card, DISCARD_PILE)
                                    self.discard()
                                    self.sort_phase_pile()
                                    self.end_turn(n)
                            else:
                                draw_pile = True
                    else:
                        draw_pile = True
                # If Left comp player is returning cards to their hand from their phase piles
                else:
                    if self.get_pile_for_card(self.held_cards[0]) == (self.player_list[0].last_pile + 1) or self.get_pile_for_card(self.held_cards[0]) == (self.player_list[0].last_pile + 2):
                        for card in self.held_cards:
                            self.move_card_to_new_pile(card, pile_index)
                            self.sort_phase_pile()

                    else:
                        draw_pile = True

                # reset card position if move was invalid
                reset_position = draw_pile

            # If Mid comp hand
            elif pile_index == MCOMP_HAND_PILE:
                # If another player, other than Mid comp, is dropping card.
                if self.player_list[2].turn == False:
                    # Check if current player has drawn a card yet
                    if self.player_list[n].draw_card == False:
                        for dropped_card in self.held_cards:
                            # If card is a skip, skip mid comp
                            if dropped_card.get_value() == "13":
                                self.player_list[2].skipped = True
                                if len(self.piles[DISCARD_PILE]) > 0:
                                    top_card = self.piles[DISCARD_PILE][-1]
                                    dropped_card.position = top_card.position
                                    self.move_card_to_new_pile(dropped_card, DISCARD_PILE)
                                    self.discard()
                                    self.sort_phase_pile()
                                    self.end_turn(n)
                                else:
                                    dropped_card.position = self.pile_mat_list[DISCARD_PILE].position
                                    self.move_card_to_new_pile(dropped_card, DISCARD_PILE)
                                    self.discard()
                                    self.sort_phase_pile()
                                    self.end_turn(n)
                            else:
                                draw_pile = True
                    else:
                        draw_pile = True
                # If Mid comp player is returning cards to their hand from their phase piles
                else:
                    if self.get_pile_for_card(self.held_cards[0]) == (self.player_list[1].last_pile + 1) or self.get_pile_for_card(self.held_cards[0]) == (self.player_list[1].last_pile + 2):
                        for card in self.held_cards:
                            self.move_card_to_new_pile(card, pile_index)
                            self.sort_phase_pile()

                    else:
                        draw_pile = True

                # reset card position if move was invalid
                reset_position = draw_pile
                    
            # If Right comp hand
            elif pile_index == RCOMP_HAND_PILE:
                # If another player, other than Right comp, is dropping card.
                if self.player_list[3].turn == False:
                    # Check if current player has drawn a card yet
                    if self.player_list[n].draw_card == False:
                        for dropped_card in self.held_cards:
                            # If card is a skip, skip right comp
                            if dropped_card.get_value() == "13":
                                self.player_list[3].skipped = True
                                if len(self.piles[DISCARD_PILE]) > 0:
                                    top_card = self.piles[DISCARD_PILE][-1]
                                    dropped_card.position = top_card.position
                                    self.move_card_to_new_pile(dropped_card, DISCARD_PILE)
                                    self.discard()
                                    self.sort_phase_pile()
                                    self.end_turn(n)
                                else:
                                    dropped_card.position = self.pile_mat_list[DISCARD_PILE].position
                                    self.move_card_to_new_pile(dropped_card, DISCARD_PILE)
                                    self.discard()
                                    self.sort_phase_pile()
                                    self.end_turn(n)
                            else:
                                draw_pile = True
                    else:
                        draw_pile = True
                # If Right comp player is returning cards to their hand from their phase piles
                else:
                    if self.get_pile_for_card(self.held_cards[0]) == (self.player_list[2].last_pile + 1) or self.get_pile_for_card(self.held_cards[0]) == (self.player_list[2].last_pile + 2):
                        for card in self.held_cards:
                            self.move_card_to_new_pile(card, pile_index)
                            self.sort_phase_pile()

                    else:
                        draw_pile = True

                # reset card position if move was invalid
                reset_position = draw_pile



            # Release on phase pile
            elif PHASE_PILE_1 <= pile_index <= LAST_PHASE_PILE:
                # check if current player has 1 or 2 phase piles
                if self.player_list[n].phase in PHASE_1_MATS:
                    # if players own phase pile
                    if pile_index == self.player_list[n].last_pile:
                        # check if you are "hitting" or adding to your own phase pile after you have already completed phase on a previous turn
                        if self.player_list[n].complete:
                            self.hit_on_phase(pile, pile_index)
                            # self.sort_pile(self.player_list[n].hand)

                        #if not complete add any card
                        else:
                            self.play_on_phase(pile, pile_index)
                            self.round_over()
                            
                    # if not players own phase pile
                    else:
                        # if other player phase pile has cards -- (meaning other player phase is complete)
                        if len(self.piles[pile_index]) > 0:
                            # is current player phase complete in order it "hit" on other players phase piles
                            if self.player_list[n].phase_complete():
                                self.player_list[n].complete = True
                                self.sort_phase_pile()
                            
                            if self.player_list[n].complete:
                                self.hit_on_phase(pile, pile_index)
                                if self.player_list[p].phase in PHASE_2_MATS:
                                    if len(self.piles[pile_index]) > 5:
                                        self.compress_cards(pile, pile_index)
                                    # if len(self.player_list[p].phase_pile_b) > 5:
                                    #     self.compress_cards(self.pile_sprite, pile_index)
                                # no need to sort if one big phase pile
                                else:
                                    pass
                                # self.sort_pile(self.player_list[n].hand)

                            # if not complete, return card
                            else:
                                draw_pile = True
                        # if other player phase pile is empty, can't place there.
                        else:
                            draw_pile = True

                # if 2 phase piles
                else:
                    # if current player is user
                    if n == 0:
                        # if dropping on own phase piles
                        if pile_index == (self.player_list[n].last_pile - 1) or pile_index == self.player_list[n].last_pile:
                            # check if you are "hitting"
                            if self.player_list[n].complete:
                                self.hit_on_phase(pile, pile_index)
                                if len(self.piles[pile_index]) > 5:
                                    self.compress_cards(pile, pile_index)
                                # if len(self.player_list[p].phase_pile_b) > 5:
                                #     self.compress_cards(self.pile_sprite, pile_index)
                                # self.sort_pile(self.player_list[n].hand)

                            # if not complete add any card
                            else:
                                self.play_on_phase(pile, pile_index)
                                if len(self.piles[pile_index]) > 5:
                                    self.compress_cards(pile, pile_index)
                                self.round_over()

                        # if not dropping on own piles
                        else:
                             # if other player phase pile has cards
                            if len(self.piles[pile_index]) > 0:
                                # current player needs phase complete in order to "hit" on other players phase piles
                                # Check if current player phase is complete
                                if self.player_list[n].phase_complete():
                                    self.player_list[n].complete = True
                                    self.sort_phase_pile()

                                # If phase is complete, "hit" on other players phase pile
                                if self.player_list[n].complete:
                                    self.hit_on_phase(pile, pile_index)
                                    if self.player_list[p].phase in PHASE_2_MATS:
                                        if len(self.piles[pile_index]) > 5:
                                            self.compress_cards(pile, pile_index)
                                    else:
                                        pass
                                    # self.sort_pile(self.player_list[n].hand)

                                # if not complete, return card 
                                else:
                                    draw_pile = True

                            # if other player phase pile is empty - their phase pile can't be played on
                            else:
                                draw_pile = True

                    # if current player not user
                    else:
                        # if dropping on own phase piles
                        if pile_index == self.player_list[n - 1].last_pile + 1 or pile_index == self.player_list[n - 1].last_pile + 2:
                            # check if you are "hitting"
                            if self.player_list[n].complete:
                                self.hit_on_phase(pile, pile_index)
                                if len(self.piles[pile_index]) > 5:
                                    self.compress_cards(pile, pile_index)
                                # self.sort_pile(self.player_list[n].hand)

                            # if not complete add any card
                            else:
                                self.play_on_phase(pile, pile_index)
                                if len(self.piles[pile_index]) > 5:
                                    self.compress_cards(pile, pile_index)
                                self.round_over()

                        # if not dropping on own piles
                        else:
                            # if other player phase pile has cards
                            if len(self.piles[pile_index]) > 0:
                                # is current player phase complete in order it "hit" on other players phase piles
                                if self.player_list[n].phase_complete():
                                    self.player_list[n].complete = True
                                    self.sort_phase_pile()
                                    

                                if self.player_list[n].complete:
                                    self.hit_on_phase(pile, pile_index)
                                    if self.player_list[p].phase in PHASE_2_MATS:
                                        if len(self.piles[pile_index]) > 5:
                                            self.compress_cards(pile, pile_index)
                                    # self.sort_pile(self.player_list[n].hand)

                                # if not complete, return card 
                                else:
                                    draw_pile = True

                            # if other player phase pile is empty - their phase pile can't be played on
                            else:
                                draw_pile = True

                # reset card position if move was invalid
                reset_position = draw_pile


            # Release on discard pile
            elif pile_index == DISCARD_PILE:
                if self.player_list[n].draw_card == False:
                    if len(self.piles[pile_index]) > 0:
                        top_card = self.piles[pile_index][-1]
                        for dropped_card in self.held_cards:
                            # dropped_card.face_up()
                            dropped_card.position = top_card.position
                    else:
                        for dropped_card in self.held_cards:
                            # dropped_card.face_up()
                            dropped_card.position = pile.position
                    # self.pull_to_top(self.held_cards[-1])
                    for card in self.held_cards:
                        self.move_card_to_new_pile(card, pile_index)

                    self.discard()
                    self.sort_phase_pile()
                    # self.sort_pile(self.player_list[n].hand)
                    self.end_turn(n)

                else:
                    draw_pile = True
                # reset card position if move was invalid
                reset_position = draw_pile

        if reset_position:
            # Where-ever we were dropped, it wasn't valid. Reset the each card's position
            # to its original spot.
            for pile_index, card in enumerate(self.held_cards):
                card.position = self.held_cards_original_position[pile_index]

        # We are no longer holding cards
        self.held_cards = []
    

    def compress_cards(self, pile_sprite, pile_index):
        """Make cards smaller to fit with small phase piles."""
        self.pile_sprite = pile_sprite
        self.pile_index = pile_index
        i = 0
        first_card = self.piles[self.pile_index][0]
        next_card = self.piles[self.pile_index][i]
        
        for card in self.piles[self.pile_index]:
            card.width = CARD_WIDTH * CARD_SCALE
            if card == first_card:
                card.position = self.pile_sprite.center_x - (CARD_HORIZONTAL_OFFSET * 5) / 2, \
                                self.pile_sprite.center_y
                i += 1
            else:
                card.position = first_card.center_x + i * (CARD_HORIZONTAL_OFFSET * CARD_SCALE),\
                                    next_card.center_y
                i += 1


    def play_on_phase(self, pile_sprite, pile_index):
        """Add cards to phase pile"""
        self.pile_sprite = pile_sprite
        self.pile_index = pile_index
        if len(self.piles[self.pile_index]) > 0: # add hitting method/check for comp phases? or if user.complete = True
            # Move cards to proper position
            top_card = self.piles[self.pile_index][-1]
            for dropped_card in self.held_cards:
                dropped_card.position = top_card.center_x + CARD_HORIZONTAL_OFFSET, \
                                            top_card.center_y

        else:
            # Are there no cards in the phase pile?
            for dropped_card in self.held_cards:
                # Move cards to proper position
                # If 1 phase pile
                if self.pile_sprite.width == PHASE_1_MAT_WIDTH:
                    dropped_card.position = self.pile_sprite.center_x - (CARD_HORIZONTAL_OFFSET * 9) / 2, \
                                        self.pile_sprite.center_y
                # If 2 phase piles
                else:
                    dropped_card.position = self.pile_sprite.center_x - (CARD_HORIZONTAL_OFFSET * 4) / 2, \
                                            self.pile_sprite.center_y

        # Move card to card list
        for card in self.held_cards:
            self.move_card_to_new_pile(card, self.pile_index)

    def hit_on_phase(self, pile_sprite, pile_index):
        """"play cards on a phase pile that has already been completed previously"""
        self.pile_sprite = pile_sprite
        self.pile_index = pile_index
        n = self.get_turn()
        p = self.get_player_for_phase_pile(self.piles, self.pile_index)
        if self.player_list[n].draw_card == False:
            for card in self.held_cards:
                self.piles[self.pile_index].append(card)
                self.sort_pile(self.pile_index)
                if self.player_list[p].phase_complete():
                    self.move_card_to_new_pile(card, self.pile_index)
                    self.round_over()

                else:
                    self.piles[self.pile_index].remove(card)
                    for pile_index, card in enumerate(self.held_cards):
                        card.position = self.held_cards_original_position[pile_index]
        else:
            for pile_index, card in enumerate(self.held_cards):
                card.position = self.held_cards_original_position[pile_index]
            


    def sort_phase_pile(self):
        """finds the correct indexes of the players' phase piles and sorts them"""
        n = self.get_turn()
        if self.player_list[n].phase in PHASE_1_MATS:
                self.sort_pile(self.player_list[n].last_pile)
        elif self.player_list[n].phase in PHASE_2_MATS:
            if n == 0:
                self.sort_pile(self.player_list[n].last_pile - 1)
                self.sort_pile(self.player_list[n].last_pile)
                if len(self.player_list[n].phase_pile) > 5:
                    self.compress_cards(self.pile_mat_list[(self.player_list[n].last_pile -1)], (self.player_list[n].last_pile -1))
                if len(self.player_list[n].phase_pile_b) > 5:
                    self.compress_cards(self.pile_mat_list[(self.player_list[n].last_pile)], (self.player_list[n].last_pile))
            else:
                self.sort_pile(self.player_list[n - 1].last_pile + 1)
                self.sort_pile(self.player_list[n - 1].last_pile + 2)
                if len(self.player_list[n].phase_pile) > 5:
                    self.compress_cards(self.pile_mat_list[(self.player_list[n - 1].last_pile + 1)], (self.player_list[n - 1].last_pile + 1))
                if len(self.player_list[n].phase_pile_b) > 5:
                    self.compress_cards(self.pile_mat_list[(self.player_list[n - 1].last_pile + 2)], (self.player_list[n - 1].last_pile + 2))


    def discard(self):
        """checks to see if there are invalid cards in phase pile when discarding, and return cards if invalid"""
        n = self.get_turn()
        if self.player_list[n].draw_card == False:
            if self.player_list[n].phase in PHASE_1_MATS:
                if len(self.player_list[n].phase_pile) > 0:
                    if self.player_list[n].phase_complete():
                        self.player_list[n].complete = True

                    else:
                        if self.player_list[n].complete == False:
                            if n == 0:
                                for card in self.piles[self.player_list[n].last_pile][:]:
                                    self.move_card_to_new_pile(card, self.player_list[n].hand)
                            else:
                                for card in self.piles[self.player_list[n - 1].last_pile + 1][:]:
                                    self.move_card_to_new_pile(card, self.player_list[n].hand)
                        else:
                            for pile_index, card in enumerate(self.held_cards):
                                card.position = self.held_cards_original_position[pile_index]
                else:
                    pass

            elif self.player_list[n].phase in PHASE_2_MATS:
                if len(self.player_list[n].phase_pile) > 0 or len(self.player_list[n].phase_pile_b) > 0:
                    if self.player_list[n].phase_complete():
                        self.player_list[n].complete = True 

                    else:
                        if self.player_list[n].complete == False:
                            if n == 0:
                                for card in self.piles[self.player_list[n].last_pile - 1][:]:
                                    self.move_card_to_new_pile(card, self.player_list[n].hand)
                                for card in self.piles[self.player_list[n].last_pile][:]:
                                    self.move_card_to_new_pile(card, self.player_list[n].hand)
                            else:
                                for card in self.piles[self.player_list[n - 1].last_pile + 1][:]:
                                    self.move_card_to_new_pile(card, self.player_list[n].hand)
                                for card in self.piles[self.player_list[n - 1].last_pile + 2][:]:
                                    self.move_card_to_new_pile(card, self.player_list[n].hand)
                        else:
                            for pile_index, card in enumerate(self.held_cards):
                                card.position = self.held_cards_original_position[pile_index]
                                
                else:
                    pass
        else:
            for pile_index, card in enumerate(self.held_cards):
                card.position = self.held_cards_original_position[pile_index]
    
    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """ User moves mouse """

        # If we are holding cards, move them with the mouse
        for card in self.held_cards:
            card.center_x += dx
            card.center_y += dy
    
    def round_over(self):
        """check to see if the round is over or if someone has won."""
        for pile_no in range(USER_HAND_PILE, RCOMP_HAND_PILE + 1):
            if len(self.piles[pile_no]) == 0:
                self.discard()
                if len(self.piles[pile_no]) == 0:
                    for player in self.player_list:
                        player.add_score(self.piles)
                        if player.complete:
                            player.phase += 1
                    for player in self.player_list:
                        if player.phase <= 10:
                            player.complete = False
                        else:
                            self.keep_playing = False
                            self.game_over = True
                            win_list = []
                            if player.phase == 11:
                                win_list.append(player)
                            score_dict = {player: player.score for player in win_list}
                            score_list = (sorted(score_dict.items(), key= lambda item: item[1]))
                            self.winner = score_list[0][0]
                    if self.keep_playing == True:
                        self.setup() # -- add flag for a key press to move to next round
                        self.on_draw()
            else:
                pass


def main():
    """ Main function """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()