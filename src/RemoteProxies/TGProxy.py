import asyncio, hashlib
from datetime import datetime
from aiogram.types import  InputTextMessageContent, InlineQueryResultArticle, \
    InputFile, InlineQueryResultCachedPhoto
from src.RemoteProxies.BaseProxy import BaseProxy


class TGProxy(BaseProxy):
    
    def __init__(self, tgbot, my_id):
        self.bot = tgbot
        self.me = my_id
    
    async def startup(self, dp):
        dt = datetime.now().strftime("%d-%m-%Y %H:%M")
        upmsg = f"Bot has started: {dt}"
        await self.bot.send_message(self.me, upmsg)
        await dp.skip_updates()
        asyncio.ensure_future(dp.start_polling())
    
    async def _send_response(self, query, formatted_results):
        await self.bot.answer_inline_query(query.id, results=formatted_results,
                                     cache_time=1)
    
    async def _upload_image_get_id(self, image_bytes):
        image_file = InputFile(image_bytes)
        pic = await self.bot.send_photo(self.me, image_file)
        await self.bot.delete_message(self.me, pic.message_id)
        photoid = pic.photo[0].file_id
        return photoid
    
    async def _format_response(self, query, req_results):
        article_hash = hashlib.md5(query.id.encode()).hexdigest()
        articles = []
        if "image_bytes" in req_results:
            photoid = await self._upload_image_get_id(req_results["image_bytes"])
            photo_article = InlineQueryResultCachedPhoto(id=article_hash+"1",
                                                   photo_file_id=photoid)
            articles.append(photo_article)
        if "text" in req_results:
            text_content = InputTextMessageContent(''.join(req_results["text"]))
            text_article = InlineQueryResultArticle(
                id=article_hash,
                title=f'Information for {query.query!r}',
                input_message_content=text_content,
            )
            articles.append(text_article)
        return articles