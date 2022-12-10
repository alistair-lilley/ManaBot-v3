import re
import xml.etree.ElementTree as ET
import json
from collections import namedtuple
from Card import Card

ZIP = "zip"
COD = "cod"
MWDECK = "mwDeck"
TXT = "txt"
RAW = "rawtext"
JSON = "JSON"
IMAGEPATH = "cardimages/"
JSONPATH = "jsoncards/"
SAVEPATH = "textfiles/"
NAME = 'name'
NUMBER = 'number'
BANNED = 'banned'
RESTRICTED = 'restricted'
LEGAL = 'legal'

CardPair = namedtuple("CardPair", "num cardobj")

class Deck:
    '''
        A deck is a collection of cards (implemented as Card objects).
    '''
    def __init__(self, deck_file, file_type, data_dir, info_sections, text_dir):
        self.textdir = text_dir
        self.datadir = data_dir
        self.name = deck_file
        self.jsonpaths = data_dir + JSONPATH
        self.imagepaths = data_dir + IMAGEPATH
        self.savedir = data_dir + SAVEPATH
        self.info_sections = info_sections
        formats = open('testdata/formats.txt')
        self.default_legality_formats = {line.strip().split(',')[0] : 
                                         line.strip().split(',')[1]
                                         for line in formats}
        formats.close()
        self.comments, self.mainboard, self.sideboard \
            = self._parse_deck(deck_file, file_type)

    def _make_card(self, card):
        card = self._simplify(card)
        return Card(self.jsonpaths + card + '.json', 
                    self.imagepaths + card + '.jpg', self.info_sections)

    def _parse_deck(self, deck_file, file_type):
        if file_type == RAW:
            card_list = self._from_raw(deck_file)
            comments, mainboard, sideboard = card_list
        else:
            card_list = self._from_file(deck_file, file_type)
            comments, mainboard, sideboard = card_list
        return comments, mainboard, sideboard

    def _from_file(self, deck_file, file_type):
        with open(self.datadir + "testdecks/" + deck_file + '.' + file_type) \
                  as read_deck_file:
            deck_data = read_deck_file.read()
        if file_type == COD:
            return self._fromcod(deck_data)
        elif file_type in [MWDECK, TXT] :
            return self._from_mw_deck_txt(deck_data, file_type)
        elif file_type == JSON:
            return self._from_json(deck_data)
        else:
            return deck_data

    # cod file is basically an xml file, so we parse it like an XML tree
    # deck_data is passed in as a string of the XML (cod) file
    def _fromcod(self, deck_data):
        codtree = ET.ElementTree(ET.fromstring(deck_data))
        codroot = codtree.getroot()
        comments = []
        mainboard = {}
        sideboard = {}
        for zone in codroot:
            if zone.tag in ['deckname','comments'] and zone.text:
                comments += ["//" + line for line in zone.text.split('\n')]
            elif zone.tag == "zone" and zone.attrib[NAME] == 'main':
                mainboard = self._get_board_cod(zone)
            elif zone.tag == "zone" and zone.attrib[NAME] == 'side':
                sideboard = self._get_board_cod(zone)
        return comments, mainboard, sideboard

    def _get_board_cod(self, zone):
        board = {}
        for card in zone:
            if zone.attrib[NAME] == 'main':
                board[card.attrib[NAME]] = CardPair(card.attrib[NUMBER], 
                self._make_card(card.attrib[NAME]))
        return board

    # This is both for txt and mwDeck, because the only difference is the number
    # of times you split the line mwDeck is in the format `1 [ZEN] Marsh Flats`,
    # so you want to skip the setID in the middle txt doesn't have the setID,
    # and that's the only difference
    def _from_mw_deck_txt(self, deck_file, ext):
        if ext == MWDECK:
            splitnum = 2
        else:
            splitnum = 1
        comments = []
        mainboard = {}
        sideboard = {}
        lines = deck_file.split('\n')
        for line in lines:
            if not line:
                continue
            if line[0] == '/':
                comments.append(line)
            elif line[0] == 'S':
                # Cuts out the SB: and strips it so it's the same format as a
                # non-sideboard line
                line = line.split(' ', 1)[1].strip()
                num, card = self._pull_num_card(line, splitnum)
                sideboard[card] = CardPair(num, self._make_card(card))
            elif line[0].isdigit:
                num, card = self._pull_num_card(line, splitnum)
                mainboard[card] = CardPair(num, self._make_card(card))
        return comments, mainboard, sideboard

    def _from_raw(self, deck_raw):
        return self._from_mw_deck_txt(deck_raw, TXT)

    def _to_text(self):
        deck_text = ''
        if self.comments:
            comments = [comment for comment in self.comments]
            deck_text += '\n'.join(comments) + '\n'
        mainboard = [self.mainboard[card].num + ' ' \
            + self.mainboard[card].cardobj.get_name() for card in self.mainboard]
        deck_text += '\n'.join(mainboard)
        if self.sideboard:
            sideboard = ['SB: ' + self.sideboard[card].num + ' '
                         + self.sideboard[card].cardobj.get_name()
                         for card in self.sideboard]
            deck_text += '\n' + '\n'.join(sideboard)
        return deck_text

    def _from_json(self, strdata):
        datadict = json.loads(strdata)

    def _to_ban_txt(self, bannedsets, restrictedsets, set_legalities): #, legalsets
        out = "**Banned cards**"
        for banset in bannedsets:
            set_proper_name = set_legalities[banset]
            out += f'\n__{set_proper_name}__'
            for card in bannedsets[banset]:
                out += '\n' + card
        out += "\n**Restricted cards**"
        for restset in restrictedsets:
            set_proper_name = set_legalities[restset]
            out += f'\n__{set_proper_name}__'
            for card in restrictedsets[restset]:
                out += '\n' + card
        # This is an optional section, may reinstate later
        #out += "\n**Legal cards**"
        #for legset in legalsets:
        #    out += f'\n__{set_legalities[legset]}__'
        #    for card in legalsets[legset]:
        #        out += '\n' + card
        return out

    def _get_bans_from_legalities(self, set_legalities):
        banned_cards = {}
        restricted_cards = {}
        legal_cards = {}
        allboards = {**self.mainboard, **self.sideboard}
        for card in allboards:
            cardobj = allboards[card].cardobj
            legalities = [legalset for legalset in cardobj.get_legalities() if
                          legalset in list(set_legalities.keys())]
            for legality in legalities:
                format_legality = self._simplify(cardobj.get_legality(legality))
                if format_legality == BANNED:
                    banned_cards[legality] = banned_cards.get(legality, []) \
                        + [cardobj.get_name()]
                elif format_legality == RESTRICTED:
                    restricted_cards[legality] \
                        = restricted_cards.get(legality, []) \
                            + [cardobj.get_name()]
                elif format_legality == LEGAL:
                    legal_cards[legality] = legal_cards.get(legality, []) \
                        + [cardobj.get_name()]
        bans = self._to_ban_text(banned_cards, restricted_cards, legal_cards,
                               set_legalities)

    def _simplify(self, string):
        return re.sub(r'[\_w\s]', '', string).lower()

    # Pulls the number and the card from a line in a txt or mwDeck file line
    def _pull_num_card(self, line, numsplit):
        card_line_split = line.split(' ', numsplit)
        num = card_line_split[0]
        card = card_line_split[-1]
        return num, card
        #return bans

    def get_bans(self, legalities=None):
        if not legalities:
            legalities = self.default_legality_formats
        return self._get_bans_from_legalities(legalities)
        
    def to_txt_file(self):
        with open(self.savedir + self.name, 'w') as save_deck_file:
            decktext = self._to_text()
            save_deck_file.write(decktext)