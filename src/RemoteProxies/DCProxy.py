
class DCProxy:
    
    def __init___(self, dcbot):
        pass
    
    def _send_response(self, formatted_results):
        pass
    
    def _format_response(self, command, req_results):
        pass
    
    async def send_results(self, command, req_results):
        formatted = self._format_response(command, req_results)
        await self._send_response(formatted)