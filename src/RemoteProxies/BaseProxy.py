from abc import ABCMeta, abstractmethod
from src.Constants import MSGMAX


class BaseProxy(metaclass=ABCMeta):
    
    def __init__(self):
        pass
    
    @abstractmethod
    async def _send_response(self, query, formatted_results):
        pass
    
    @abstractmethod
    async def _format_response(self, query, req_results):
        pass

    # Chunkify cuz discord cant handle text blocks more than 2000 characters
    def _chunkify_text(self, text):
        chunkified = [text[i:i+MSGMAX] 
                      for i in range(0, len(text), MSGMAX)]
        return chunkified
    
    async def _extract_data(self, req_results):
        # if None:
        #   return _failed_to_send value
        # if card:
        #   get card image_ID
        #   get card data
        #   return [text, image_ID]
        # if rule:
        #   get rule text
        #   return [text]
        pass
    
    async def _failed_to_send(self):
        # send a "database not loaded -- 
        # please wait and try again in a few minutes" thingy
        pass
    
    async def send_results(self, command, query, req_results, database):
        # _extract_data
        # _format_response
        # _send_response
        pass