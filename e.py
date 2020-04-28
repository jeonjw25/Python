suits = 'CDHS'
ranks = '23456789TJQKA'
values = dict(zip(ranks, range(2, 2+len(ranks))))



from abc import ABCMeta, abstractmethod

class Card(metaclass=ABCMeta):
    """Abstact class for playing cards
    """
    def __init__(self, rank_suit):
        if rank_suit[0] not in ranks or rank_suit[1] not in suits:
            raise ValueError(f'{rank_suit}: illegal card')
        self.card = rank_suit
        
    def __repr__(self):
        return self.card
    
    @abstractmethod
    def value(self):
        """Subclasses should implement this method
        """
        raise NotImplementedError("value method not implemented")

    # card comparison operators
    def __gt__(self, other): return self.value() > other.value()
    def __ge__(self, other): return self.value() >= other.value()
    def __lt__(self, other): return self.value() < other.value()
    def __le__(self, other): return self.value() <= other.value()
    def __eq__(self, other): return self.value() == other.value()
    def __ne__(self, other): return self.value() != other.value()


class PKCard(Card):
    """Card for Poker game
    """
    def __init__(self, rank_suit):
        if rank_suit[0] not in ranks or rank_suit[1] not in suits:
            raise ValueError(f'{rank_suit}: illegal card')
        self.card = rank_suit
        
    def __repr__(self):
        return self.card

    def value(self):
        dic = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':11, 'Q':12, 'K':13, 'A':14}
        return dic.get(self.card[0])


if __name__ == '__main__':
    c1 = PKCard('QC')
    c2 = PKCard('9D')
    c3 = PKCard('9C')
    print(f'{c1} {c2} {c3}')

    # comparison
    print(c1 > c2 == c3)

    # sorting
    cards = [c1, c2, c3, PKCard('AS'), PKCard('2D')]
    sorted_cards = sorted(cards)
    print(sorted_cards)
    cards.sort()
    print(cards)


import random
import itertools
class Deck:
    def __init__(self, cls):
        """Create a deck of 'cls' card class
        """
        self.tmplist = list(''.join(s) for s in itertools.product(ranks, suits))
        cls.deck = []
        for s in self.tmplist:
            cls.deck.append(cls(s))
        # print(cls.deck)
 
    def shuffle(self, cls):
        # for i in range(len(cls.deck)-1, 0,-1):
        #     r = random.randint(0,i)
        #     cls.deck[i], cls.deck[r] = cls.deck[r], cls.deck[i]
        self.deck = random.sample(cls.deck, len(cls.deck))
        # print(cls.deck)
        return self.deck

    def __str__(self):
        return str(self.deck)

    def __getitem__(self, index):
        return self.deck[index]

    def __len__(self):
            return len(self.deck)

    def pop(self):
        return self.deck.pop()
        

if __name__ == '__main__':
    deck = Deck(PKCard)  # deck of poker cards
    deck.shuffle(PKCard)
    c = deck[0]   # __getitem__
    print('A deck of', c.__class__.__name__)
    print(deck)   # __str__
    # testing __getitem__ method
    print(deck[-5:])
    while len(deck) >= 10:   # __len__
        my_hand = []
        your_hand = []
        for i in range(5):
            for hand in (my_hand, your_hand):
                card = deck.pop()
                hand.append(card)
        my_hand.sort(reverse=True)
        your_hand.sort(reverse=True)
        print(my_hand, '>', your_hand, '?', my_hand > your_hand)
        # my_hand = ['KS', 'QS', '7S', '5S', '3S']

