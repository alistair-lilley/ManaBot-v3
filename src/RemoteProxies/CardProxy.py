import json, filetype, os, re, math, asyncio, aiofiles, aiohttp, time
from PIL import Image
from src.Constants import CARD_SIZE, DATA_DIR, JSON_URL, CARD_ID_TYPE, \
    LOCAL_HASH, JSON_PATH, IMAGE_PATH, NAME, BACKSIDE_URL, CARD_IMAGE_URL, \
    CARD_STR_REPL, IDENTIFIERS, RATE_LIMIT
    
    
class CardProxy:
    
    def __init__(self):
        self.card_count = 0
        self.total_card_count = 0
        self.session = None
            
            
    def _create_backside_json(self):
        print("Creating backside json")
        with open(os.path.join(DATA_DIR, JSON_PATH, "backside.json"), 'w') \
                as backside:
            json.dump({}, backside)
        print("Backside json created\n")
                
                
    async def _fetch_database(self):
        self._create_backside_json()
        print("Fetching database")
        database_json = None
        while not database_json:
            try:
                async with aiohttp.ClientSession(
                    connector=aiohttp.TCPConnector(ssl=False)) as http_session:
                    download_database = await http_session.get(JSON_URL)
                    print("Database fetched\n")
                    print("Downloading full JSON")
                    database_json = await download_database.json()
            except:
                print("JSON dastabase not reached.")
        print("Full JSON downloaded\n")
        return database_json


    def _split_up_json_cards(self, json_file):
        print("Splitting JSON")
        json_cards_split_up = []
        json_card_sets = json_file['data']
        for card_set in json_card_sets:
            card_set_cards = json_card_sets[card_set]['cards']
            for card in card_set_cards:
                json_cards_split_up.append(card)
        print("JSON split up\n")
        return json_cards_split_up


    def _save_database(self, json_files):
        print("Saving database")
        for card in json_files:
            with open(f'{DATA_DIR}/{JSON_PATH}/'
                      f'{self._simplify(card[NAME])}.json', 'w') as json_card_f:
                json.dump(card, json_card_f)
        with open(f'{DATA_DIR}/{JSON_PATH}/'
                  f'backside.json', 'w') as json_card_f:
            json.dump({}, json_card_f)
        print("Database saved\n")


    async def _download_card_images(self, json_cards):
        print("Downloading cards")
        # This strips the file extension from each card file in the database, 
        # getting only the card name
        existing_cards = {cardname.split('.')[0] for cardname in
                             os.listdir(os.path.join(DATA_DIR, IMAGE_PATH))}
        new_cards = [card for card in json_cards
                     if (NAME in card and 
                     self._simplify(card[NAME]) not in existing_cards)] 
        base_card_count = len(existing_cards) + 1
        self.card_count = base_card_count
        self.total_card_count = len(json_cards)
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False)) as session:
            await self._download_backside(session)
            if not new_cards:
                print("No new cards")
                print("")
            for card in new_cards:
                asyncio.create_task(self._download_one_card_image(session,
                                    card[NAME],
                                    card[IDENTIFIERS][CARD_ID_TYPE]))
                # We have to rate limit the requests we send or the remote DB
                # sends back a rate limit error >:( oh well
                await asyncio.sleep(RATE_LIMIT)
            # This is to ensure that the final cards have time to download, cuz
            # if we don't wait a few seconds the session will close before the
            # cards are fully downloaded
            await asyncio.sleep(10)
        print("")
        print("Card download complete")        


    async def _download_backside(self, session):
        card_online = await session.get(BACKSIDE_URL)
        card_data = await card_online.read()
        cardpath = os.path.join(DATA_DIR, IMAGE_PATH, "backside")
        ext = filetype.guess(card_data).extension
        async with aiofiles.open(cardpath + '.' + ext, 'wb') as card_write:
            await card_write.write(card_data)
        self._compress_save_card_image(cardpath, ext, backside=True)
        print("")
        print("Card backside downloaded\n")
        
        
    async def _download_one_card_image(self, session, cardname, cardID):
        card_data = None
        cardurl = re.sub(CARD_STR_REPL, cardID, CARD_IMAGE_URL)
        card_online = await session.get(cardurl)
        card_data = await card_online.read()
        ext = filetype.guess(card_data).extension
        cardpath = os.path.join(DATA_DIR, IMAGE_PATH,
                                self._simplify(cardname))
        async with aiofiles.open(cardpath + '.' + ext, 'wb')\
                as card_write:
            await card_write.write(card_data)
        self._compress_save_card_image(cardpath, ext)


    def _compress_save_card_image(self, cardpath, ext, backside=False):
        with Image.open(cardpath + '.' + ext) as cardfile:
            resized_card = cardfile.resize(CARD_SIZE)
            compressed_card = Image.new("RGB", CARD_SIZE, (255, 255, 255))
            if len(resized_card.split()) > 3:
                compressed_card.paste(
                    resized_card, mask=resized_card.split()[3])
            else:
                compressed_card.paste(resized_card)
            os.remove(cardpath + '.' + ext)
            compressed_card.save(cardpath + ".jpg")
        if not backside:
            self._card_download_meter()


    def _card_download_meter(self):
        totalbars = 100
        percent = self.card_count / self.total_card_count
        num_of_bars = int(percent * totalbars // 1)
        bars = '=' * num_of_bars
        dots = '.' * (totalbars - num_of_bars - 1)
        toprint = f' [{bars}{dots}] {str(self.card_count)}/'\
            f'{str(self.total_card_count)} ({str(round(percent * 100, 1))}%)'
        print(toprint, end="\r")
        self.card_count += 1
        if self.card_count == self.total_card_count:
            self.card_count = 0
            print("")


    def _simplify(self, string):
        return re.sub(r'[\W\s]', '', string).lower()