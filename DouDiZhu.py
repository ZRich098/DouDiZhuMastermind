from Cards import Card
from AI import ExpectiMiniMaxAI, HillClimbAI, SimulatedAnnealingAI, Other
import sys
import numpy as np

class DDZ:
    def __init__(self, player1, player2, player3):
        self.players = [player1, player2, player3]
        self.current_player = 0 #0 represents player1, 1 represents player2 and 2 represents player3
        self.game_over_value = False
        self.field = []
        self.origDeck = [Card(3,'diamonds'),Card(3,'clubs'),Card(3,'hearts'),Card(3,'spades'),
                         Card(4,'diamonds'),Card(4,'clubs'),Card(4,'hearts'),Card(4,'spades'),
                         Card(5,'diamonds'),Card(5,'clubs'),Card(5,'hearts'),Card(5,'spades'),
                         Card(6,'diamonds'),Card(6,'clubs'),Card(6,'hearts'),Card(6,'spades'),
                         Card(7,'diamonds'),Card(7,'clubs'),Card(7,'hearts'),Card(7,'spades'),
                         Card(8,'diamonds'),Card(8,'clubs'),Card(8,'hearts'),Card(8,'spades'),
                         Card(9,'diamonds'),Card(9,'clubs'),Card(9,'hearts'),Card(9,'spades'),
                         Card(10,'diamonds'),Card(10,'clubs'),Card(10,'hearts'),Card(10,'spades'),
                         Card(11,'diamonds'),Card(11,'clubs'),Card(11,'hearts'),Card(11,'spades'),
                         Card(12,'diamonds'),Card(12,'clubs'),Card(12,'hearts'),Card(12,'spades'),
                         Card(13,'diamonds'),Card(13,'clubs'),Card(13,'hearts'),Card(13,'spades'),
                         Card(14,'diamonds'),Card(14,'clubs'),Card(14,'hearts'),Card(14,'spades'),
                         Card(15,'diamonds'),Card(15,'clubs'),Card(15,'hearts'),Card(15,'spades'),
                         Card(16,'joker'),Card(17,'joker')]
                         #The original deck of 54 cards including the jokers
        self.landlord = 0 # The landlord represented as an integer
        self.currentPlay = [] #Current play on the board
        self.turn = 1 #Turn number
        self.prevPlay = []



        #Shuffle cards
        np.random.shuffle(self.origDeck)
        self.deck1 = self.origDeck[:18]
        self.deck1.sort(key = lambda x: x.value)
        self.deck2 = self.origDeck[18:36]
        self.deck2.sort(key = lambda x: x.value)
        self.deck3 = self.origDeck[36:52]
        self.deck3.sort(key = lambda x: x.value)
        self.hands = [self.deck1,self.deck2,self.deck3] #Hands for all of the players in the order of p1,p2,p3
        #the hidden cards in the center of the table
        self.hidden_cards = self.origDeck[52:] #Get from parsing the Game

    #get the stakes [1,2,3] from current_player for the hidden cards.
    def stakes(self):
        return 3

    def unPlayed(self,player):
        list = []
        for card in self.origDeck:
            if card not in self.field + self.hands[self.current_player]:
                list.append(card)
        return list

    def updateCurrentPlayer(self):
        self.current_player = (self.current_player + 1) %3 

    def updateCurrentPlay(self,move):
        self.prevPlay.clear()
        self.prevPlay = self.currentPlay.copy()
        self.currentPlay.clear()
        self.currentPlay = move
        print("Player "+str(self.current_player)+" is playing "+ str(move))
        print("\n")
        self.updateCurrentPlayer()


    def use(self,mov):
        if (mov is not None):
            for ele in mov:
                if (ele in self.hands[self.current_player]):
                    self.hands[self.current_player].remove(ele) #Removes every card that is being played
                    self.field.append(ele) #Append it to the list representing the table

    #get the move they wish to make from current_player.
    def move(self):
        if(self.current_player == 0):
            
            if(self.prevPlay != [] and self.currentPlay == []):
                r1 = self.players[self.current_player].get_move(self.hands[self.current_player],self.unPlayed(self.current_player),((len(self.deck2),self.sameTeam(self.current_player, ((self.current_player+1)%3))),(len(self.deck3),self.sameTeam(self.current_player, ((self.current_player+2)%3)))),self.prevPlay)
            else:
                r1 = self.players[self.current_player].get_move(self.hands[self.current_player],self.unPlayed(self.current_player),((len(self.deck2),self.sameTeam(self.current_player, ((self.current_player+1)%3))),(len(self.deck3),self.sameTeam(self.current_player, ((self.current_player+2)%3)))),self.currentPlay)
            self.use(r1)
            
            self.updateCurrentPlay(r1)
            
             
