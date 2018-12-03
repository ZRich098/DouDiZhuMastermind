from AI import ExpectiMiniMaxAI, HillClimbAI, SimulatedAnnealingAI, Other
import Cards

class DDZ:
    def __init__(self, player1, player2, player3):
        self.players = [player1, player2, player3]
        self.current_player = 0
        self.game_over = False

        self.deck1 =
        #Get from parsing the Game. The following are examples of cards.
            [Card(1, 'spades'), #Ace of Spades
            Card(12, 'diamonds'), #Queen of Diamonds
            Card(1, 'joker'), #Uncolored Joker
            Card(2, 'joker')] #Colored Joker
        self.deck2 = [] #Get from parsing the Game
        self.deck3 = [] #Get from parsing the Game

        #the hidden cards in the center of the table
        self.hidden_cards = [] #Get from parsing the Game

    #get the stakes [1,2,3] from current_player for the hidden cards.
    def stakes(self):
        return 0

    #get the move they wish to make from current_player.
    def move(self):
        return 0

    #update the Game State in response to a move
    def update_game_state(self, move, current_player):
        return

    def game_over(self, current_player):
        return


def create_player(type, order):
    if type == 'ExpectiMiniMaxAI':
        return ExpectiMiniMaxAI(order)
    elif type == 'HillClimbAI':
        return HillClimbAI(order)
    elif type == 'SimulatedAnnealingAI':
        return SimulatedAnnealingAI(order)
    elif type == 'Other':
        return Other(order)

def main():
    #Parse players from Game State
    Player1 = 'ExpectiMiniMaxAI'
    Player2 = 'HillClimbAI'
    Player3 = 'Other'

    DDZ(create_player(Player1, 1), create_player(Player2, 2), create_player(Player3, 3))

if __name__== '__main__':
    main()
