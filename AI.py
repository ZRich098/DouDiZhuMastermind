from itertools import permutations
from Cards import Card
import random
import math

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
                        rocket.append([hand[previousCards], hand[previousCards+1]])
                        isRocket.append([hand[previousCards]])
                        isRocket.append([hand[previousCards+1]])

                    else:
                        single.append([hand[previousCards]])
                elif simplifiedHand[x+1] == 1:
                    single.append([hand[previousCards]])
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
                runningTripletSequence = runningTriplet
                for y in range(7):
                    if ((simplifiedHand[x+y+1] >= 3) and (x+y+1 < 12)):
                        newTriplet = [hand[lookaheadCards], hand[lookaheadCards+1], hand[lookaheadCards+2]]
                        runningTripletSequence = runningTripletSequence + newTriplet
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
                runningPairSequence = runningPair
                for y in range(9):
                    if ((simplifiedHand[x+y+1] >= 2) and (x+y+1 < 12)):
                        newPair = [hand[lookaheadCards], hand[lookaheadCards+1]]
                        runningPairSequence = runningPairSequence + newPair
                        if (len(runningPairSequence) >=3):
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
                        runningSingleSequence= runningSingleSequence + newSingle
                        if (len(runningSingleSequence) >= 5):
                            sequenceSingle.append(list(runningSingleSequence))
                        lookaheadCards = lookaheadCards + simplifiedHand[x+y+1]
                        cardInSequence = True
                    else:
                        break

                #setting single-attachment priority
                if cardInSequence:
                    isSequence.append([hand[previousCards]])
                else:
                    isQuad.append([hand[previousCards]])
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
                runningTripletSequence = runningTriplet
                for y in range(7):
                    if ((simplifiedHand[x+y+1] >= 3) and (x+y+1 < 12)):
                        newTriplet = [hand[lookaheadCards], hand[lookaheadCards+1], hand[lookaheadCards+2]]
                        runningTripletSequence = runningTripletSequence + newTriplet
                        sequenceTriplet.append(runningTripletSequence)
                        lookaheadCards = lookaheadCards + simplifiedHand[x+y+1]
                        cardInSequence = True
                    else:
                        break
                runningPair = [hand[previousCards], hand[previousCards+1]]
                pair.append(runningPair)
                #similar logic to triplet sequences for pair sequences
                #lookaheadCards helps track where the next numerical value of card starts
                lookaheadCards = previousCards + 3
                runningPairSequence = runningPair
                for y in range(9):
                    if ((simplifiedHand[x+y+1] >= 2) and (x+y+1 < 12)):
                        newPair = [hand[lookaheadCards], hand[lookaheadCards+1]]
                        runningPairSequence = runningPairSequence + newPair
                        if (len(runningPairSequence) >=3):
                            sequencePair.append(list(runningPairSequence))
                        lookaheadCards = lookaheadCards + simplifiedHand[x+y+1]
                        cardInSequence = True
                    else:
                        break
                #similar logic for singleton sequences
                lookaheadCards = previousCards + 3
                runningSingleSequence = [hand[previousCards]]
                for y in range(12):
                    if ((simplifiedHand[x+y+1] >= 1) and (x+y+1 < 12)):
                        newSingle = [hand[lookaheadCards]]
                        runningSingleSequence= runningSingleSequence + newSingle
                        if (len(runningSingleSequence) >= 5):
                            sequenceSingle.append(list(runningSingleSequence))
                        lookaheadCards = lookaheadCards + simplifiedHand[x+y+1]
                        cardInSequence = True
                    else:
                        break

                #setting single-attachment priority
                if cardInSequence:
                    isSequence.append([hand[previousCards]])
                else:
                    isTriplet.append([hand[previousCards]])
                previousCards = previousCards + 3

            #If the current hand has 2 copies of the card being scanned
            elif simplifiedHand[x] == 2:
                runningPair = [hand[previousCards], hand[previousCards+1]]
                pair.append(runningPair)
                #similar logic to triplet sequences for pair sequences
                #lookaheadCards helps track where the next numerical value of card starts
                lookaheadCards = previousCards + 2
                runningPairSequence = runningPair
                for y in range(9):
                    if ((simplifiedHand[x+y+1] >= 2) and (x+y+1 < 12)):
                        newPair = [hand[lookaheadCards], hand[lookaheadCards+1]]
                        runningPairSequence = runningPairSequence + newPair
                        if (len(runningPairSequence) >=3):
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
                        runningSingleSequence= runningSingleSequence + newSingle
                        if (len(runningSingleSequence) >= 5):
                            sequenceSingle.append(list(runningSingleSequence))
                        lookaheadCards = lookaheadCards + simplifiedHand[x+y+1]
                        cardInSequence = True
                    else:
                        break

                #setting single-attachment priority
                if cardInSequence:
                    isSequence.append([hand[previousCards]])
                else:
                    isPair.append([hand[previousCards]])
                previousCards = previousCards + 2

            #If current hand only has 1 of the scanned card
            elif simplifiedHand[x] == 1:
                #Only need to check for singleton sequence
                lookaheadCards = previousCards + 1
                runningSingleSequence = [hand[previousCards]]
                for y in range(12):
                    if ((simplifiedHand[x+y+1] >= 1) and (x+y+1 < 12)):
                        newSingle = [hand[lookaheadCards]]
                        runningSingleSequence= runningSingleSequence + newSingle
                        if (len(runningSingleSequence) >= 5):
                            sequenceSingle.append(list(runningSingleSequence))
                        lookaheadCards = lookaheadCards + simplifiedHand[x+y+1]
                        cardInSequence = True
                    else:
                        break

                #setting single-attachment priority
                if cardInSequence:
                    isSequence.append([hand[previousCards]])
                else:
                    single.append([hand[previousCards]])
                previousCards = previousCards + 1

        single = single + isPair + isTriplet + isQuad + isSequence + isRocket
        #single = [single, isPair, isTriplet, isQuad, isSequence, isRocket]
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

    def check_bomb(self, hand):
        bombValue = hand[0].value
        return [(hand[0].value == hand[1].value and hand[0].value == hand[2].value and hand[0].value == hand[3].value), bombValue]

    def check_rocket(self, hand):
        return (hand[len(hand) - 2].value == 16 and hand[len(hand) - 1].value == 17)

    def check_single_sequence(self, hand):
        prevHandValue = -1
        sequenceStart = hand[0].value
        for x in range (len(hand)):
            if hand[x].value == prevHandValue+1 or prevHandValue == -1:
                prevHandValue = hand[x].value
                if x == len(hand) - 1:
                    return [True, sequenceStart]
            else:
                return [False, sequenceStart]

    def check_pair_sequence(self, hand):
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

    def check_triplet_sequence(self, hand):
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

    def check_triplet_sequence_attachments(self, hand, needed):
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
            return [False, sequenceStart]

    def check_quadplex_set_1(self, hand):
        prevHandValue = -1
        totalNumber = len(hand)
        attachment1 = -1
        attachment2 = -1
        quadValue = -1
        for x in range (totalNumber):
            if (x+3 >= totalNumber):
                break
            if (hand[x].value == hand[x+1].value and hand[x].value == hand[x+2].value and hand[x].value == hand[x+3].value):
                quadValue = hand[x].value
                break
        if quadValue == -1:
            return [False, quadValue]
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

    def check_quadplex_set_2(self, hand):
        prevHandValue = -1
        totalNumber = len(hand)
        pair1 = -1
        pair2 = -1
        quadValue = -1
        for x in range (totalNumber):
            if (x+3 >= totalNumber):
                break
            if (hand[x].value == hand[x+1].value and hand[x].value == hand[x+2].value and hand[x].value == hand[x+3].value):
                quadValue = hand[x].value
                break
        if quadValue == -1:
            return [False, quadValue]
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

        #if 0
        if len(hand) == 0:
            return analyzedPlay

        #if 1, must be single card
        if len(hand) == 1:
            analyzedPlay = [11, hand[0].value, 1]
            return analyzedPlay

        #if 2, must be pair, or rocket
        elif len(hand) == 2:
            if self.check_rocket(hand):
                analyzedPlay = [0, 16, 2]
                return analyzedPlay
            else:
                checkedPair = self.check_pair_sequence(hand)
                if checkedPair[0]:
                    analyzedPlay = [9, checkedPair[1], 2]
                    return analyzedPlay
            #Throw error
            return analyzedPlay

        #if 3, must be triplet
        elif len(hand) == 3:
            checkedTriplet = self.check_triplet_sequence(hand)
            if checkedTriplet[0]:
                analyzedPlay = [7, checkedTriplet[1], 3]
                return analyzedPlay
            #throw error

        #if 4, could be one of the following:
        # - Triplet with attachment
        # - Bomb
        elif len(hand) == 4:
            checkedBomb = self.check_bomb(hand)
            checkedTripletSingleAttachment = self.check_triplet_sequence_attachments(hand, 1)
            if checkedBomb[0]:
                analyzedPlay = [1, checkedBomb[1], 4]
                return analyzedPlay
            elif checkedTripletSingleAttachment[0]:
                analyzedPlay = [5, checkedTripletSingleAttachment[1], 4]
                return analyzedPlay
            #throw error

        #if 5, could be one of the following:
        # - Triplet with attached pair
        # - Sequence of 5 single cards
        elif len(hand) == 5:
            checkedTripletPairAttachment = self.check_triplet_sequence_attachments(hand, 1)
            checkedSequence = self.check_single_sequence(hand)
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
            checkedSequence = self.check_single_sequence(hand)
            checkedTripletSequence = self.check_triplet_sequence(hand)
            checkedPairSequence = self.check_pair_sequence(hand)
            checkedQuadplexSet1 = self.check_quadplex_set_1(hand)
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
            checkedSequence = self.check_single_sequence(hand)
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
            checkedSequence = self.check_single_sequence(hand)
            checkedPairSequence = self.check_pair_sequence(hand)
            checkedTripletSequenceSingleAttachment = self.check_triplet_sequence_attachments(hand, 2)
            checkedQuadplexSet2 = self.check_quadplex_set_2(hand)
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
                checkedSequence = self.check_single_sequence(hand)
                if (checkedSequence[0]):
                    return [10, checkedSequence[1], totalNumber]
            if (possiblePairs):
                checkedPairSequence = self.check_pair_sequence(hand)
                if (checkedPairSequence[0]):
                    return [8, checkedPairSequence[1], totalNumber]
            if (possibleTriplets):
                checkedTripletSequence = self.check_triplet_sequence(hand)
                if (checkedTripletSequence[0]):
                    return [6, checkedTripletSequence[1], totalNumber]
            if (possibleTripletsSingleAttachment):
                totalTripletsNeeded = int(totalNumber/4)
                checkedTripletSequenceSingleAttachment = self.check_triplet_sequence_attachments(hand, totalTripletsNeeded)
                if (checkedTripletSequenceSingleAttachment[0]):
                    return [5, checkedTripletSequenceSingleAttachment[1], totalNumber]
            if (possibleTripletsPairAttachment):
                totalTripletsNeeded = int(totalNumber/5)
                checkedTripletsPairAttachment = self.check_triplet_sequence_attachments(hand, totalTripletsNeeded)
                if (checkedTripletsPairAttachment[0]):
                    return [4, checkedTripletsPairAttachment[1], totalNumber]
            #throw error if we get here: no matches

    #takes the current hand and currently on-board play, and returns a list of all legal plays from this state
    #Input FORMATTING NOTE: hand and play must both be lists of cards
    #
    #Return format:
    #combinedPlays[] defined as a list of all legal plays of cards, where each play is a list of cards.
    #Note that this function will return the empty list if there are no legal plays. Functions utilizing combine_play
    #should take note of this case and treat it as no-legal-plays-possible (i.e. needs to pass).
    def combine_play(self, hand, playPre):
        play = []
        for pl in playPre:
            if isinstance(pl, list):
                for plsub in pl:
                    play = play + [plsub]
            else:
                play = play + [pl]

        #THEY SHOULD ALL BE SORTED, DOUBLE CHECK THIS
        analyzedPlay = self.analyze_play(play)
        validPlays = self.valid_plays(hand)
        #separating out plays
        rockets = validPlays[0]
        quads = validPlays[1]
        tripletSequences = validPlays[2]
        triplets = validPlays[3]
        pairSequences = validPlays[4]
        pairs = validPlays[5]
        singleSequences = validPlays[6]
        #note that singles is constructed by concatenation, not multiple lists, so you can access it normally
        singles = validPlays[7]
        
        typeOfPlay = 0
        rankOfPlay = 18
        if (analyzedPlay is not None):
            typeOfPlay = analyzedPlay[0]
            rankOfPlay = analyzedPlay[1]
        #if empty play, can play anything
        if typeOfPlay == -1:
            legalQuadSingles = []
            for x in range (len(quads)):
                if quads[x][0].value > rankOfPlay:
                    for y in range (len(singles)):
                        if singles[y][0].value != quads[x][0].value:
                            for z in range (len(singles)):
                                if singles[z][0].value != quads[x][0].value and singles[z][0].value != singles[y][0].value and (singles[z][0].value + singles[y][0].value < 33):
                                    attachmentPlay = quads[x]+[singles[y][0]]+[singles[z][0]]
                                    legalQuadSingles.append(attachmentPlay)
            legalQuadPairs = []
            for x in range (len(quads)):
                if quads[x][0].value > rankOfPlay:
                    for y in range (len(pairs)):
                        if len(pairs) <=1:
                            break
                        if pairs[y][0].value != quads[x][0].value:
                            for z in range (len(pairs)):
                                if pairs[z][0].value != quads[x][0].value and pairs[z][0].value != pairs[y][0].value:
                                    attachmentPlay = quads[x]+pairs[y]+pairs[z]
                                    legalQuadPairs.append(attachmentPlay)
            legalTripletSingleSequences = []
            for x in range (len(tripletSequences)):
                usedNumbers = []
                for a in range (0, len(tripletSequences[x]), 3):
                    usedNumbers.append(tripletSequences[x][a].value)
                neededSingles = int(len(tripletSequences[x])/4)
                foundSingles = []
                for y in range (len(singles)):
                    if usedNumbers.count(singles[y][0].value) == 0:
                        foundSingles.append(singles[y][0])
                if len(foundSingles) >= neededSingles:
                    perm = permutations(foundSingles, neededSingles)
                    for i in perm:
                        attachmentPlay = tripletSequences[x]+list(i)
                        legalTripletSingleSequences.append(attachmentPlay)
            legalTripletSingles = []
            for x in range (len(triplets)):
                if (triplets[x][0].value > rankOfPlay):
                    usedNumbers = []
                    for a in range (0, len(triplets[x]), 3):
                        usedNumbers.append(triplets[x][a].value)
                    neededSingles = 1
                    foundSingles = []
                    for y in range (len(singles)):
                        if usedNumbers.count(singles[y][0].value) == 0:
                            foundSingles.append(singles[y][0])
                    if len(foundSingles) >= neededSingles:
                        perm = permutations(foundSingles, neededSingles)
                        for i in perm:
                            attachmentPlay = triplets[x]+list(i)
                            legalTripletSingles.append(attachmentPlay)
            legalTripletPairSequences = []
            for x in range (len(tripletSequences)):
                if (tripletSequences[x][0].value > rankOfPlay):
                    usedNumbers = []
                    for a in range (0, len(tripletSequences[x]), 3):
                        usedNumbers.append(tripletSequences[x][a].value)
                    neededPairs = int(len(tripletSequences[x])/5)
                    foundPairs = []
                    for y in range (len(pairs)):
                        if usedNumbers.count(pairs[y][0].value) == 0:
                            foundPairs.append(pairs[y])
                    if len(foundPairs) >= neededPairs:
                        finalFoundPairs = []
                        perm = permutations(foundPairs, neededPairs)
                        for i in perm:
                            i2 = list(i)
                            attachmentPlay = tripletSequences[x]
                            for j in range (len(i2)):
                                attachmentPlay = attachmentPlay + i2[j]
                            legalTripletPairSequences.append(attachmentPlay)
            legalTripletPairs = []
            for x in range (len(triplets)):
                if (triplets[x][0].value > rankOfPlay):
                    usedNumbers = []
                    for a in range (0, len(triplets[x]), 3):
                        usedNumbers.append(triplets[x][a].value)
                    neededPairs = 1
                    foundPairs = []
                    for y in range (len(pairs)):
                        if usedNumbers.count(pairs[y][0].value) == 0:
                            foundPairs.append(pairs[y])
                    if len(foundPairs) >= neededPairs:
                        finalFoundPairs = []
                        perm = permutations(foundPairs, neededPairs)
                        for i in perm:
                            i2 = list(i)
                            attachmentPlay = triplets[x]
                            for j in range (len(i2)):
                                attachmentPlay = attachmentPlay + i2[j]
                            legalTripletPairs.append(attachmentPlay)
            return rockets + quads + legalQuadSingles + legalQuadPairs + legalTripletPairSequences + legalTripletPairs + legalTripletSingleSequences + legalTripletSingles + tripletSequences + triplets + pairSequences + pairs + singleSequences + singles

        #rocket: Can't be beaten
        if typeOfPlay == 0:
            return []
        #quad(bomb): Beaten by higher bombs or rockets
        if typeOfPlay == 1:
            legalQuads = []
            for x in range (len(quads)):
                if quads[x][0].value > rankOfPlay:
                    legalQuads.append(quads[x])
            return rockets + legalQuads
        #quad(pair attachments): beaten by higher quad-pair sets, any bombs, or rockets
        if typeOfPlay == 2:
            legalQuadPairs = []
            for x in range (len(quads)):
                if quads[x][0].value > rankOfPlay:
                    for y in range (len(pairs)):
                        if len(pairs) <=1:
                            break
                        if pairs[y][0].value != quads[x][0].value:
                            for z in range (len(pairs)):
                                if pairs[z][0].value != quads[x][0].value and pairs[z][0].value != pairs[y][0].value:
                                    attachmentPlay = quads[x]+pairs[y]+pairs[z]
                                    legalQuadPairs.append(attachmentPlay)
            return rockets + quads + legalQuadPairs
        #quad(single attachments): beaten by higher quad-single sets, any bombs, or rockets
        if typeOfPlay == 3:
            legalQuadSingles = []
            for x in range (len(quads)):
                if quads[x][0].value > rankOfPlay:
                    for y in range (len(singles)):
                        if singles[y][0].value != quads[x][0].value:
                            for z in range (len(singles)):
                                if singles[z][0].value != quads[x][0].value and singles[z][0].value != singles[y][0].value and (singles[z][0].value + singles[y][0].value < 33):
                                    attachmentPlay = quads[x]+[singles[y]]+[singles[z]]
                                    legalQuadSingles.append(attachmentPlay)
            return rockets + quads + legalQuadSingles
        #triplet sequence with pair attachments: beaten by higher rank same-length pair-attached sequences, and bombs/rockets
        if typeOfPlay == 4:
            legalTripletPairSequences = []
            if analyzedPlay[2] == 5:
                tripletSequences = triplets
            for x in range (len(tripletSequences)):
                if (tripletSequences[x][0].value > rankOfPlay) and (len(tripletSequences[x]) == (int(len(play)/5)*3)):
                    usedNumbers = []
                    for a in range (0, len(tripletSequences[x]), 3):
                        usedNumbers.append(tripletSequences[x][a].value)
                    neededPairs = int(len(play)/5)
                    foundPairs = []
                    for y in range (len(pairs)):
                        if usedNumbers.count(pairs[y][0].value) == 0:
                            foundPairs.append(pairs[y])
                    if len(foundPairs) >= neededPairs:
                        finalFoundPairs = []
                        perm = permutations(foundPairs, neededPairs)
                        for i in perm:
                            i2 = list(i)
                            attachmentPlay = tripletSequences[x]
                            for j in range (len(i2)):
                                attachmentPlay = attachmentPlay + i2[j]
                            legalTripletPairSequences.append(attachmentPlay)
            return rockets + quads + legalTripletPairSequences
        '''
        if typeOfPlay == 4:
            legalTripletPairSequences = []
            if analyzedPlay[2] == 5:
                tripletSequences = triplets
            for x in range (len(tripletSequences)):
                if (tripletSequences[x][0].value > rankOfPlay) and (len(tripletSequences[x]) == (int(len(play)/5)*3)):
                    usedNumbers = []
                    for a in range (0, len(tripletSequences[x]), 3):
                        usedNumbers.append(tripletSequences[x][a].value)
                    neededPairs = int(len(play)/5)
                    foundPairs = []
                    for y in range (len(pairs)):
                        if usedNumbers.count(pairs[y][0].value) == 0:
                            foundPairs.append(pairs[y])
                    if len(foundPairs) >= neededPairs:
                        finalFoundPairs = []
                        for r in range (len(foundPairs)):
                            firstPair = foundPairs[r]
                            finalFoundPairs.append(firstPair)
                            if (len(finalFoundPairs) == neededPairs):
                                attachmentPlay = tripletSequences[x]+finalFoundPairs[0]
                                legalTripletPairSequences.append(attachmentPlay)
                                finalFoundPairs.pop()
                            else:
                                for j in range (r+1, len(foundPairs)):
                                    nextPair = foundPairs[j]
                                    finalFoundPairs.append(nextPair)
                                    if (len(finalFoundPairs) == neededPairs):
                                        attachmentPlay = tripletSequences[x]+finalFoundPairs[0]+finalFoundPairs[1]
                                        legalTripletPairSequences.append(attachmentPlay)
                                        finalFoundPairs.pop()
                                    else:
                                        for k in range (j+1, len(foundPairs)):
                                            nextPair = foundPairs[k]
                                            finalFoundPairs.append(nextPair)
                                            if (len(finalFoundPairs) == neededPairs):
                                                attachmentPlay = tripletSequences[x]+finalFoundPairs[0]+finalFoundPairs[1]+finalFoundPairs[2]
                                                legalTripletPairSequences.append(attachmentPlay)
                                                finalFoundPairs.pop()
                                            else:
                                                for l in range (k+1, len(foundPairs)):
                                                    nextPair = foundPairs[l]
                                                    finalFoundPairs.append(nextPair)
                                                    if (len(finalFoundPairs) == neededPairs):
                                                        attachmentPlay = tripletSequences[x]+finalFoundPairs[0]+finalFoundPairs[1]+finalFoundPairs[2]+finalFoundPairs[3]
                                                        legalTripletPairSequences.append(attachmentPlay)
                                                        finalFoundPairs.pop()
                                                finalFoundPairs.pop()
                                        finalFoundPairs.pop()
                                finalFoundPairs.pop()
            return rockets + quads + legalTripletPairSequences
            '''
        #Triplet sequence with single attachment, beatable by higher ranked triplet-with-single or rocket/bomb
        if typeOfPlay == 5:
            legalTripletSingleSequences = []
            if analyzedPlay[2] == 4:
                tripletSequences = triplets
                for x in range (len(tripletSequences)):
                    if (tripletSequences[x][0].value > rankOfPlay) and (len(tripletSequences[x]) == (int(len(play)/4)*3)):
                        usedNumbers = []
                        for a in range (0, len(tripletSequences[x]), 3):
                            usedNumbers.append(tripletSequences[x][a].value)
                        neededSingles = int(len(play)/4)
                        foundSingles = []
                        for y in range (len(singles)):
                            if usedNumbers.count(singles[y][0].value) == 0:
                                foundSingles.append(singles[y])
                        if len(foundSingles) >= neededSingles:
                            perm = permutations(foundSingles, neededSingles)
                            for i in perm:
                                if isinstance(i, list):
                                    attachmentPlay = tripletSequences[x]+i
                                    legalTripletSingleSequences.append(attachmentPlay)
                                else:
                                    attachmentPlay = tripletSequences[x]+list(i)
                                    legalTripletSingleSequences.append(attachmentPlay)
            else:
                for x in range (len(tripletSequences)):
                    if (tripletSequences[x][0].value > rankOfPlay) and (len(tripletSequences[x]) == (int(len(play)/4)*3)):
                        usedNumbers = []
                        for a in range (0, len(tripletSequences[x]), 3):
                            usedNumbers.append(tripletSequences[x][a].value)
                        neededSingles = int(len(play)/4)
                        foundSingles = []
                        for y in range (len(singles)):
                            if usedNumbers.count(singles[y][0].value) == 0:
                                foundSingles.append(singles[y])
                        if len(foundSingles) >= neededSingles:
                            perm = permutations(foundSingles, neededSingles)
                            for i in perm:
                                attachmentPlay = tripletSequences[x]+list(i)
                                legalTripletSingleSequences.append(attachmentPlay)
            return rockets + quads + legalTripletSingleSequences
        #standard triplet sequence
        if typeOfPlay == 6:
            legalTripletSequences = []
            for x in range (len(tripletSequences)):
                if tripletSequences[x][0].value > rankOfPlay:
                    legalTripletSequences.append(tripletSequences[x])
            return rockets + quads + legalTripletSequences
        #single triplet
        if typeOfPlay == 7:
            legalTriplets = []
            for x in range (len(triplets)):
                if triplets[x][0].value > rankOfPlay:
                    legalTriplets.append(triplets[x])
            return rockets + quads + legalTriplets
        #pair sequence
        if typeOfPlay == 8:
            legalPairSequences = []
            for x in range (len(pairSequences)):
                if pairSequences[x][0].value > rankOfPlay and len(pairSequences[x]) == len(play):
                    legalPairSequences.append(pairSequences[x])
            return rockets + quads + legalPairSequences

        #pair
        if typeOfPlay == 9:
            legalPairs = []
            for x in range (len(pairs)):
                if pairs[x][0].value > rankOfPlay:
                    legalPairs.append(pairs[x])
            return rockets + quads + legalPairs
        #single sequence
        if typeOfPlay == 10:
            legalSingleSequences = []
            for x in range (len(singleSequences)):
                if singleSequences[x][0].value > rankOfPlay and len(singleSequences[x]) == len(play):
                    legalSingleSequences.append(singleSequences[x])
            return rockets + quads + legalSingleSequences
        #singles
        if typeOfPlay == 11:
            legalSingles = []
            for x in range (len(singles)):
                if singles[x][0].value > rankOfPlay:
                    legalSingles.append(singles[x])
            return rockets + quads + legalSingles
        
        if (rockets is not None):
            return rockets
        else:
            return []
        
    #gets the raw value of a card
    def value_lookup(self, card):
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

    #play numbers in order starting from 0
    #plays = [[rocket], [quad], [sequenceTriplet], [triplet], [sequencePair], [pair], [sequenceSingle], [single]]
    def play_lookup(self,play_number,length):
        table = {
            0: 50,
            1: 45,
            2: length*8,
            3: 10,
            4: length*8,
            5: 5,
            6: length*9,
            7: 0}
        return table.get(play_number,0)

    #find the estimated value of a hand to use as a base in evaluation
    def evaluation_heuristic(self, hand):
        plays = self.valid_plays(hand)
        sum_plays = 0
        for x in range(len(plays)):
            for y in plays[x]:
                sum_plays = sum_plays + self.play_lookup(x,len(y))
        sum_cards = self.evaluate_hand_separate(hand)
        length_penalty = len(hand)*110
        if (length_penalty == 0):
            return 1000000
        return sum_plays + sum_cards - length_penalty

    def to_plays_array(self, array):
        arr = []
        for e in array:
            if (isinstance(e, list)):
                for sube in e:
                    if (isinstance(sube, list)):
                        arr.append(sube)
                    else:
                        arr.append(e)
            else:
                arr.append(e)
        return arr

    #find expected value of own hand, taking into account different plays that could be made
    def evaluate_hand(self, hand,unplayed_cards,others_data, depth):
        #if hand empty then win
        if (not hand): return 1000000
        poss_plays = self.to_plays_array(self.valid_plays(hand))
        value_of_plays = [self.evaluate_play(hand, poss_play,unplayed_cards,others_data, depth) for poss_play in poss_plays]
        return max(value_of_plays)

    #returns a (play, value) pair of expected values of plays
    def evaluate_hand_dict(self, hand):
        #if hand empty then win
        if (not hand): return 1000000
        poss_plays = self.to_plays_array(self.valid_plays(hand))
        value_of_plays = [self.evaluate_play(hand, poss_play) for poss_play in poss_plays]
        return dict(zip(poss_play, value_of_plays))

    #find expected value of own hand, taking into account different plays
    #that could be made on the current board
    def evaluate_hand_given_play(self, hand, play):
        #if hand empty then win
        if (not hand): return 1000000
        poss_plays = self.combine_play(hand, play)
        value_of_plays = [self.evaluate_play(hand, poss_play) for poss_play in poss_plays]
        return max(value_of_plays)

    #find expected value of a play based on own hand
    def evaluate_play(self, hand, play, unplayed_cards,others_data, depth):
        leftover_hand = [card for card in hand if card not in play]
        leftover_quality = sum([self.value_lookup(card) for card in leftover_hand])
        if (depth == 0):
            return leftover_quality - 50 + self.evaluation_heuristic(leftover_hand)
        (next_player, player_after) = others_data
        (next_size, next_allegiance) = next_player
        (after_size, after_allegiance) = player_after
        next_player_quality = self.evaluate_other_player(next_size, hand, unplayed_cards)
        player_after_quality = self.evaluate_other_player(after_size, hand, unplayed_cards)
        total = leftover_quality - 50
        if next_allegiance:
            total = total + next_player_quality
        else: total = total - next_player_quality
        if after_allegiance:
            total = total + player_after_quality
        else: total = total - player_after_quality
        return total + self.evaluate_hand(leftover_hand,unplayed_cards,others_data, depth - 1)

    #find expected value of a hand, disregarding combinations of cards
    def evaluate_hand_separate(self, hand):
        return sum([self.value_lookup(card) for card in hand])

    #find expected values of another player's hand in comparison to your own
    #value > 0 means on average the your hand is better than their's
    #value < 0 means on average the your hand is worse than their's
    #requires other player hand size, your hand, and the cards still not played
    def evaluate_other_player(self, other_player_hand_size, hand, unplayed_cards):
        own_value = self.evaluate_hand_separate(hand)
        total_other_value = self.evaluate_hand_separate(unplayed_cards)
        other_value = total_other_value * other_player_hand_size / len(unplayed_cards)
        return own_value - other_value

    #return the best move based on expectimax
    #others_data is a tuple of tuples:
    #((next player's hand size, other player's allegiance),(player after's hand size, player after's allegiance))
    def get_move(self, hand, unplayed_cards, others_data, play):
        poss_plays = self.combine_play(hand, play)
        if (not poss_plays): return []
        value_of_plays = [self.evaluate_play(hand, poss_play, unplayed_cards, others_data, 3) for poss_play in poss_plays]
        max_index = value_of_plays.index(max(value_of_plays))
        return poss_plays[max_index]

