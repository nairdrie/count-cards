# TODO: if the player busts, dealer doesnt need to play out hand
# TODO: try with less decks and higher pen.
# TODO: the counter should be divided by the number of decks in the shoe

import time
import random
import os
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import numpy as np
clearConsole = lambda: os.system('cls')


# get the time the program started, formated as a string
startTime = time.strftime("%Y-%m-%d_%H%M%S", time.localtime())

AUTOPLAY = True
SPEED_MULTIPLIER = 10000000
CARD_COUNTER_WEIGHT = 1
INITIAL_BALANCE = 1000

MIN_BET = 1
INITIAL_BET = 10
MAX_BET = 5000
NUM_DECKS = 8
SUITS = ['♣', '♦', '♥', '♠']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
DECK_SIZE = len(SUITS) * len(RANKS)
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
    0:  [2, 2, 2, 2, 2, 2, 2, 2, 2, 2], # A
    1:  [0, 0, 0, 2, 2, 2, 2, 0, 0, 0], # 2
    2:  [0, 0, 0, 2, 2, 2, 2, 0, 0, 0], # 3
    3:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 4
    4:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 5
    5:  [0, 0, 2, 2, 2, 2, 0, 0, 0, 0], # 6
    6:  [0, 2, 2, 2, 2, 2, 2, 0, 0, 0], # 7
    7:  [2, 2, 2, 2, 2, 2, 2, 2, 2, 2], # 8
    8:  [1, 2, 2, 2, 2, 2, 1, 2, 2, 1], # 9
    9:  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # 10
    10: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # J
    11: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # Q
    12: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # K
}

START_TIME = 0# delete me

hiLoRatio = 0
deck = []
bankroll = INITIAL_BALANCE
handsPlayed = 0

winRecord = {}
lossRecord = {}
totalWins = 0
totalLosses = 0

bankrollHistory = []
scaledHiLoHistory = []


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
    global hiLoRatio
    deck = []
    hiLoRatio = 0

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

def deal(deck, betAmount, auto=False):
    global SPEED_MULTIPLIER, START_TIME, bankroll # delete me
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

    # Player's turn
    for hand in playerHands:
        # handsComplete = 0
        # if handsComplete == len(playerHands):
        #     break
        while True:
            # if it has been 10 seconds since the last action, speed up the game
            # if time.time() - START_TIME > 10:
            #     SPEED_MULTIPLIER = 100
            if auto:
                action = decideMove(hand, dealerHand)
                # if action.lower() == 'split':
                #     SPEED_MULTIPLIER = 0.5
                #     time.sleep(2)
                #     # note the current time
                #     START_TIME = time.time()
            else:
                action = input('(H)it, (S)tand?, or s(P)lit? ')

            if action.lower() == 'hit' or action.lower() == 'h':
                nextCard = drawCard(deck)
                nextCard.flip()
                hand.append(nextCard)
                printGame(dealerHand, playerHands, betAmount)
                if handValue(hand) > 21:
                    break
            elif action.lower() == 'stand' or action.lower() == 's':
                break
            elif action.lower() == 'split' or action.lower() == 'p':
                if len(hand) == 2 and hand[0].rank == hand[1].rank:
                    bankroll -= betAmount
                    splitHand = []
                    splitHand.append(hand.pop())
                    nextCard = drawCard(deck)
                    nextCard.flip()
                    hand.append(nextCard)
                    nextCard = drawCard(deck)
                    nextCard.flip()
                    splitHand.append(nextCard)
                    playerHands.append(splitHand)
                    printGame(dealerHand, playerHands, betAmount) 
                else:
                    print('Invalid input')
            else:
                print('Invalid input')
    
    # flip the dealer's face down card
    dealerHand[1].flip()
    printGame(dealerHand, playerHands, betAmount)

    
    # playerValue = handValue(playerHand)
    # playerHasBlackjack = playerValue == 21 and len(playerHand) == 2

    # if not didBust and not playerHasBlackjack:
    # Dealer's turn
    while handValue(dealerHand) < 17:
        nextCard = deck.pop()
        nextCard.flip()
        dealerHand.append(nextCard)
        printGame(dealerHand, playerHands, betAmount)
        if handValue(dealerHand) > 21:
            break
    
    return determineWinner(dealerHand, playerHands)
    
