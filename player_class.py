import arcade
from Phase_10_constants import PHASE_1_MATS, PHASE_2_MATS, PHASE_PILE_1, PHASE_PILE_2, CARD_SCALE, CARD_VALUES
from phase_10 import Card

# card_class = Card()

class Player:
    def __init__(self, name, turn=False, phase=1, score=0):
        self.name = name
        self.turn = turn
        self.phase = phase
        self.score = score
        self.phase_pile = None
        self.phase_pile_b = None

    def determine_phase_piles(self, pile_mat_list):
        self.pile_mat_list = pile_mat_list

        if self.name == "user":
            if self.phase in PHASE_1_MATS:
                self.phase_pile = self.pile_mat_list[PHASE_PILE_1]
                last_user_pile = self.pile_mat_list[PHASE_PILE_1]
            elif self.phase in PHASE_2_MATS:
                self.phase_pile = self.pile_mat_list[PHASE_PILE_1]
                self.phase_pile_b = self.pile_mat_list[PHASE_PILE_2]
                last_user_pile = self.pile_mat_list[PHASE_PILE_2]

        elif self.name == "lcomp":
            if self.phase in PHASE_1_MATS:
                self.phase_pile = self.pile_mat_list[last_user_pile + 1]
                last_lcomp_pile = last_user_pile + 1
            elif self.phase in PHASE_2_MATS:
                self.phase_pile = self.pile_mat_list[last_user_pile + 1]
                self.phase_pile_b = self.pile_mat_list[last_user_pile + 2]
                last_lcomp_pile = last_user_pile + 2

        elif self.name == "mcomp":
            if self.phase in PHASE_1_MATS:
                self.phase_pile = self.pile_mat_list[last_lcomp_pile + 1]
                last_mcomp_pile = last_lcomp_pile + 1
            elif self.phase in PHASE_2_MATS:
                self.phase_pile = self.pile_mat_list[last_lcomp_pile + 1]
                self.phase_pile_b = self.pile_mat_list[last_lcomp_pile + 2] 
                last_mcomp_pile = last_lcomp_pile + 2

        elif self.name == "rcomp":
            if self.phase in PHASE_1_MATS:
                self.phase_pile = self.pile_mat_list[last_mcomp_pile + 1]
            elif self.phase in PHASE_2_MATS:
                self.phase_pile = self.pile_mat_list[last_mcomp_pile + 1]
                self.phase_pile_b = self.pile_mat_list[last_mcomp_pile + 2]    

    def check_set(self, amount, pile):
        """check to see if cards in phase pile meets the phase requirement for a set.
        amount = number of cards with same value needed to complete phase
        pile = the list of cards in the phase pile being checked
        returns bool"""
        self.amount = amount
        self.pile = pile
        # get first card value other than wild or skip
        while True:
            n = 0
            card_1 = self.pile[n]
            if card_1.get_color() == "black":   ## change to card_1 == Card("black", "wild", CARD_SCALE) or card_1 == Card("black", "skip", CARD_SCALE)
                n += 1
            else:
                break
        # create an empty result list for acceptable cards and bad list for invalid cards
        res = []
        bad = []
        for card in self.pile:
            if card.get_value() == "wild":
                self.amount -= 1
            elif card.get_value() == card_1.get_value():
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
        while True:
            n = 0
            card_1 = self.pile[n]
            if card_1.get_color() == "black":
                n += 1
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
            elif card.get_color() == card_1.get_color():
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
        res = []
        bad = []
        for card in self.pile:  ### need to change value of wild card when adding into run.
            if len(res) > 0:
                start_card = res[0]
                prev_card = res[-1]
                if card.get_value() == "skip":
                    bad.append(card)
                elif prev_card.get_value() == "wild": #and len(res) == 1:
                    res.append(card)
                ### change below to -- elif: card.getvalue().isdigit() --- change else: to return False/put cards back (because of skip)
                elif card.get_value() == "wild" or int(card.get_value()) == (int(prev_card.get_value()) + 1):
                        res.append(card)
                else:
                    bad.append(card)
            else:
                if card.get_value() == "skip":
                    bad.append(card)
                else:
                    res.append(card)
        if len(res) >= self.amount and len(bad) == 0:
            # hit_on_run = True  --for future 'hitting' func
            return True
        else:
            return False

    def phase_complete(self):
        if self.phase == 1:
            return self.check_set(3, self.phase_pile_b) and self.check_set(3, self.phase_pile)
            # if self.check_set(3, self.phase_pile_b) and self.check_set(3, self.phase_pile):
            #     # hit_on_set = True  -- phase_pile_b.hit_on_set() phase_pile.hit_on_set()
            #     return True
            # else:
            #     # self.phase_complete = False
            #     return False

        elif self.phase == 2:
            return (self.check_set(3, self.phase_pile) and self.check_run(4, self.phase_pile_b))\
                or (self.check_set(3, self.phase_pile_b) and self.check_run(4, self.phase_pile))
            # if (self.check_set(3, self.phase_pile) and self.check_run(4, self.phase_pile_b))\
            #     or (self.check_set(3, self.phase_pile_b) and self.check_run(4, self.phase_pile)):
            #     self.phase_complete = True
            # else:
            #     self.phase_complete = False

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

    def add_score(self, player):
        """at end of round, add the point total for each card remaining in hand to total score."""
        self.player = player
        for card in player.hand:
            if card in CARD_VALUES[:9]:
                player.score += 5
            elif card in CARD_VALUES[10:12]:
                player.score += 10
            elif card == CARD_VALUES[13]:
                player.score += 15
            else:
                player.score += 25  

class User(Player):
    def __init__(self, name, turn, phase=1, phase_complete=False, score=0):
        super().__init__(name, turn, phase, phase_complete, score)

    ## add func to figure out phase piles

class Comp(Player):
    def __init__(self, name, turn, phase=1, phase_complete=False, score=0):
        super().__init__(name, turn, phase, phase_complete, score)

    ##add func to figure out phase piles

if __name__ == "__main__":
    pass