class HillClimbAI:
    def __init__(self, order):
        self.order = order
        self.str = 'HillClimbAI ' + str(order)

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
                        rocket.append([hand[previousCards], hand[previousCards+1]])
                        isRocket.append([hand[previousCards]])
                        isRocket.append([hand[previousCards+1]])

                    else:
                        single.append([hand[previousCards]])
                elif simplifiedHand[x+1] == 1:
                    single.append([hand[previousCards]])
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
                runningTripletSequence = runningTriplet
                for y in range(7):
                    if ((simplifiedHand[x+y+1] >= 3) and (x+y+1 < 12)):
                        newTriplet = [hand[lookaheadCards], hand[lookaheadCards+1], hand[lookaheadCards+2]]
                        runningTripletSequence = runningTripletSequence + newTriplet
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
                runningPairSequence = runningPair
                for y in range(9):
                    if ((simplifiedHand[x+y+1] >= 2) and (x+y+1 < 12)):
                        newPair = [hand[lookaheadCards], hand[lookaheadCards+1]]
                        runningPairSequence = runningPairSequence + newPair
                        if (len(runningPairSequence) >=3):
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
                        runningSingleSequence= runningSingleSequence + newSingle
                        if (len(runningSingleSequence) >= 5):
                            sequenceSingle.append(list(runningSingleSequence))
                        lookaheadCards = lookaheadCards + simplifiedHand[x+y+1]
                        cardInSequence = True
                    else:
                        break

                #setting single-attachment priority
                if cardInSequence:
                    isSequence.append([hand[previousCards]])
                else:
                    isQuad.append([hand[previousCards]])
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
                runningTripletSequence = runningTriplet
                for y in range(7):
                    if ((simplifiedHand[x+y+1] >= 3) and (x+y+1 < 12)):
                        newTriplet = [hand[lookaheadCards], hand[lookaheadCards+1], hand[lookaheadCards+2]]
                        runningTripletSequence = runningTripletSequence + newTriplet
                        sequenceTriplet.append(runningTripletSequence)
                        lookaheadCards = lookaheadCards + simplifiedHand[x+y+1]
                        cardInSequence = True
                    else:
                        break
                runningPair = [hand[previousCards], hand[previousCards+1]]
                pair.append(runningPair)
                #similar logic to triplet sequences for pair sequences
                #lookaheadCards helps track where the next numerical value of card starts
                lookaheadCards = previousCards + 3
                runningPairSequence = runningPair
                for y in range(9):
                    if ((simplifiedHand[x+y+1] >= 2) and (x+y+1 < 12)):
                        newPair = [hand[lookaheadCards], hand[lookaheadCards+1]]
                        runningPairSequence = runningPairSequence + newPair
                        if (len(runningPairSequence) >=3):
                            sequencePair.append(list(runningPairSequence))
                        lookaheadCards = lookaheadCards + simplifiedHand[x+y+1]
                        cardInSequence = True
                    else:
                        break
                #similar logic for singleton sequences
                lookaheadCards = previousCards + 3
                runningSingleSequence = [hand[previousCards]]
                for y in range(12):
                    if ((simplifiedHand[x+y+1] >= 1) and (x+y+1 < 12)):
                        newSingle = [hand[lookaheadCards]]
                        runningSingleSequence= runningSingleSequence + newSingle
                        if (len(runningSingleSequence) >= 5):
                            sequenceSingle.append(list(runningSingleSequence))
                        lookaheadCards = lookaheadCards + simplifiedHand[x+y+1]
                        cardInSequence = True
                    else:
                        break

                #setting single-attachment priority
                if cardInSequence:
                    isSequence.append([hand[previousCards]])
                else:
                    isTriplet.append([hand[previousCards]])
                previousCards = previousCards + 3

            #If the current hand has 2 copies of the card being scanned
            elif simplifiedHand[x] == 2:
                runningPair = [hand[previousCards], hand[previousCards+1]]
                pair.append(runningPair)
                #similar logic to triplet sequences for pair sequences
                #lookaheadCards helps track where the next numerical value of card starts
                lookaheadCards = previousCards + 2
                runningPairSequence = runningPair
                for y in range(9):
                    if ((simplifiedHand[x+y+1] >= 2) and (x+y+1 < 12)):
                        newPair = [hand[lookaheadCards], hand[lookaheadCards+1]]
                        runningPairSequence = runningPairSequence + newPair
                        if (len(runningPairSequence) >=3):
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
                        runningSingleSequence= runningSingleSequence + newSingle
                        if (len(runningSingleSequence) >= 5):
                            sequenceSingle.append(list(runningSingleSequence))
                        lookaheadCards = lookaheadCards + simplifiedHand[x+y+1]
                        cardInSequence = True
                    else:
                        break

                #setting single-attachment priority
                if cardInSequence:
                    isSequence.append([hand[previousCards]])
                else:
                    isPair.append([hand[previousCards]])
                previousCards = previousCards + 2

            #If current hand only has 1 of the scanned card
            elif simplifiedHand[x] == 1:
                #Only need to check for singleton sequence
                lookaheadCards = previousCards + 1
                runningSingleSequence = [hand[previousCards]]
                for y in range(12):
                    if ((simplifiedHand[x+y+1] >= 1) and (x+y+1 < 12)):
                        newSingle = [hand[lookaheadCards]]
                        runningSingleSequence= runningSingleSequence + newSingle
                        if (len(runningSingleSequence) >= 5):
                            sequenceSingle.append(list(runningSingleSequence))
                        lookaheadCards = lookaheadCards + simplifiedHand[x+y+1]
                        cardInSequence = True
                    else:
                        break

                #setting single-attachment priority
                if cardInSequence:
                    isSequence.append([hand[previousCards]])
                else:
                    single.append([hand[previousCards]])
                previousCards = previousCards + 1

        single = single + isPair + isTriplet + isQuad + isSequence + isRocket
        #single = [single, isPair, isTriplet, isQuad, isSequence, isRocket]
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

    def check_bomb(self, hand):
        bombValue = hand[0].value
        return [(hand[0].value == hand[1].value and hand[0].value == hand[2].value and hand[0].value == hand[3].value), bombValue]

    def check_rocket(self, hand):
        return (hand[len(hand) - 2].value == 16 and hand[len(hand) - 1].value == 17)

    def check_single_sequence(self, hand):
        prevHandValue = -1
        sequenceStart = hand[0].value
        for x in range (len(hand)):
            if hand[x].value == prevHandValue+1 or prevHandValue == -1:
                prevHandValue = hand[x].value
                if x == len(hand) - 1:
                    return [True, sequenceStart]
            else:
                return [False, sequenceStart]

    def check_pair_sequence(self, hand):
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

    def check_triplet_sequence(self, hand):
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

    def check_triplet_sequence_attachments(self, hand, needed):
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
            return [False, sequenceStart]

    def check_quadplex_set_1(self, hand):
        prevHandValue = -1
        totalNumber = len(hand)
        attachment1 = -1
        attachment2 = -1
        quadValue = -1
        for x in range (totalNumber):
            if (x+3 >= totalNumber):
                break
            if (hand[x].value == hand[x+1].value and hand[x].value == hand[x+2].value and hand[x].value == hand[x+3].value):
                quadValue = hand[x].value
                break
        if quadValue == -1:
            return [False, quadValue]
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

    def check_quadplex_set_2(self, hand):
        prevHandValue = -1
        totalNumber = len(hand)
        pair1 = -1
        pair2 = -1
        quadValue = -1
        for x in range (totalNumber):
            if (x+3 >= totalNumber):
                break
            if (hand[x].value == hand[x+1].value and hand[x].value == hand[x+2].value and hand[x].value == hand[x+3].value):
                quadValue = hand[x].value
                break
        if quadValue == -1:
            return [False, quadValue]
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

        #if 0
        if len(hand) == 0:
            return analyzedPlay

        #if 1, must be single card
        if len(hand) == 1:
            analyzedPlay = [11, hand[0].value, 1]
            return analyzedPlay

        #if 2, must be pair, or rocket
        elif len(hand) == 2:
            if self.check_rocket(hand):
                analyzedPlay = [0, 16, 2]
                return analyzedPlay
            else:
                checkedPair = self.check_pair_sequence(hand)
                if checkedPair[0]:
                    analyzedPlay = [9, checkedPair[1], 2]
                    return analyzedPlay
            #Throw error
            return analyzedPlay

        #if 3, must be triplet
        elif len(hand) == 3:
            checkedTriplet = self.check_triplet_sequence(hand)
            if checkedTriplet[0]:
                analyzedPlay = [7, checkedTriplet[1], 3]
                return analyzedPlay
            #throw error

        #if 4, could be one of the following:
        # - Triplet with attachment
        # - Bomb
        elif len(hand) == 4:
            checkedBomb = self.check_bomb(hand)
            checkedTripletSingleAttachment = self.check_triplet_sequence_attachments(hand, 1)
            if checkedBomb[0]:
                analyzedPlay = [1, checkedBomb[1], 4]
                return analyzedPlay
            elif checkedTripletSingleAttachment[0]:
                analyzedPlay = [5, checkedTripletSingleAttachment[1], 4]
                return analyzedPlay
            #throw error

        #if 5, could be one of the following:
        # - Triplet with attached pair
        # - Sequence of 5 single cards
        elif len(hand) == 5:
            checkedTripletPairAttachment = self.check_triplet_sequence_attachments(hand, 1)
            checkedSequence = self.check_single_sequence(hand)
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
            checkedSequence = self.check_single_sequence(hand)
            checkedTripletSequence = self.check_triplet_sequence(hand)
            checkedPairSequence = self.check_pair_sequence(hand)
            checkedQuadplexSet1 = self.check_quadplex_set_1(hand)
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
            checkedSequence = self.check_single_sequence(hand)
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
            checkedSequence = self.check_single_sequence(hand)
            checkedPairSequence = self.check_pair_sequence(hand)
            checkedTripletSequenceSingleAttachment = self.check_triplet_sequence_attachments(hand, 2)
            checkedQuadplexSet2 = self.check_quadplex_set_2(hand)
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
                checkedSequence = self.check_single_sequence(hand)
                if (checkedSequence[0]):
                    return [10, checkedSequence[1], totalNumber]
            if (possiblePairs):
                checkedPairSequence = self.check_pair_sequence(hand)
                if (checkedPairSequence[0]):
                    return [8, checkedPairSequence[1], totalNumber]
            if (possibleTriplets):
                checkedTripletSequence = self.check_triplet_sequence(hand)
                if (checkedTripletSequence[0]):
                    return [6, checkedTripletSequence[1], totalNumber]
            if (possibleTripletsSingleAttachment):
                totalTripletsNeeded = int(totalNumber/4)
                checkedTripletSequenceSingleAttachment = self.check_triplet_sequence_attachments(hand, totalTripletsNeeded)
                if (checkedTripletSequenceSingleAttachment[0]):
                    return [5, checkedTripletSequenceSingleAttachment[1], totalNumber]
            if (possibleTripletsPairAttachment):
                totalTripletsNeeded = int(totalNumber/5)
                checkedTripletsPairAttachment = self.check_triplet_sequence_attachments(hand, totalTripletsNeeded)
                if (checkedTripletsPairAttachment[0]):
                    return [4, checkedTripletsPairAttachment[1], totalNumber]
            #throw error if we get here: no matches

    #takes the current hand and currently on-board play, and returns a list of all legal plays from this state
    #Input FORMATTING NOTE: hand and play must both be lists of cards
    #
    #Return format:
    #combinedPlays[] defined as a list of all legal plays of cards, where each play is a list of cards.
    #Note that this function will return the empty list if there are no legal plays. Functions utilizing combine_play
    #should take note of this case and treat it as no-legal-plays-possible (i.e. needs to pass).
    def combine_play(self, hand, playPre):
        play = []
        for pl in playPre:
            if isinstance(pl, list):
                for plsub in pl:
                    play = play + [plsub]
            else:
                play = play + [pl]

        #THEY SHOULD ALL BE SORTED, DOUBLE CHECK THIS
        analyzedPlay = self.analyze_play(play)
        validPlays = self.valid_plays(hand)
        #separating out plays
        rockets = validPlays[0]
        quads = validPlays[1]
        tripletSequences = validPlays[2]
        triplets = validPlays[3]
        pairSequences = validPlays[4]
        pairs = validPlays[5]
        singleSequences = validPlays[6]
        #note that singles is constructed by concatenation, not multiple lists, so you can access it normally
        singles = validPlays[7]
        
        typeOfPlay = 0
        rankOfPlay = 18
        if (analyzedPlay is not None):
            typeOfPlay = analyzedPlay[0]
            rankOfPlay = analyzedPlay[1]
        #if empty play, can play anything
        if typeOfPlay == -1:
            legalQuadSingles = []
            for x in range (len(quads)):
                if quads[x][0].value > rankOfPlay:
                    for y in range (len(singles)):
                        if singles[y][0].value != quads[x][0].value:
                            for z in range (len(singles)):
                                if singles[z][0].value != quads[x][0].value and singles[z][0].value != singles[y][0].value and (singles[z][0].value + singles[y][0].value < 33):
                                    attachmentPlay = quads[x]+[singles[y][0]]+[singles[z][0]]
                                    legalQuadSingles.append(attachmentPlay)
            legalQuadPairs = []
            for x in range (len(quads)):
                if quads[x][0].value > rankOfPlay:
                    for y in range (len(pairs)):
                        if len(pairs) <=1:
                            break
                        if pairs[y][0].value != quads[x][0].value:
                            for z in range (len(pairs)):
                                if pairs[z][0].value != quads[x][0].value and pairs[z][0].value != pairs[y][0].value:
                                    attachmentPlay = quads[x]+pairs[y]+pairs[z]
                                    legalQuadPairs.append(attachmentPlay)
            legalTripletSingleSequences = []
            for x in range (len(tripletSequences)):
                usedNumbers = []
                for a in range (0, len(tripletSequences[x]), 3):
                    usedNumbers.append(tripletSequences[x][a].value)
                neededSingles = int(len(tripletSequences[x])/4)
                foundSingles = []
                for y in range (len(singles)):
                    if usedNumbers.count(singles[y][0].value) == 0:
                        foundSingles.append(singles[y][0])
                if len(foundSingles) >= neededSingles:
                    perm = permutations(foundSingles, neededSingles)
                    for i in perm:
                        attachmentPlay = tripletSequences[x]+list(i)
                        legalTripletSingleSequences.append(attachmentPlay)
            legalTripletSingles = []
            for x in range (len(triplets)):
                if (triplets[x][0].value > rankOfPlay):
                    usedNumbers = []
                    for a in range (0, len(triplets[x]), 3):
                        usedNumbers.append(triplets[x][a].value)
                    neededSingles = 1
                    foundSingles = []
                    for y in range (len(singles)):
                        if usedNumbers.count(singles[y][0].value) == 0:
                            foundSingles.append(singles[y][0])
                    if len(foundSingles) >= neededSingles:
                        perm = permutations(foundSingles, neededSingles)
                        for i in perm:
                            attachmentPlay = triplets[x]+list(i)
                            legalTripletSingles.append(attachmentPlay)
            legalTripletPairSequences = []
            for x in range (len(tripletSequences)):
                if (tripletSequences[x][0].value > rankOfPlay):
                    usedNumbers = []
                    for a in range (0, len(tripletSequences[x]), 3):
                        usedNumbers.append(tripletSequences[x][a].value)
                    neededPairs = int(len(tripletSequences[x])/5)
                    foundPairs = []
                    for y in range (len(pairs)):
                        if usedNumbers.count(pairs[y][0].value) == 0:
                            foundPairs.append(pairs[y])
                    if len(foundPairs) >= neededPairs:
                        finalFoundPairs = []
                        perm = permutations(foundPairs, neededPairs)
                        for i in perm:
                            i2 = list(i)
                            attachmentPlay = tripletSequences[x]
                            for j in range (len(i2)):
                                attachmentPlay = attachmentPlay + i2[j]
                            legalTripletPairSequences.append(attachmentPlay)
            legalTripletPairs = []
            for x in range (len(triplets)):
                if (triplets[x][0].value > rankOfPlay):
                    usedNumbers = []
                    for a in range (0, len(triplets[x]), 3):
                        usedNumbers.append(triplets[x][a].value)
                    neededPairs = 1
                    foundPairs = []
                    for y in range (len(pairs)):
                        if usedNumbers.count(pairs[y][0].value) == 0:
                            foundPairs.append(pairs[y])
                    if len(foundPairs) >= neededPairs:
                        finalFoundPairs = []
                        perm = permutations(foundPairs, neededPairs)
                        for i in perm:
                            i2 = list(i)
                            attachmentPlay = triplets[x]
                            for j in range (len(i2)):
                                attachmentPlay = attachmentPlay + i2[j]
                            legalTripletPairs.append(attachmentPlay)
            return rockets + quads + legalQuadSingles + legalQuadPairs + legalTripletPairSequences + legalTripletPairs + legalTripletSingleSequences + legalTripletSingles + tripletSequences + triplets + pairSequences + pairs + singleSequences + singles

        #rocket: Can't be beaten
        if typeOfPlay == 0:
            return []
        #quad(bomb): Beaten by higher bombs or rockets
        if typeOfPlay == 1:
            legalQuads = []
            for x in range (len(quads)):
                if quads[x][0].value > rankOfPlay:
                    legalQuads.append(quads[x])
            return rockets + legalQuads
        #quad(pair attachments): beaten by higher quad-pair sets, any bombs, or rockets
        if typeOfPlay == 2:
            legalQuadPairs = []
            for x in range (len(quads)):
                if quads[x][0].value > rankOfPlay:
                    for y in range (len(pairs)):
                        if len(pairs) <=1:
                            break
                        if pairs[y][0].value != quads[x][0].value:
                            for z in range (len(pairs)):
                                if pairs[z][0].value != quads[x][0].value and pairs[z][0].value != pairs[y][0].value:
                                    attachmentPlay = quads[x]+pairs[y]+pairs[z]
                                    legalQuadPairs.append(attachmentPlay)
            return rockets + quads + legalQuadPairs
        #quad(single attachments): beaten by higher quad-single sets, any bombs, or rockets
        if typeOfPlay == 3:
            legalQuadSingles = []
            for x in range (len(quads)):
                if quads[x][0].value > rankOfPlay:
                    for y in range (len(singles)):
                        if singles[y][0].value != quads[x][0].value:
                            for z in range (len(singles)):
                                if singles[z][0].value != quads[x][0].value and singles[z][0].value != singles[y][0].value and (singles[z][0].value + singles[y][0].value < 33):
                                    attachmentPlay = quads[x]+[singles[y]]+[singles[z]]
                                    legalQuadSingles.append(attachmentPlay)
            return rockets + quads + legalQuadSingles
        #triplet sequence with pair attachments: beaten by higher rank same-length pair-attached sequences, and bombs/rockets
        if typeOfPlay == 4:
            legalTripletPairSequences = []
            if analyzedPlay[2] == 5:
                tripletSequences = triplets
            for x in range (len(tripletSequences)):
                if (tripletSequences[x][0].value > rankOfPlay) and (len(tripletSequences[x]) == (int(len(play)/5)*3)):
                    usedNumbers = []
                    for a in range (0, len(tripletSequences[x]), 3):
                        usedNumbers.append(tripletSequences[x][a].value)
                    neededPairs = int(len(play)/5)
                    foundPairs = []
                    for y in range (len(pairs)):
                        if usedNumbers.count(pairs[y][0].value) == 0:
                            foundPairs.append(pairs[y])
                    if len(foundPairs) >= neededPairs:
                        finalFoundPairs = []
                        perm = permutations(foundPairs, neededPairs)
                        for i in perm:
                            i2 = list(i)
                            attachmentPlay = tripletSequences[x]
                            for j in range (len(i2)):
                                attachmentPlay = attachmentPlay + i2[j]
                            legalTripletPairSequences.append(attachmentPlay)
            return rockets + quads + legalTripletPairSequences
        '''
        if typeOfPlay == 4:
            legalTripletPairSequences = []
            if analyzedPlay[2] == 5:
                tripletSequences = triplets
            for x in range (len(tripletSequences)):
                if (tripletSequences[x][0].value > rankOfPlay) and (len(tripletSequences[x]) == (int(len(play)/5)*3)):
                    usedNumbers = []
                    for a in range (0, len(tripletSequences[x]), 3):
                        usedNumbers.append(tripletSequences[x][a].value)
                    neededPairs = int(len(play)/5)
                    foundPairs = []
                    for y in range (len(pairs)):
                        if usedNumbers.count(pairs[y][0].value) == 0:
                            foundPairs.append(pairs[y])
                    if len(foundPairs) >= neededPairs:
                        finalFoundPairs = []
                        for r in range (len(foundPairs)):
                            firstPair = foundPairs[r]
                            finalFoundPairs.append(firstPair)
                            if (len(finalFoundPairs) == neededPairs):
                                attachmentPlay = tripletSequences[x]+finalFoundPairs[0]
                                legalTripletPairSequences.append(attachmentPlay)
                                finalFoundPairs.pop()
                            else:
                                for j in range (r+1, len(foundPairs)):
                                    nextPair = foundPairs[j]
                                    finalFoundPairs.append(nextPair)
                                    if (len(finalFoundPairs) == neededPairs):
                                        attachmentPlay = tripletSequences[x]+finalFoundPairs[0]+finalFoundPairs[1]
                                        legalTripletPairSequences.append(attachmentPlay)
                                        finalFoundPairs.pop()
                                    else:
                                        for k in range (j+1, len(foundPairs)):
                                            nextPair = foundPairs[k]
                                            finalFoundPairs.append(nextPair)
                                            if (len(finalFoundPairs) == neededPairs):
                                                attachmentPlay = tripletSequences[x]+finalFoundPairs[0]+finalFoundPairs[1]+finalFoundPairs[2]
                                                legalTripletPairSequences.append(attachmentPlay)
                                                finalFoundPairs.pop()
                                            else:
                                                for l in range (k+1, len(foundPairs)):
                                                    nextPair = foundPairs[l]
                                                    finalFoundPairs.append(nextPair)
                                                    if (len(finalFoundPairs) == neededPairs):
                                                        attachmentPlay = tripletSequences[x]+finalFoundPairs[0]+finalFoundPairs[1]+finalFoundPairs[2]+finalFoundPairs[3]
                                                        legalTripletPairSequences.append(attachmentPlay)
                                                        finalFoundPairs.pop()
                                                finalFoundPairs.pop()
                                        finalFoundPairs.pop()
                                finalFoundPairs.pop()
            return rockets + quads + legalTripletPairSequences
            '''
        #Triplet sequence with single attachment, beatable by higher ranked triplet-with-single or rocket/bomb
        if typeOfPlay == 5:
            legalTripletSingleSequences = []
            if analyzedPlay[2] == 4:
                tripletSequences = triplets
                for x in range (len(tripletSequences)):
                    if (tripletSequences[x][0].value > rankOfPlay) and (len(tripletSequences[x]) == (int(len(play)/4)*3)):
                        usedNumbers = []
                        for a in range (0, len(tripletSequences[x]), 3):
                            usedNumbers.append(tripletSequences[x][a].value)
                        neededSingles = int(len(play)/4)
                        foundSingles = []
                        for y in range (len(singles)):
                            if usedNumbers.count(singles[y][0].value) == 0:
                                foundSingles.append(singles[y])
                        if len(foundSingles) >= neededSingles:
                            perm = permutations(foundSingles, neededSingles)
                            for i in perm:
                                if isinstance(i, list):
                                    attachmentPlay = tripletSequences[x]+i
                                    legalTripletSingleSequences.append(attachmentPlay)
                                else:
                                    attachmentPlay = tripletSequences[x]+list(i)
                                    legalTripletSingleSequences.append(attachmentPlay)
            else:
                for x in range (len(tripletSequences)):
                    if (tripletSequences[x][0].value > rankOfPlay) and (len(tripletSequences[x]) == (int(len(play)/4)*3)):
                        usedNumbers = []
                        for a in range (0, len(tripletSequences[x]), 3):
                            usedNumbers.append(tripletSequences[x][a].value)
                        neededSingles = int(len(play)/4)
                        foundSingles = []
                        for y in range (len(singles)):
                            if usedNumbers.count(singles[y][0].value) == 0:
                                foundSingles.append(singles[y])
                        if len(foundSingles) >= neededSingles:
                            perm = permutations(foundSingles, neededSingles)
                            for i in perm:
                                attachmentPlay = tripletSequences[x]+list(i)
                                legalTripletSingleSequences.append(attachmentPlay)
            return rockets + quads + legalTripletSingleSequences
        #standard triplet sequence
        if typeOfPlay == 6:
            legalTripletSequences = []
            for x in range (len(tripletSequences)):
                if tripletSequences[x][0].value > rankOfPlay:
                    legalTripletSequences.append(tripletSequences[x])
            return rockets + quads + legalTripletSequences
        #single triplet
        if typeOfPlay == 7:
            legalTriplets = []
            for x in range (len(triplets)):
                if triplets[x][0].value > rankOfPlay:
                    legalTriplets.append(triplets[x])
            return rockets + quads + legalTriplets
        #pair sequence
        if typeOfPlay == 8:
            legalPairSequences = []
            for x in range (len(pairSequences)):
                if pairSequences[x][0].value > rankOfPlay and len(pairSequences[x]) == len(play):
                    legalPairSequences.append(pairSequences[x])
            return rockets + quads + legalPairSequences

        #pair
        if typeOfPlay == 9:
            legalPairs = []
            for x in range (len(pairs)):
                if pairs[x][0].value > rankOfPlay:
                    legalPairs.append(pairs[x])
            return rockets + quads + legalPairs
        #single sequence
        if typeOfPlay == 10:
            legalSingleSequences = []
            for x in range (len(singleSequences)):
                if singleSequences[x][0].value > rankOfPlay and len(singleSequences[x]) == len(play):
                    legalSingleSequences.append(singleSequences[x])
            return rockets + quads + legalSingleSequences
        #singles
        if typeOfPlay == 11:
            legalSingles = []
            for x in range (len(singles)):
                if singles[x][0].value > rankOfPlay:
                    legalSingles.append(singles[x])
            return rockets + quads + legalSingles
        
        if (rockets is not None):
            return rockets
        else:
            return []

    #gets the raw value of a card
    def value_lookup(self, card):
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

    #play numbers in order starting from 0
    #plays = [[rocket], [quad], [sequenceTriplet], [triplet], [sequencePair], [pair], [sequenceSingle], [single]]
    def play_lookup(self, play_number,length):
        table = {
            0: 50,
            1: 45,
            2: length*8,
            3: 10,
            4: length*8,
            5: 5,
            6: length*9,
            7: 0}
        return table.get(play_number,0)

    #find the estimated value of a hand to use as a base in evaluation
    def evaluation_heuristic(self, hand):
        plays = self.valid_plays(hand)
        sum_plays = 0
        for x in range(len(plays)):
            for y in plays[x]:
                sum_plays = sum_plays + self.play_lookup(x,len(y))
        sum_cards = self.evaluate_hand_separate(hand)
        length_penalty = len(hand)*110
        if (length_penalty == 0):
            return 1000000
        return sum_plays + sum_cards - length_penalty

    def to_plays_array(self, array):
        arr = []
        for e in array:
            if (isinstance(e, list)):
                for sube in e:
                    if (isinstance(sube, list)):
                        arr.append(sube)
                    else:
                        arr.append(e)
            else:
                arr.append(e)
        return arr

    #find expected value of own hand, taking into account different plays that could be made
    def evaluate_hand(self, hand):
        #if hand empty then win
        if (not hand): return 1000000
        poss_plays = self.to_plays_array(self.valid_plays(hand))
        value_of_plays = [self.evaluate_play(hand, poss_play) for poss_play in poss_plays]
        return max(value_of_plays)

    def return_best_play_from_hand(self, hand):
        #if hand empty then win
        if (not hand): return 1000000
        poss_plays = self.to_plays_array(self.valid_plays(hand))
        value_of_plays = [self.evaluate_play(hand, poss_play) for poss_play in poss_plays]
        return poss_plays[value_of_plays.index(max(value_of_plays))]

    #returns a (play, value) pair of expected values of plays
    def evaluate_hand_dict(self, hand):
        poss_plays = self.to_plays_array(self.valid_plays(hand))
        value_of_plays = [self.evaluate_play(hand, poss_play) for poss_play in poss_plays]
        return dict(zip(poss_play, value_of_plays))

    #find expected value of own hand, taking into account different plays
    #that could be made on the current board
    def evaluate_hand_given_play(self, hand, play):
        #if hand empty then win
        if (not hand): return 1000000
        poss_plays = self.combine_play(hand, play)
        value_of_plays = [self.evaluate_play(hand, poss_play) for poss_play in poss_plays]
        return max(value_of_plays)

    #find expected value of a play based on own hand
    def evaluate_play(self, hand, play):
        leftover_hand = [card for card in hand if card not in play]
        leftover_quality = sum([self.value_lookup(card) for card in leftover_hand])
        return leftover_quality - 50 + self.evaluation_heuristic(leftover_hand)

    #find expected value of a hand, disregarding combinations of cards
    def evaluate_hand_separate(self, hand):
        return sum([self.value_lookup(card) for card in hand])

    #find expected values of another player's hand in comparison to your own
    #value > 0 means on average the your hand is better than their's
    #value < 0 means on average the your hand is worse than their's
    #requires other player hand size, your hand, and the cards still not played
    def evaluate_other_player(self, other_player_hand_size, hand, unplayed_cards):
        own_value = self.evaluate_hand_separate(hand)
        total_other_value = self.evaluate_hand_separate(unplayed_cards)
        other_value = total_other_value * other_player_hand_size / len(unplayed_cards)
        return own_value - other_value

    #return the best move based on expectiminimax using pruning
    def get_move(self, hand, play):
        poss_plays = self.combine_play(hand, play)
        if (not poss_plays): return []
        value_of_plays = [self.evaluate_play(hand, poss_play) for poss_play in poss_plays]
        r2 =  poss_plays[value_of_plays.index(max(value_of_plays))]
        return r2

