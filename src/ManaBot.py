import os
from src.Singleton import Singleton
from src.RemoteProxies.TGProxy import TGProxy
from src.RemoteProxies.DCProxy import DCProxy
from src.DatabaseObjs.Database import Database
from src.Constants import CARD_INFO_SECTIONS

MINUTE = 60

class ManaBot(Singleton, TGProxy, DCProxy):
    
    def __init__(self, tgbot, dcbot):
        # create tgproxy, dcproxy, database (none), and startup objects
        pass
    
    async def startup(self):
        # run startup object returning a loaded database
        # Loop until database object is not `None` (block execution)
        # run dcproxy startup calling tgproxy startup
        pass
    
    def _get_card(self, req_content):
        # search database for card
        # set card to None if database is not loaded
        # return card
        pass
    
    def _get_rule(self, req_content):
        # search database for rule
        # set rule to None if database is not loaded
        # return rule
        pass
    
    async def run_command(self, query, command, req_content, platform):
        pass