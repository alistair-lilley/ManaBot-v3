'''
    This file contains constants used elsewhere
'''

# URLs
BULK_DATA_URL = "https://api.scryfall.com/bulk-data"
BACKSIDE_URL = "https://static.wikia.nocookie.net/" \
                "mtgsalvation_gamepedia/images/f/f8/" \
                "Magic_card_back.jpg/revision/latest/scale-to-width-down" \
                "/250?cb=20140813141013"
RULES_URL = "https://media.wizards.com/" \
                "%YR%/downloads/MagicCompRules%20%YR%%MO%%DAY%.txt"
                
# Paths
DATA_DIR = "data"
JSON_PATH = "json_cards"
IMAGE_PATH = "cardimages"
RULES_FILE = "rules.txt"
SAVE_PATH = "textfiles/"
LOCAL_HASH = "hash"

# Card data
NAME = "name"
POWER = "power"
TOUGHNESS = "toughness"
LEGALITIES = "legalities"
MANACOST = "mana_cost"
COLORS = "colors"
COLORID = "color_identity"
PT = "pt"
TEXT = "oracle_text"
TYPE = "type_line"
IMAGE_URIS = "image_uris"
LARGE_IMAGE = "large"
NUMBER = 'collector_number' # is thit right?
BANNED = 'banned'
RESTRICTED = 'restricted'
LEGAL = 'legal'

## Get these into a convenient list
CARD_INFO_SECTIONS = [
        NAME, 
        POWER, 
        TOUGHNESS,
        #LEGALITIES,
        MANACOST,
        COLORS,
        COLORID,
        PT,
        TEXT,
        TYPE,
        IMAGE_URIS
    ]

PRETTY_SECTIONS = {
    NAME: "Name",
    POWER: "Power",
    TOUGHNESS: "Toughness",
    MANACOST: "Converted mana cost",
    COLORS: "Colors",
    COLORID: "Color ID",
    TEXT: "Card text",
    TYPE: "Card type"
}

# Deck data
ZIP = "zip"
COD = "cod"
MWDECK = "mwDeck"
TXT = "txt"
RAW = "rawtext"
JSON = "JSON"

# Magic numbers
MSGMAX = 2000
HEAP_MAX = 5
CARD_SIZE = (360, 500)
MINUTE = 60
HOUR = MINUTE*60
DAY = HOUR*24
CARD_CHUNK = 100
RATE_LIMIT = 1/10

# Misc?
CARD_DOWNLOAD_ERROR = "CARD FAILED TO DOWNLOAD"
EMPTY = ""
IDENTIFIERS = "identifiers"
CARD_STR_REPL = "%scryfallId%"
CARD_ID_TYPE = "scryfallId"
DATABASE_NOT_LOADED = "The database has not been loaded yet. "\
    "Please try again in a few minutes."