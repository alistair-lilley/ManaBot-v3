import discord
from datetime import datetime
from src.RemoteProxies.BaseProxy import BaseProxy


class DCProxy(BaseProxy):
    
    def __init__(self, my_id):
        self.me = my_id
    
    
    async def startup(self, client, guild):
        for guild in client.guilds:
            if guild.name == guild:
                break
        print(
            f'{client.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )
        dt = datetime.now().strftime("%d-%m-%Y %H:%M")
        user = await client.fetch_user(self.me)
        await user.send(f'{client.user} is connected to the following guild:'\
            f'\n{guild.name}(id: {guild.id})\n{dt})')

    
    async def _send_response(self, query, formatted_results):
        if "image_path" in formatted_results:
            await query.channel.send(file=formatted_results["image_path"])
        if "text" in formatted_results:
            for chunk in formatted_results["text"]:
                await query.channel.send(chunk)
    
    
    async def _format_response(self, query_, req_results):
        formatted_results = {}
        if "image_path" in req_results:
            formatted_results["image_path"] =\
                discord.File(req_results["image_path"])
        if "text" in req_results:
            formatted_results["text"] = self._chunkify_text(req_results["text"])
        return formatted_results
