class ExpectiMiniMaxAI:
    #order is the order the AIs go: 0, 1, 2 for first, second, third
    def __init__(self, order):
        self.order = order
        self.str = 'ExpectiMiniMaxAI ' + str(order)

    #valid_plays(self,hand) returns the list of all valid sub hands to play from the current hand.
    #
    #RETURN FORMAT: Returns a list of lists, where each sublist corresponds to the valid subhands of a type of play, in this order:
    #plays = [[rocket], [quad], [sequenceTriplet], [triplet], [sequencePair], [pair], [sequenceSingle], [single]]
    #
    #Furthermore, [single] is separated into sublists that note what cards are being used in what potential plays, in this order:
    #single = [single, isPair, isTriplet, isQuad, isSequence, isRocket]
    #
    #USAGE NOTE: The lists returned do not factor in attachment possibilities; this should be handled in the play-deciding function, instead
    #
    #Note that the [single] array is ordered in decreasing order of priority for attachment, for ease of use; for example,
    #if all singleton plays will disrupt potential big plays, single[0] will be an empty list [], and it might be 
    #smarter to avoid playing
    def valid_plays(self, hand):
        #NOTE 1: Cards should be represented as follows (such that values are in ascending order of rank):
        #Card(3, 'spades'): 3 of Spades
        #Card(13, 'spades'): King of Spades
        #Card(14, 'diamonds'): Ace of Diamonds
        #Card(15, 'spades'): 2 of Spades
        #Card(16, 'joker'): Uncolored Joker
        #Card(17, 'joker'): Colored Joker
        hand.sort(key = lambda card: card.value)
        
        #cards are stored in ascending order of rank; simplifiedHand[0] is the number of 3's held, 
        #[12] stores number of 2's held, [13] stores number of black jokers, and [14] stores number of colored jokers
        simplifiedHand = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for x in hand:
            if x.color == 'joker':
                #black joker
                if x.value == 16:
                    simplifiedHand[13] = simplifiedHand[13] + 1
                #colored joker
                else:
                    simplifiedHand[14] = simplifiedHand[14] + 1
            else:
                simplifiedHand[(x.value - 3)] = simplifiedHand[(x.value - 3)] + 1
        
        plays = []
        rocket = []
        quad = []
        sequenceTriplet = []
        triplet = []
        sequencePair = []
        pair = []
        sequenceSingle = []
        #single should be ordered in increasing order priority for usage in attachments to larger plays (that is, decreasing order of "value")
        #e.g. triplet with attached single card; the "isX" lists are used to keep track of which cards are part of big plays, 
        #since we want to use less-useful cards as the attachments
        #NOTE 2: We can change the order of the isX lists in single[] to adjust what hands the AI prioritizes keeping
        isRocket = []
        isQuad = []
        isTriplet = []
        isPair = []
        isSequence = []
        single = []
        #Note 3: We will insert Single in later
        plays.extend([rocket, quad, sequenceTriplet, triplet, sequencePair, pair, sequenceSingle])
        
        #QUERY 1: Should we be making copies of the cards to put into plays, or linking the actual cards?
        
        #Here, we scan over all possible values of card starting from 3 and going to Colored Joker;
        #previousCards keeps track of how many cards we have already scanned, so as to 
        #properly fetch cards from the Hand array
        previousCards = 0
        for x in range(15):
            #boolean to keep track of if the currently scanned card is part of any sequence
            cardInSequence = False
            #if we are scanning jokers:
            if (x == 13):
                if simplifiedHand[x] == 1:
                    #checking for rocket
                    if simplifiedHand[x+1] == 1:
                        rocket.append(hand[previousCards], hand[previousCards+1])
                        isRocket.append(hand[previousCards])
                        isRocket.append(hand[previousCards+1])
                        
                    else:
                        single.append(hand[previousCards])
                elif simplifiedHand[x+1] == 1:
                    single.append(hand[previousCards])
                break
            
            #if the hand has 4 of the current card being scanned 
            elif simplifiedHand[x] == 4:
                quad.append([hand[previousCards], hand[previousCards+1], hand[previousCards+2], hand[previousCards+3]])
                runningTriplet = [hand[previousCards], hand[previousCards+1], hand[previousCards+2]]
                triplet.append(runningTriplet)
                #logic for triplet sequences:
                #look at the next numerical value of card, and if it also has a triplet, add the running sequence of triplets
                #to the sequenceTriplet[] array
                #lookaheadCards helps track where the next numerical value of card starts
                lookaheadCards = previousCards + 4
                runningTripletSequence = [runningTriplet]
                for y in range(7):
                    if ((simplifiedHand[x+y+1] >= 3) and (x+y+1 < 12)):
                        newTriplet = [hand[lookaheadCards], hand[lookaheadCards+1], hand[lookaheadCards+2]]
                        runningTripletSequence.append(newTriplet)
                        sequenceTriplet.append(runningTripletSequence.copy())
                        lookaheadCards = lookaheadCards + simplifiedHand[x+y+1]
                        cardInSequence = True
                    else:
                        break 
                        
                runningPair = [hand[previousCards], hand[previousCards+1]]
                pair.append(runningPair)
                #similar logic to triplet sequences for pair sequences
                #lookaheadCards helps track where the next numerical value of card starts
                lookaheadCards = previousCards + 4
                runningPairSequence = [runningPair]
                for y in range(9):
                    if ((simplifiedHand[x+y+1] >= 2) and (x+y+1 < 12)):
                        newPair = [hand[lookaheadCards], hand[lookaheadCards+1]]
                        runningPairSequence.append(newPair)
                        sequencePair.append(runningPairSequence.copy())
                        lookaheadCards = lookaheadCards + simplifiedHand[x+y+1]
                        cardInSequence = True
                    else:
                        break
                        
                #similar logic for singleton sequences
                lookaheadCards = previousCards + 4
                runningSingleSequence = [hand[previousCards]]
                for y in range(12):
                    if ((simplifiedHand[x+y+1] >= 1) and (x+y+1 < 12)):
                        newSingle = [hand[lookaheadCards]]
                        runningSingleSequence.append(newSingle)
                        sequenceSingle.append(runningSingleSequence.copy())
                        lookaheadCards = lookaheadCards + simplifiedHand[x+y+1]
                        cardInSequence = True
                    else:
                        break
                        
                #setting single-attachment priority
                if cardInSequence:
                    isSequence.append(hand[previousCards])
                else:
                    isQuad.append(hand[previousCards])
                previousCards = previousCards + 4
                
            #If the current hand has 3 of the current card being scanned
            elif simplifiedHand[x] == 3:
                runningTriplet = [hand[previousCards], hand[previousCards+1], hand[previousCards+2]]
                triplet.append(runningTriplet)
                #logic for triplet sequences:
                #look at the next numerical value of card, and if it also has a triplet, add the running sequence of triplets
                #to the sequenceTriplet[] array
                #lookaheadCards helps track where the next numerical value of card starts
                lookaheadCards = previousCards + 3
                runningTripletSequence = [runningTriplet]
                for y in range(7):
                    if ((simplifiedHand[x+y+1] >= 3) and (x+y+1 < 12)):
                        newTriplet = [hand[lookaheadCards], hand[lookaheadCards+1], hand[lookaheadCards+2]]
                        runningTripletSequence.append(newTriplet)
                        sequenceTriplet.append(runningTripletSequence.copy())
                        lookaheadCards = lookaheadCards + simplifiedHand[x+y+1]
                        cardInSequence = True
                    else:
                        break
                runningPair = [hand[previousCards], hand[previousCards+1]]
                pair.append(runningPair)
                #similar logic to triplet sequences for pair sequences
                #lookaheadCards helps track where the next numerical value of card starts
                lookaheadCards = previousCards + 3
                runningPairSequence = [runningPair]
                for y in range(9):
                    if ((simplifiedHand[x+y+1] >= 2) and (x+y+1 < 12)):
                        newPair = [hand[lookaheadCards], hand[lookaheadCards+1]]
                        runningPairSequence.append(newPair)
                        sequencePair.append(runningPairSequence.copy())
                        lookaheadCards = lookaheadCards + simplifiedHand[x+y+1]
                        cardInSequence = true
                    else:
                        break
                #similar logic for singleton sequences
                lookaheadCards = previousCards + 3
                runningSingleSequence = [hand[previousCards]]
                for y in range(12):
                    if ((simplifiedHand[x+y+1] >= 1) and (x+y+1 < 12)):
                        newSingle = [hand[lookaheadCards]]
                        runningSingleSequence.append(newSingle)
                        sequenceSingle.append(runningSingleSequence.copy())
                        lookaheadCards = lookaheadCards + simplifiedHand[x+y+1]
                        cardInSequence = True
                    else:
                        break
                
                #setting single-attachment priority
                if cardInSequence:
                    isSequence.append(hand[previousCards])
                else:
                    isTriplet.append(hand[previousCards])
                previousCards = previousCards + 3
                
            #If the current hand has 2 copies of the card being scanned
            elif simplifiedHand[x] == 2:
                runningPair = [hand[previousCards], hand[previousCards+1]]
                pair.append(runningPair)
                #similar logic to triplet sequences for pair sequences
                #lookaheadCards helps track where the next numerical value of card starts
                lookaheadCards = previousCards + 2
                runningPairSequence = [runningPair]
                for y in range(9):
                    if ((simplifiedHand[x+y+1] >= 2) and (x+y+1 < 12)):
                        newPair = [hand[lookaheadCards], hand[lookaheadCards+1]]
                        runningPairSequence.append(newPair)
                        sequencePair.append(runningPairSequence.copy())
                        lookaheadCards = lookaheadCards + simplifiedHand[x+y+1]
                        cardInSequence = True
                    else:
                        break
                #similar logic for singleton sequences
                lookaheadCards = previousCards + 2
                runningSingleSequence = [hand[previousCards]]
                for y in range(12):
                    if ((simplifiedHand[x+y+1] >= 1) and (x+y+1 < 12)):
                        newSingle = [hand[lookaheadCards]]
                        runningSingleSequence.append(newSingle)
                        sequenceSingle.append(runningSingleSequence.copy())
                        lookaheadCards = lookaheadCards + simplifiedHand[x+y+1]
                        cardInSequence = True
                    else:
                        break
                
                #setting single-attachment priority
                if cardInSequence:
                    isSequence.append(hand[previousCards])
                else:
                    isPair.append(hand[previousCards])
                previousCards = previousCards + 2
                
            #If current hand only has 1 copy of the scanned card
            elif simplifiedHand[x] == 1:
                #Only need to check for singleton sequence
                lookaheadCards = previousCards + 1
                runningSingleSequence = [hand[previousCards]]
                for y in range(12):
                    if ((simplifiedHand[x+y+1] >= 1) and (x+y+1 < 12)):
                        newSingle = [hand[lookaheadCards]]
                        runningSingleSequence.append(newSingle)
                        sequenceSingle.append(runningSingleSequence.copy())
                        lookaheadCards = lookaheadCards + simplifiedHand[x+y+1]
                        cardInSequence = True
                    else:
                        break
                
                #setting single-attachment priority
                if cardInSequence:
                    isSequence.append(hand[previousCards])
                else:
                    single.append(hand[previousCards])
                previousCards = previousCards + 1

                
                
        #single = single + isPair + isTriplet + isQuad + isSequence + isRocket
        single = [single, isPair, isTriplet, isQuad, isSequence, isRocket]
        plays.append(single)
        return plays

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
