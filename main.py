import discord, asyncio, hashlib
from aiogram import Bot, Dispatcher, executor
from aiogram.types import InlineQuery, Message
from dotenv import load_dotenv, dotenv_values

from src.ManaBot import ManaBot

load_dotenv()

config = dotenv_values(".env")

intents = discord.Intents().all()

tgtoken = config["TG_TOKEN"]
dctoken = config["DC_TOKEN"]
metg = config["ALI_TG"]
medc = config["ALI_DC"]
guild = config["GUILD"]
client = discord.Client(intents=intents)
tgbot = Bot(token=tgtoken)
dp = Dispatcher(tgbot)

bot = ManaBot(tgbot, metg, medc)

@client.event
async def on_ready():
    await dp.skip_updates()
    asyncio.create_task(bot.startup(dp, client, guild))
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return 
    
    if message.content[0] == '!':
        await bot.run_command(message, message.content[1:], "DC")


@dp.inline_handler()
async def on_inline(message: InlineQuery):
    await bot.run_command(message, message.query, "TG")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(client.run(dctoken))
    loop.run_forever()