#            self.players[current_player].get_move(self.deck1,len(self.deck2),len(self.deck3),unPlayed())
        elif(self.current_player == 1):
            if(self.prevPlay != [] and self.currentPlay == []):
                r2 = self.players[self.current_player].get_move(self.hands[self.current_player], self.prevPlay)
            else:
                r2 = self.players[self.current_player].get_move(self.hands[self.current_player], self.currentPlay)
            self.use(r2)
            
            self.updateCurrentPlay(r2)
            
            
        else:
            if(self.prevPlay != [] and self.currentPlay == []):
                r3 = self.players[self.current_player].get_move(self.hands[self.current_player], self.prevPlay,self.turn)
            else:
                r3 = self.players[self.current_player].get_move(self.hands[self.current_player], self.currentPlay,self.turn)
            self.use(r3)
            
            self.updateCurrentPlay(r3)
            
            




    #update the Game State in response to a move
    def update_game_state(self, mv):

        # if one of the players has no more cards, then they win, and if they're not the landlord, then, their
        # partner wins as well.
        if(len(self.deck1) == 0 or len(self.deck2) == 0 or len(self.deck3) == 0):
            self.game_over()
        else: # Otherwise, we update the game state with the moves of each of the players after every turn.
            self.turn += 1
            self.update_game_state(self.move())

    #Note for this function I have not decided how the stakes function should run yet so I have just hard coded it for now
    def game_over(self):
        if(self.game_over_value == True and self.deck1 == 0): #if the game is over and player1's hand is empty
            if(self.landlord == 0):
                print ("You have won Landlord!!")
                print ("Game over filthy Peasants")
            else:
                print ("You and your partner have won " + str(self.current_player))
                print ("Game over Landlord")
        elif(self.game_over_value == False and self.deck2 == 0): #if the game is over and player2's hand is empty
            if(self.landlord == 0):
                print ("You have won Landlord!!")
                print ("Game over filthy Peasants")
            else:
                print ("You and your partner have won " + str(self.current_player))
                print ("Game over Landlord")
        else:  #if the game is over and player3's hand is empty
            if(self.landlord == 0):
                print ("You have won Landlord!!")
                print ("Game over filthy Peasants")
            else:
                print ("You and your partner have won " + str(self.current_player))
                print ("Game over Landlord")
     
    def sameTeam(self,p1,p2):
        if p1 != self.landlord and p2 != self.landlord:  
            return True
        else:
            return False

    def updateLandlord(self):
        val1 = self.players[0].evaluate_other_player(17,self.deck1,self.unPlayed(1))
        val2 = self.players[1].evaluate_other_player(17,self.deck2,self.unPlayed(0))
        val3 = self.players[2].evaluate_other_player(17,self.deck3,self.unPlayed(1))

        if(val1 >= val2 and val1 >= val3):
            return 0
        elif(val2 >= val1 and val2 >= val3):
            return 1
        else:
            return 2

def create_player(type, order):
    if type == 'ExpectiMiniMaxAI':
        return ExpectiMiniMaxAI(order)
    elif type == 'HillClimbAI':
        return HillClimbAI(order)
    elif type == 'SimulatedAnnealingAI':
        return SimulatedAnnealingAI(order)
    elif type == 'Other':
        return Other(order)

#main function
def main():
    #Parse players from Game State

    Player1 = 'ExpectiMiniMaxAI'
    Player2 = 'HillClimbAI'
    Player3 = 'SimulatedAnnealingAI'

    game = DDZ(create_player(Player1, 1), create_player(Player2, 2), create_player(Player3, 3))
    game.landlord = game.updateLandlord()
    game.hands[game.landlord] = game.hands[game.landlord] + game.hidden_cards
    game.update_game_state(game.move())

if __name__== '__main__':
    main()



#tests
hand = [
Card(4, "hearts"), Card(5, "diamonds"), Card(6,"spades"),
Card(7, "hearts"), Card(8, "diamonds"), Card(9,"spades")]
"""
hand = [
Card(4, "hearts"), Card(5, "diamonds"), Card(6,"spades"),
Card(7, "hearts"), Card(8, "diamonds"), Card(9,"spades"),
Card(11, "hearts"), Card(11, "diamonds"), Card(12,"spades"),
Card(13, "hearts"), Card(14, "diamonds"), Card(15,"spades"),
Card(15, "hearts"), Card(16, "joker"), Card(17,"joker")]
"""
current_play = [Card(3,"clubs"), Card(3, "spades")]
current_play = [Card(3,"clubs")]
current_play = []


eai = ExpectiMiniMaxAI(1)

#tests
hai = HillClimbAI(1)
hai.combine_play(hand, current_play)
hai.get_move(hand, current_play)

#tests
sai = SimulatedAnnealingAI(1)
sai.combine_play(hand, current_play)
sai.get_move(hand,current_play, 1) #move on turn 1
