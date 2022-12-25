from src.Singleton import Singleton
from src.RemoteProxies.TGProxy import TGProxy
from src.RemoteProxies.DCProxy import DCProxy


class ServerProxy(Singleton):
    
    def __init__(self):
        # Initialize TG proxy and DB proxy
        # initialize the formatter
        # Initialize the startup object
        # Run startup
        # initalize what commands there are (external json?)
        pass
    
    async def _startup(self):
        # run the startup command in the startup object
        pass
    
    def _select_command(self, platform, req_type):
        # Take command and select return function by what the command is and
        # what platform it's coming from (TG/DC)
        # return the function?
        # return a key to the function?
        pass
    
    async def run_command(self, platform, req_type, req_content):
        # select request type
        # run request through function
        # format with the return formatter
        # send the result through the TG and DC proxies
        pass