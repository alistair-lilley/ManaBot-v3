import os, re
import editdistance as edist
from collections import namedtuple
from src.Singleton import Singleton
from src.DatabaseObjs.Deck import Deck
from src.DatabaseObjs.Rules import Rules
from src.Constants import HEAP_MAX, RAW, DATA_DIR, JSON_PATH, EMPTY

Heap_item = namedtuple("HeapItem", "distance card")

class Database(Singleton, Deck, Rules):

    def __init__(self):
        super(Database, self).__init__(deck_file=EMPTY, file_type=RAW)
        self.sorted_cards = None
        print("Database initialized")
    
    
    def _card_edist(self, cardname):
        topcards = MinHeap()
        for card in self.sorted_cards:
            distance = edist.distance(card, cardname)
            topcards.insert(Heap_item(distance, card))
        card = topcards.serialize()[0]
        return card
    
    
    def reload(self):
        deck_file = '\n'.join(['0 '+ card.split('.')[0] for card in 
                               os.listdir(os.path.join(DATA_DIR, JSON_PATH))])
        self.comments, self.mainboard, self.sideboard \
            = self._parse_deck(deck_file, RAW)
        self.sorted_cards = sorted(self.mainboard.keys())
        self.ruletree = self._make_rules_tree()
        print("Database reloaded")
    
    
    def search_for_card(self, cardname):
        if cardname in self.mainboard.keys():
            return self.mainboard[cardname].cardobj
        #closest_card, similars = self._card_edist(cardname)
        closest_card = self._card_edist(self._simplify(cardname))
        return self.mainboard[closest_card].cardobj #, similars
    
    
    def search_for_rule(self, rulename):
        return self.retrieve_rule(self._simplify(rulename))
    

class MinHeap:
    
    def __init__(self):
        self.heap = []
        self.size = 0
        self.max = HEAP_MAX
    
    def _left(self, idx):
        return (idx + 1)*2 - 1
    
    def _right(self, idx):
        return (idx + 1)*2
    
    def insert(self, val):
        self.heap.append(val)
        self._heapify()
        if self.size >= self.max:
            self.heap = self.heap[:-1]
        else:
            self.size += 1
    
    def serialize(self):
        return [card.card for card in self.heap]
    
    def _heapify(self, idx=0):
        if (self._left(idx) <= self.size 
            and self.heap[idx].distance > self.heap[self._left(idx)].distance):
            temp = self.heap[idx]
            self.heap[idx] = self.heap[self._left(idx)]
            self.heap[self._left(idx)] = temp
            self._heapify(self._left(idx))
        if (self._right(idx) <= self.size 
            and self.heap[idx].distance > self.heap[self._right(idx)].distance):
            temp = self.heap[idx]
            self.heap[idx] = self.heap[self._right(idx)]
            self.heap[self._right(idx)] = temp
            self._heapify(self._right(idx))
        if idx < self.size - 1:
            self._heapify(idx+1)