def determineWinner(dealerHand, playerHands):
     # determine winner
    winnings = []
    dealerValue = handValue(dealerHand)
    dealerHasBlackjack = dealerValue == 21 and len(dealerHand) == 2
    for hand in playerHands:
        playerValue = handValue(hand)
        playerHasBlackjack = handValue(hand) == 21 and len(hand) == 2
        if playerHasBlackjack and dealerHasBlackjack:
            print('Push!')
            winnings.append(1)
        elif playerHasBlackjack:
            print('Blackjack! Player wins.')
            winnings.append(3)
        elif dealerHasBlackjack:
            print('Blackjack. Dealer wins.')
            winnings.append(0)
        elif playerValue > 21:
            print('Bust! Dealer wins.')
            winnings.append(0)
        elif dealerValue > 21:
            print('Bust! Player wins.')
            winnings.append(2)
        elif playerValue > dealerValue:
            print('Player Wins.')
            winnings.append(2)
        elif playerValue < dealerValue:
            print('Dealer Wins.')
            winnings.append(0)
        else:
            print('Push!')
            winnings.append(1)

    return winnings

def formatTime(seconds):
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)

def printGame(dealerHand, playerHands, betAmount):
    global bankroll, deck, hiLoRatio, handsPlayed, totalWins, totalLosses

    clearConsole()

    decksRemaining = len(deck) / DECK_SIZE

    print ('Bet Amount:', betAmount)
    print ('Bankroll:', bankroll)
    print ('Cards remaining:', len(deck))
    print ('Hi-Lo Ratio:', hiLoRatio)
    # ronded to 2 decimal places
    print ('Scaled Hi-Lo Ratio:', round(hiLoRatio / decksRemaining, 2))
    if totalWins + totalLosses > 0:
        print ('Overall Win Rate:', round(totalWins / (totalWins + totalLosses), 2))
    else:
        print ('Overall Win Rate: N/A')
    print ('Hands played:', handsPlayed)
    print ('Time elapsed:', formatTime(handsPlayed * AVG_HAND_TIME))
    print( '----------------------------------------')
    print ('Dealer\'s Hand:', handValue(dealerHand))
    printHand(dealerHand)
    for hand in playerHands:
        print ('Player\'s Hand:', handValue(hand))
        printHand(hand)
    time.sleep(1 / SPEED_MULTIPLIER)

def drawCard(deck):
    global hiLoRatio

    nextCard = deck.pop()

    # if its 2-6, increment the count
    if nextCard.rank > 0 and nextCard.rank < 6:
        hiLoRatio += 1
    # if its 10-A, decrement the count
    elif nextCard.rank == 0 or nextCard.rank >= 9:
        hiLoRatio -= 1

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

def determineBetAmount():
    return INITIAL_BET
    return hiLoBetAmount()
    
def hiLoBetAmount():
    global hiLoRatio, bankroll, deck
    decksRemaining = len(deck) / DECK_SIZE
    betAmount = INITIAL_BET * hiLoRatio / decksRemaining

    # clamp bet amount between INITIAL_BET and 50% of bankroll
    if betAmount < INITIAL_BET:
        betAmount = INITIAL_BET
    if betAmount > bankroll*0.5: 
        betAmount = bankroll*0.5
    if betAmount > MAX_BET:
        betAmount = MAX_BET

    # round betAmount to a multiple of MIN_BET
    betAmount = betAmount - betAmount % MIN_BET

    return betAmount

