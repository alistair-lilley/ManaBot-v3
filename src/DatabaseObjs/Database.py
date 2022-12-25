import os
import editdistance as edist
from src.Singleton import Singleton
from src.DatabaseObjs.Deck import Deck
from src.DatabaseObjs.Rules import Rules

RAW = "rawtext"

class Database(Singleton, Deck, Rules):

    def __init__(self, json_path, data_dir, info_sections, 
                 rules_file):
        deck_file = '\n'.join([f'0 {card[:-4]}' for card in 
                               os.listdir(data_dir + json_path)])
        super(Singleton, self).__init__()
        super(Deck, self).__init__(deck_file, RAW, data_dir, 
                                   info_sections)
        super(Rules, self).__init__(rules_file)
        self.sorted_cards = sorted(self.mainboard.keys())
    
    def _card_edist(self, cardname):
        topcards = MinHeap()
        for card in self.sorted_cards:
            distance = edist.distance(card, cardname)
            topcards.insert((distance, card))
        cards = topcards.serialize()
        return card[0], cards[1:]
    
    def search_for_card(self, cardname):
        if cardname in self.mainboard.keys():
            return self.mainboard[cardname]
        closest_card, similars = self._card_edist(cardname)
        return self.mainboard[closest_card], similars
    

class MinHeap:
    
    def __init__(self):
        self.heap = []
        self.size = 0
        self.max = 6
    
    def _left(self, idx):
        return idx*2
    
    def _right(self, idx):
        return idx*2 + 1
    
    def insert_val(self, val):
        self.heap.append(val)
        self._heapify(0)
        if self.size == self.max:
            self.heap = self.heap[:-1]
            return
        self.size += 1
    
    def serialize(self):
        return [card[1] for card in self.heap]
    
    def _heapify(self, idx):
        if (self._left(idx) < self.size 
            and self.heap[idx][0] > self.heap[self._left(idx)][0]):
            temp = self.heap[idx]
            self.heap[idx] = self.heap[self._left(idx)]
            self.heap[self._left(idx)] = temp
            self._heapify(self._left(idx))
        if (self._right(idx) < self.size 
            and self.heap[idx][0] > self.heap[self._right(idx)][0]):
            temp = self.heap[idx]
            self.heap[idx] = self.heap[self._right(idx)]
            self.heap[self._right(idx)] = temp
            self._heapify(self._right(idx))
        if self.idx < self.size - 1:
            self._heapify(idx+1)