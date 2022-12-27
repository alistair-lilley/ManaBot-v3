import re, io, json, os
from collections import namedtuple
from PIL import Image
from io import BytesIO


Section = namedtuple("Section", "name default")

NAME = "name"
POWER = "power"
TOUGHNESS = "toughness"
LEGALITIES = "legalities"


class Card:
    '''
        A Card is a singular object that contains a selected section of the
        information pertaining to that card, as well as its image as a _p_i_l 
        object. Two cards can be compared to each other and evaluated as <, >,
        or == based on their names.
    '''
    # card_info_sections is passed list of _section tuples for extracting from 
    # card_json
    def __init__(self, card_json_path, card_image_dir, card_info_sections):
        with open(card_json_path) as read_card:
            card_json = json.load(read_card)
        self.cardinfo = self._extract(card_json, card_info_sections)
        self.image_path = os.path.join(card_image_dir, card_json_path)

    def __lt__(self, other_card):
        return self._comp_cards_alphabetically(other_card)

    def __gt__(self, other_card):
        return not self._comp_cards_alphabetically(other_card)

    def __eq__(self, other_card):
        return self.cardinfo[NAME] == other_card.get_name()

    def _comp_cards_alphabetically(self, other_card):
        thisname = self.cardinfo[NAME]
        other_card_name = other_card.get_name()
        for this_char, other_char in list(zip(thisname, other_card_name)):
            if this_char < other_char:
                return True
            elif this_char > other_char:
                return False
        return len(thisname) < len(other_card_name)

    def _extract(self, card_json, card_info_sections):
        cardinfo = dict()
        for section in card_info_sections:
            if section.name in card_json:
                if not card_json[section.name]:
                    cardinfo[section.name] = section.default
                else:
                    if type(card_json[section.name]) == dict:
                        cardinfo[section.name] = card_json[section.name]
                    else:
                        cardinfo[section.name] = str(card_json[section.name])
        return cardinfo
    
    def _get_image_bytes(self):
        image = Image.open(self.image_path)
        image_stream = image.tobytes()
        image_bytesio = BytesIO(image_stream)
        return image_bytesio

    def _simplify(self, string):
        return re.sub(r'[\_w\s]', '', string).lower()

    @property
    def name(self):
        return self.cardinfo[NAME]

    @property
    def short_name(self):
        return self._simplify(self.cardinfo[NAME])

    @property
    def simple_name(self):
        return self._simplify(self.name)

    @property
    def legalities(self):
        return self.cardinfo[LEGALITIES]
    
    @property
    def image_bytes(self):
        return self._get_image_bytes()
        
    @property
    def information(self):
        return self.cardinfo
    
    @property
    def info_pretty(self):
        text = '\n'.join([f"**{section}**: {self.information[section]}" 
                          for section in self.information])
        return text