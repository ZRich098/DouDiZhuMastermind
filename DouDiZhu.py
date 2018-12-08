from AI import ExpectiMiniMaxAI, HillClimbAI, SimulatedAnnealingAI, Other
import Cards
import sys

class DDZ:
    def __init__(self, player1, player2, player3):
        self.players = [player1, player2, player3]
        self.current_player = 0 #0 represents player1, 1 represents player2 and 2 represents player3
        self.game_over = False
        self.field = []
        self.deck1 =
            #Get from parsing the Game. The following are examples of cards.
            [Card(14, 'spades'), #Ace of Spades
             Card(12, 'diamonds'), #Queen of Diamonds
             Card(16, 'joker'), #Uncolored Joker
             Card(17, 'joker')] #Colored Joker
        self.deck2 = [] #Get from parsing the Game
        self.deck3 = [] #Get from parsing the Game
        self.hands = [self.deck1,self.deck2,self.deck3] #Hands for all of the players in the order of p1,p2,p3
        
        #the hidden cards in the center of the table
        self.hidden_cards = [] #Get from parsing the Game
    
    #get the stakes [1,2,3] from current_player for the hidden cards.
    def stakes(self):
        return 0
    
    #get the move they wish to make from current_player.
    def move(self, current_player):
        self.players[current_player].get_move()
    
    #update the Game State in response to a move
    def update_game_state(self,move, current_player):
        for ele in move:
            self.hands[current_player].remove(ele) #Removes every card that is being played
            self.field.append(ele) #Append it to the list representing the table
        # if one of the players has no more cards, then they win, and if they're not the landlord, then, their
        # partner wins as well.
        if(len(self.deck1) == 0 || len(self.deck2) == 0 || len(self.deck3) == 0):
            game_over(current_player)
        else: # Otherwise, we update the game state with the moves of each of the players after every turn.
            update_game_state(self.players[(current_player+1)%3].get_move(),(current_player+1)%3)

#Note for this function I have not decided how the stakes function should run yet so I have just hard coded it for now
def game_over(self, current_player):
    if(self.game_over == true and self.deck1 == 0): #if the game is over and player1's hand is empty
        print ("You and your partner have won " + current_player)
        print ("Game over Landlord")
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

#main function
def main():
    #Parse players from Game State
    Player1 = 'ExpectiMiniMaxAI'
    Player2 = 'HillClimbAI'
    Player3 = 'Other'
    
    DDZ(create_player(Player1, 1), create_player(Player2, 2), create_player(Player3, 3))

if __name__== '__main__':
    main()
