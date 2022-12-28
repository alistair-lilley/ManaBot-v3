'''
    This file contains constants used elsewhere
'''

JSON_URL = "https://mtgjson.com/api/v5/AllPrintings.json"
CARD_IMAGE_URL = "https://gatherer.wizards.com/" \
                "Handlers/Image.ashx?name=%CARD%&type=card"
RULES_URL = "https://media.wizards.com/" \
                "%YR%/downloads/MagicCompRules%20%YR%%MO%%DAY%.txt"
CARD_STR_REPL = "%CARD%"
CARD_ID_TYPE = "name"
CARD_SIZE = (360, 500)

JSON_PATH = "json"

DATABASE_NOT_LOADED = "The database has not been loaded yet. "\
    "Please try again in a few minutes."

MSGMAX = 2000
HEAP_MAX = 1

COMMANDS = [
    "card",
    "rule"
]


NAME = "name"
POWER = "power"
TOUGHNESS = "toughness"
LEGALITIES = "legalities"
MANACOST = "convertedManaCost"
COLORS = "colors"
COLORID = "colorIdentity"
PT = "pt"
TEXT = "text"
TYPE = "type"

CARD_INFO_SECTIONS = [
        NAME, 
        POWER, 
        TOUGHNESS,
        LEGALITIES,
        MANACOST,
        COLORS,
        COLORID,
        PT,
        TEXT,
        TYPE
    ]