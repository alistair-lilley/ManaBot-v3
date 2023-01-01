import json, filetype, os, re, urllib, asyncio, aiofiles, time
from PIL import Image
from src.Constants import CARD_SIZE, DATA_DIR, JSON_URL, CARD_ID_TYPE, \
    LOCAL_HASH, JSON_PATH, IMAGE_PATH, NAME, BACKSIDE_URL, CARD_IMAGE_URL, \
    CARD_STR_REPL
    
    
class CardProxy:
    
    def __init__(self):
        self.card_count = 0
        self.total_card_count = 0
        
    async def _update_hash(self):
        with open(os.path.join(DATA_DIR, LOCAL_HASH), 'w') as update_hash:
            online_hash = await self.http_session.get(self.remote_update_hash)
            update_hash.write(await online_hash.text())
        
    async def _fetch_database(self):
        print("Fetching database")
        try:
            download_database = await self.http_session.get(JSON_URL)
            return await download_database.json()
        except:
            print("JSON dastabase not reached.")
        print("Database fetcehd")

    def _split_up_json_cards(self, json_file):
        json_cards_split_up = []
        json_card_sets = json_file['data']
        for card_set in json_card_sets:
            card_set_cards = json_card_sets[card_set]['cards']
            for card in card_set_cards:
                json_cards_split_up.append(card)
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
        print("Database saved")

    def _compress_save_card_image(self, cardpath, ext):
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

    async def _download_backside(self):
        try:
            card_online = await self.http_session.get(BACKSIDE_URL)
            card_data = await card_online.read()
            cardpath = os.path.join(DATA_DIR, IMAGE_PATH, "backside")
            ext = filetype.guess(card_data).extension
            async with aiofiles.open(cardpath + '.' + ext, 'wb') as card_write:
                await card_write.write(card_data)
            self._compress_save_card_image(cardpath, ext)
        except:
            print("Failed to download card -- remote server down?", end='\r')
        print("backside downloaded")
        self._card_download_meter()

    def _make_remote_image_url(self, cardname):
        return re.sub(CARD_STR_REPL, urllib.parse.quote(cardname), 
                      CARD_IMAGE_URL)

    async def _download_one_card_image(self, cardname, cardID):
        #try:
        wizardsurl = self._make_remote_image_url(cardID)
        card_online = await self.http_session.get(wizardsurl)
        card_data = await card_online.read()
        cardpath = os.path.join(DATA_DIR, IMAGE_PATH,
                                self._simplify(cardname))
        ext = filetype.guess(card_data).extension
        async with aiofiles.open(cardpath + '.' + ext, 'wb') as card_write:
            await card_write.write(card_data)
        self._compress_save_card_image(cardpath, ext)
        #except:
        #    print(f"Failed to download card {cardname} -- card base down?")
        self._card_download_meter()

    async def _download_card_images(self, json_cards):
        print("Downloading cards")
        # This strips the file extension from each card file in the database, 
        # getting only the card name
        existing_cards = {cardname.split('.')[0] for cardname in
                             os.listdir(os.path.join(DATA_DIR, IMAGE_PATH))}
        new_cards = [card for card in json_cards
                     if (NAME in card and 
                     self._simplify(card[NAME]) not in existing_cards)] 
        base_card_count = len(existing_cards)
        self.card_count = base_card_count
        self.total_card_count = len(json_cards)
        await self._download_backside()
        if not new_cards:
            print("No new cards")
            print("")
        for card in new_cards:
            if self._simplify(card[NAME]) in existing_cards:
                print("found in existing cards")
            else:
                asyncio.create_task(self._download_one_card_image(card[NAME],
                                                            card[CARD_ID_TYPE]))
        # This is to block it from moving onto actually generating the database
        # before all the images have been loaded
        while (len(os.listdir(os.path.join(DATA_DIR, JSON_PATH))) 
                != len(os.listdir(os.path.join(DATA_DIR, IMAGE_PATH)))):
            #print(len(os.listdir(os.path.join(DATA_DIR, IMAGE_PATH))), len(os.listdir(os.path.join(DATA_DIR, JSON_PATH))))
            await asyncio.sleep(1)
        print("")
        print("Card download complete")

    def _card_download_meter(self):
        totalbars = 100
        percent = self.card_count / self.total_card_count
        num_of_bars = int(percent * totalbars // 1)
        bars = '=' * num_of_bars
        dots = '.' * (totalbars - num_of_bars - 1)
        toprint = f' [{bars}{dots}] {str(self.card_count)}/'\
            f'{str(self.total_card_count)} {str(round(percent * 100, 1))}%)'
        print(toprint, end="\r")
        self.card_count += 1
        if self.card_count == self.total_card_count:
            self.card_count = 0

    def _simplify(self, string):
        return re.sub(r'[\W\s]', '', string).lower()