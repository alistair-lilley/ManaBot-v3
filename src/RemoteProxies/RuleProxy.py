import re, datetime, os, aiohttp
from src.Constants import  DATA_DIR, RULES_URL, RULES_FILE

class RuleProxy:
    
    def __init__(self):
        pass

    async def _update_rules(self):
        print("Updating rules")
        rules_text = None
        current_rules_url = await self._find_rules_url()
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False)) as http_session:
            rules_online = await http_session.get(current_rules_url)
            rules_text = await rules_online.text()
        with open(os.path.join(DATA_DIR, RULES_FILE),
                  'w') as rulesfile:
            rulesfile.write(rules_text)
        print("Rules updated\n")


    async def _find_rules_url(self):
        year, month, day = [int(piece) for piece in 
                            datetime.datetime.now()\
                                .strftime("%Y %m %d").split()]
        url_completed = self._complete_url(RULES_URL, year, month, day)
        # Basically we work backwards to find the latest update
        while True:
            async with aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(ssl=False)) as http_session:
                rulestext = await (await http_session.get(url_completed)).text()
            if rulestext != "Not found\n":
                return url_completed
            year, month, day = self._decrement_date(year, month, day)
            url_completed = self._complete_url(RULES_URL, year, month,
                                                day)
            if (year, month, day) == (1993, 1, 1):
                raise("Checked all dates, rules look up failed...")


    def _complete_url(self, rules_url, year, month, day):
        rules_url = re.sub('%YR%', str(year), rules_url)
        rules_url = re.sub('%MO%', str(month), rules_url)
        rules_url = re.sub('%DAY%', str(day), rules_url)
        return rules_url
    
    
    def _decrement_date(self, year, month, day):
        day -= 1
        if day == 0:
            day = 31
            month -= 1
        if month == 0:
            month = 12
            year -= 1
        return year, month, day


    def _simplify(self, string):
        return re.sub(r'[\W\s]', '', re.sub(r' ', '_', string)).lower()