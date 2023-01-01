import aiohttp, re, urllib, os, asyncio
from src.Singleton import Singleton
from src.RemoteProxies.CardProxy import CardProxy
from src.RemoteProxies.RuleProxy import RuleProxy
from src.Constants import DATA_DIR, JSON_URL, LOCAL_HASH, JSON_PATH, \
    IMAGE_PATH, DAY


class DBProxy(Singleton, CardProxy, RuleProxy):
    '''
        The DataBase Proxy sends requests and receives data from the remote 
        databases that hold MtG card data. It also requests and receives data
        from the Rules database. It updates the local database files.
    '''
    def __init__(self):
        self.http_session = None
        while not self.http_session:
            try:
                self.http_session = aiohttp.ClientSession(
                    connector=aiohttp.TCPConnector(verify_ssl=False))
                print("http session online")
            except: 
                print("http session failed to connect... Reconnecting in",
                        end="")
                countdown = 10
                while countdown:
                    print(countdown, end='\r')
                    print("")
                    countdown -= 1
        self.local_hash = os.path.join(DATA_DIR, LOCAL_HASH)
        self.remote_update_hash = JSON_URL + '.sha256'
        if not os.path.exists(DATA_DIR):
            os.mkdir(DATA_DIR)
        if not os.path.exists(os.path.join(DATA_DIR, JSON_PATH)):
            os.mkdir(os.path.join(DATA_DIR, JSON_PATH))
        if not os.path.exists(os.path.join(DATA_DIR, IMAGE_PATH)):
            os.mkdir(os.path.join(DATA_DIR, IMAGE_PATH))

    async def _should_update(self):
        if not os.path.exists(LOCAL_HASH):
            with open(LOCAL_HASH, 'w') as newhash:
                newhash.write('')
                print("Hash file made")
        while True:
            try:
                online_hash = \
                        await self.http_session.get(self.remote_update_hash)
                break
            except:
                print(f"Remote update hash not reached: "
                      f"{self.remote_update_hash}\nTrying again in 10 seconds")
                await asyncio.sleep(10)
        with open(os.path.join(DATA_DIR, LOCAL_HASH)) as update_hash:
            downloaded_hash = await online_hash.text()
            local_hash = update_hash.read() 
            if local_hash == downloaded_hash:
                print("Hash found -- database up to date.")
                return False    
            else:
                print("New hash found -- updating database.")
                return True

    async def _update_db(self):
        #json_cards = self._split_up_json_cards(await self._fetch_database())
        #self._save_database(json_cards)
        import json
        json_cards = [json.load(open(os.path.join(DATA_DIR, JSON_PATH, card))) for card in os.listdir(os.path.join(DATA_DIR, JSON_PATH))]
        await self._download_card_images(json_cards)
        await self._update_rules()
        await self._update_hash()
        print("Database fully updated")
    
    def clear_hash(self):
        print("Clearing hash")
        with open(self.local_hash, 'w') as update_hash:
            update_hash.write('')
        print("Hash cleared")

    def clear_images(self):
        print("Clearing images")
        for image_file in os.listdir(os.path.join(DATA_DIR, IMAGE_PATH)):
            os.remove(os.path.join(DATA_DIR, IMAGE_PATH, image_file))
        print("Images cleared")

    async def check_update_db(self, database, no_update,
                              clear_hash, clear_images):
        if clear_hash:
            self.clear_hash()
        if clear_images:
            self.clear_images()
        if no_update:
            print("Skipping first update")
            await asyncio.sleep(DAY)
        while True:
            if await self._should_update():
                await self._update_db()
                database.reload()
                print("Database reloaded")
            await asyncio.sleep(DAY)