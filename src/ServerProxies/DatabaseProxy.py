import aiohttp, re, json, filetype, urllib, os, asyncio
from PIL import Image
from src.Singleton import Singleton

NAME = 'name'
IMAGE_PATH = 'cardimages'
JSON_PATH = 'json_cards'
JSON_URL = "https://mtgjson.com/api/v5/AllPrintings.json"
CARD_IMAGE_URL = "https://gatherer.wizards.com/" \
                "Handlers/Image.ashx?name=[CARD]type=card"
RULES_URL = "https://media.wizards.com/" \
                "[YR]/downloads/MagicCompRules%20[YR][MO][DAY].txt"
DAY = 60*60*24

class DBProxy(Singleton):
    '''
        The DataBase Proxy sends requests and receives data from the remote 
        databases that hold MtG card data. It also requests and receives data
        from the Rules database. It updates the local database files.
    '''
    def __init__(self, json_url, database_dir, local_update_hash, 
                cards_url, url_repl_str, database_id_type, rules_url):
        while True:
            print("Connecting to http session")
            try:
                self.http_session = aiohttp.ClientSession()
                print("http session online")
                break
            except: 
                print("`http session failed to connect... Reconnecting in",
                      end="")
                countdown = 10
                while countdown:
                    print(countdown, end='\r')
                    print("")
                    countdown -= 1
        self.json_url = json_url
        self.database_dir = database_dir
        self.local_update_hash = local_update_hash
        self.remote_update_hash = self.json_url + '.sha256'
        self.cards_url = cards_url
        self.url_repl_str = url_repl_str
        self.database_ID_type = database_id_type
        self.rules_url = rules_url

    async def _should_update(self):
        try:
            with open(self.local_update_hash) as update_hash:
                online_hash = \
                            await self.http_session.get(self.remote_update_hash)
                if update_hash.read() == await online_hash.text():
                    print("Hash found -- database up to date.")
                    return False
                else:
                    print("New hash found -- updating database.")
                    return True
        except:
            print(f"Remote update hash not reached: {self.remote_update_hash}")
            return False

    async def _update_hash(self):
        with open(self.local_update_hash, 'w') as update_hash:
            online_hash = await self.http_session.get(self.remote_update_hash)
            update_hash.write(await online_hash.text())

    async def _fetch_database(self, database_url):
        try:
            download_database = await self.http_session.get(database_url)
            return await download_database.json()
        except:
            print("JSON dastabase not reached.")

    def _split_up_json_cards(self, json_file):
        json_cards_split_up = []
        json_card_sets = json_file['data']
        for cardSet in json_card_sets:
            card_set_cards = json_card_sets[cardSet]['cards']
            for card in card_set_cards:
                json_cards_split_up.append(card)
        return json_cards_split_up

    def _save_database(self, database_dir, json_files):
        # Sanity check: make sure there's a database directory
        if not os.listdir(database_dir):
            os.mkdir(database_dir)
        for card in json_files:
            with open(f'{database_dir}/{JSON_PATH}/'
                      f'{self._simplify(card[NAME])}.json', 'w') as json_card_f:
                json.dump(card, json_card_f)

    def _compress_card_image(self, cardpath, ext):
        with Image.open(cardpath + "." + ext) as cardfile:
            compressed_card = cardfile.resize((360,500))
            compressed_card.save(cardpath + ".jpg")

    async def _download_one_card_image(self, cardname, cardID):
        try:
            wizardsurl = self._make_remote_image_url(cardID)
            card_online = await self.http_session.get(wizardsurl)
            card_data = await card_online.read()
            cardpath = self.database_dir + "/" + IMAGE_PATH + "/"  \
                       + self._simplify(cardname)
            ext = filetype.guess(card_data).extension
            with open(cardpath + '.' + ext, 'wb') as card_write:
                card_write.write(card_data)
            self._compress_card_image(cardpath, ext)
        except:
            print("Failed to download card -- wizards down?")

    async def _download_card_images(self, json_cards):
        print("Downloading cards: ")
        # This strips the file extension from each card file in the database, 
        # getting only the card name
        existing_cards = set([cardname[:cardname.index('.')] for cardname in
                             os.listdir(self.database_dir + '/' + IMAGE_PATH)])
        print(self.database_dir+'/'+IMAGE_PATH)
        cardcount = 0
        numcards = len(json_cards)
        for card in json_cards:
            cardcount += 1
            self._card_download_meter(cardcount, numcards)
            if self._simplify(card[NAME]) in existing_cards:
                continue
            await self._download_one_card_image(card[NAME], 
                            card['identifiers'][self.database_ID_type])
        print("Complete")

    def _card_download_meter(self, cardcount, jsoncardlen):
        totalbars = 100
        percent = cardcount / jsoncardlen
        num_of_bars = int(percent * totalbars // 1)
        toprint = ' [' + '=' * num_of_bars + '.' * (totalbars - num_of_bars) \
                  + '] ' + str(cardcount) + '/' + str(jsoncardlen) \
                  + ' (' + str(round(percent * 100, 1)) + '%)'
        print(toprint, end="\r")


    async def _update_rules(self, rules_url):
        rules_online = await self.http_session.get(rules_url)
        rules_text = await rules_online.text()
        with open(self.database_dir + "/rules", 'w') as rulesfile:
            rulesfile.write(rules_text)

    async def _update_db(self):
        print("Downloading database...")
        json_cards = self._split_up_json_cards(await 
                                           self._fetch_database(self.json_url))
        print("Database downloaded")
        print("Saving database...")
        self._save_database(self.database_dir, json_cards)
        print("Database saved")
        print("Downloading card images...")
        await self._download_card_images(json_cards)
        print("Card images downloaded")
        await self._update_hash()
        await self._update_rules(self.rules_url)

    async def loop_check_and_update(self):
        while True:
            if await self._should_update():
                await self._update_db()
            await asyncio.sleep(DAY)

    def _simplify(self, string):
        return re.sub(r'[\W\s]', '', string).lower()

    def _make_remote_image_url(self, cardname):
        return re.sub(self.url_repl_str, urllib.parse.quote(cardname), 
                      self.cards_url)