def main():
    global bankroll, deck, handsPlayed, hiLoRatio, winRecord, lossRecord, bankrollHistory, scaledHiLoHistory, totalWins, totalLosses

    while True:
        deck = shuffle()
        # print('Shuffling new deck...')
        time.sleep(2 / SPEED_MULTIPLIER)
        while bankroll > 0 and len(deck) > TOTAL_CARDS / 2:
            betAmount = determineBetAmount()
            decksRemaining = len(deck) / DECK_SIZE
            prevScaledHiLoRatio = hiLoRatio / decksRemaining
            # round prevScaledHiLoRatio to the nearest 0.5
            prevScaledHiLoRatio = round(prevScaledHiLoRatio * 2) / 2
            bankroll -= betAmount
            results = deal(deck, betAmount, auto=AUTOPLAY)
            for result in results:
                bankroll += betAmount * result

                if(result > 1):
                    totalWins += 1
                    if(winRecord.get(prevScaledHiLoRatio) is None):
                        winRecord[prevScaledHiLoRatio] = 0
                    winRecord[prevScaledHiLoRatio] += 1
                elif(result < 1):
                    totalLosses += 1
                    if(lossRecord.get(prevScaledHiLoRatio) is None):
                        lossRecord[prevScaledHiLoRatio] = 0
                    lossRecord[prevScaledHiLoRatio] += 1
            handsPlayed += 1
            bankrollHistory.append(bankroll)
            scaledHiLoHistory.append(hiLoRatio/decksRemaining)

            # plot the win/loss ratio and the bankroll every 100 hands
            if handsPlayed % 100 == 0:
                plotWinLossRatio()
                plotBankroll()

            time.sleep(2 / SPEED_MULTIPLIER)

def plotWinLossRatio():
    global winRecord, lossRecord

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
                percentage = winRecord[key] / total * 100
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
        if percentage > 0:
            winPercentages[key] = percentage
    # get the average total humber of hands for each ratio
    totalHands = 0
    for key in winPercentages.keys():
        totalHands += winRecord[key] + lossRecord[key]

    if len(winPercentages.keys()) == 0:
        return
    averageTotalHands = totalHands / len(winPercentages.keys())
    # loop through win percentages, if the total number of hands played for that ratio is an outlier, remove it
    for key in list(winPercentages.keys()):
        total = winRecord[key] + lossRecord[key]
        if total < averageTotalHands * 0.5:
            del winPercentages[key]            
    plt.clf()
    plt.bar(winPercentages.keys(), winPercentages.values(), width=0.45)
    x = np.array(list(winPercentages.keys()))
    y = np.array(list(winPercentages.values()))
    #calculate equation for trendline
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    #add trendline to plot
    plt.plot(x, p(x), 'r')

    plt.xlabel('Scaled Hi-Lo Ratio')
    plt.ylabel('Win Percentage')
    plt.title('Win Percentage vs Hi-Lo Ratio')
    # plt.grid(True)
    
    # get the slope of the trendline
    slope = z[0]
    # display it on the graph
    plt.text(0.5, 0.5, 'Slope: ' + str(round(slope, 2)), horizontalalignment='center', verticalalignment='center', transform=plt.gca().transAxes)

    # save the graph to a file, with startTime in the filename
    plt.savefig('win_percentage_scaled_hi_lo_' + str(startTime) + '.png')

def plotBankroll():
    global bankrollHistory, scaledHiLoHistory, handsPlayed
    # plot the bankroll and the hiLoHistory on 2 separate y axes vs hands played
    # the hiLoHistory is plotted on the right y axis in a lighter color & dashed line, behind the bankroll
    fig, ax1 = plt.subplots()
    ax1.plot(range(handsPlayed), bankrollHistory, 'b', linewidth=0.5)
    ax1.set_xlabel('Hands Played')
    ax1.set_ylabel('Bankroll', color='b')
    ax1.tick_params('y', colors='b')
    
    ax2 = ax1.twinx()
    ax2.plot(range(handsPlayed), scaledHiLoHistory, 'pink',  linewidth=0.5)
    ax2.set_ylabel('Hi-Lo Ratio', color='r')
    ax2.tick_params('y', colors='r')

    fig.tight_layout()
    plt.savefig('bankroll_min_bet_' + str(startTime) + '.png')



if __name__ == '__main__':
    main()

