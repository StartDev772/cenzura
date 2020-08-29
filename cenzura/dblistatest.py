import discord
from discord.ext import commands
from dblista import DBLista
import requests
import config

class Dblistatest(commands.Cog):
    def __init__(self, client):
        self.bot = client
        
    @commands.command(description="Pokazuje informacje o bocie ze strony DBLista", usage="botinfo [bot]")
    async def botinfo(self, ctx, bot: discord.User=None):
        bot = bot or self.bot.user

        dbl = DBLista(self.bot, config.dblista)
        info = await dbl.bot_info(bot.id)

        e = discord.Embed(title=bot.name)
        e.add_field(name="Short description:", value=(info.short_description if not len(info.short_description) > 1000 else info.short_description[:round(len(info.short_description) / 2)]) or "none", inline=False)
        e.add_field(name="Full description:", value=(info.full_description if not len(info.full_description) > 1000 else info.full_description[:round(len(info.full_description) / 2)]) or "none", inline=False)
        e.add_field(name="Prefix:", value=info.prefix or "none", inline=False)
        e.add_field(name="Library:", value=info.library or "none", inline=False)
        e.add_field(name="Tags:", value=", ".join(info.tags) or "none", inline=False)
        e.add_field(name="Votes:", value=info.votes or "none", inline=False)

        e.add_field(name="Discord server:", value=info.discord_server or "none", inline=False)
        e.add_field(name="Git repository:", value=info.git_repository or "none", inline=False)
        e.add_field(name="Website:", value=info.website or "none", inline=False)

        e.add_field(name="Owner:", value=f"<@!{info.owner or 'none'}>", inline=False)
        e.add_field(name="Owners:", value=", ".join([f"<@!{o}>" for o in info.owners]) or "none", inline=False)

        e.add_field(name="Booster:", value=f"<@!{info.booster or 'none'}>", inline=False)
        e.add_field(name="Average:", value=info.average or "none", inline=False)
        
        e2 = discord.Embed(title="Ratings:", description="\n".join([f"{'⭐' * r['rating']} <@!{r['author']}> : {r['details']}" for r in info.ratings]))

        await ctx.send(embed=e)
        await ctx.send(embed=e2)

    @commands.command(description="Aktualizuje statystyki na DBLista", usage="updatestats")
    async def updatestats(self, ctx):
        dbl = DBLista(self.bot, config.dblista)
        update = await dbl.update_stats()

        await ctx.send(f"{update} | {len(self.bot.guilds)} guilds, {len(self.bot.users)} members")
        
def setup(client):
    client.add_cog(Dblistatest(client))
    print("Załadowano dblistatest")
