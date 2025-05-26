import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv
load_dotenv()

client = commands.Bot(command_prefix=".", 
                      activity=discord.Activity(type=discord.ActivityType.watching, name="for .help"),
                      intents=discord.Intents.all())

client.remove_command('help')

TOKEN = os.environ.get('TOKEN')
async def start():
  await client.load_extension('utilities') 
  await client.load_extension('events') 
  await client.start(TOKEN) 

if __name__ == "__main__":
  asyncio.run(start())
