import asyncio, discord
from src.Constants import MEDC
from src.RemoteProxies.BaseProxy import BaseProxy


class DCProxy(BaseProxy):
    
    def __init___(self):
        pass
    
    async def startup(self):
        pass
    
    async def _send_response(self, query, formatted_results):
        if "image" in formatted_results:
            await query.channel.send(file=formatted_results["image"])
        if "text" in formatted_results:
            for chunk in formatted_results["text"]:
                await query.channel.send(chunk)
    
    async def _format_response(self, query_, req_results):
        formatted_results = {}
        if "image" in req_results:
            formatted_results["image"] = discord.File(req_results["image"])
        if "text" in req_results:
            formatted_results["text"] = self._chunkify_text(req_results["text"])
        return formatted_results
