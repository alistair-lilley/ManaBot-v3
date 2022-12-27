import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher, executor
from aiogram.types import InlineQuery, InputTextMessageContent, \
    InlineQueryResultArticle
from src.Constants import METG
from src.RemoteProxies.BaseProxy import BaseProxy


class TGProxy(BaseProxy):
    
    def __init___(self, tgtoken):
        pass
    
    async def startup(self, tgstart):
        pass
    
    async def _send_response(self, query, formatted_results):
        # Answer inline query (aiogram func)
        pass
    
    def _format_response(self, query, req_results):
        # keep track of an article
        # if content has text:
        #   put text into `InlineQueryResultArticle`
        #   insert into article
        # if content has image:
        #   format image into `InlineQueryResultCachedPhoto`
        #   insert into article
        # return article
        pass
    
    async def _upload_image_get_id(self, req_results):
        # Retrive image bytesio from card obj (req_result)
        # Create InputFile aiogram object
        # Upload file to me
        # Retrieve image ID (within TG)
        # Delete image
        # Return image ID
        pass