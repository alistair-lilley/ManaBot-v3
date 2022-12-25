
class TGProxy:
    
    def __init___(self, tgbot):
        pass
    
    def _send_response(self, message, formatted_results):
        pass
    
    def _format_response(self, command, req_results):
        pass
    
    async def send_results(self, command, req_results):
        formatted = self._format_response(command, req_results)
        await self._send_response(formatted)