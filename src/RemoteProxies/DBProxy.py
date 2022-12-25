import aiohttp, re, json, filetype, urllib, os, asyncio, datetime
from PIL import Image
from src.Constants import CARD_SIZE
from src.Singleton import Singleton

NAME = 'name'
IMAGE_PATH = 'cardimages'
JSON_PATH = 'json_cards'
DAY = 60*60*24

class DBProxy(Singleton):
    '''
        The DataBase Proxy sends requests and receives data from the remote 
        databases that hold MtG card data. It also requests and receives data
        from the Rules database. It updates the local database files.
    '''
    def __init__(self, json_url, database_dir, local_hash, 
                cards_url, url_repl_str, database_id_type, rules_url,
                clear_hash=False):
        connected = False
        while not connected:
            print("Connecting to http session")
            try:
                self.http_session = aiohttp.ClientSession(
                    connector=aiohttp.TCPConnector(verify_ssl=False))
                print("http session online")
                connected = True
            except: 
                print("http session failed to connect... Reconnecting in",
                      end="")
                countdown = 10
                while countdown:
                    print(countdown, end='\r')
                    print("")
                    countdown -= 1
        self.json_url = json_url
        self.database_dir = database_dir
        self.local_hash = os.path.join(self.database_dir, local_hash)
        self.remote_update_hash = self.json_url + '.sha256'
        self.cards_url = cards_url
        self.url_repl_str = url_repl_str
        self.database_ID_type = database_id_type
        self.rules_url = rules_url
        self.clear_hash = clear_hash
        if not os.path.exists(self.database_dir):
            os.mkdir(self.database_dir)
        if not os.path.exists(os.path.join(self.database_dir, JSON_PATH)):
            os.mkdir(os.path.join(self.database_dir, JSON_PATH))
        if not os.path.exists(os.path.join(self.database_dir, IMAGE_PATH)):
            os.mkdir(os.path.join(self.database_dir, IMAGE_PATH))

    async def _should_update(self):
        if not os.path.exists(self.local_hash):
            with open(self.local_hash, 'w') as newhash:
                newhash.write('')
                print("Hash file made")
        try:
            with open(self.local_hash) as update_hash:
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
        with open(self.local_hash, 'w') as update_hash:
            online_hash = await self.http_session.get(self.remote_update_hash)
            update_hash.write(await online_hash.text())
        
    async def _fetch_database(self):
        try:
            download_database = await self.http_session.get(self.json_url)
            return await download_database.json()
        except:
            print("JSON dastabase not reached.")

    def _split_up_json_cards(self, json_file):
        json_cards_split_up = []
        json_card_sets = json_file['data']
        for card_set in json_card_sets:
            card_set_cards = json_card_sets[card_set]['cards']
            for card in card_set_cards:
                json_cards_split_up.append(card)
        return json_cards_split_up

    def _save_database(self, json_files):
        # Sanity check: make sure there's a database directory
        for card in json_files:
            with open(f'{self.database_dir}/{JSON_PATH}/'
                      f'{self._simplify(card[NAME])}.json', 'w') as json_card_f:
                json.dump(card, json_card_f)

    def _compress_save_card_image(self, cardpath, ext):
        with Image.open(cardpath + '.' + ext) as cardfile:
            resized_card = cardfile.resize(CARD_SIZE)
            compressed_card = Image.new("RGB", CARD_SIZE, (255, 255, 255))
            if ext == "PNG":
                compressed_card.paste(
                    resized_card, mask=resized_card.split()[3])
            else:
                compressed_card.paste(resized_card)
            compressed_card.save(cardpath + ".jpg")
            os.remove(cardpath + '.' + ext)

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
            self._compress_save_card_image(cardpath, ext)
        except:
            print("Failed to download card -- wizards down?", end='\r')

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
                            card[self.database_ID_type])
        print("Complete")

    def _card_download_meter(self, cardcount, jsoncardlen):
        totalbars = 100
        percent = cardcount / jsoncardlen
        num_of_bars = int(percent * totalbars // 1)
        toprint = ' [' + '=' * num_of_bars + '.' * (totalbars - num_of_bars) \
                  + '] ' + str(cardcount) + '/' + str(jsoncardlen) \
                  + ' (' + str(round(percent * 100, 1)) + '%)'
        print(toprint, end="\r")

    def _decrement_date(self, year, month, day):
        day -= 1
        if day == 0:
            day = 31
            month -= 1
        if month == 0:
            month = 12
            year -= 1
        return year, month, day

    def _complete_url(self, rules_url, year, month, day):
        rules_url = re.sub('%YR%', str(year), rules_url)
        rules_url = re.sub('%MO%', str(month), rules_url)
        rules_url = re.sub('%DAY%', str(day), rules_url)
        return rules_url

    async def _find_rules_url(self):
        year, month, day = [int(piece) for piece in 
                            datetime.datetime.now()\
                                .strftime("%Y %m %d").split()]
        url_completed = self._complete_url(self.rules_url, year, month, day)
        # Basically we work backwards to find the latest update
        while True:
            rulestext = await \
                (await self.http_session.get(url_completed)).text()
            if rulestext != "Not found\n":
                return url_completed
            year, month, day = self._decrement_date(year, month, day)
            url_completed = self._complete_url(self.rules_url, year, month,
                                                day)
            if (year, month, day) == (1993, 1, 1):
                year, month, day = [int(piece) for piece in datetime.datetime\
                    .now().strftime("%Y %m %d").split()]

    async def _update_rules(self):
        current_rules_url = await self._find_rules_url()
        rules_online = await self.http_session.get(current_rules_url)
        rules_text = await rules_online.text()
        with open(os.path.join(self.database_dir, "rules.txt"), 'w') as rulesfile:
            rulesfile.write(rules_text)

    async def _update_db(self):
        print("Downloading database...")
        json_cards = self._split_up_json_cards(await self._fetch_database())
        print("Database downloaded")
        print("Saving database...")
        self._save_database(self.database_dir, json_cards)
        print("Database saved")
        print("Downloading card images...")
        await self._download_card_images(json_cards)
        print("Card images downloaded")
        await self._update_hash()
        await self._update_rules(self.rules_url)

    def _simplify(self, string):
        return re.sub(r'[\W\s]', '', string).lower()

    def _make_remote_image_url(self, cardname):
        return re.sub(self.url_repl_str, urllib.parse.quote(cardname), 
                      self.cards_url)
    
    def clear_hash(self):
        with open(self.local_hash, 'w') as update_hash:
            update_hash.write('')

    async def check_update_db(self):
        if await self._should_update():
            await self._update_db()
    
    @property
    def clear_hash(self):
        return self.clear_hash