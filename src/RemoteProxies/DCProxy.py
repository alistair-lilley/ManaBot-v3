import asyncio
from src.Constants import MEDC
from src.RemoteProxies.BaseProxy import BaseProxy


class DCProxy(BaseProxy):
    
    def __init___(self, dctoken, client):
        pass
    
    async def startup(self):
        pass
    
    async def _send_response(self, query, formatted_results):
        # if req_results has photo
        #   send photo
        # if req_results has text
        #   chunkify text
        #   send text
        pass
    
    async def _format_response(self, query, req_results):
        return req_results