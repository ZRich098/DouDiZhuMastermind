#just here for testing, remove later -Richard
class Card:
    def __init__(self, value, color):
        self.value = value
        self.color = color

    def __repr__ (self):
        table = {
            11: "Jack",
            12: "Queen",
            13: "King",
            14: "Ace",
            15: "Two"}

        if self.value == 16: return "Uncolored Joker"
        elif self.value == 17: return "Colored Joker"
        return table.get(self.value,str(self.value)) + " of " + self.color

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
            #black joker
            if x.value == 16:
                simplifiedHand[13] = simplifiedHand[13] + 1
            #colored joker
            elif x.value == 17:
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
                        sequenceTriplet.append(list(runningTripletSequence))
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
                        sequencePair.append(list(runningPairSequence))
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
                        sequenceSingle.append(list(runningSingleSequence))
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
                        sequenceTriplet.append(list(runningTripletSequence))
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
                        sequencePair.append(list(runningPairSequence))
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
                        sequenceSingle.append(list(runningSingleSequence))
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
                        sequencePair.append(list(runningPairSequence))
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
                        sequenceSingle.append(list(runningSingleSequence))
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

            #If current hand only has 1 of the scanned card
            elif simplifiedHand[x] == 1:
                #Only need to check for singleton sequence
                lookaheadCards = previousCards + 1
                runningSingleSequence = [hand[previousCards]]
                for y in range(12):
                    if ((simplifiedHand[x+y+1] >= 1) and (x+y+1 < 12)):
                        newSingle = [hand[lookaheadCards]]
                        runningSingleSequence.append(newSingle)
                        sequenceSingle.append(list(runningSingleSequence))
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

    #EXTREMELY IMPORTANT NOTE:
    #ALL THE BELOW SEQUENCE CHECKING FUNCTIONS ASSUME A SORTED HAND
    #Additionally, they will be updated later to have the following return format:
    #
    #returnFormat is a 2-length array where:
    #returnFormat[0] is a boolean that is True if the hand is of the type being scanned
    #returnFormat[1] is an array, determined by the type being scanned, that contains the
    #particulars of the hand, e.g. the starting card of a sequence or the values of a quadplex set

    def check_bomb(hand):
        bombValue = hand[x].value
        return [(hand[x].value == hand[x+1].value and hand[x].value == hand[x+2].value and hand[x].value == hand[x+3].value), bombValue]

    def check_rocket(hand):
        return (hand[0].value == 16 and hand[1].value == 17)

    def check_single_sequence(hand):
        prevHandValue = -1
        sequenceStart = hand[0].value
        for x in range (len(hand)):
            if hand[x].value == prevHandValue+1 or prevHandValue == -1:
                prevHandValue = hand[x].value
                if x == len(hand) - 1:
                    return [True, sequenceStart]
            else:
                return [False, sequenceStart]

    def check_pair_sequence(hand):
        prevHandValue = -1
        totalNumber = len(hand)
        sequenceStart = hand[0].value
        for x in range (0, totalNumber, 2):
            if (hand[x].value == prevHandValue+1 and hand[x+1].value == prevHandValue + 1 and hand[x].value == hand[x+1].value) or prevHandValue == -1:
                prevHandValue = hand[x].value
                if x >= len(hand) - 2:
                    return [True, sequenceStart]
            else:
                return [False, sequenceStart]

    def check_triplet_sequence(hand):
        prevHandValue = -1
        totalNumber = len(hand)
        sequenceStart = hand[0].value
        for x in range (0, totalNumber, 3):
            if (hand[x].value == prevHandValue+1 and hand[x+1].value == prevHandValue+1 and hand[x+2].value == prevHandValue+1) or prevHandValue == -1:
                prevHandValue = hand[x].value
                if x >= len(hand) - 3:
                    return [True, sequenceStart]
            else:
                return [False, sequenceStart]

    def check_triplet_sequence_attachments(hand, needed):
        prevHandValue = -1
        totalNumber = len(hand)
        sequenceStart = -1
        for x in range (totalNumber):
            prevHandValue = -1
            totalTripletsNeeded = needed
            noTripletFound = False
            for x in range (totalNumber-2):
                #found the beginning of the sequence
                if hand[x].value == hand[x+1].value and hand[x].value == hand[x+2].value:
                    sequenceStart = hand[x].value
                    #note: y is a variable tracking the total number of triplets found, identical to totalTripletsFound
                    for y in range (totalTripletsNeeded):
                        if ((x+(y*3)) >= len(hand)):
                            noTripletFound == True
                            break
                        if prevHandValue == -1 or (hand[x+(y*3)].value == prevHandValue + 1 and
                                                   hand[x+1+(y*3)].value == prevHandValue + 1 and
                                                   hand[x+2+(y*3)].value == prevHandValue + 1):
                            prevHandValue = hand[x+(y*3)].value
                            if y >= int(totalTripletsNeeded) - 1:
                                return [True, sequenceStart]
                        else:
                            noTripletFound = True
                            break
                    if noTripletFound == True:
                        return [False, sequenceStart]

    def check_quadplex_set_1(hand):
        prevHandValue = -1
        totalNumber = len(hand)
        attachment1 = -1
        attachment2 = -1
        quadValue = -1
        for x in range (totalNumber):
            if (hand[x].value == hand[x+1].value and hand[x].value == hand[x+2].value and hand[x].value == hand[x+3].value):
                quadValue = hand[x].value
                break
        if quadValue == -1:
            return False
        for y in range (totalNumber):
            if (hand[y].value != quadValue):
                if attachment1 == -1:
                    attachment1 = hand[y].value
                elif attachment2 == -1:
                    attachment2 = hand[y].value
        if (attachment1 != attachment2):
            return [True, quadValue]
        else:
            return [False, quadValue]

    def check_quadplex_set_2(hand):
        prevHandValue = -1
        totalNumber = len(hand)
        pair1 = -1
        pair2 = -1
        quadValue = -1
        for x in range (totalNumber):
            if (hand[x].value == hand[x+1].value and hand[x].value == hand[x+2].value and hand[x].value == hand[x+3].value):
                quadValue = hand[x].value
                break
        if quadValue == -1:
            return False
        for y in range (totalNumber-1):
            if (hand[y].value == hand[y+1].value and hand[y].value != quadValue):
                if pair1 == -1:
                    pair1 = hand[y].value
                elif pair2 == -1:
                    pair2 = hand[y].value
        if (pair1 != pair2 and pair1 != 16 and pair1 != 17 and pair2 != 16 and pair2 != 17):
            return [True, quadValue]
        else:
            return [False, quadValue]

    #return format:
    #
    #returns analyzedPlay[], which is an array of length 3, formatted as follows:
    #analyedPlay[0] = int, which corresponds to the type of play of the hand, as follows:
    #   - 0: Rocket
    #   - 1: Quad (Bomb)
    #   - 2: Quad (Set with pair attachments)
    #   - 3: Quad (Set with single attachments)
    #   - 4: Triplet Sequence with pair attachments
    #   - 5: Triplet Sequence with single attachments
    #   - 6: Triplet Sequence
    #   - 7: Triplet
    #   - 8: Pair Sequence
    #   - 9: Pair
    #   - 10: Single Sequence
    #   - 11: Single
    #analyzedPlay[1] = int, which is the "value" of the play (lowest card in sequence if sequence)
    #analyzedPlay[2] = int, which is the size of the hand
    #
    #Note: perhaps analyzedPlay[2] should be the number of sequence elements needed? we'll have to calculate this anyways
    #
    #External functions that use this function should be able to find a necessary play from these
    def analyze_play(self, hand):
        hand.sort(key = lambda card: card.value)
        totalNumber = len(hand)
        analyzedPlay = [-1, -1, -1]
        #if 1, must be single card
        if len(hand) == 1:
            analyzedPlay = [11, hand[0].value, 1]
            return analyzedPlay

        #if 2, must be pair, or rocket
        elif len(hand) == 2:
            if check_rocket(hand):
                analyzedPlay = [0, 16, 2]
                return analyzedPlay
            else:
                checkedPair = check_pair_sequence(hand)
                if checkedPair[0]:
                    analyzedPlay = [9, checkedPair[1], 2]
                    return analyzedPlay
            #Throw error
            return analyzedPlay

        #if 3, must be triplet
        elif len(hand) == 3:
            checkedTriplet = check_triplet_sequence(hand)
            if checkedTriplet[0]:
                analyzedPlay = [7, checkedTriplet[1], 3]
                return analyzedPlay
            #throw error

        #if 4, could be one of the following:
        # - Triplet with attachment
        # - Bomb
        elif len(hand) == 4:
            checkedBomb = check_bomb(hand)
            checkedTripletSingleAttachment = check_triplet_sequence_attachments(hand, 1)
            if checkedBomb[0]:
                analyzedPlay = [1, checkedBomb[1], 4]
                return analyzedPlay
            elif checkedTripletsSingleAttachment[0]:
                analyzedPlay = [5, checkedTripletSingleAttachment[1], 4]
                return analyzedPlay
            #throw error

        #if 5, could be one of the following:
        # - Triplet with attached pair
        # - Sequence of 5 single cards
        elif len(hand) == 5:
            checkedTripletPairAttachment = check_triplet_sequence_attachments(hand, 1)
            checkedSequence = check_single_sequence(hand)
            if checkedTripletPairAttachment[0]:
                analyzedPlay = [4, checkedTripletPairAttachment[1], 5]
                return analyzedPlay
            elif checkedSequence[0]:
                analyzedPlay = [10, checkedSequence[1], 5]
                return analyzedPlay
            #throw error

        #if 6, could be one of the following:
        # - Sequence of 6 single cards
        # - Sequence of 2 triplets
        # - Sequence of 3 pairs
        # - Quadplex set #1 (bomb with 2 different single cards attached)
        elif len(hand) == 6:
            checkedSequence = check_single_sequence(hand)
            checkedTripletSequence = check_triplet_sequence(hand)
            checkedPairSequence = check_pair_sequence(hand)
            checkedQuadplexSet1 = check_quadplex_set_1(hand)
            if checkedSequence[0]:
                analyzedPlay = [10, checkedSequence[1], 6]
                return analyzedPlay
            elif checkedTripletSequence[0]:
                analyzedPlay = [6, checkedTripletSequence[1], 6]
                return analyzedPlay
            elif checkedPairSequence[0]:
                analyzedPlay = [8, checkedPairSequence[1], 6]
                return analyzedPlay
            elif checkedQuadplexSet1[0]:
                analyzedPlay = [3, checkedQuadplexSet1[1], 6]
                return analyzedPlay
            #throw error

        #if 7, could be one of the following:
        # - Sequence of 7 single cards
        elif len(hand) == 7:
            checkedSequence = check_single_sequence(hand)
            if checkedSequence[0]:
                analyzedPlay = [10, checkedSequence[1], 7]
                return analyzedPlay
            #throw error
        #if 8, could be one of the following:
        # - Sequence of 8 single cards
        # - Sequence of 4 pairs
        # - Sequence of 2 triplets with attached single cards
        # - Quadplex set #2 (bomb with 2 different pairs attached)
        elif len(hand) == 8:
            checkedSequence = check_single_sequence(hand)
            checkedPairSequence = check_pair_sequence(hand)
            checkedTripletSequenceSingleAttachment = check_triplet_sequence_attachments(hand, 2)
            checkedQuadplexSet2 = check_quadplex_set_2(hand)
            if (checkedSequence[0]):
                analyzedPlay = [10, checkedSequence[1], 8]
                return analyzedPlay
            elif checkedPairSequence[0]:
                analyzedPlay = [8, checkedPairSequence[1], 8]
                return analyzedPlay
            #checking triplets w/ attachment sequence
            elif checkedTripletSequenceSingleAttachment[0]:
                analyzedPlay = [5, checkedTripletSequenceSingleAttachment[1], 8]
                return analyzedPlay
            if (checkedQuadplexSet2[0]):
                analyzedPlay = [2, checkedQuadplexSet2[1], 8]
                return analyzedPlay
            #throw error

        #at 9 and after, only the following cases exist:
        # - Sequence of X single cards, up to 12
        # - Sequence of X pairs (at even numbers only), up to 20
        # - Sequence of X triplets with no attachment (multiples of 3 only), up to 18
        # - Sequence of X triplets with single card attachment each (multiples of 4 only), up to 20
        # - Sequence of X triplets with pair attachment each (multiples of 5 only), up to 20
        elif len(hand) > 8 and len(hand) <= 20:
            possibleSingles = (totalNumber <= 12)
            possiblePairs = (totalNumber%2 == 0)
            possibleTriplets = (totalNumber%3 == 0)
            possibleTripletsSingleAttachment = (totalNumber%4 == 0)
            possibleTripletsPairAttachment = (totalNumber%5 == 0)

            if (possibleSingles):
                checkedSequence = check_single_sequence(hand)
                if (checkedSequence[0]):
                    return [10, checkedSequence[1], totalNumber]
            if (possiblePairs):
                checkedPairSequence = check_pair_sequence(hand)
                if (checkedPairSequence[0]):
                    return [8, checkedPairSequence[1], totalNumber]
            if (possibleTriplets):
                checkedTripletSequence = check_triplet_sequence(hand)
                if (checkedTripletSequence[0]):
                    return [6, checkedTripletSequence[1], totalNumber]
            if (possibleTripletsSingleAttachment):
                totalTripletsNeeded = int(totalNumber/4)
                checkedTripletSequenceSingleAttachment = check_triplet_sequence_attachments(hand, totalTripletsNeeded)
                if (checkedTripletSequenceSingleAttachment[0]):
                    return [5, checkedTripletSequenceSingleAttachment[1], totalNumber]
            if (possibleTripletsPairAttachment):
                totalTripletsNeeded = int(totalNumber/5)
                checkedTripletsPairAttachment = check_triplet_sequence_attachments(hand, totalTripletsNeeded)
                if (checkedTripletsPairAttachment[0]):
                    return [4, checkedTripletsPairAttachment[1], totalNumber]
            #throw error if we get here: no matches


    #gets the raw value of a card
    def value_lookup(card):
        table = {
            3: 1,
            4: 2,
            5: 3,
            6: 4,
            7: 5,
            8: 6,
            9: 8,
            10: 10,
            11: 13, #jack
            12: 16, #queen
            13: 20, #king
            14: 25, #ace
            15: 32, #two
            16: 40, #uncolored joker
            17: 50 } #colored joker
        return table.get(card.value, 0)

    turn_penalty = 50 #penalty for taking more turns

    #find expected value of own hand, taking into account different plays that could be made
    def evaluate_hand(self, hand):
        #if hand empty then win
        if (not hand): return 1000000
        poss_plays = valid_plays(self, hand)
        value_of_plays = [evaluate_play(hand, poss_play) for poss_play in poss_plays]
        return max(value_of_plays)
        #this would return the best evaluated play instead
        #return poss_plays[value_of_plays.index(max(value_of_plays))]

    #find expected value of a play based on own hand
    def evaluate_play(self, hand, play):
        leftover_hand = [card for card in hand if card not in play]
        leftover_quality = sum([value_lookup(card) for card in leftover_hand])
        return leftover_quality - turn_penalty + evaluate_hand(leftover_hand)

    #find expected value of a hand, disregarding combinations of cards
    def evaluate_hand_separate(self, hand):
        return sum([value_lookup(card) for card in hand])

    #find expected values of another player's hand in comparison to your own
    #value > 0 means on average the your hand is better than their's
    #value < 0 means on average the your hand is worse than their's
    #requires other player hand size, your hand, and the cards still not played
    def evaluate_other_player(self, other_player_hand_size, hand, unplayed_cards):
        own_value = evaluate_hand_separate(hand)
        total_other_value = evaluate_hand_separate(unplayed_cards)
        other_value = total_other_value * other_player_hand_size / len(unplayed_cards)
        return own_value - other_value

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
