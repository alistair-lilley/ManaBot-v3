import re, json, os
from collections import namedtuple
from PIL import Image
from io import BytesIO
from src.Constants import NAME, LEGALITIES, IMAGE_PATH, CARD_INFO_SECTIONS, DATA_DIR, JSON_PATH


Section = namedtuple("Section", "name default")


class Card:
    '''
        A Card is a singular object that contains a selected section of the
        information pertaining to that card, as well as its image as a _p_i_l 
        object. Two cards can be compared to each other and evaluated as <, >,
        or == based on their names.
    '''
    # card_info_sections is passed list of _section tuples for extracting from 
    # card_json
    def __init__(self, card_name):
        card_json = None
        with open(os.path.join(DATA_DIR, JSON_PATH, card_name + ".json"))\
            as read_card:
            card_json = json.load(read_card)
        self.cardinfo = self._extract(card_json)
        self.path = os.path.join(DATA_DIR, IMAGE_PATH, card_name + ".jpg")

    def __lt__(self, other_card):
        return self._comp_cards_alphabetically(other_card)

    def __gt__(self, other_card):
        return not self._comp_cards_alphabetically(other_card)

    def __eq__(self, other_card):
        return self.cardinfo[NAME] == other_card.get_name()

    def _comp_cards_alphabetically(self, other_card):
        thisname = self.cardinfo[NAME]
        other_card_name = other_card.name
        for this_char, other_char in list(zip(thisname, other_card_name)):
            if this_char < other_char:
                return True
            elif this_char > other_char:
                return False
        return len(thisname) < len(other_card_name)

    def _extract(self, card_json):
        cardinfo = dict()
        for section in CARD_INFO_SECTIONS:
            if section in card_json:
                if not card_json[section]:
                    cardinfo[section] = None
                else:
                    if type(card_json[section]) == dict:
                        cardinfo[section] = card_json[section]
                    else:
                        cardinfo[section] = str(card_json[section])
        return cardinfo
    
    def _simplify(self, string):
        return re.sub(r'[\W\s]', '', string).lower()

    @property
    def name(self):
        return self.cardinfo[NAME]

    @property
    def short_name(self):
        return self._simplify(self.cardinfo[NAME])

    @property
    def simple_name(self):
        return self._simplify(self[NAME])

    @property
    def legalities(self):
        return self.cardinfo[LEGALITIES]
    
    @property
    def image_path(self):
        return self.path
    
    @property
    def image_bytes(self):
        return BytesIO(open(self.path, 'rb').read())
        
    @property
    def information(self):
        return self.cardinfo
    
    @property
    def info_pretty(self):
        text = '\n'.join([f"**{section}**: {self.information[section]}" 
                          for section in self.information])
        return text