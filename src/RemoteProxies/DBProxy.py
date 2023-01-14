import aiohttp, os, asyncio, json
from src.Singleton import Singleton
from src.RemoteProxies.CardProxy import CardProxy
from src.RemoteProxies.RuleProxy import RuleProxy
from src.Constants import DATA_DIR, LOCAL_HASH, JSON_PATH, \
    IMAGE_PATH, DAY, BULK_DATA_URL


class DBProxy(Singleton, CardProxy, RuleProxy):
    '''
        The DataBase Proxy sends requests and receives data from the remote 
        databases that hold MtG card data. It also requests and receives data
        from the Rules database. It updates the local database files.
    '''
    def __init__(self):
        self.local_hash = os.path.join(DATA_DIR, LOCAL_HASH)
        if not os.path.exists(DATA_DIR):
            os.mkdir(DATA_DIR)
        if not os.path.exists(os.path.join(DATA_DIR, JSON_PATH)):
            os.mkdir(os.path.join(DATA_DIR, JSON_PATH))
        if not os.path.exists(os.path.join(DATA_DIR, IMAGE_PATH)):
            os.mkdir(os.path.join(DATA_DIR, IMAGE_PATH))
        self.no_json_update = False
               
                
    async def _fetch_bulk_data(self):
        print("Fetching bulk data object")
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False)) as http_session:
            bulk_database = await http_session.get(BULK_DATA_URL)
            print("Bulk data object fetched")
            print("Downloading bulk data object")
            bulk_json_downloaded = await bulk_database.json()
            print("Bulk data json downloaded")
        data = bulk_json_downloaded["data"]
        bulk_json = None
        for db in data:
            if db["type"] == "oracle_cards":
                bulk_json = db
        return bulk_json


    # Lets fix this up with argparse later
    async def check_update_db(self, database, no_update, clear_hash,
                              no_json_update):
        self.no_json_update = no_json_update
        if clear_hash:
            self._clear_hash()
        if no_update:
            print("Skipping first update")
            print("Ready to go!\n")
            await asyncio.sleep(DAY)
        while True:
            db = await self._should_update()
            if db:
                await self._update_db(db)
            database.reload()
            print("Ready to go!\n")
            await asyncio.sleep(DAY)


    async def _should_update(self):
        if not os.path.exists(os.path.join(DATA_DIR, LOCAL_HASH)):
            with open(os.path.join(DATA_DIR, LOCAL_HASH), 'w') as newhash:
                newhash.write('')
                print("Hash file made")
        bulk_json = await self._fetch_bulk_data()
        with open(os.path.join(DATA_DIR, LOCAL_HASH)) as hash:
            if hash.read() == bulk_json["updated_at"]:
                print("Hash found -- database up to date.\n")
                return None
            else:
                print("New hash found -- updating database.\n")
                return bulk_json


    async def _update_db(self, bulk_json):
        if self.no_json_update:
            print("Not clearing JSONs")
            json_cards = [json.load(open(os.path.join(DATA_DIR, JSON_PATH,
                                                      json_card)))
                          for json_card in os.listdir(os.path.join(
                              DATA_DIR, JSON_PATH))]
            self.no_json_update = False
        else:
            json_cards = self._split_up_json_cards(await self._fetch_database(bulk_json))
            self._save_database(json_cards)
        await self._update_rules()
        self._update_hash(bulk_json)
        print("Database fully updated")
    
    
    def _update_hash(self, bulk_json):
            with open(os.path.join(DATA_DIR, LOCAL_HASH), 'w') as newhash:
                newhash.write(bulk_json["updated_at"])
            print("Hash updated")
        
    
    def _clear_hash(self):
        print("Clearing hash")
        with open(self.local_hash, 'w') as update_hash:
            update_hash.write('')
        print("Hash cleared")


    def _clear_images(self):
        print("Clearing images")
        for image_file in os.listdir(os.path.join(DATA_DIR, IMAGE_PATH)):
            os.remove(os.path.join(DATA_DIR, IMAGE_PATH, image_file))
        print("Images cleared")