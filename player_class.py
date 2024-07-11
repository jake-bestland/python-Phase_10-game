import arcade
from Phase_10_constants import PHASE_1_MATS, PHASE_2_MATS, PHASE_PILE_1, PHASE_PILE_2, CARD_HORIZONTAL_OFFSET, DECK_FACE_DOWN_PILE


# add hand param. then in phase complete method, if false return cards to hand?
class Player:
    def __init__(self, name, hand, phase=1, turn=False, score=0):  
        self.name = name
        # self.player_number = player_number
        self.phase = phase
        self.hand = hand
        self.turn = turn
        self.score = score
        self.phase_pile = None
        self.phase_pile_b = None
        self.last_pile = None
        self.skipped = False
        self.draw_card = True
        self.complete = False

    def draw_card_from_deck(self, pile_list, pile_mat_list, deck_index, hand):
        self.pile_list = pile_list
        self.pile_mat_list = pile_mat_list
        self.deck_index = deck_index
        self.hand = hand

        card = self.pile_list[self.deck_index][-1]
        card.face_up()
        card.position = pile_mat_list[self.hand].position
        self.pile_list[self.deck_index].remove(card)
        self.pile_list[self.hand].append(card)
        self.draw_card = False

    # def discard(self, pile_list, hand):
    #     self.pile_list = pile_list
    #     self.hand = hand
    #     if self.phase in PHASE_1_MATS:
    #         if len(self.phase_pile) > 0:
    #             if self.phase_complete():
    #                 self.complete = True
    #                 self.sort_pile(self.phase_pile)
    #             else:
    #                 for card in self.pile_list[self.phase_pile][:]:
    #                     self.move_card_to_new_pile(card, self.hand)
    #                     self.sort_pile(self.hand)
    #         else:
    #             pass

    #     elif self.phase in PHASE_2_MATS:
    #         if len(self.phase_pile) > 0 or len(self.phase_pile_b) > 0:
    #             if self.phase_complete():
    #                 self.complete = True
    #                 self.sort_pile(self.phase_pile)
    #                 self.sort_pile(self.phase_pile_b)
    #             else:
    #                 for card in self.piles[self.phase_pile][:]:
    #                     self.move_card_to_new_pile(card, self.hand)
    #                 for card in self.piles[self.phase_pile_b][:]:
    #                     self.move_card_to_new_pile(card, self.hand)
    #                 self.sort_pile(self.hand)
    #         else:
    #             pass

    def determine_phase_piles(self, pile_list, last_pile=5):
        self.pile_list = pile_list
        self.last_pile = last_pile
        if self.name == "user":
            if self.phase in PHASE_1_MATS:
                self.phase_pile = self.pile_list[PHASE_PILE_1]
                self.last_pile = PHASE_PILE_1
            elif self.phase in PHASE_2_MATS:
                self.phase_pile = self.pile_list[PHASE_PILE_1]
                self.phase_pile_b = self.pile_list[PHASE_PILE_2]
                self.last_pile = PHASE_PILE_2

        elif self.name == "lcomp":
            if self.phase in PHASE_1_MATS:
                self.phase_pile = self.pile_list[self.last_pile + 1]
                self.last_pile = self.last_pile + 1
            elif self.phase in PHASE_2_MATS:
                self.phase_pile = self.pile_list[self.last_pile + 1]
                self.phase_pile_b = self.pile_list[self.last_pile + 2]
                self.last_pile = self.last_pile + 2

        elif self.name == "mcomp":
            if self.phase in PHASE_1_MATS:
                self.phase_pile = self.pile_list[self.last_pile + 1]
                self.last_pile = self.last_pile + 1
            elif self.phase in PHASE_2_MATS:
                self.phase_pile = self.pile_list[self.last_pile + 1]
                self.phase_pile_b = self.pile_list[self.last_pile + 2] 
                self.last_pile = self.last_pile + 2

        elif self.name == "rcomp":
            if self.phase in PHASE_1_MATS:
                self.phase_pile = self.pile_list[self.last_pile + 1]
            elif self.phase in PHASE_2_MATS:
                self.phase_pile = self.pile_list[self.last_pile + 1]
                self.phase_pile_b = self.pile_list[self.last_pile + 2]    

    def check_set(self, amount, pile):
        """check to see if cards in phase pile meets the phase requirement for a set.
        amount = number of cards with same value needed to complete phase
        pile = the list of cards in the phase pile being checked
        returns bool"""
        self.amount = amount
        self.pile = pile
        # create an empty result list for acceptable cards and bad list for invalid cards
        res = []
        bad = []
        # if there are no cards
        if len(self.pile) > 0:
            # assign first card in pile to variable to check value against
            card_1 = self.pile[0]
            for card in self.pile:
                if card.get_value() == card_1.get_value():
                    res.append(card)
                elif card.get_value() == "12":
                    res.append(card)
                else:
                    bad.append(card)
        else:
            return False    
        return len(res) >= self.amount and len(bad) == 0

    def check_color(self, amount, pile):
        """ checks to see if all cards in pile has same color. returns bool.  """
        self.amount = amount
        self.pile = pile
        # create an empty result list for acceptable cards and bad list for invalid cards
        res = []
        bad = []
        if len(self.pile) > 0:
            # assign first card in pile to variable to check color against
            card_1 = self.pile[0]
            for card in self.pile:
                if card.get_value() == "12":
                    res.append(card)
                if card.get_color() == card_1.get_color():
                    res.append(card)
                else:
                    bad.append(card)
        else:
            return False
        return len(res) >= self.amount and len(bad) == 0

    def check_run(self, amount, pile):
        self.amount = amount
        self.pile = pile
        # create an empty result list for acceptable cards and bad list for invalid cards
        res = []
        bad = []
        # list to put wild cards in
        wild = []
        # list of the numbered cards (non-wild/skip cards)
        num = []
        if len(self.pile) > 0:
            # sort cards into appropriate list
            # skip cards to bad list, wild cards into wild list, and numbered cards into num list
            for card in self.pile:
                if card.get_value() == "13":
                    bad.append(card)
                elif card.get_value() == "12":
                    wild.append(card)
                else:
                    num.append(card)
        else:
            return False
        # itereate over numbered cards and start forming run of cards
        for card in num:
            if len(res) > 0:
                # check if the second card is one number higher than first
                prev_card = res[-1]
                if int(card.get_value()) == (int(prev_card.get_value()) + 1):
                    res.append(card)
                # check if cards are the same number, which is not valid for a run
                elif int(card.get_value()) == int(prev_card.get_value()):
                    bad.append(card)
                # if the next card does not come next in the run, check is a wild card(s) can be used as next card in run.
                elif len(wild) >= (int(card.get_value()) - int(prev_card.get_value())) - 1:
                    # loop for number of wild cards that are being used iin between numbered cards.
                    for i in range((int(card.get_value()) - int(prev_card.get_value())) - 1):
                        new_card = wild.pop()
                        # change value of the wild card to the number it is being used as in the run.
                        new_card.change_value(int(prev_card.get_value()) + 1)
                        res.append(new_card)
                        # set prev_card to the wild card
                        prev_card = new_card
                    res.append(card)
                else:
                    bad.append(card)
            # add first card to list
            else:
                res.append(card)

        # add remaining wild cards to end of the run
        while len(wild) > 0:
            prev_card = res[-1]
            new_card = wild.pop()
            # check if last card is 12, or the highest card
            if int(prev_card.get_value()) < 11:
                new_card.change_value(int(prev_card.get_value()) + 1)
                res.append(new_card)
            # if last card is 12, add wild to the beginning of the run
            else:
                start_card = res[0]
                new_card.change_value(int(start_card.get_value()) - 1)
                print(new_card.get_value())
                res.insert(0, new_card)

        # check if there are enough valid cards to complete the run and no invalid cards
        if len(res) >= self.amount and len(bad) == 0:
            # hit_on_run = True  --for future 'hitting' func
            return True
        else:
            #change value of wild cards back to original
            for card in self.pile:
                if card.image_file_name == "./images/black_cards/black13.png":
                    card.change_value("13")
            return False

    def phase_complete(self):
        if self.phase == 1:
            return (self.check_set(3, self.phase_pile_b) and self.check_set(3, self.phase_pile))

        elif self.phase == 2:
            return (self.check_set(3, self.phase_pile) and self.check_run(4, self.phase_pile_b))\
                or (self.check_set(3, self.phase_pile_b) and self.check_run(4, self.phase_pile))

        elif self.phase == 3:
            return (self.check_set(4, self.phase_pile) and self.check_run(4, self.phase_pile_b))\
                or (self.check_set(4, self.phase_pile_b) and self.check_run(4, self.phase_pile))

        elif self.phase == 4:
            return self.check_run(7, self.phase_pile)

        elif self.phase == 5:
            return self.check_run(8, self.phase_pile)

        elif self.phase == 6:
            return self.check_run(9, self.phase_pile)

        elif self.phase == 7:
            return self.check_set(4, self.phase_pile_b) and self.check_set(4, self.phase_pile)

        elif self.phase == 8:
            return self.check_color(7, self.phase_pile)

        elif self.phase == 9:
            return (self.check_set(5, self.phase_pile) and self.check_set(2, self.phase_pile_b))\
                or (self.check_set(5, self.phase_pile_b) and self.check_set(2, self.phase_pile))

        elif self.phase == 10:
            return (self.check_set(5, self.phase_pile) and self.check_set(3, self.phase_pile_b))\
                or (self.check_set(5, self.phase_pile_b) and self.check_set(3, self.phase_pile))

    # def end_turn(self, pile_list, n):
    #     self.pile_list = pile_list
    #     self.n = n
    #     # self.player_list = player_list
        
    #     self.turn = False
    #     for card in self.pile_list[self.hand]:
    #         card.face_down()
    #     if n < 3:
    #         self.n = self.n + 1
    #     else:
    #         self.n = self.n - 3
    #     print(self.name)
    #     self.turn = True
    #     self.draw_card = True
    #     for card in self.pile_list[self.hand]:
    #         card.face_up()

            
        
        


    def add_score(self, hand):
        """at end of round, add the point total for each card remaining in hand to total score."""
        self.hand = hand
        if len(self.hand) > 0:
            for card in self.hand:
                if int(card.get_value()) in range(0, 9):
                    self.score += 5
                elif int(card.get_value()) in range(9, 12):
                    self.score += 10
                elif card.get_value() == "13":
                    self.score += 15
                else:
                    self.score += 25
        else:
            pass
        print(self.score)

### use this class to create computter AI methods
class Comp(Player):
    def __init__(self, name, turn, phase=1, phase_complete=False, score=0):
        super().__init__(name, turn, phase, phase_complete, score)

    ##add methods for what to do on comp turn.

# if __name__ == "__main__":
#     pass