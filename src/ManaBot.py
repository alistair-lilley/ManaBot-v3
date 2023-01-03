import asyncio, sys
from src.Singleton import Singleton
from src.RemoteProxies.TGProxy import TGProxy
from src.RemoteProxies.DCProxy import DCProxy
from src.RemoteProxies.DBProxy import DBProxy
from src.DatabaseObjs.Database import Database
    

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
        clear_hash = "clear_hash" in sys.argv
        no_update = "no_update" in sys.argv
        clear_images = "clear_images" in sys.argv
        no_json_update = "no_json_update" in sys.argv
        asyncio.create_task(self.database_proxy.check_update_db(self.database,
                                                no_update,
                                                clear_hash, clear_images,
                                                no_json_update))
        telegram_start_args = [dp]
        dicsord_start_args = [client, guild]
        bot_args = {
            "TG": telegram_start_args,
            "DC": dicsord_start_args
        }
        for bot in self.bots.keys():
            asyncio.create_task(self.bots[bot].startup(*bot_args[bot]))
    
    
    def _get_card(self, req_content):
        return self.database.search_for_card(req_content)
    
    
    def _get_rule(self, req_content):
        return self.database.search_for_rule(req_content)
    
    
    async def run_command(self, query, content, platform):
        if ' ' in content.lower():
            command, req_query = content.lower().split(' ', 1)
        results = self.commands[command](req_query)
        await self.bots[platform].send_results(query, results)  
    