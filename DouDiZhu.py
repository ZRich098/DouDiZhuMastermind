from AI import ExpectiMiniMaxAI, HillClimbAI, SimulatedAnnealingAI, Other
import Cards
import sys
import numpy as np

""" debug code for hydrogen
class ExpectiMiniMaxAI:
    #order is the order the AIs go: 0, 1, 2 for first, second, third
    def __init__(self, order):
        self.order = order
        self.str = 'ExpectiMiniMaxAI ' + str(order)

    def get_move(self, a, b):
        return []
class HillClimbAI:
    #order is the order the AIs go: 0, 1, 2 for first, second, third
    def __init__(self, order):
        self.order = order
        self.str = 'HillClimbAI ' + str(order)

    def get_move(self, a, b):
        return [Card(1,"a")]

class SimulatedAnnealingAI:
    #order is the order the AIs go: 0, 1, 2 for first, second, third
    def __init__(self, order):
        self.order = order
        self.str = 'SimulatedAnnealingAI ' + str(order)

    def get_move(self, a, b):
        return [Card(2,"b")]
"""

class DDZ:
    def __init__(self, player1, player2, player3):
        self.players = [player1, player2, player3]
        self.current_player = 0 #0 represents player1, 1 represents player2 and 2 represents player3
        self.game_over = False
        self.field = []
        self.origDeck = [(3,'diamonds'),(3,'clubs'),(3,'hearts'),(3,'spades'),
                         (4,'diamonds'),(4,'clubs'),(4,'hearts'),(4,'spades'),
                         (5,'diamonds'),(5,'clubs'),(5,'hearts'),(5,'spades'),
                         (6,'diamonds'),(6,'clubs'),(6,'hearts'),(6,'spades'),
                         (7,'diamonds'),(7,'clubs'),(7,'hearts'),(7,'spades'),
                         (8,'diamonds'),(8,'clubs'),(8,'hearts'),(8,'spades'),
                         (9,'diamonds'),(9,'clubs'),(9,'hearts'),(9,'spades'),
                         (10,'diamonds'),(10,'clubs'),(10,'hearts'),(10,'spades'),
                         (11,'diamonds'),(11,'clubs'),(11,'hearts'),(11,'spades'),
                         (12,'diamonds'),(12,'clubs'),(12,'hearts'),(12,'spades'),
                         (13,'diamonds'),(13,'clubs'),(13,'hearts'),(13,'spades'),
                         (14,'diamonds'),(14,'clubs'),(14,'hearts'),(14,'spades'),
                         (15,'diamonds'),(15,'clubs'),(15,'hearts'),(15,'spades'),
                         (16,'joker'),(17,'joker')]
                         #The original deck of 54 cards including the jokers
        self.landlord = 0 # The landlord represented as an integer
        self.currentPlay = [] #Current play on the board
        self.turn = 0 #Turn number



        #Shuffle cards
        np.random.shuffle(self.origDeck)
        self.deck1 = self.origDeck[:18]
        self.deck1.sort(key = lambda a,b: a)
        self.deck2 = self.origDeck[18:36]
        self.deck2.sort(key = lambda a,b: a)
        self.deck3 = self.origDeck[36:52]
        self.deck3.sort(key = lambda a,b: a)
        self.hands = [self.deck1,self.deck2,self.deck3] #Hands for all of the players in the order of p1,p2,p3
        #the hidden cards in the center of the table
        self.hidden_cards = self.origDeck[52:] #Get from parsing the Game

    #get the stakes [1,2,3] from current_player for the hidden cards.
    def stakes(self):
        return 3

    def unPlayed(self,current_player):
        [card for card in self.origDeck not in (self.field + hands[current_player])]


    def updateCurrentPlay(self,move):
        self.currentPlay.clear()
        self.currentPlay = move



    #get the move they wish to make from current_player.
    def move(self, current_player):
        if(current_player == 0):
            self.players[current_player].get_move(self.deck2, self.currentPlay)
#        self.players[current_player].get_move(self.deck1,len(self.deck2),len(self.deck3),unPlayed())
        elif(current_player == 1):
            self.players[current_player].get_move(self.deck2, self.currentPlay)
        else:
            self.players[current_player].get_move(self.deck3,self.turn, self.currentPlay)


    #update the Game State in response to a move
    def update_game_state(self,move, current_player):
        for ele in move:
            self.hands[current_player].remove(ele) #Removes every card that is being played
            self.field.append(ele) #Append it to the list representing the table
        # if one of the players has no more cards, then they win, and if they're not the landlord, then, their
        # partner wins as well.
        if(len(self.deck1) == 0 or len(self.deck2) == 0 or len(self.deck3) == 0):
            game_over(current_player)
        else: # Otherwise, we update the game state with the moves of each of the players after every turn.
            update_game_state(move(current_player),(current_player+1)%3)
            updateCurrentPlay(move(current_player))
            self.turn += 1

    #Note for this function I have not decided how the stakes function should run yet so I have just hard coded it for now
    def game_over(self, current_player):
        if(self.game_over == true and self.deck1 == 0): #if the game is over and player1's hand is empty
            print ("You have won Landlord!!")
            print ("Game over filthy Peasants")
        elif(self.game_over == false and self.deck2 == 0): #if the game is over and player2's hand is empty
            print ("You and your partner have won " + current_player)
            print ("Game over Landlord")
        else:  #if the game is over and player3's hand is empty
            print ("You and your partner have won " + current_player)
            print ("Game over Landlord")

    def create_player(type, order):
        if type == 'ExpectiMiniMaxAI':
            return ExpectiMiniMaxAI(order)
        elif type == 'HillClimbAI':
            return HillClimbAI(order)
        elif type == 'SimulatedAnnealingAI':
            return SimulatedAnnealingAI(order)
        elif type == 'Other':
            return Other(order)

    def updateLandlord(self,current_player):
        return evalueate_other_player(17,hand,unplayed(current_player))

#main function
def main():
    #Parse players from Game State
#    Player1 = 'ExpectiMiniMaxAI'
    Player1 = 'HillClimbAI'
    Player2 = 'HillClimbAI'
    Player3 = 'SimulatedAnnealingAI'

    DDZ(create_player(Player1, 1), create_player(Player2, 2), create_player(Player3, 3))
    DDZ.landlord = updateLandlord(self.current_player)
    DDZ.hands[DDZ.landlord] = DDZ.hands[DDZ.landlord] + DDZ.hidden_cards

if __name__== '__main__':
    main()
