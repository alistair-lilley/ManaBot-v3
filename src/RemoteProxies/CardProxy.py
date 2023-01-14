import json, os, re, aiohttp
from PIL import Image
from src.Constants import JSON_PATH, DATA_DIR, NAME
    
    
class CardProxy:
    
    def __init__(self):
        self.card_count = 0
        self.total_card_count = 0
        self.session = None
                      
    async def _fetch_database(self, bulk_json):
        uri = bulk_json['download_uri']
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False)) as http_session:
            print("Fetching database")
            database_fetch = await http_session.get(uri)
            print("Database fetched")
            print("Downloading database")
            database = await database_fetch.json()
            print("Database downloaded")
        return database


    def _split_up_json_cards(self, database):
        print("Splitting JSON")
        json_cards_split_up = [card for card in database]
        print("JSON split up")
        return json_cards_split_up


    def _save_database(self, json_cards_split_up):
        print("Saving database")
        for card in json_cards_split_up:
            with open(f'{DATA_DIR}/{JSON_PATH}/'
                      f'{self._simplify(card[NAME])}.json', 'w') as json_card_f:
                json.dump(card, json_card_f)
        print("Database saved\n")   
    
    
    def _simplify(self, string):
        return re.sub(r'[\W\s]', '', re.sub(r' ', '_', string)).lower()