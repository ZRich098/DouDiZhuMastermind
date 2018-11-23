class ExpectiMiniMaxAI:
    #order is the order the AIs go: 0, 1, 2 for first, second, third
    def __init__(self, order):
        self.order = order
        self.str = 'ExpectiMiniMaxAI ' + str(order)

    #get list of all valid sub hands to play
    def valid_plays(self, hand):
        return [hand]

    #find expected value of own hand
    def evaluate_hand(self, hand):
        return 0

    #find expected values of others' hands
    def evaluate_others(unplayed_cards):
        return 0

    def evaluate_game_state(self, hand, unplayed_cards):
        return 0

    #return the best move based on expectiminimax using pruning
    def get_move(self):
        return valid_plays[1]

class HillClimbAI:
    def __init__(self, order):
        self.order = order
        self.str = 'HillClimbAI ' + str(order)

class SimulatedAnnealingAI:
    def __init__(self, order):
        self.order = order
        self.str = 'SimulatedAnnealingAI ' + str(order)

#Other Actual Non-AI Players
class Other:
    def __init__(self, order):
        self.order = order
        self.str = 'Other ' + str(order)
