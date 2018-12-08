from Cards import Cards, Player, PlayRecords
from Utility import game_init
import jsonpickle
import time
import copy                   
class Game(object):
    
    def __init__(self, model):
        #Initialize a deck of cards
        self.cards = Cards()
        
        #import related parameters
        self.end = False
        self.last_move_type = self.last_move = "start"
        self.playround = 1
        self.i = 0
        self.Pass = []
        
        #choose model
        self.model = model
        
    #deals the cards
    def game_start(self):
        
        #initialize players
        self.players = []
        for i in range(1,4):
            self.players.append(Player(i))
        
        #Initialize the class of recording cards
        self.playrecords = PlayRecords()    
        
        #deal the cards
        game_init(self.players, self.playrecords, self.cards)
    
    
    #返回扑克牌记录类 Return the record of cards
    def get_record(self):
        web_show = WebShow(self.playrecords)
        return jsonpickle.encode(web_show, unpicklable=False)
        
    #In the middle of the game   
    def next_move(self):
        
        self.last_move_type, self.last_move, self.end, self.Pass = self.players[self.i].go(self.last_move_type, self.last_move, self.playrecords, self.model)
        if self.Pass:
            self.Pass.append(self.i)
        else:
            self.Pass = []
        #All of the rest players "Pass" the current round
        if len(self.Pass) == 2:
            self.Pass = []
            self.last_move_type = self.last_move = "start"
        if self.end:
            self.playrecords.winner = self.i+1
        self.i = self.i + 1
        #The end of one round
        if self.i > 2:
            #playrecords.show("=============Round " + str(playround) + " End=============")
            self.playround = self.playround + 1
            #playrecords.show("=============Round " + str(playround) + " Start=============")
            self.i = 0    
        
   
if __name__=="__main__":
    
    begin = time.time()
    game_ddz = Game("random") 
    game_ddz.game_start()
    for j in range(10000):
        #game_ddz = copy.deepcopy(game_ddz)
        i = 0
        while(game_ddz.playrecords.winner == 0):
            #game_ddz.playrecords.show(str(i))
            game_ddz.next_move()
            i = i + 1
        print(game_ddz.playrecords.winner)
    print(time.time()-begin)