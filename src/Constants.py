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

MSGMAX = 2000

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