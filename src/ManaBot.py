from src.Singleton import Singleton
from src.RemoteProxies.TGProxy import TGProxy
from src.RemoteProxies.DCProxy import DCProxy
from src.DatabaseObjs.Database import Database
from src.Constants import CARD_INFO_SECTIONS

IMAGE_PATH = 'cardimages'
JSON_PATH = 'json_cards'
RULES_FILE = 'rules.txt'
DATA_DIR = 'data'
MINUTE = 60

class ManaBot(Singleton):
    
    def __init__(self, tgtoken):
        super(Singleton, self).__init__()
        # startup
        self.database = None
        self.bots = {
            "TG": TGProxy(tgtoken),
            "DC": DCProxy()
        }
        self.commands = {
            "card": self._get_card, 
            "rule": self._get_rule
        }
    
    async def startup(self):
        # run startup object returning a loaded database
        # Loop until database object is not `None`
        # run dcproxy startup calling tgproxy startup
        pass
    
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
    
    async def run_command(self, query, platform):
        command, req_query = query.split(' ', 1)
        results = self.commands[command](req_query)
        await self.bots[platform].send_results(query, results)
        