class SimulatedAnnealingAI:
    def __init__(self, order):
        self.order = order
        self.str = 'SimulatedAnnealingAI ' + str(order)

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
                        rocket.append([hand[previousCards], hand[previousCards+1]])
                        isRocket.append([hand[previousCards]])
                        isRocket.append([hand[previousCards+1]])

                    else:
                        single.append([hand[previousCards]])
                elif simplifiedHand[x+1] == 1:
                    single.append([hand[previousCards]])
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
                runningTripletSequence = runningTriplet
                for y in range(7):
                    if ((simplifiedHand[x+y+1] >= 3) and (x+y+1 < 12)):
                        newTriplet = [hand[lookaheadCards], hand[lookaheadCards+1], hand[lookaheadCards+2]]
                        runningTripletSequence = runningTripletSequence + newTriplet
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
                runningPairSequence = runningPair
                for y in range(9):
                    if ((simplifiedHand[x+y+1] >= 2) and (x+y+1 < 12)):
                        newPair = [hand[lookaheadCards], hand[lookaheadCards+1]]
                        runningPairSequence = runningPairSequence + newPair
                        if (len(runningPairSequence) >=3):
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
                        runningSingleSequence= runningSingleSequence + newSingle
                        if (len(runningSingleSequence) >= 5):
                            sequenceSingle.append(list(runningSingleSequence))
                        lookaheadCards = lookaheadCards + simplifiedHand[x+y+1]
                        cardInSequence = True
                    else:
                        break

                #setting single-attachment priority
                if cardInSequence:
                    isSequence.append([hand[previousCards]])
                else:
                    isQuad.append([hand[previousCards]])
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
                runningTripletSequence = runningTriplet
                for y in range(7):
                    if ((simplifiedHand[x+y+1] >= 3) and (x+y+1 < 12)):
                        newTriplet = [hand[lookaheadCards], hand[lookaheadCards+1], hand[lookaheadCards+2]]
                        runningTripletSequence = runningTripletSequence + newTriplet
                        sequenceTriplet.append(runningTripletSequence)
                        lookaheadCards = lookaheadCards + simplifiedHand[x+y+1]
                        cardInSequence = True
                    else:
                        break
                runningPair = [hand[previousCards], hand[previousCards+1]]
                pair.append(runningPair)
                #similar logic to triplet sequences for pair sequences
                #lookaheadCards helps track where the next numerical value of card starts
                lookaheadCards = previousCards + 3
                runningPairSequence = runningPair
                for y in range(9):
                    if ((simplifiedHand[x+y+1] >= 2) and (x+y+1 < 12)):
                        newPair = [hand[lookaheadCards], hand[lookaheadCards+1]]
                        runningPairSequence = runningPairSequence + newPair
                        if (len(runningPairSequence) >=3):
                            sequencePair.append(list(runningPairSequence))
                        lookaheadCards = lookaheadCards + simplifiedHand[x+y+1]
                        cardInSequence = True
                    else:
                        break
                #similar logic for singleton sequences
                lookaheadCards = previousCards + 3
                runningSingleSequence = [hand[previousCards]]
                for y in range(12):
                    if ((simplifiedHand[x+y+1] >= 1) and (x+y+1 < 12)):
                        newSingle = [hand[lookaheadCards]]
                        runningSingleSequence= runningSingleSequence + newSingle
                        if (len(runningSingleSequence) >= 5):
                            sequenceSingle.append(list(runningSingleSequence))
                        lookaheadCards = lookaheadCards + simplifiedHand[x+y+1]
                        cardInSequence = True
                    else:
                        break

                #setting single-attachment priority
                if cardInSequence:
                    isSequence.append([hand[previousCards]])
                else:
                    isTriplet.append([hand[previousCards]])
                previousCards = previousCards + 3

            #If the current hand has 2 copies of the card being scanned
            elif simplifiedHand[x] == 2:
                runningPair = [hand[previousCards], hand[previousCards+1]]
                pair.append(runningPair)
                #similar logic to triplet sequences for pair sequences
                #lookaheadCards helps track where the next numerical value of card starts
                lookaheadCards = previousCards + 2
                runningPairSequence = runningPair
                for y in range(9):
                    if ((simplifiedHand[x+y+1] >= 2) and (x+y+1 < 12)):
                        newPair = [hand[lookaheadCards], hand[lookaheadCards+1]]
                        runningPairSequence = runningPairSequence + newPair
                        if (len(runningPairSequence) >=3):
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
                        runningSingleSequence= runningSingleSequence + newSingle
                        if (len(runningSingleSequence) >= 5):
                            sequenceSingle.append(list(runningSingleSequence))
                        lookaheadCards = lookaheadCards + simplifiedHand[x+y+1]
                        cardInSequence = True
                    else:
                        break

                #setting single-attachment priority
                if cardInSequence:
                    isSequence.append([hand[previousCards]])
                else:
                    isPair.append([hand[previousCards]])
                previousCards = previousCards + 2

            #If current hand only has 1 of the scanned card
            elif simplifiedHand[x] == 1:
                #Only need to check for singleton sequence
                lookaheadCards = previousCards + 1
                runningSingleSequence = [hand[previousCards]]
                for y in range(12):
                    if ((simplifiedHand[x+y+1] >= 1) and (x+y+1 < 12)):
                        newSingle = [hand[lookaheadCards]]
                        runningSingleSequence= runningSingleSequence + newSingle
                        if (len(runningSingleSequence) >= 5):
                            sequenceSingle.append(list(runningSingleSequence))
                        lookaheadCards = lookaheadCards + simplifiedHand[x+y+1]
                        cardInSequence = True
                    else:
                        break

                #setting single-attachment priority
                if cardInSequence:
                    isSequence.append([hand[previousCards]])
                else:
                    single.append([hand[previousCards]])
                previousCards = previousCards + 1

        single = single + isPair + isTriplet + isQuad + isSequence + isRocket
        #single = [single, isPair, isTriplet, isQuad, isSequence, isRocket]
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

    def check_bomb(self, hand):
        bombValue = hand[0].value
        return [(hand[0].value == hand[1].value and hand[0].value == hand[2].value and hand[0].value == hand[3].value), bombValue]

    def check_rocket(self, hand):
        return (hand[len(hand) - 2].value == 16 and hand[len(hand) - 1].value == 17)

    def check_single_sequence(self, hand):
        prevHandValue = -1
        sequenceStart = hand[0].value
        for x in range (len(hand)):
            if hand[x].value == prevHandValue+1 or prevHandValue == -1:
                prevHandValue = hand[x].value
                if x == len(hand) - 1:
                    return [True, sequenceStart]
            else:
                return [False, sequenceStart]

    def check_pair_sequence(self, hand):
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

    def check_triplet_sequence(self, hand):
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

    def check_triplet_sequence_attachments(self, hand, needed):
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
            return [False, sequenceStart]

    def check_quadplex_set_1(self, hand):
        prevHandValue = -1
        totalNumber = len(hand)
        attachment1 = -1
        attachment2 = -1
        quadValue = -1
        for x in range (totalNumber):
            if (x+3 >= totalNumber):
                break
            if (hand[x].value == hand[x+1].value and hand[x].value == hand[x+2].value and hand[x].value == hand[x+3].value):
                quadValue = hand[x].value
                break
        if quadValue == -1:
            return [False, quadValue]
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

    def check_quadplex_set_2(self, hand):
        prevHandValue = -1
        totalNumber = len(hand)
        pair1 = -1
        pair2 = -1
        quadValue = -1
        for x in range (totalNumber):
            if (x+3 >= totalNumber):
                break
            if (hand[x].value == hand[x+1].value and hand[x].value == hand[x+2].value and hand[x].value == hand[x+3].value):
                quadValue = hand[x].value
                break
        if quadValue == -1:
            return [False, quadValue]
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

        #if 0
        if len(hand) == 0:
            return analyzedPlay

        #if 1, must be single card
        if len(hand) == 1:
            analyzedPlay = [11, hand[0].value, 1]
            return analyzedPlay

        #if 2, must be pair, or rocket
        elif len(hand) == 2:
            if self.check_rocket(hand):
                analyzedPlay = [0, 16, 2]
                return analyzedPlay
            else:
                checkedPair = self.check_pair_sequence(hand)
                if checkedPair[0]:
                    analyzedPlay = [9, checkedPair[1], 2]
                    return analyzedPlay
            #Throw error
            return analyzedPlay

        #if 3, must be triplet
        elif len(hand) == 3:
            checkedTriplet = self.check_triplet_sequence(hand)
            if checkedTriplet[0]:
                analyzedPlay = [7, checkedTriplet[1], 3]
                return analyzedPlay
            #throw error

        #if 4, could be one of the following:
        # - Triplet with attachment
        # - Bomb
        elif len(hand) == 4:
            checkedBomb = self.check_bomb(hand)
            checkedTripletSingleAttachment = self.check_triplet_sequence_attachments(hand, 1)
            if checkedBomb[0]:
                analyzedPlay = [1, checkedBomb[1], 4]
                return analyzedPlay
            elif checkedTripletSingleAttachment[0]:
                analyzedPlay = [5, checkedTripletSingleAttachment[1], 4]
                return analyzedPlay
            #throw error

        #if 5, could be one of the following:
        # - Triplet with attached pair
        # - Sequence of 5 single cards
        elif len(hand) == 5:
            checkedTripletPairAttachment = self.check_triplet_sequence_attachments(hand, 1)
            checkedSequence = self.check_single_sequence(hand)
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
            checkedSequence = self.check_single_sequence(hand)
            checkedTripletSequence = self.check_triplet_sequence(hand)
            checkedPairSequence = self.check_pair_sequence(hand)
            checkedQuadplexSet1 = self.check_quadplex_set_1(hand)
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
            checkedSequence = self.check_single_sequence(hand)
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
            checkedSequence = self.check_single_sequence(hand)
            checkedPairSequence = self.check_pair_sequence(hand)
            checkedTripletSequenceSingleAttachment = self.check_triplet_sequence_attachments(hand, 2)
            checkedQuadplexSet2 = self.check_quadplex_set_2(hand)
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
                checkedSequence = self.check_single_sequence(hand)
                if (checkedSequence[0]):
                    return [10, checkedSequence[1], totalNumber]
            if (possiblePairs):
                checkedPairSequence = self.check_pair_sequence(hand)
                if (checkedPairSequence[0]):
                    return [8, checkedPairSequence[1], totalNumber]
            if (possibleTriplets):
                checkedTripletSequence = self.check_triplet_sequence(hand)
                if (checkedTripletSequence[0]):
                    return [6, checkedTripletSequence[1], totalNumber]
            if (possibleTripletsSingleAttachment):
                totalTripletsNeeded = int(totalNumber/4)
                checkedTripletSequenceSingleAttachment = self.check_triplet_sequence_attachments(hand, totalTripletsNeeded)
                if (checkedTripletSequenceSingleAttachment[0]):
                    return [5, checkedTripletSequenceSingleAttachment[1], totalNumber]
            if (possibleTripletsPairAttachment):
                totalTripletsNeeded = int(totalNumber/5)
                checkedTripletsPairAttachment = self.check_triplet_sequence_attachments(hand, totalTripletsNeeded)
                if (checkedTripletsPairAttachment[0]):
                    return [4, checkedTripletsPairAttachment[1], totalNumber]
            #throw error if we get here: no matches

    #takes the current hand and currently on-board play, and returns a list of all legal plays from this state
    #Input FORMATTING NOTE: hand and play must both be lists of cards
    #
    #Return format:
    #combinedPlays[] defined as a list of all legal plays of cards, where each play is a list of cards.
    #Note that this function will return the empty list if there are no legal plays. Functions utilizing combine_play
    #should take note of this case and treat it as no-legal-plays-possible (i.e. needs to pass).
    def combine_play(self, hand, playPre):
        play = []
        for pl in playPre:
            if isinstance(pl, list):
                for plsub in pl:
                    play = play + [plsub]
            else:
                play = play + [pl]

        #THEY SHOULD ALL BE SORTED, DOUBLE CHECK THIS
        analyzedPlay = self.analyze_play(play)
        validPlays = self.valid_plays(hand)
        #separating out plays
        rockets = validPlays[0]
        quads = validPlays[1]
        tripletSequences = validPlays[2]
        triplets = validPlays[3]
        pairSequences = validPlays[4]
        pairs = validPlays[5]
        singleSequences = validPlays[6]
        #note that singles is constructed by concatenation, not multiple lists, so you can access it normally
        singles = validPlays[7]
        
        typeOfPlay = 0
        rankOfPlay = 18
        if (analyzedPlay is not None):
            typeOfPlay = analyzedPlay[0]
            rankOfPlay = analyzedPlay[1]
        #if empty play, can play anything
        if typeOfPlay == -1:
            legalQuadSingles = []
            for x in range (len(quads)):
                if quads[x][0].value > rankOfPlay:
                    for y in range (len(singles)):
                        if singles[y][0].value != quads[x][0].value:
                            for z in range (len(singles)):
                                if singles[z][0].value != quads[x][0].value and singles[z][0].value != singles[y][0].value and (singles[z][0].value + singles[y][0].value < 33):
                                    attachmentPlay = quads[x]+[singles[y][0]]+[singles[z][0]]
                                    legalQuadSingles.append(attachmentPlay)
            legalQuadPairs = []
            for x in range (len(quads)):
                if quads[x][0].value > rankOfPlay:
                    for y in range (len(pairs)):
                        if len(pairs) <=1:
                            break
                        if pairs[y][0].value != quads[x][0].value:
                            for z in range (len(pairs)):
                                if pairs[z][0].value != quads[x][0].value and pairs[z][0].value != pairs[y][0].value:
                                    attachmentPlay = quads[x]+pairs[y]+pairs[z]
                                    legalQuadPairs.append(attachmentPlay)
            legalTripletSingleSequences = []
            for x in range (len(tripletSequences)):
                usedNumbers = []
                for a in range (0, len(tripletSequences[x]), 3):
                    usedNumbers.append(tripletSequences[x][a].value)
                neededSingles = int(len(tripletSequences[x])/4)
                foundSingles = []
                for y in range (len(singles)):
                    if usedNumbers.count(singles[y][0].value) == 0:
                        foundSingles.append(singles[y][0])
                if len(foundSingles) >= neededSingles:
                    perm = permutations(foundSingles, neededSingles)
                    for i in perm:
                        attachmentPlay = tripletSequences[x]+list(i)
                        legalTripletSingleSequences.append(attachmentPlay)
            legalTripletSingles = []
            for x in range (len(triplets)):
                if (triplets[x][0].value > rankOfPlay):
                    usedNumbers = []
                    for a in range (0, len(triplets[x]), 3):
                        usedNumbers.append(triplets[x][a].value)
                    neededSingles = 1
                    foundSingles = []
                    for y in range (len(singles)):
                        if usedNumbers.count(singles[y][0].value) == 0:
                            foundSingles.append(singles[y][0])
                    if len(foundSingles) >= neededSingles:
                        perm = permutations(foundSingles, neededSingles)
                        for i in perm:
                            attachmentPlay = triplets[x]+list(i)
                            legalTripletSingles.append(attachmentPlay)
            legalTripletPairSequences = []
            for x in range (len(tripletSequences)):
                if (tripletSequences[x][0].value > rankOfPlay):
                    usedNumbers = []
                    for a in range (0, len(tripletSequences[x]), 3):
                        usedNumbers.append(tripletSequences[x][a].value)
                    neededPairs = int(len(tripletSequences[x])/5)
                    foundPairs = []
                    for y in range (len(pairs)):
                        if usedNumbers.count(pairs[y][0].value) == 0:
                            foundPairs.append(pairs[y])
                    if len(foundPairs) >= neededPairs:
                        finalFoundPairs = []
                        perm = permutations(foundPairs, neededPairs)
                        for i in perm:
                            i2 = list(i)
                            attachmentPlay = tripletSequences[x]
                            for j in range (len(i2)):
                                attachmentPlay = attachmentPlay + i2[j]
                            legalTripletPairSequences.append(attachmentPlay)
            legalTripletPairs = []
            for x in range (len(triplets)):
                if (triplets[x][0].value > rankOfPlay):
                    usedNumbers = []
                    for a in range (0, len(triplets[x]), 3):
                        usedNumbers.append(triplets[x][a].value)
                    neededPairs = 1
                    foundPairs = []
                    for y in range (len(pairs)):
                        if usedNumbers.count(pairs[y][0].value) == 0:
                            foundPairs.append(pairs[y])
                    if len(foundPairs) >= neededPairs:
                        finalFoundPairs = []
                        perm = permutations(foundPairs, neededPairs)
                        for i in perm:
                            i2 = list(i)
                            attachmentPlay = triplets[x]
                            for j in range (len(i2)):
                                attachmentPlay = attachmentPlay + i2[j]
                            legalTripletPairs.append(attachmentPlay)
            return rockets + quads + legalQuadSingles + legalQuadPairs + legalTripletPairSequences + legalTripletPairs + legalTripletSingleSequences + legalTripletSingles + tripletSequences + triplets + pairSequences + pairs + singleSequences + singles

        #rocket: Can't be beaten
        if typeOfPlay == 0:
            return []
        #quad(bomb): Beaten by higher bombs or rockets
        if typeOfPlay == 1:
            legalQuads = []
            for x in range (len(quads)):
                if quads[x][0].value > rankOfPlay:
                    legalQuads.append(quads[x])
            return rockets + legalQuads
        #quad(pair attachments): beaten by higher quad-pair sets, any bombs, or rockets
        if typeOfPlay == 2:
            legalQuadPairs = []
            for x in range (len(quads)):
                if quads[x][0].value > rankOfPlay:
                    for y in range (len(pairs)):
                        if len(pairs) <=1:
                            break
                        if pairs[y][0].value != quads[x][0].value:
                            for z in range (len(pairs)):
                                if pairs[z][0].value != quads[x][0].value and pairs[z][0].value != pairs[y][0].value:
                                    attachmentPlay = quads[x]+pairs[y]+pairs[z]
                                    legalQuadPairs.append(attachmentPlay)
            return rockets + quads + legalQuadPairs
        #quad(single attachments): beaten by higher quad-single sets, any bombs, or rockets
        if typeOfPlay == 3:
            legalQuadSingles = []
            for x in range (len(quads)):
                if quads[x][0].value > rankOfPlay:
                    for y in range (len(singles)):
                        if singles[y][0].value != quads[x][0].value:
                            for z in range (len(singles)):
                                if singles[z][0].value != quads[x][0].value and singles[z][0].value != singles[y][0].value and (singles[z][0].value + singles[y][0].value < 33):
                                    attachmentPlay = quads[x]+[singles[y]]+[singles[z]]
                                    legalQuadSingles.append(attachmentPlay)
            return rockets + quads + legalQuadSingles
        #triplet sequence with pair attachments: beaten by higher rank same-length pair-attached sequences, and bombs/rockets
        if typeOfPlay == 4:
            legalTripletPairSequences = []
            if analyzedPlay[2] == 5:
                tripletSequences = triplets
            for x in range (len(tripletSequences)):
                if (tripletSequences[x][0].value > rankOfPlay) and (len(tripletSequences[x]) == (int(len(play)/5)*3)):
                    usedNumbers = []
                    for a in range (0, len(tripletSequences[x]), 3):
                        usedNumbers.append(tripletSequences[x][a].value)
                    neededPairs = int(len(play)/5)
                    foundPairs = []
                    for y in range (len(pairs)):
                        if usedNumbers.count(pairs[y][0].value) == 0:
                            foundPairs.append(pairs[y])
                    if len(foundPairs) >= neededPairs:
                        finalFoundPairs = []
                        perm = permutations(foundPairs, neededPairs)
                        for i in perm:
                            i2 = list(i)
                            attachmentPlay = tripletSequences[x]
                            for j in range (len(i2)):
                                attachmentPlay = attachmentPlay + i2[j]
                            legalTripletPairSequences.append(attachmentPlay)
            return rockets + quads + legalTripletPairSequences
        '''
        if typeOfPlay == 4:
            legalTripletPairSequences = []
            if analyzedPlay[2] == 5:
                tripletSequences = triplets
            for x in range (len(tripletSequences)):
                if (tripletSequences[x][0].value > rankOfPlay) and (len(tripletSequences[x]) == (int(len(play)/5)*3)):
                    usedNumbers = []
                    for a in range (0, len(tripletSequences[x]), 3):
                        usedNumbers.append(tripletSequences[x][a].value)
                    neededPairs = int(len(play)/5)
                    foundPairs = []
                    for y in range (len(pairs)):
                        if usedNumbers.count(pairs[y][0].value) == 0:
                            foundPairs.append(pairs[y])
                    if len(foundPairs) >= neededPairs:
                        finalFoundPairs = []
                        for r in range (len(foundPairs)):
                            firstPair = foundPairs[r]
                            finalFoundPairs.append(firstPair)
                            if (len(finalFoundPairs) == neededPairs):
                                attachmentPlay = tripletSequences[x]+finalFoundPairs[0]
                                legalTripletPairSequences.append(attachmentPlay)
                                finalFoundPairs.pop()
                            else:
                                for j in range (r+1, len(foundPairs)):
                                    nextPair = foundPairs[j]
                                    finalFoundPairs.append(nextPair)
                                    if (len(finalFoundPairs) == neededPairs):
                                        attachmentPlay = tripletSequences[x]+finalFoundPairs[0]+finalFoundPairs[1]
                                        legalTripletPairSequences.append(attachmentPlay)
                                        finalFoundPairs.pop()
                                    else:
                                        for k in range (j+1, len(foundPairs)):
                                            nextPair = foundPairs[k]
                                            finalFoundPairs.append(nextPair)
                                            if (len(finalFoundPairs) == neededPairs):
                                                attachmentPlay = tripletSequences[x]+finalFoundPairs[0]+finalFoundPairs[1]+finalFoundPairs[2]
                                                legalTripletPairSequences.append(attachmentPlay)
                                                finalFoundPairs.pop()
                                            else:
                                                for l in range (k+1, len(foundPairs)):
                                                    nextPair = foundPairs[l]
                                                    finalFoundPairs.append(nextPair)
                                                    if (len(finalFoundPairs) == neededPairs):
                                                        attachmentPlay = tripletSequences[x]+finalFoundPairs[0]+finalFoundPairs[1]+finalFoundPairs[2]+finalFoundPairs[3]
                                                        legalTripletPairSequences.append(attachmentPlay)
                                                        finalFoundPairs.pop()
                                                finalFoundPairs.pop()
                                        finalFoundPairs.pop()
                                finalFoundPairs.pop()
            return rockets + quads + legalTripletPairSequences
            '''
        #Triplet sequence with single attachment, beatable by higher ranked triplet-with-single or rocket/bomb
        if typeOfPlay == 5:
            legalTripletSingleSequences = []
            if analyzedPlay[2] == 4:
                tripletSequences = triplets
                for x in range (len(tripletSequences)):
                    if (tripletSequences[x][0].value > rankOfPlay) and (len(tripletSequences[x]) == (int(len(play)/4)*3)):
                        usedNumbers = []
                        for a in range (0, len(tripletSequences[x]), 3):
                            usedNumbers.append(tripletSequences[x][a].value)
                        neededSingles = int(len(play)/4)
                        foundSingles = []
                        for y in range (len(singles)):
                            if usedNumbers.count(singles[y][0].value) == 0:
                                foundSingles.append(singles[y])
                        if len(foundSingles) >= neededSingles:
                            perm = permutations(foundSingles, neededSingles)
                            for i in perm:
                                if isinstance(i, list):
                                    attachmentPlay = tripletSequences[x]+i
                                    legalTripletSingleSequences.append(attachmentPlay)
                                else:
                                    attachmentPlay = tripletSequences[x]+list(i)
                                    legalTripletSingleSequences.append(attachmentPlay)
            else:
                for x in range (len(tripletSequences)):
                    if (tripletSequences[x][0].value > rankOfPlay) and (len(tripletSequences[x]) == (int(len(play)/4)*3)):
                        usedNumbers = []
                        for a in range (0, len(tripletSequences[x]), 3):
                            usedNumbers.append(tripletSequences[x][a].value)
                        neededSingles = int(len(play)/4)
                        foundSingles = []
                        for y in range (len(singles)):
                            if usedNumbers.count(singles[y][0].value) == 0:
                                foundSingles.append(singles[y])
                        if len(foundSingles) >= neededSingles:
                            perm = permutations(foundSingles, neededSingles)
                            for i in perm:
                                attachmentPlay = tripletSequences[x]+list(i)
                                legalTripletSingleSequences.append(attachmentPlay)
            return rockets + quads + legalTripletSingleSequences
        #standard triplet sequence
        if typeOfPlay == 6:
            legalTripletSequences = []
            for x in range (len(tripletSequences)):
                if tripletSequences[x][0].value > rankOfPlay:
                    legalTripletSequences.append(tripletSequences[x])
            return rockets + quads + legalTripletSequences
        #single triplet
        if typeOfPlay == 7:
            legalTriplets = []
            for x in range (len(triplets)):
                if triplets[x][0].value > rankOfPlay:
                    legalTriplets.append(triplets[x])
            return rockets + quads + legalTriplets
        #pair sequence
        if typeOfPlay == 8:
            legalPairSequences = []
            for x in range (len(pairSequences)):
                if pairSequences[x][0].value > rankOfPlay and len(pairSequences[x]) == len(play):
                    legalPairSequences.append(pairSequences[x])
            return rockets + quads + legalPairSequences

        #pair
        if typeOfPlay == 9:
            legalPairs = []
            for x in range (len(pairs)):
                if pairs[x][0].value > rankOfPlay:
                    legalPairs.append(pairs[x])
            return rockets + quads + legalPairs
        #single sequence
        if typeOfPlay == 10:
            legalSingleSequences = []
            for x in range (len(singleSequences)):
                if singleSequences[x][0].value > rankOfPlay and len(singleSequences[x]) == len(play):
                    legalSingleSequences.append(singleSequences[x])
            return rockets + quads + legalSingleSequences
        #singles
        if typeOfPlay == 11:
            legalSingles = []
            for x in range (len(singles)):
                if singles[x][0].value > rankOfPlay:
                    legalSingles.append(singles[x])
            return rockets + quads + legalSingles
        
        if (rockets is not None):
            return rockets
        else:
            return []

    #gets the raw value of a card
    def value_lookup(self, card):
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

    #play numbers in order starting from 0
    #plays = [[rocket], [quad], [sequenceTriplet], [triplet], [sequencePair], [pair], [sequenceSingle], [single]]
    def play_lookup(self, play_number,length):
        table = {
            0: 50,
            1: 45,
            2: length*8,
            3: 10,
            4: length*8,
            5: 5,
            6: length*9,
            7: 0}
        return table.get(play_number,0)

    #find the estimated value of a hand to use as a base in evaluation
    def evaluation_heuristic(self, hand):
        plays = self.valid_plays(hand)
        sum_plays = 0
        for x in range(len(plays)):
            for y in plays[x]:
                sum_plays = sum_plays + self.play_lookup(x,len(y))
        sum_cards = self.evaluate_hand_separate(hand)
        length_penalty = len(hand)*110
        if (length_penalty == 0):
            return 1000000
        return sum_plays + sum_cards - length_penalty

    def to_plays_array(self, array):
        arr = []
        for e in array:
            if (isinstance(e, list)):
                for sube in e:
                    if (isinstance(sube, list)):
                        arr.append(sube)
                    else:
                        arr.append(e)
            else:
                arr.append(e)
        return arr

    #find expected value of own hand, taking into account different plays that could be made
    def evaluate_hand(self, hand):
        #if hand empty then win
        if (not hand): return 1000000
        poss_plays = self.to_plays_array(self.valid_plays(hand))
        value_of_plays = [self.evaluate_play(hand, poss_play) for poss_play in poss_plays]
        return max(value_of_plays)

    def return_best_play_from_hand(self, hand):
        poss_plays = self.to_plays_array(self.valid_plays(hand))
        value_of_plays = [self.evaluate_play(hand, poss_play) for poss_play in poss_plays]
        return poss_plays[value_of_plays.index(max(value_of_plays))]

    #find expected value of own hand, taking into account different plays
    #that could be made on the current board
    def evaluate_hand_given_play(self, hand, play):
        #if hand empty then win
        if (not hand): return 1000000
        poss_plays = self.combine_play(hand, play)
        value_of_plays = [self.evaluate_play(hand, poss_play) for poss_play in poss_plays]
        return max(value_of_plays)

    #find expected value of a play based on own hand
    def evaluate_play(self, hand, play):
        leftover_hand = [card for card in hand if card not in play]
        leftover_quality = sum([self.value_lookup(card) for card in leftover_hand])
        return leftover_quality - 50 + self.evaluation_heuristic(leftover_hand)

    #find expected value of a hand, disregarding combinations of cards
    def evaluate_hand_separate(self, hand):
        return sum([self.value_lookup(card) for card in hand])

    #find expected values of another player's hand in comparison to your own
    #value > 0 means on average the your hand is better than their's
    #value < 0 means on average the your hand is worse than their's
    #requires other player hand size, your hand, and the cards still not played
    def evaluate_other_player(self, other_player_hand_size, hand, unplayed_cards):
        own_value = self.evaluate_hand_separate(hand)
        total_other_value = self.evaluate_hand_separate(unplayed_cards)
        other_value = total_other_value * other_player_hand_size / len(unplayed_cards)
        return own_value - other_value

    #returns a sorted list of plays based on expected values
    def evaluate_hand_list(self, hand, play):
        poss_plays = self.combine_play(hand, play)
        value_of_plays = [self.evaluate_play(hand, poss_play) for poss_play in poss_plays]
        indexes = sorted(range(len(value_of_plays)) ,key=lambda x:value_of_plays[x])
        plays = [poss_plays[len(indexes) - i - 1] for i in indexes]
        return plays

    #return the best move based on simulated annealing, given a hand and a turn (starting at 1)
    def get_move(self, hand, play, turn):
        temperature = 10./turn
        plays = self.evaluate_hand_list(hand, play)
        if (len(plays)==0):
            index = int(math.floor(random.random() * temperature))%1
            if (not plays or 0 > index or index >= len(plays)): return []
            return plays[index]
        else:
            index = int(math.floor(random.random() * temperature))%len(plays)
            if (not plays or 0 > index or index >= len(plays)): return []
            return plays[index]

#Other Actual Non-AI Players
class Other:
    def __init__(self, order):
        self.order = order
        self.str = 'Other ' + str(order)
        
