import discord, asyncio
from aiogram import Bot, Dispatcher, executor
from aiogram.types import InlineQuery
from dotenv import load_dotenv, dotenv_values

from src.ManaBot import ManaBot

load_dotenv()

config = dotenv_values(".env")

tgtoken = config["TG_TOKEN"]
dctoken = config["DC_TOKEN"]
client = discord.Client()

bot = ManaBot(tgtoken)
    
@client.event
async def on_ready():
    asyncio.create_task(bot.startup())
    
@client.event
async def on_dc_message(message):
    if message[0] == '!':
        bot.run_command(message[1:], "DC")

@dp.inline_handler()
async def on_tg_message(inline_query: InlineQuery):
    bot.run_command(inline_query, "TG")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(client.run(dctoken))
    loop.run_forever()