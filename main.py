import discord
from aiogram import Bot, Dispatcher, executor
from aiogram.types import InlineQuery

from src.ManaBot import ManaBot

tgbot = Bot(token='BOT_TOKEN_HERE')
dp = Dispatcher(tgbot)
client = discord.Client()


bot = ManaBot()

@dp.inline_handler()
async def on_tg_message(inline_query: InlineQuery):
    await bot.run_command(*(inline_query.split(' ', 1)))
    
    
@client.event
async def on_dc_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('!'):
        await bot.run_command(*(message[1:].split(' ', 1)))


if __name__ == "__main__":
    pass