import os
from src.Singleton import Singleton
from src.RemoteProxies.TGProxy import TGProxy
from src.RemoteProxies.DCProxy import DCProxy
from src.DatabaseObjs.Database import Database
from src.Constants import CARD_INFO_SECTIONS

MINUTE = 60

class ManaBot(Singleton):
    
    def __init__(self, tgbot, dcbot):
        # Initialize the startup object
        # Run startup
        self.proxies = {
                "TG": TGProxy(tgbot), 
                "DC": DCProxy(dcbot)
            }
        self.data_base = Database("json_cards", "data", CARD_INFO_SECTIONS,
                                  "rules.txt")
        # We'll specifically leave this in here because I want it to grab the
        # command's *method*, reducing conditional blocks
        commands = {
            "card": self._get_card, 
            "rule": self._get_rule
            }
    
    async def _startup(self):
        # run the startup command in the startup object
        pass
    
    def _get_card(self, req_content):
        return self.data_base.search_for_card(req_content)
    
    def _get_rule(self, req_content):
        return self.data_base.search_for_rule(req_content)
    
    async def run_command(self, platform, command, req_content):
        if command not in self.commands:
            raise("Error: invalid command. Ignoring.")
        results = self.commands[command](req_content)
        await self.proxies[platform].send_results(command, results)