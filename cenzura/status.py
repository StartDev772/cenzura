import discord
from discord.ext import commands, tasks
import datetime
import random
import asyncio

class Status(commands.Cog):
    def __init__(self, client):
        self.bot = client
        self.zn.start()
        
    def cog_unload(self):
        self.zn.cancel()
           
    @tasks.loop(seconds=10.0)
    async def zn(self):
        await self.bot.change_presence(activity=discord.Activity(name=f"{len(self.bot.guilds)} serwerów", type=discord.ActivityType.watching), status=discord.Status.dnd)
        await asyncio.sleep(10)
        await self.bot.change_presence(activity=discord.Activity(name=f"{len(self.bot.users)} użytkowników", type=discord.ActivityType.listening), status=discord.Status.dnd)
        await asyncio.sleep(10)
        await self.bot.change_presence(activity=discord.Activity(name="komende pomoc", type=discord.ActivityType.watching), status=discord.Status.dnd)
        await asyncio.sleep(10)
        await self.bot.change_presence(activity=discord.Activity(name=f"\u200e", type=discord.ActivityType.watching), status=discord.Status.dnd)
        await asyncio.sleep(10)

    @zn.before_loop
    async def before_zn(self):
        await self.bot.wait_until_ready()
            
def setup(client):
    client.add_cog(Status(client))
    print("Załadowano status")
