import discord
from discord.ext import commands
import json
import functions
class Lvls(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot:
            return
            
        with open("checkguildlvl.json", "r") as f:
            cg = json.load(f)

            if not str(msg.guild.id) in cg:
                checkguild = "off"
            else:
                checkguild = cg[str(msg.guild.id)]

        with open("osoby.json", "r") as f:
            lvl = json.load(f)

            if not str(msg.guild.id) in lvl:
                lvl[str(msg.guild.id)] = {}

            if not str(msg.author.id) in lvl[str(msg.guild.id)]:
                lvl[str(msg.guild.id)][str(msg.author.id)] = {}
                lvl[str(msg.guild.id)][str(msg.author.id)]["level"] = 1
                lvl[str(msg.guild.id)][str(msg.author.id)]["exp"] = 0

            lvl[str(msg.guild.id)][str(msg.author.id)]["exp"] = lvl[str(msg.guild.id)][str(msg.author.id)]["exp"] + 1

            if lvl[str(msg.guild.id)][str(msg.author.id)]["exp"] > lvl[str(msg.guild.id)][str(msg.author.id)]["level"] * 125:
                lvl[str(msg.guild.id)][str(msg.author.id)]["level"] = lvl[str(msg.guild.id)][str(msg.author.id)]["level"] + 1
                lvl[str(msg.guild.id)][str(msg.author.id)]["exp"] = 0
                if checkguild == "on":
                    await msg.channel.send(f"{msg.author.name} zdobyłeś(-aś) `{lvl[str(msg.guild.id)][str(msg.author.id)]['level']}` level!")

        with open("osoby.json", "w") as f:
            json.dump(lvl, f, indent=4)

    @commands.command(description="Pokazuje aktualny level", usage="level [osoba]", aliases=["lvl"])
    async def level(self, ctx, member: discord.Member=None):
        if not functions.check(ctx, "level", "level"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `level.level`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
          
        if not member:
            member = ctx.author

        with open("osoby.json", "r") as f:
            lvl = json.load(f)

            exp = lvl[str(ctx.guild.id)][str(member.id)]["exp"]
            level = lvl[str(ctx.guild.id)][str(member.id)]["level"]

        with open("profil.json", "r") as f:
            glvl = json.load(f)

            gexp = glvl[str(member.id)]["global_levels"]["exp"]
            glevel = glvl[str(member.id)]["global_levels"]["level"]

        e = discord.Embed(title=f"Levele użytkownika {member.name}:", description=f"**Serwerowy level:**\nLevel: `{level}`\nExp: `{exp}` / `{level * 125}`\n\n**Globalny level:**\nLevel: `{glevel}`\nExp: `{gexp}` / `{glevel * 125}`", color=discord.Color.red())
        e.set_thumbnail(url=str(member.avatar_url))

        await ctx.send(embed=e)
        
    @commands.command(description="Włącza wiadomość po zdobyciu nowego levelu", usage="lvlon")
    async def lvlon(self, ctx):
        if not functions.check(ctx, "level", "lvlon"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `level.lvlon`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
          
        with open("checkguildlvl.json", "r") as f:
            lvl = json.load(f)

            lvl[str(ctx.guild.id)] = "on"

        with open("checkguildlvl.json", "w") as f:
            json.dump(lvl, f, indent=4)

        await ctx.send("Włączono wiadomości o nowym levelu.")

    @commands.command(description="Wyłącza wiadomość po zdobyciu nowego levelu", usage="lvloff")
    async def lvloff(self, ctx):
        if not functions.check(ctx, "level", "lvloff"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `level.lvloff`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
          
        with open("checkguildlvl.json", "r") as f:
            lvl = json.load(f)

            lvl[str(ctx.guild.id)] = "off"

        with open("checkguildlvl.json", "w") as f:
            json.dump(lvl, f, indent=4)

        await ctx.send("Wyłączono wiadomości o nowym levelu.")
        
    @commands.command(description="Pokazuje levele użytkowników", usage="levels", aliases=["lvls"])
    async def levels(self, ctx):
        if not functions.check(ctx, "level", "levels"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `level.levels`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
            
        with open("osoby.json", "r") as f:
            lvl = json.load(f)
            
            e = discord.Embed(title="Levele:", description="\n".join([f"{m.name} : `{lvl[str(ctx.guild.id)][str(m.id)]['level']}` (`{lvl[str(ctx.guild.id)][str(m.id)]['exp']}` / `{lvl[str(ctx.guild.id)][str(m.id)]['level'] * 125}`)" for m in [self.bot.get_user(int(m)) for m in lvl[str(ctx.guild.id)] if lvl[str(ctx.guild.id)][m]["level"] > 1 if m in [str(i.id) for i in ctx.guild.members]]]), color=discord.Color.red())
            
            await ctx.send(embed=e)

    @commands.command(description="Włącza wiadomość po zdobyciu globalnego levelu", usage="glvlon")
    async def glvlon(self, ctx):
        if not functions.check(ctx, "glevel", "glvlon"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `glevel.glvlon`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
          
        with open("glvls.json", "r") as f:
            glvl = json.load(f)

            if not str(ctx.guild.id) in glvl:
                glvl[str(ctx.guild.id)] = "on"

            glvl[str(ctx.guild.id)] = "on"

        with open("glvls.json", "w") as f:
            json.dump(glvl, f, indent=4)

        await ctx.send("Włączono powiadomienia o nowym global levelu.")

    @commands.command(description="Wyłącza wiadomość po zdobyciu globalnego levelu", usage="glvloff")
    async def glvloff(self, ctx):
        if not functions.check(ctx, "glevel", "glvloff"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `glevel.glvloff`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
          
        with open("glvls.json", "r") as f:
            glvl = json.load(f)

            if not str(ctx.guild.id) in glvl:
                glvl[str(ctx.guild.id)] = "off"

            glvl[str(ctx.guild.id)] = "off"

        with open("glvls.json", "w") as f:
            json.dump(glvl, f, indent=4)

        await ctx.send("Wyłączono powiadomienia o nowym global levelu.")

def setup(client):
    client.add_cog(Lvls(client))
    print("Załadowano lvls")
