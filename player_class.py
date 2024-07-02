import arcade
from Phase_10_constants import PHASE_1_MATS, PHASE_2_MATS, PHASE_PILE_1, PHASE_PILE_2, CARD_HORIZONTAL_OFFSET


# add hand param. then in phase complete method, if false return cards to hand?
class Player:
    def __init__(self, name, turn=False, phase=1, score=0):  
        self.name = name
        self.turn = turn
        self.phase = phase
        self.score = score
        self.phase_pile = None
        self.phase_pile_b = None
        self.last_pile = None
        self.draw_card = True
        self.complete = False

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
        # get first card value other than wild or skip
        # while True:
        #     n = 0
        #     card_1 = self.pile[n]
        #     if card_1.get_color() == 4:   ## change to card_1 == Card("black", "wild", CARD_SCALE) or card_1 == Card("black", "skip", CARD_SCALE)
        #         n += 1
        #     else:
        #         break
        # create an empty result list for acceptable cards and bad list for invalid cards
        res = []
        bad = []
        card_1 = self.pile[0]
        for card in self.pile:
            if card.get_value() == card_1.get_value():
                res.append(card)
            elif card.get_value() == "12":
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

    def check_color(self, amount, pile):
        """ checks to see if all cards in pile has same color. returns bool.  """
        self.amount = amount
        self.pile = pile
        # get first card color, other than wild or skip
        # while True:
        #     n = 0
        #     card_1 = self.pile[n]
        #     if card_1.get_color() == "4":
        #         n += 1
        #     else:
        #         break
        # create an empty result list for acceptable cards and bad list for invalid cards
        res = []
        bad = []
        card_1 = self.pile[0]
        for card in self.pile:
            if card.get_value() == "12":
                res.append(card)
            if card.get_color() == card_1.get_color():
                res.append(card)
            else:
                bad.append(card)
        return len(res) >= self.amount and len(bad) == 0
        # if len(res) >= self.amount and len(bad) == 0:
        #     # self.complete = True   ### maybe change to a phase check = True (from a phase check func?)
        #     # hit_on_color = True  --for future 'hitting' func
        #     return True
        # else:
        #     # self.complete = False
        #     return False

    def check_run(self, amount, pile):
        self.amount = amount
        self.pile = pile
        # create an empty result list for acceptable cards and bad list for invalid cards        
        bad = []
        wild = []
        run = []
        ### maybe instead of reversing to pull wild cards. just run a loop on self.pile and take out wild cards and end?
        reverse_hand = []
        while len(self.pile) != 0:
            reverse_hand.append(self.pile.pop())
        for card in reverse_hand:
            if card.get_value() == "13":
                bad.append(card)
            elif card.get_value() == "12":
                wild.append(card)
            else:
                run.insert(0, card)

        for card in run:
            if len(self.pile) > 0:
                prev_card = self.pile[-1]
                if int(card.get_value()) == (int(prev_card.get_value()) + 1):
                    self.pile.append(card)
                elif int(card.get_value()) == int(prev_card.get_value()):
                    bad.append(card)
                elif len(wild) >= (int(card.get_value()) - int(prev_card.get_value())) - 1:
                    for i in range((int(card.get_value()) - int(prev_card.get_value())) - 1):
                        new_card = wild.pop()
                        new_card.change_value(int(prev_card.get_value()) + 1)
                        self.pile.append(new_card)
                        ## use sort_pile method ?
                        new_card.position = prev_card.center_x + CARD_HORIZONTAL_OFFSET, \
                                                prev_card.center_y
                        prev_card = new_card
                    self.pile.append(card)
                    card.position = prev_card.center_x + CARD_HORIZONTAL_OFFSET, \
                                            prev_card.center_y
                else:
                    bad.append(card)
            else:
                self.pile.append(card)

        while len(wild) > 0:
            prev_card = self.pile[-1]
            new_card = wild.pop()
            if int(prev_card.get_value()) < 11:
                new_card.change_value(int(prev_card.get_value()) + 1)
                self.pile.append(new_card)
                continue
            else:
                start_card = self.pile[0]
                new_card.change_value(int(start_card.get_value()) - 1)
                print(new_card.get_value())
                self.pile.insert(0, new_card)
                continue

        # self.sort_pile(self.pile)
        if len(self.pile) >= self.amount and len(bad) == 0:
            # hit_on_run = True  --for future 'hitting' func
            return True
        else:
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
            # if (self.check_set(4, self.phase_pile) and self.check_run(4, self.phase_pile_b))\
            #     or (self.check_set(4, self.phase_pile_b) and self.check_run(4, self.phase_pile)):
            #     self.phase_complete = True
            # else:
            #     self.phase_complete = False

        elif self.phase == 4:
            return self.check_run(7, self.phase_pile)
            # if self.check_run(7, self.phase_pile):
            #     self.phase_complete = True
            # else:
            #     self.phase_complete = False

        elif self.phase == 5:
            return self.check_run(8, self.phase_pile)
            # if self.check_run(8, self.phase_pile):
            #     self.phase_complete = True
            # else:
            #     self.phase_complete = False

        elif self.phase == 6:
            return self.check_run(9, self.phase_pile)
            # if self.check_run(9, self.phase_pile):
            #     self.phase_complete = True
            # else:
            #     self.phase_complete = False

        elif self.phase == 7:
            return self.check_set(4, self.phase_pile_b) and self.check_set(4, self.phase_pile)
            # if self.check_set(4, self.phase_pile_b) and self.check_set(4, self.phase_pile):
            #     self.phase_complete = True
            # else:
            #     self.phase_complete = False

        elif self.phase == 8:
            return self.check_color(7, self.phase_pile)
            # if self.check_color(7, self.phase_pile):
            #     self.phase_complete = True
            # else:
            #     self.phase_complete = False

        elif self.phase == 9:
            return (self.check_set(5, self.phase_pile) and self.check_set(2, self.phase_pile_b))\
                or (self.check_set(5, self.phase_pile_b) and self.check_set(2, self.phase_pile))
            # if (self.check_set(5, self.phase_pile) and self.check_set(2, self.phase_pile_b))\
            #     or (self.check_set(5, self.phase_pile_b) and self.check_set(2, self.phase_pile)):
            #     self.phase_complete = True
            # else:
            #     self.phase_complete = False

        elif self.phase == 10:
            return (self.check_set(5, self.phase_pile) and self.check_set(3, self.phase_pile_b))\
                or (self.check_set(5, self.phase_pile_b) and self.check_set(3, self.phase_pile))
            # if (self.check_set(5, self.phase_pile) and self.check_set(3, self.phase_pile_b))\
            #     or (self.check_set(5, self.phase_pile_b) and self.check_set(3, self.phase_pile)):
            #     self.phase_complete = True
            # else:
            #     self.phase_complete = False

    def add_score(self, hand):
        """at end of round, add the point total for each card remaining in hand to total score."""
        self.hand = hand
        if len(self.hand) > 0:
            for card in self.hand:
                if card.get_value() in range(0, 8):
                    self.score += 5
                elif card.get_value() in range(9,11):
                    self.score += 10
                elif card.get_value() == "13":
                    self.score += 15
                else:
                    self.score += 25
        else:
            pass
        print(self.score)

class User(Player):  # may not need
    def __init__(self, name, turn, phase=1, phase_complete=False, score=0):
        super().__init__(name, turn, phase, phase_complete, score)

    ## add func to figure out phase piles

class Comp(Player):
    def __init__(self, name, turn, phase=1, phase_complete=False, score=0):
        super().__init__(name, turn, phase, phase_complete, score)

    ##add methods for what to do on comp turn.

# if __name__ == "__main__":
#     pass