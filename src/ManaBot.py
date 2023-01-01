import asyncio, sys
from src.Singleton import Singleton
from src.RemoteProxies.TGProxy import TGProxy
from src.RemoteProxies.DCProxy import DCProxy
from src.RemoteProxies.DBProxy import DBProxy
from src.DatabaseObjs.Database import Database
from src.Constants import CARD_INFO_SECTIONS, JSON_URL, CARD_IMAGE_URL, \
    CARD_STR_REPL, CARD_ID_TYPE, RULES_URL, JSON_PATH, RULES_FILE, DATA_DIR
    

class ManaBot(Singleton):
    
    def __init__(self, tgbot, tg_id, dc_id):
        print("Running startup")
        self.database_proxy = DBProxy()
        self.database = Database()
        self.bots = {
            "TG": TGProxy(tgbot, tg_id),
            "DC": DCProxy(dc_id)
        }
        self.commands = {
            "card": self._get_card, 
            "rule": self._get_rule
        }
    
    async def startup(self, dp, client, guild):
        clear_hash = (sys.argv and "clearhash" in sys.argv)
        no_update = (sys.argv and "no_update" in sys.argv)
        clear_images = (sys.argv and "clearimages" in sys.argv)
        asyncio.ensure_future(self.database_proxy\
            .check_update_db(self.database, no_update, clear_hash, clear_images))
        telegram_start_args = [dp]
        dicsord_start_args = [client, guild]
        bot_args = {
            "TG": telegram_start_args,
            "DC": dicsord_start_args
        }
        for bot in self.bots.keys():
            asyncio.ensure_future(self.bots[bot].startup(*bot_args[bot]))
    
    def _get_card(self, req_content):
        try:
            return self.database.search_for_card(req_content)
        except:
            print("Card search failed; database not loaded?")
            return None
    
    def _get_rule(self, req_content):
        try:
            return self.database.search_for_rule(req_content)
        except:
            print("Rule search failed; database not loaded?")
            return None
    
    async def run_command(self, query, content, platform):
        try:
            command, req_query = content.lower().split(' ', 1)
        except:
            raise("Command not complete")
        #try:
        results = self.commands[command](req_query)
        #except:
        #    print("Bad command")
        #    results = None
        await self.bots[platform].send_results(query, results)
        