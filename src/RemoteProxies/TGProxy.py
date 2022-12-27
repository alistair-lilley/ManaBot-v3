import asyncio, hashlib, random
from datetime import datetime
from aiogram import Bot, Dispatcher, executor
from aiogram.types import InlineQuery, InputTextMessageContent, \
    InlineQueryResultArticle, InputFile, InlineQueryResultCachedPhoto
from src.Constants import METG
from src.RemoteProxies.BaseProxy import BaseProxy


class TGProxy(BaseProxy):
    
    def __init___(self):
        pass
    
    async def startup(self):
        pass
    
    async def _send_response(self, query, formatted_results):
        self.bot.answer_inline_query(query.id, results=formatted_results,
                                     cache_time=1)
    
    async def _upload_image_get_id(self, image_bytes):
        image_file = InputFile(image_bytes)
        pic = await self.bot.send_photo(self.metg, image_file)
        await self.bot.delete_message(self.metg, pic.message_id)
        photoid = pic.photo[0].file_id
        return photoid
    
    def _format_response(self, query, req_results):
        article_hash = hashlib.md5(query.id.encode()).hexdigest()
        articles = []
        if "image" in req_results:
            photoid = self._upload_image_get_id(req_results["image"])
            photo_article = InlineQueryResultCachedPhoto(id=article_hash+"1",
                                                   photo_file_id=photoid)
            articles.append(photo_article)
        if "text" in req_results:
            text_content = InputTextMessageContent(''.join(req_results["text"]))
            text_article = InlineQueryResultArticle(
                id=article_hash,
                title=f'Information for {query!r}',
                input_message_content=text_content,
            )
            articles.append(text_article)
        return articles