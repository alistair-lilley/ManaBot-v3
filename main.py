import discord
from aiogram import Bot, Dispatcher, executor
from aiogram.types import InlineQuery
from dotenvn import load_dotenv, dotenv_values

from src.ManaBot import ManaBot

load_dotenv()

config = dotenv_values(".env")

tgtoken = config["TG_TOKEN"]
dctoken = config["DC_TOKEN"]
client = discord.Client()

bot = ManaBot(tgtoken, dctoken)
    
@client.event
async def on_ready():
    pass
    
@client.event
async def on_dc_message(message):
    pass

@dp.inline_handler()
async def on_tg_message(inline_query: InlineQuery):
    pass


if __name__ == "__main__":
    pass