import numpy as np

 
#The function that displays cards
def card_show(cards, info, n):
    
    #Display the record of the cards
    if n == 1:
        print(info)
        names = []
        for i in cards:
            names.append(i.name+i.color)
        print(names)    
    #Moves display
    elif n == 2:
        if len(cards) == 0:
            return 0
        print(info)
        moves = []
        for i in cards:
            names = []
            for j in i:
                names.append(j.name+j.color)
            moves.append(names)
        print(moves)  
    #record display
    elif n == 3:
        print(info)
        names = []
        for i in cards:
            tmp = []
            tmp.append(i[0])
            tmp_name = []
            #Handle the case that player pass the round
            try:
                for j in i[1]:
                    tmp_name.append(j.name+j.color)
                tmp.append(tmp_name)
            except:
                tmp.append(i[1])
            names.append(tmp)
        print(names)
       

#Choose the way/model to play cards from Player's next move
def choose(next_move_types, next_moves, last_move_type, model):
    
    if model == "random":
        return choose_random(next_move_types, next_moves, last_move_type)

#random
def choose_random(next_move_types, next_moves, last_move_type):
    #Pass/Players do not choose to play any cards for the current round
    if len(next_moves) == 0:
        return "Pass", []
    else:
        #start "Must play some cards for the current round"
        if last_move_type == "start":
            r_max = len(next_moves)
        else:
            r_max = len(next_moves)+1
        r = np.random.randint(0,r_max)
        #Insert "Pass" as an option for the next move
        if r == len(next_moves):
            return "Pass", []
        
    return next_move_types[r], next_moves[r] 
    
#Deal cards
def game_init(players, playrecords, cards):
    
    #Shuffle cards
    np.random.shuffle(cards.cards)
    #Sort the order of cards
    p1_cards = cards.cards[:18]
    p1_cards.sort(key=lambda x: x.rank)
    p2_cards = cards.cards[18:36]
    p2_cards.sort(key=lambda x: x.rank)
    p3_cards = cards.cards[36:]
    p3_cards.sort(key=lambda x: x.rank)
    players[0].cards_left = playrecords.cards_left1 = p1_cards
    players[1].cards_left = playrecords.cards_left2 = p2_cards
    players[2].cards_left = playrecords.cards_left3 = p3_cards    