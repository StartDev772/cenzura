import discord
from discord.ext import commands
import json
import functions

class Inne(commands.Cog):
    def __init__(self, client):
        self.bot = client
        self.ow = {}

    @commands.group(description="Lista komend todo", usage="todo", invoke_without_command=True)
    async def todo(self, ctx):
        e = discord.Embed(title="Komendy todo:", description="> `todo add (tekst)`, `todo view (osoba/id)`, `todo remove (nazwa)`, `todo clear`", colour=discord.Color.red())
        await ctx.send(embed=e)

    @todo.command(description="Dodaje tekst do todo", usage="todo add (tekst)", aliases=["+"])
    async def add(self, ctx, *, arg):
        arg = arg.replace("@", "@\u200b")
        if len(arg) > 100:
            return await ctx.send("Wiadomość przekroczyła limit znaków (`limit 100`)")

        with open("todo.json", "r") as f:
            t = json.load(f)
            if not str(ctx.author.id) in t:
                t[str(ctx.author.id)] = "Lista rzeczy do zrobienia:"
            
            t[str(ctx.author.id)] = t[str(ctx.author.id)] + "\n- " + arg

        with open("todo.json", "w") as f:
            json.dump(t, f, indent=4)

        await ctx.send(f"Dodano `{arg}` do twojego todo")

    @todo.command(description="Pokazuje todo", usage="todo view [osoba]", aliases=["zobacz"])
    async def view(self, ctx, member: discord.User=None):
        if not member:
            with open("todo.json", "r") as f:
                iu = json.load(f)

            if str(ctx.author.id) not in iu:
                ius = "Użytkownik nie ma todo."
            else:
                ius = iu[str(ctx.author.id)]
                
            e=discord.Embed(title=f"Todo użytkownika {ctx.author.name}", description=ius, colour=discord.Colour.red())
            e.set_footer(text=f"Wywołane przez {ctx.author.id}")

            return await ctx.send(embed=e)

        with open("todo.json", "r") as f:
            iu = json.load(f)

        if str(member.id) not in iu:
            ius = "Użytkownik nie ma todo."
        else:
            ius = iu[str(member.id)]

        e=discord.Embed(title=f"Todo użytkownika {member.name}", description=ius, colour=discord.Colour.red(), timestamp=ctx.message.created_at)

        await ctx.send(embed=e)

    @todo.command(description="Czyści todo", usage="todo clear")
    async def clear(self, ctx):
        with open("todo.json", "r") as f:
            iu = json.load(f)
            iu[str(ctx.author.id)] = "Lista rzeczy do zrobienia:"

        with open("todo.json", "w") as f:
            json.dump(iu, f, indent=4)

        await ctx.send("Wyczyszczono twoje todo")

    @todo.command(description="Usuwa tekst z todo", usage="todo remove (tekst)", aliases=["-", "delete", "rem", "del"])
    async def remove(self, ctx, *, arg):
        arg = arg.replace("@", "@\u200b")
        with open("todo.json", "r") as f:
            t = json.load(f)

            t[str(ctx.author.id)] = t[str(ctx.author.id)].replace("\n- " + arg, "")

        with open("todo.json", "w") as f:
            json.dump(t, f, indent=4)

        await ctx.send(f"Usunięto `{arg}` z todo.")

    @commands.Cog.listener()
    async def on_message_delete(self, msg):
        if msg.author.bot:
            return
            
        if not str(msg.guild.id) in self.ow:
            self.ow[str(msg.guild.id)] = []

        self.ow[str(msg.guild.id)].append(msg)

    @commands.command(description="Pokazuje ostatnią usuniętą wiadomość", usage="snipe")
    async def snipe(self, ctx):
        if not functions.check(ctx, "inne", "snipe"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `inne.snipe`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
          
        if not str(ctx.guild.id) in self.ow:
            return await ctx.send("Nie udało mi sie złapać żadnej wiadomości.")
            
        snipe = self.ow[str(ctx.guild.id)] if len(self.ow[str(ctx.guild.id)]) < 10 else [self.ow[str(ctx.guild.id)][::-1][ow] for ow in range(10)][::-1]
          
        e = discord.Embed(title="Lista ostatnich usuniętych wiadomości:", description="\n".join([f"{self.ow[str(ctx.guild.id)].index(ow) + 1}. {ow.channel.mention} {ow.author.mention}: {ow.content}" for ow in snipe]), colour=discord.Colour.red())
        e.set_footer(text=f"Wywołane przez {ctx.author.id}")
        await ctx.send(embed=e)

    @commands.group(description="Lista komend cmd", usage="cmd", invoke_without_command=True)
    async def cmd(self, ctx):
        if not functions.check(ctx, "inne", "cmd"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `inne.cmd`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)

        e=discord.Embed(title="Komendy cmd:", description="> `cmd add (nazwa komendy) (tekst)`, `cmd remove (nazwa komendy)`, `cmd info (nazwa komendy)`, `cmd list`", color=discord.Color.red())
        e.set_footer(text="<> = nazwa użytkownika, [] = wzmianka")

        await ctx.send(embed=e)

    @cmd.command(description="Dodaje komende serwerową", usage="cmd add (komenda) (tekst)", aliases=["+", "add"])
    async def _add(self, ctx, cmd: str, *, arg):
        if not functions.check(ctx, "inne", "cmd"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `inne.cmd`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje d  o różnych ról (komenda perm)")
            return await ctx.send(embed=e)
            
        with open("customcmd.json", "r") as f:
            c = json.load(f)

            if not str(ctx.guild.id) in c:
                c[str(ctx.guild.id)] = {}

            if not cmd in c:
                c[str(ctx.guild.id)][cmd] = {}
                c[str(ctx.guild.id)][cmd]['komenda'] = cmd
                c[str(ctx.guild.id)][cmd]['msg'] = arg
                c[str(ctx.guild.id)][cmd]['author_name'] = str(ctx.author)
                c[str(ctx.guild.id)][cmd]['author_id'] = str(ctx.author.id) 

            c[str(ctx.guild.id)][cmd]['komenda'] = cmd
            c[str(ctx.guild.id)][cmd]['msg'] = arg
            c[str(ctx.guild.id)][cmd]['author_name'] = str(ctx.author)
            c[str(ctx.guild.id)][cmd]['author_id'] = str(ctx.author.id) 

        with open("customcmd.json","w") as f:
            json.dump(c, f, indent=4)

        await ctx.send("Dodano komende.")

    @cmd.command(description="Usuwa komende serwerową", usage="cmd remove (komenda)", aliases=["-", "rem", "remove"])
    async def _remove(self, ctx, cmd: str):
        if not functions.check(ctx, "inne", "cmd"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `inne.cmd`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
          
        with open("customcmd.json", "r") as f:
            c = json.load(f)
            
            del c[str(ctx.guild.id)][cmd]

        with open("customcmd.json","w") as f:
            json.dump(c, f, indent=4)

        await ctx.send("Usunięto komende.")

    @cmd.command(description="Pokazuje informacje o komendzie serwerowej", usage="cmd info (komenda)")
    async def info(self, ctx, arg):
        with open("customcmd.json", "r") as f:
            c = json.load(f)
            
            author_name = c[str(ctx.guild.id)][arg]['author_name']
            author_id = c[str(ctx.guild.id)][arg]['author_id']
            msg = c[str(ctx.guild.id)][arg]['msg']

        e=discord.Embed(title=f"Informacje o {arg}", description=f"Stworzona przez: `{author_name}` (`{author_id}`)\nWiadomość w niej: `{msg}`", colour=discord.Colour.red())

        await ctx.send(embed=e)

    @cmd.command(description="Pokazuje liste serwerowych komend", usage="cmd list")
    async def list(self, ctx):
        commands = []
        with open("customcmd.json", "r") as f:
            c = json.load(f)
            
            for cmd in c[str(ctx.guild.id)]:
                commands.append(cmd)
                
        e = discord.Embed(title=f"Serwerowe komendy ({len(commands)}):", description=", ".join(commands), color=discord.Color.red())
        await ctx.send(embed=e)

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot:
            return

        with open("glvls.json", "r") as f:
            glvl = json.load(f)

            if not str(msg.guild.id) in glvl:
                glevel = "off"
            else:
                glevel = glvl[str(msg.guild.id)]

        with open("profil.json", "r") as f:
            profile = json.load(f)

            if not str(msg.author.id) in profile:
                profile[str(msg.author.id)] = {}
                profile[str(msg.author.id)]["imie"] = "nie podano"
                profile[str(msg.author.id)]["plec"] = "nie podano"
                profile[str(msg.author.id)]["wiek"] = "nie podano"
                profile[str(msg.author.id)]["orientacja"] = "nie podano"
                profile[str(msg.author.id)]["global_levels"] = {}
                profile[str(msg.author.id)]["global_levels"]["level"] = 1
                profile[str(msg.author.id)]["global_levels"]["exp"] = 0

            profile[str(msg.author.id)]["global_levels"]["exp"] = profile[str(msg.author.id)]["global_levels"]["exp"] + 1

            if profile[str(msg.author.id)]["global_levels"]["exp"] > profile[str(msg.author.id)]["global_levels"]["level"] * 125:
                profile[str(msg.author.id)]["global_levels"]["level"] = profile[str(msg.author.id)]["global_levels"]["level"] + 1
                profile[str(msg.author.id)]["global_levels"]["exp"] = 0
                if glevel == "on":
                    await msg.channel.send(f"{msg.author.name} zdobyłeś(-aś) `{profile[str(msg.author.id)]['global_levels']['level']}` globalny level!")

        with open("profil.json", "w") as f:
            json.dump(profile, f, indent=4)

    @commands.group(description="Lista komend profile", usage="profile", invoke_without_command=True)
    async def profile(self, ctx):
        e = discord.Embed(title="Komendy profile:", description="> `profile view [osoba]`, `profile set`", colour=discord.Color.red())

        await ctx.send(embed=e)

    @profile.command(description="Wyświetla profil", usage="profile view [osoba]", aliases=["view"])
    async def _view(self, ctx, member: discord.User=None):
        member = member or ctx.author

        with open("profil.json", "r") as f:
            profile = json.load(f)

            imie = profile[str(member.id)]["imie"]
            plec = profile[str(member.id)]["plec"]
            wiek = profile[str(member.id)]["wiek"]
            orientacja = profile[str(member.id)]["orientacja"]
            level = profile[str(member.id)]["global_levels"]["level"]
            exp = profile[str(member.id)]["global_levels"]["exp"]

        e = discord.Embed(title=f"Profil użytkownika {member.name}:", description=f"**Ogólne:**\nImie: `{imie}`\nPłeć: `{plec}`\nWiek: `{wiek}`\nOrientacja: `{orientacja}`\n\n**Statystyki:**\nGlobalny level: `{level}`\nGlobalny exp: `{exp}` / `{level * 125}`", color=discord.Color.red())
        e.set_thumbnail(url=str(member.avatar_url))
        e.set_footer(text=f"Wywołane przez {ctx.author.id}")

        await ctx.send(embed=e)

    @profile.group(description="Lista komend profile set", usage="profile set", invoke_without_command=True, aliases=["set"])
    async def _set(self, ctx):
        e = discord.Embed(title="Komendy profile set:", description="> `profile set name (imie)`, `profile set gender (m/f)`, `profile set age (wiek)`, `profile set orientation (hetero/bi/homo)`\n\n```Aby usunąć coś należy wpisać np. profile set name remove```", color=discord.Color.red())

        await ctx.send(embed=e)

    @_set.command(description="Ustawia imie", usage="profile set name (imie)")
    async def name(self, ctx, arg):
        arg = arg.replace("@everyone", "@\u200beveryone").replace("@here", "@\u200bhere")
        if len(arg) > 10:
            return await ctx.send("Limit znaków to 10")
            
        arg = arg.split(" ")[0].replace("`", "'")
            
        if arg == "remove":
            arg = "none"

        with open("profil.json", "r") as f:
            profil = json.load(f)

            profil[str(ctx.author.id)]["imie"] = arg

        with open("profil.json", "w") as f:
            json.dump(profil, f, indent=4)

        if arg == "nie podano":
            return await ctx.send("Usunięto `imie`.")

        await ctx.send(f"Twoje imie teraz to `{arg}`.")

    @_set.command(description="Ustawia płeć", usage="profile set gender (m/f)")
    async def gender(self, ctx, arg):
        if not arg:
            return await ctx.send("Musisz podać `M` albo `F`.")

        if arg == "remove":
            plec = "none"
            arg = "none"
        else:
            if arg == "M" or arg == "m" or arg == "male":
                plec = "mężczyzna"
            elif arg == "F" or arg == "f" or arg == "female":
                plec = "kobieta"
            elif not arg == "M" or arg == "m" or arg == "mezczyzna" or arg == "F" or arg == "f" or arg == "female":
                return await ctx.send("Musisz podać `M` albo `F`.")

        with open("profil.json", "r") as f:
            profil = json.load(f)

            profil[str(ctx.author.id)]["plec"] = plec

        with open("profil.json", "w") as f:
            json.dump(profil, f, indent=4)

        if arg == "nie podano":
            return await ctx.send("Usunięto `płeć`.")

        await ctx.send(f"Ustawiono płeć jako `{plec}`.")

    @_set.command(description="Ustawia wiek", usage="profile set age (wiek)")
    async def age(self, ctx, arg):
        try:
            if int(arg) > 100:
                return await ctx.send("Za dużo")
            if int(arg) < 13:
                return await ctx.send("Za mało")
        except:
            arg = "none"

        with open("profil.json", "r") as f:
            profil = json.load(f)

            try:
                profil[str(ctx.author.id)]["wiek"] = int(arg)
            except:
                arg = "nie podano"
                profil[str(ctx.author.id)]["wiek"] = str(arg)

        with open("profil.json", "w") as f:
            json.dump(profil, f, indent=4)

        if arg == "nie podano":
            return await ctx.send("Usunięto `wiek`.")

        await ctx.send(f"Ustawiono wiek na `{arg}`.")

    @_set.command(description="Ustawia orientacje", usage="profile set orientation (hetero/bi/homo)")
    async def orientation(self, ctx, arg):
        if not arg:
            return await ctx.send("Musisz podać orientacje `hetero`/`bi`/`homo`.")

        if arg == "remove":
            orientacja = "none"
            arg = "none"
        else:
            if arg == "hetero":
                orientacja = arg
            elif arg == "bi":
                orientacja = arg
            elif arg == "homo":
                orientacja = arg
            elif not arg in ["hetero", "bi", "homo"]:
                return await ctx.send("Musisz podać `hetero`/`bi`/`homo`.")

        with open("profil.json", "r") as f:
            profil = json.load(f)

            profil[str(ctx.author.id)]["orientacja"] = str(orientacja)

        with open("profil.json", "w") as f:
            json.dump(profil, f, indent=4)

        if arg == "nie podano":
            return await ctx.send("Usunięto `orientacja`.")

        await ctx.send(f"Ustawiono orientacje na `{arg}`.")

def setup(client):
    client.add_cog(Inne(client))
    print("Załadowano inne")
