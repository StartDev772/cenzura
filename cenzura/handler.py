import discord
from discord.ext import commands
import config

class Handler(commands.Cog):
    def __init__(self, client):
        self.bot = client
        self.debug = False
        
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        error = getattr(error, "original", error)
 
        if ctx.author.id in config.owners:
            if self.debug:
                return await ctx.send(f"```{error}```")
          
        if isinstance(error, commands.CommandNotFound):
            return await ctx.send("Nie znaleziono takiej komendy")
          
        elif isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
            return await ctx.send(f"Poprawne użycie to `{ctx.command.usage}`")
            
        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send("Ta komenda jest wyłączona")

        elif isinstance(error, KeyError):
            return await ctx.send("Nie znaleziono")
          
    @commands.command(description="Pokazuje wszystkie errory", usage="debug")
    async def debug(self, ctx):
        if ctx.author.id in config.owners:
            if self.debug:
                self.debug = False
                return await ctx.send("Wyłączono debugowanie")
            else:
                self.debug = True
                return await ctx.send("Włączono debugowanie")
          
        e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `handler.debug`", color=discord.Color.red())
        await ctx.send(embed=e)
    
def setup(client):
    client.add_cog(Handler(client))
    print("Załadowano handler")