class Hands:
    def __init__(self, cards):
        if len(cards) != 5:
            raise ValueError('not 5 cards')
        self.cards = sorted(cards, reverse=True)

    def __str__(self):
        return str(self.cards)

    def __getitem__(self, x):
        return self.cards[x]

    def value(self, val):
        dic = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':11, 'Q':12, 'K':13, 'A':14}
        return dic.get(val)    

    def is_flush(self):
        test_suit = str(self.cards[0])
        # print(test_suit[1])
        # for i in self.cards:
        #     print(str(i)[1])
        if(all(str(element)[1] == test_suit[1] for element in self.cards)):
            return True
        else:
            return False

    def is_straight(self):
        temp = []
        # for i in self.cards:
        #     print(self.value(str(i)[0]))
        for i in self.cards:
            temp.append(self.value(str(i)[0]))
        temp.sort()
        self.cards_by_ranks = temp
        if temp == [2, 3, 4, 5, 14]:
            return True
        else:
            stop = 1
            for i in range (0, 4):
                if temp[i]+1 != temp[i+1]:
                    stop = 0
                    return False
            if stop == 1:
                return True

    def classify_by_rank(self):
        self.dic = {}
        for i in self.cards_by_ranks:
            if i not in self.dic:
                self.dic[i] = 1
            else:
                self.dic[i] = self.dic[i] + 1
                
        # print('dic : ', self.dic)
        return self.dic

    def find_a_kind(self):
        dic = self.classify_by_rank()
        val_num = []
        for i in dic.values():
            val_num.append(i)
        # print('val_num : ', val_num)
        if 4 in val_num:
            return 'Four of a kind'
        elif 3 in val_num and 2 in val_num:
            return 'Full house'
        elif val_num.count(2) == 2:
            return 'Two pairs'
        elif 3 in val_num:
            return 'Three of a kind'
        elif 2 in val_num:
            return 'One pair'
        else:
            return 'High card'

    def tell_hand_ranking(self):
        if self.is_flush() == True:
            flush = True
        else:
            flush = False
        if self.is_straight() == True:
            straight = True
        else:
            straight = False
        self.fak = self.find_a_kind()
        if flush == True and straight == True:
            return 9, self.cards, self.dic
            # return 'Straight flush'
        elif self.fak == 'Four of a kind':
            return 8, self.cards, self.dic
            # return 'Four of a kind'
        elif self.fak == 'Full house':
            return 7, self.cards, self.dic
            # return 'Full house'
        elif flush == True:
            return 6, self.cards, self.dic
            # return 'Flush'
        elif straight == True:
            return 5, self.cards, self.dic
            # return 'Straight'
        elif self.fak == 'Three of a kind':
            return 4, self.cards, self.dic
            # return 'Three of a kind'
        elif self.fak == 'Two pairs':
            return 3, self.cards, self.dic
            # return 'Two pairs'
        elif self.fak == 'One pair':
            return 2, self.cards, self.dic
            # return 'One pair'
        else:
            return 1, self.cards, self.dic
            # return 'High card'

