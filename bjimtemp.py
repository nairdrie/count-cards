import time
import random
import os
import matplotlib.pyplot as plt
clearConsole = lambda: os.system('cls')

AUTOPLAY = True
SPEED_MULTIPLIER = 10
CARD_COUNTER_WEIGHT = 1
INITIAL_BALANCE = 5000
INITIAL_BET_AMT = 1
MIN_BET = 1
MAX_BET = 5000
NUM_DECKS = 8
SUITS = ['♣', '♦', '♥', '♠']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
TOTAL_CARDS = len(SUITS) * len(RANKS) * NUM_DECKS
DECISIONS = ['HIT', 'STAND', 'SPLIT', 'DOUBLE']
AVG_HAND_TIME = 60

HARD_STRATEGY_CHART = {
    #    A  2  3  4  5  6  7  8  9  10  
    4:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    5:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    6:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    7:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    8:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    9:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    10: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    11: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    12: [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
    13: [0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    14: [0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    15: [0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    16: [0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    17: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    18: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    19: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    20: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    21: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
}

SOFT_STRATEGY_CHART = {
    #    A  2  3  4  5  6  7  8  9  10
    12: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # A, A. we should split this. remove eventually.
    13: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    14: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    15: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    16: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    17: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    18: [0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    19: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    20: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    21: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
}

SPLIT_STRATEGY_CHART = {
#        A  2  3  4  5  6  7  8  9  10
    2:  [0, 0, 0, 2, 2, 2, 2, 0, 0, 0],
    3:  [0, 0, 0, 2, 2, 2, 2, 0, 0, 0],
    4:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    5:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    6:  [0, 0, 2, 2, 2, 2, 0, 0, 0, 0],
    7:  [0, 2, 2, 2, 2, 2, 2, 0, 0, 0],
    8:  [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    9:  [1, 2, 2, 2, 2, 2, 1, 2, 2, 1],
    10: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    11: [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
}

cardCounter = 0
deck = []
bankroll = INITIAL_BALANCE
betAmt = INITIAL_BET_AMT
handsPlayed = 0

winRecord = {}
lossRecord = {}
winPercentages = {}

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.visible = False

    def flip(self):
        self.visible = True

    def print(self):
        # return
        if self.visible:
            print('+-----+')
            print('|', RANKS[self.rank], '  |')
            print('|', '', SUITS[self.suit], ' |')
            print('|', ' ', RANKS[self.rank], '|')
            print('+-----+')
        else:
            print('+-----+')
            print('|', ' ', '  |')
            print('|', ' ', ' |')
            print('|', ' ', '  |')
            print('+-----+')

# randomly generate a shuffled standard deck of cards
def shuffle():
    global cardCounter
    deck = []
    cardCounter = 0

    for i in range(NUM_DECKS):
        for suit in range(4):
            for rank in range(13):
                card = Card(rank, suit)
                deck.append(card)
    random.shuffle(deck)
    return deck


def printHand(hand):
    handString = ''

    # TOP ROW
    for card in hand:
        handString += '+-----+ '
    handString += '\n'

    # RANK ROW
    for card in hand:
        row = ''
        row += '| ' + RANKS[card.rank]
        if card.rank == 9:
            row += '  | '
        else:
            row += '   | '
        if not card.visible:
            # replace every alphanumeric character with a space
            row = ''.join([c if not c.isalnum() else ' ' for c in row])
        handString += row
    handString += '\n'

    # SUIT ROW
    for card in hand:
        if card.visible:
            handString += '|  ' + SUITS[card.suit] + '  | '
        else:
            handString += '|     | '
    handString += '\n'

    # RANK ROW
    for card in hand:
        row = ''
        if card.rank == 9:
            row += '|  ' + RANKS[card.rank]
        else:
            row += '|   ' + RANKS[card.rank]
        row += ' | '
        if not card.visible:
            # replace every alphanumeric character with a space
            row = ''.join([c if not c.isalnum() else ' ' for c in row])
        handString += row
    handString += '\n'

    # BOTTOM ROW
    for card in hand:
        handString += '+-----+ '
    
    print(handString)

def deal(deck, betAmount, bankroll, auto=False):
    playerHands = []
    # give the player 1 hand to start
    playerHands.append([])
    dealerHand = []
    # Deal player a face up card
    for hand in playerHands:
        nextCard = drawCard(deck)
        nextCard.flip()
        hand.append(nextCard)
    # Deal dealer a face up card
    nextCard = drawCard(deck)
    nextCard.flip()
    dealerHand.append(nextCard)
    # Deal player a face up card
    for hand in playerHands:
        nextCard = drawCard(deck)
        nextCard.flip()
        hand.append(nextCard)
    # Deal dealer a face down card
    nextCard = drawCard(deck)
    dealerHand.append(nextCard)
    printGame(dealerHand, playerHands, betAmount)

    didBust = False
    # Player's turn
    while True:
        for hand in playerHands:
            if auto:
                action = decideMove(hand, dealerHand)
            else:
                action = input('(H)it, (S)tand?, or s(P)lit? ')

            if action.lower() == 'hit' or action.lower() == 'h':
                nextCard = drawCard(deck)
                nextCard.flip()
                hand.append(nextCard)
                printGame(dealerHand, playerHands, betAmount)
                if handValue(hand) > 21:
                    didBust = True
                    break
            elif action.lower() == 'stand' or action.lower() == 's':
                break
            elif action.lower() == 'split' or action.lower() == 'p':
                if len(hand) == 2 and hand[0].rank == hand[1].rank:
                    splitHand.append(playerHand.pop())
                    nextCard = drawCard(deck)
                    nextCard.flip()
                    playerHand.append(nextCard)
                    nextCard = drawCard(deck)
                    nextCard.flip()
                    splitHand.append(nextCard)
                    printGame(dealerHand, playerHand, betAmount, splitHand) 
                else:
                    print('Invalid input')
            else:
                print('Invalid input')
    
    # flip the dealer's face down card
    dealerHand[1].flip()
    printGame(dealerHand, playerHand, betAmount)

    playerValue = handValue(playerHand)
    playerHasBlackjack = playerValue == 21 and len(playerHand) == 2

    if not didBust and not playerHasBlackjack:
        # Dealer's turn
        while handValue(dealerHand) < 17:
            nextCard = deck.pop()
            nextCard.flip()
            dealerHand.append(nextCard)
            printGame(dealerHand, playerHand, betAmount)
            if handValue(dealerHand) > 21:
                break
    
    # determine winner
    dealerValue = handValue(dealerHand)
    dealerHasBlackjack = dealerValue == 21 and len(dealerHand) == 2
    if playerHasBlackjack and dealerHasBlackjack:
        print('Push!')
        return 1
    elif playerHasBlackjack:
        print('Blackjack! Player wins.')
        return 3
    elif dealerHasBlackjack:
        print('Blackjack. Dealer wins.')
        return 0
    elif playerValue > 21:
        print('Bust! Dealer wins.')
        return 0
    elif dealerValue > 21:
        print('Bust! Player wins.')
        return 2
    elif playerValue > dealerValue:
        print('Player Wins.')
        return 2
    elif playerValue < dealerValue:
        print('Dealer Wins.')
        return 0
    else:
        print('Push!')
        return 1
    
def formatTime(seconds):
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)

def printGame(dealerHand, playerHand, betAmount):
    global bankroll, deck, cardCounter, handsPlayed, winRecord, lossRecord, winPercentages

    clearConsole()

    print ('Bet Amount:', betAmount)
    print ('Bankroll:', bankroll)
    print ('Cards remaining:', len(deck))
    print ('Card Counter:', cardCounter)
    print ('Hands played:', handsPlayed)
    print ('Time elapsed:', formatTime(handsPlayed * AVG_HAND_TIME))

    print ('Dealer\'s Hand:', handValue(dealerHand))
    printHand(dealerHand)
    print ('Player\'s Hand:', handValue(playerHand))
    printHand(playerHand)
    time.sleep(1 / SPEED_MULTIPLIER)

def drawCard(deck):
    global cardCounter

    nextCard = deck.pop()

    # if its 2-6, increment the count
    if nextCard.rank > 0 and nextCard.rank < 6:
        cardCounter += 1
    # if its 10-A, decrement the count
    elif nextCard.rank == 0 or nextCard.rank >= 9:
        cardCounter -= 1

    return nextCard


def formattedHandValue(hand):
    value = 0
    # sort the hand by rank
    sortedHand = sorted(hand, key=lambda x: x.rank)
    # count the number of aces
    numAces = 0
    for card in sortedHand:
        if not card.visible:
            continue
        if card.rank == 0:
            numAces += 1
    # count the value of the hand
    
    for card in sortedHand:
        if not card.visible:
            continue
        if card.rank > 9:
            value += 10
        else:
            value += card.rank + 1
    didUseAce = False
    # adjust the value of the hand for aces
    for i in range(numAces):
        if value + 10 <= 21:
            didUseAce = True
            value += 10
    if(value == 21 and len(hand) == 2):
        return 'Blackjack!'
    if didUseAce:
        return str(value - 10) + ' / ' + str(value)
    return str(value)

def handValue(hand):
    value = 0
    # sort the hand by rank
    sortedHand = sorted(hand, key=lambda x: x.rank)
    # count the number of aces
    numAces = 0
    for card in sortedHand:
        if not card.visible:
            continue
        if card.rank == 0:
            numAces += 1
    # count the value of the hand
    
    for card in sortedHand:
        if not card.visible:
            continue
        if card.rank > 9:
            value += 10
        else:
            value += card.rank + 1
    # adjust the value of the hand for aces
    for i in range(numAces):
        if value + 10 <= 21:
            value += 10

    return value

def decideMove(hand, dealerHand):
    isSoft = formattedHandValue(hand).find('/') != -1
    isSplit = len(hand) == 2 and hand[0].rank == hand[1].rank

    # if the hand is a split hand, use the split hand strategy
    if(isSplit):
        return splitStrategy(hand, dealerHand)

    # if the hand is a soft hand, use the soft hand strategy
    if isSoft:
        return softStrategy(hand, dealerHand)
    
    # if the hand is not a soft hand, use the hard hand strategy
    return hardStrategy(hand, dealerHand)

def hardStrategy(hand, dealerHand):
    dealerValueIndex = dealerHand[0].rank
    if dealerValueIndex > 9:
        dealerValueIndex = 9

    decision = HARD_STRATEGY_CHART[handValue(hand)][dealerValueIndex]
    return DECISIONS[decision];

def softStrategy(hand, dealerHand):
    dealerValueIndex = dealerHand[0].rank
    if dealerValueIndex > 9:
        dealerValueIndex = 9

    decision = SOFT_STRATEGY_CHART[handValue(hand)][dealerValueIndex];
    return DECISIONS[decision];

def splitStrategy(hand, dealerHand):
    dealerValueIndex = dealerHand[0].rank
    if dealerValueIndex > 9:
        dealerValueIndex = 9

    decision = SPLIT_STRATEGY_CHART[hand[0].rank][dealerValueIndex];
    return DECISIONS[decision];

def getBetAmount():
    global cardCounter, bankroll
    if cardCounter < 0:
        betAmount = MIN_BET
    else: 
        # quadratic with respect to cardCounter
        # betAmount = INITIAL_BET_AMT + INITIAL_BET_AMT * cardCounter*cardCounter
        # ?
        betAmount = INITIAL_BET_AMT + INITIAL_BET_AMT * cardCounter*cardCounter * bankroll / 1000
    if betAmount > bankroll*0.5: 
        betAmount = bankroll*0.5
    # round betAmount to a multiple of MIN_BET
    betAmount = betAmount - betAmount % MIN_BET
    return betAmount
    
def main():
    global bankroll, deck, handsPlayed, cardCounter

    while True:
        deck = shuffle()
        # print('Shuffling new deck...')
        time.sleep(2 / SPEED_MULTIPLIER)
        while bankroll > 0 and len(deck) > TOTAL_CARDS / 2:
            betAmount = getBetAmount()
            bankroll -= betAmount
            prevCardCounter = cardCounter
            result = deal(deck, betAmount, bankroll, auto=AUTOPLAY)
            bankroll += betAmount * result

            if(result > 1):
                if(winRecord.get(prevCardCounter) is None):
                    winRecord[prevCardCounter] = 0
                winRecord[prevCardCounter] += 1
            else:
                if(lossRecord.get(prevCardCounter) is None):
                    lossRecord[prevCardCounter] = 0
                lossRecord[prevCardCounter] += 1
            handsPlayed += 1

            if handsPlayed % 100 == 0:
                # get all the keys in winRecord and lossRecord and sort them.
                # this will be used to print the win/loss record in order
                keys = sorted(list(set(list(winRecord.keys()) + list(lossRecord.keys()))))
                winPercentages = {}
                for key in keys:
                    if key in winRecord and key in lossRecord:
                        total = winRecord[key] + lossRecord[key]
                        if(total < 10):
                            percentage = 0
                        else:
                            percentage = winRecord[key] / (winRecord[key] + lossRecord[key]) * 100
                    elif key in winRecord:
                        total = winRecord[key]
                        if(total < 10):
                            percentage = 0
                        else:
                            percentage = 100
                    else:
                        percentage = 0
                    # round to 1 decimal place
                    percentage = round(percentage, 1)
                    winPercentages[key] = percentage
                plt.clf()
                plt.bar(winPercentages.keys(), winPercentages.values())
                plt.pause(0.01)
                # return
            # after each hand, plot our bankroll
            # plt.plot(handsPlayed, bankroll, 'ro')
            # plt.pause(0.01)

            time.sleep(2 / SPEED_MULTIPLIER)


if __name__ == '__main__':
    main()

