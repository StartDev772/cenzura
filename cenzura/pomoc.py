import discord
from discord.ext import commands
import json

class Pomoc(commands.Cog):
    def __init__(self, client):
        self.bot = client
        
    @commands.command(description="Pokazuje pomoc", usage="pomoc [komenda]", aliases=["help"])
    async def pomoc(self, ctx, *, cmd=None):
        if cmd:
            cmd = cmd
            cmd2 = self.bot.get_command(cmd)

            if not cmd2:
                return await ctx.send("Nie znaleziono takiej komendy")

            description = cmd2.description or "brak"
            usage = cmd2.usage or "brak"
            aliases = "`" + ", ".join(cmd2.aliases or ["brak"]) + "`"

            embed = discord.Embed(title="POMOC:", description=f"Opis: `{description}`\nUżycie: `{usage}`\nAliasy: {aliases}", color=discord.Color.red())
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            embed.set_footer(text="() - obowiązkowe, [] - opcjonalne")
            return await ctx.send(embed=embed)

        with open("prefixes.json", "r") as f:
             prefixes = json.load(f)

        if not str(ctx.guild.id) in prefixes:
            prefix = ";"
        else:
            prefix = prefixes[str(ctx.guild.id)]

        names = {
            "Fun": "4Fun",
            "Lvls": "Levele",
            "Sranks": "Serwerowe permisje",
            "Info": "O bocie",
            "Dblistatest": "DBLista",
            "_8ball": "8ball"
        }

        commands = {}
        hiddencogs = ["status", "jishaku", "eventy", "developerskie", "handler", "pomoc"]

        for cog in self.bot.cogs:
            if not cog.lower() in hiddencogs:
                commands[cog] = [names[cmd.name] if cmd.name in names else cmd.name for cmd in self.bot.get_cog(cog).get_commands()]

        e = discord.Embed(title="POMOC:", description=f"Prefix na tym serwerze to `{prefix}`\nWpisz `pomoc [komenda]` by sprawdzić użycie danej komendy", colour=discord.Colour.red())
        
        for cog in commands:
            e.add_field(name=(names[cog] if cog in names else cog) + ":", value="> " + ", ".join(["`" + cmd + "`" for cmd in commands[cog]]), inline=False)

        e.add_field(name="\u200b", value=f"\[ [Dodaj bota](https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=305196118&scope=bot) \] \[ [Support](https://discord.gg/3MRjT2x) \] \[ [Kod bota](https://github.com/CZUBIX/cenzura) \]", inline=False)
        
        await ctx.send(embed=e)
        
def setup(client):
    client.add_cog(Pomoc(client))
    print("Załadowano pomoc")