def play_game(player1, player2):
    p1, c1, d1 = player1.tell_hand_ranking()
    p2, c2, d2 = player2.tell_hand_ranking()
    # d1_key_sorted = list(sorted(d1.keys(), reverse=True))
    # d2_key_sorted = list(sorted(d2.keys(), reverse=True))
    # d1_value_sorted = list(sorted(d1.items(), key=lambda item:item[1], reverse=True))
    # d2_value_sorted = list(sorted(d2.items(), key=lambda item:item[1], reverse=True))
    temp1 = []
    for i in c1:
        temp1.append(value(str(i)[0]))
    c1_sorted = sorted(temp1, reverse=True)
    temp2 = []
    for i in c2:
        temp2.append(value(str(i)[0]))
    c2_sorted = sorted(temp2, reverse=True)

    # print('c1_sorted : ', c1_sorted)
    # print('c2_sorted : ', c2_sorted)

    if p1 > p2:
        return "I have won!!"
    elif p1 < p2:
        return "You have won!!"
    elif p1 == 9 or p1 == 6 or p1 == 5 or p1 == 1:
        if c1_sorted > c2_sorted:
            return "I have won!!"
        elif c1_sorted < c2_sorted:
            return "You have won!!"
        else: return "Draw!!"
    elif p1 == 8:
        for k, v in d1.items():
            if v == 4:
                k1 = k
        for k, v in d2.items():
            if v == 4:
                k2 = k
        if k1 > k2:
            return "I have won!!"
        else:   
            return "You have won!!"
    elif p1 == 7 or p1 ==4:
        for k, v in d1.items():
            if v == 3:
                k1 = k
        for k, v in d2.items():
            if v == 3:
                k2 = k
        if k1 > k2:
            return "I have won!!"
        else:   
            return "You have won!!"
    elif p1 == 3:
        k1 = []
        for k, v in d1.items():
            if v == 2:
                k1.append(k)
        k2 = []
        for k, v in d2.items():
            if v == 2:
                k2.append(k)
        for k, v in d1.items():
            if v == 1:
                k3 = k
        for k, v in d2.items():
            if v == 1:
                k4 = k
        
        if sorted(k1, reverse=True) > sorted(k2, reverse=True):
            return "I have won!!"
        elif sorted(k1, reverse=True) < sorted(k2, reverse=True): 
            return "You have won!!"
        elif k3 > k4:
            return "I have won!!"
        elif k3 < k4:
            return "You have won!!"
        else: return "Draw!!"
    else:
        
        for k, v in d1.items():
            if v == 2:
                k1 = k
        for k, v in d2.items():
            if v == 2:
                k2 = k
        q1 = []
        for k, v in d1.items():
            if v == 1:
                q1.append(k)
        q2 = []
        for k, v in d2.items():
            if v == 1:
                q2.append(k)
        
        if k1 > k2:
           return "I have won!!"
        elif k1 < k2:
           return "You have won!!"
        elif sorted(q1, reverse=True) > sorted(q2, reverse=True):
            return "I have won!!"
        elif sorted(q1, reverse=True) < sorted(q2, reverse=True): 
            return "You have won!!"
        else: return "Draw!!"
    


def value(s):
    dic = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':11, 'Q':12, 'K':13, 'A':14}
    return dic.get(s)          



if __name__ == '__main__':
    import sys
    def test(did_pass):
        """  Print the result of a test.  """
        linenum = sys._getframe(1).f_lineno   # Get the caller's line number.
        if did_pass:
            msg = "Test at line {0} ok.".format(linenum)
        else:
            msg = ("Test at line {0} FAILED.".format(linenum))
        print(msg)

    # your test cases here



# Straight Flush
# your_hand = ['KC', 'QC', 'JC', 'TC', '9C']
# my_hand = ['JS', 'TS', '9S', '8S', '7S']

# Four of a kind
# your_hand = ['QC', 'QS', 'QD', 'QH', 'TH']
# my_hand = ['JC', 'JS', 'JD', 'JH', '9H']

# Full house
# your_hand = ['QC', 'QS', 'QD', 'AH', 'AD']
# my_hand = ['KC', 'KS', 'KD', 'JH', 'JD']

# Flush
# my_hand = ['KC', '2C', 'JC', 'TC', '9C']
# your_hand = ['JS', 'TS', '3S', '8S', '7S']

# Straight
# my_hand = ['KC', 'QD', 'JC', 'TC', '9C']
# your_hand = ['JS', 'TS', '9S', '8H', '7S']

# Three of a kind
# your_hand = ['QC', 'QS', 'QD', '8H', 'TH']
# my_hand = ['JC', 'JS', '3D', 'JH', '9H']

# Two pairs
# my_hand = ['9C', '9D', 'TD', 'JH', 'JD']
# your_hand = ['JC', 'JS', 'TH', '9S', '9H']

# One pair
# my_hand = ['2C', 'QS', 'TD', '8H', 'TH']
# your_hand = ['QC', '8S', '2D', 'TS', 'TC']

# High card
# my_hand = ['2C', 'QS', 'TD', '8H', '3H']
# your_hand = ['QC', '8S', '2D', 'KS', 'TC']


my = Hands(my_hand)
your = Hands(your_hand)

print('my hand : ', my.tell_hand_ranking())
print('your hand : ', your.tell_hand_ranking())
print('Game Result : ', play_game(my, your))

