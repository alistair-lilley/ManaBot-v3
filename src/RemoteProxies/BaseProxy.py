from abc import ABCMeta, abstractmethod
from src.DatabaseObjs.Card import Card
from src.DatabaseObjs.Rules import Rule
from src.Constants import MSGMAX, DATABASE_NOT_LOADED


class BaseProxy(metaclass=ABCMeta):
    
    def __init__(self, bot_token):
        self.token = bot_token
    
    @abstractmethod
    async def startup(self):
        pass
    
    @abstractmethod
    async def _send_response(self, query, formatted_results):
        pass
    
    @abstractmethod
    async def _format_response(self, req_results):
        pass
    
    async def _extract_card(self, req_results):
        text = req_results.info_pretty
        image_bytes = req_results.iamge_bytes
        return {"text": text, "image": image_bytes}

    async def _extract_rule(self, req_results):
        return {"text": req_results.text}

    # Chunkify for DC cuz it cant handle text blocks more than 2000 characters
    def _chunkify_text(self, text):
        chunkified = [text[i:i+MSGMAX] 
                      for i in range(0, len(text), MSGMAX)]
        return chunkified
    
    async def _extract_data(self, req_results):
        if not req_results:
            return DATABASE_NOT_LOADED
        if isinstance(req_results, Card):
            return self._extract_card(req_results)
        elif isinstance(req_results, Rule):
            return self._extract_rule(req_results)
        else:
            raise("Error: unknown object type found in _extract_data")
    
    async def send_results(self, query, req_results):
        result_data = await self._extract_data(req_results)
        formatted_response = self._format_response(query, result_data)
        await self._send_response(query, formatted_response)