import discord
from discord.ext import commands
import requests
import os
import psutil
import humanize
import platform

class Info(commands.Cog):
    def __init__(self, client):
        self.bot = client
        
    @commands.command(description="Pokazuje ekipe bota", usage="team")
    async def team(self, ctx):
        czubix = self.bot.get_user(636096693712060416)
        _6bytes = self.bot.get_user(264905890824585216)
        e = discord.Embed(title="Ekipa:", description=f"{czubix} - Developer\n{_6bytes} - IT", color= discord.Color.red())
        e.set_thumbnail(url=self.bot.user.avatar_url)
        await ctx.send(embed=e)
        
    @commands.command(description="Pokazuje statystyki bota", usage="botstats")
    async def botstats(self, ctx):
        e = discord.Embed(title="Statystyki bota:", description=f"Serwery: `{len(self.bot.guilds)}`\nUżytkownicy: `{len(self.bot.users)}`\n\nKomendy: `{len(self.bot.commands)}`\n\nWersja Python: `{platform.python_version()}`\nWersja discord.py: `{discord.__version__}`\n\nWykorzystana pamięć RAM: `{humanize.naturalsize(psutil.Process().memory_full_info().rss)}`\nWykorzystane CPU: `{psutil.cpu_percent()}%`", color=discord.Color.red())
        
        await ctx.send(embed=e)
      
def setup(client):
    client.add_cog(Info(client))
    print("Załadowano info")
