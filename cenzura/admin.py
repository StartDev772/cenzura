import discord
from discord.ext import commands
import asyncio
import json
import functions

class Administracja(commands.Cog):
    def __init__(self, client):
        self.bot = client
        
    @commands.command(description="Daje ostrzeżenie", usage="warn (osoba) [powód]")
    async def warn(self, ctx, member: discord.Member, *, reason="nie podano powodu"):
        if not functions.check(ctx, "admin", "warn"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `admin.warn`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
          
        if ctx.author.top_role <= member.top_role:
            return await ctx.send("Nie możesz dać warna tej osobie")
    
        with open("warns.json", "r") as f:
            warns = json.load(f)
            if not str(ctx.guild.id) in warns:
                warns[str(ctx.guild.id)] = {}

            if not str(member.id) in warns[str(ctx.guild.id)]:
                warns[str(ctx.guild.id)][str(member.id)] = {}

            warns[str(ctx.guild.id)][str(member.id)][str(len(warns[str(ctx.guild.id)][str(member.id)]) + 1)] = reason

        with open("warns.json", "w") as f:
            json.dump(warns, f, indent=4)
        
        await ctx.send(f"`{member.name}` dostał ostrzeżenie z powodu {reason}")
        await member.send(f"Dostałeś ostrzeżenie przez `{ctx.author.name}` na serwerze `{ctx.guild.name}` z powodu {reason}")

    @commands.command(description="Sprawdza ilość ostrzeżeń", usage="warns [osoba]")
    async def warns(self, ctx, member: discord.Member=None):
        if not functions.check(ctx, "admin", "warns"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `admin.warns`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
          
        member = member or ctx.author
        
        with open("warns.json", "r") as f:
            warns = json.load(f)

        e = discord.Embed(title=f"Warny użytkownika {member.name}:", description="\n".join([f"{warn}. {warns[str(ctx.guild.id)][str(member.id)][warn]}" for warn in warns[str(ctx.guild.id)][str(member.id)]]), color=discord.Color.red())
        await ctx.send(embed=e)

    @commands.command(description="Usuwa ostrzeżenie", usage="removewarn (osoba) (id)", aliases=["rwarn", "dwarn", "delwarn"])
    async def removewarn(self, ctx, member: discord.Member, _id: str):
        if not functions.check(ctx, "admin", "removewarn"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `admin.removewarn`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
          
        with open("warns.json", "r") as f:
            warns = json.load(f)
            del warns[str(ctx.guild.id)][str(member.id)][_id]

        with open("warns.json", "w") as f:
            json.dump(warns, f, indent=4)
        
        await ctx.send(f"Usunięto warna o ID `{_id}` użytkownikowi `{member.name}`")

    @commands.command(description="Usuwa wszystkie ostrzeżenia", usage="clearwarns (osoba)", aliases=["cwarns"])
    async def clearwarns(self, ctx, member: discord.Member):
        if not functions.check(ctx, "admin", "clearwarns"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `admin.clearwarns`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
          
        with open("warns.json", "r") as f:
            warns = json.load(f)
            del warns[str(ctx.guild.id)][str(member.id)]

        with open("warns.json", "w") as f:
            json.dump(warns, f, indent=4)
        
        await ctx.send(f"Użytkownik `{member.name}` został wyczyszczony z warnów")
            
    @commands.command(description="Wyrzuca osobe", usage="kick (osoba) [powód]")
    async def kick(self, ctx, member: discord.Member, *, arg="nie podano powodu"):
        if not functions.check(ctx, "admin", "kick"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `admin.kick`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
          
        if ctx.author.top_role <= member.top_role:
            return await ctx.send("Nie możesz wyrzucić tej osoby")
            
        arg = arg or "nie podano powodu"
        
        try:
            await member.kick(reason=arg)
        except discord.Forbidden:
            return await ctx.send("Bot nie ma uprawnień")

        await ctx.send(f"`{member.name}` został wyrzucony z powodu {arg}")
        await member.send(f"Zostałeś wyrzucony przez `{ctx.author.name}` na serwerze `{ctx.guild.name}` z powodu {arg}")
            
    @commands.command(description="Banuje osobe", usage="ban (osoba) [powód]")
    async def ban(self, ctx, member: discord.Member, *, arg="nie podano powodu"):
        if not functions.check(ctx, "admin", "ban"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `admin.ban`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
          
        if ctx.author.top_role <= member.top_role:
            return await ctx.send("Nie możesz zbanować tej osoby")
            
        arg = arg or "nie podano powodu"
        
        try:
            await member.ban(reason=arg)
        except discord.Forbidden:
            return await ctx.send("Bot nie ma uprawnień")
            
        await ctx.send(f"`{member.name}` został zbanowany z powodu {arg}")
        await member.send(f"Zostałeś zbanowany przez `{ctx.author.name}` na serwerze `{ctx.guild.name}` z powodu {arg}")
            
    @commands.command(description="Usuwa wiadomości", usage="clear (maks. 1000) [osoba]")
    async def clear(self, ctx, amount=100, member: discord.Member=None):
        if not functions.check(ctx, "admin", "clear"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `admin.clear`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)

        if amount > 1000:
            return await ctx.send("Limit to `1000`")
          
        def check(m):
            return m.author == member
           
        if member:
            await ctx.message.delete()
            try:
                await ctx.channel.purge(limit=amount, check=check)
            except discord.Forbidden:
                return await ctx.send("Bot nie ma uprawnień")
              
            return await ctx.send(f"Usunięto `{amount}` wiadomości użytkownika `{member.name}`.", delete_after=5)
          
        try:
            await ctx.channel.purge(limit=amount + 1)
        except discord.Forbidden:
            return await ctx.send("Bot nie ma uprawnień")
          
        await ctx.send(f"Usunięto `{amount}` wiadomości.", delete_after=5)
                        
    @commands.command(usage="userinfo [osoba]")
    async def userinfo(self, ctx, member: discord.Member=None):
        if not functions.check(ctx, "admin", "userinfo"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `admin.userinfo`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
          
        member = member or ctx.author
        
        embed = discord.Embed(title=f'Informacje o {member.name}{" BOT" if member.bot else ""}', colour = member.color)

        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name='ID:', value="`" + str(member.id) + "`", inline=False)
        embed.add_field(name='Nick z tagiem:', value="`" + str(member) + "`", inline=False)
        embed.add_field(name='Role:', value="`" + ', '.join([role.name for role in member.roles[1:]]) + "`", inline=False)
        embed.add_field(name='Top rola:', value="`" + member.top_role.name + "`", inline=False)
        embed.add_field(name='Konto zrobione:', value="`" + str(member.created_at).split(".", 1)[0] + "`", inline=False)
        embed.add_field(name='Dołączył na serwer:', value="`" + str(member.joined_at).split(".", 1)[0] + "`", inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command(usage="serverinfo")
    async def serverinfo(self, ctx):
        if not functions.check(ctx, "admin", "serverinfo"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `admin.serverinfo`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
          
        b = 0
        for member in ctx.guild.members:
            if member.bot:
               b += 1
                
        osoby = len(ctx.guild.members) - b

        time = str(ctx.message.guild.created_at).split(" ")[0]
    
        embed = discord.Embed(
            colour = discord.Colour.red()
        )
    
        embed.set_author(name=f'Informacje o serwerze {ctx.guild}')
        embed.add_field(name='Właściciel:', value=f'{ctx.guild.owner.mention} ({ctx.guild.owner.id})', inline=False)
        embed.add_field(name='ID Serwera:', value=ctx.message.guild.id, inline=False)
        embed.add_field(name='Ilość osób:', value=osoby, inline=False)
        embed.add_field(name='Ilość botów:', value=b, inline=False)
        embed.add_field(name='Ilość kanałów:', value=len(ctx.guild.channels), inline=False)
        embed.add_field(name='Ilość ról:', value=len(ctx.guild.roles), inline=False)
        embed.add_field(name='Ilość emotek:', value=len(ctx.guild.emojis), inline=False)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_footer(text=f'Serwer został stworzony dnia {time}')
    
        await ctx.send(embed=embed)

    @commands.group(description="Lista komend set", usage="set", invoke_without_command=True, aliases=["ustaw"])
    async def set(self, ctx):
        if not functions.check(ctx, "admin", "set"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `admin.set`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
          
        e = discord.Embed(title="Komendy set:", description="> `set prefix (prefix)`, `set welcomemsg (kanał) (wiadomość)`, `set offwelcomemsg`, `set leavemsg (kanał) (wiadomość)`, `set offleavemsg`, `set autorole (rola)`, `set offautorole`, `set offbadwords`, `set onbadwords`, `set offinvites`, `set oninvites`, `set cleverbot (kanał)`, `set offcleverbot`", colour=discord.Colour.red())
        e.set_footer(text="<> = nick osoby, [] = wzmianka, {} = licznik osób")

        await ctx.send(embed=e)

    @set.command(description="Ustawia prefix", usage="set prefix (prefix)")
    async def prefix(self, ctx, *, arg):
        if not functions.check(ctx, "admin", "set"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `admin.set`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
          
        with open(r"prefixes.json", "r") as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = arg
        with open(r"prefixes.json", "w") as f:
            json.dump(prefixes, f, indent=4)

        await ctx.send(f"Ustawiono `{arg}` jako prefix na ten serwer.")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            with open("welcome.json", "r") as f:
                w = json.load(f)
                if not str(member.guild.id) in w:
                    return

                c = w[str(member.guild.id)]['channel']
                m = w[str(member.guild.id)]['msg']

            m = m.replace("<>", member.name)
            m = m.replace("[]", member.mention)
            m = m.replace("{}", str(len(member.guild.members)))
            m = m.replace("@", "@\u200b")
            await member.guild.get_channel(c).send(m)

        except:
            return

    @set.command(description="Ustawia wiadomość powitalną", usage="set welcomemsg (kanał) (wiadomość)")
    async def welcomemsg(self, ctx, channel: discord.TextChannel, *, arg):
        if not functions.check(ctx, "admin", "set"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `admin.set`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
          
        with open("welcome.json", "r") as f:
            w = json.load(f)
            if not str(ctx.guild.id) in w:
                w[str(ctx.guild.id)] = ctx.guild.id
                w[str(ctx.guild.id)] = {}

            if not str(channel.id) in w:
                w[str(ctx.guild.id)]['channel'] = channel.id
                w[str(ctx.guild.id)]['msg'] = arg

            w[str(ctx.guild.id)] = ctx.guild.id
            w[str(ctx.guild.id)] = {}
            w[str(ctx.guild.id)]['channel'] = channel.id
            w[str(ctx.guild.id)]['msg'] = arg

        with open("welcome.json", "w") as f:
            json.dump(w, f, indent=4)

        await ctx.send(f"Ustawiono `{arg}` jako wiadomość powitalna na kanał {channel.mention}.")

    @set.command(description="Wyłącza wiadomość powitalną", usage="set offwelcomemsg")
    async def offwelcomemsg(self, ctx):
        if not functions.check(ctx, "admin", "set"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `admin.set`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
          
        with open("welcome.json", "r") as f:
            w = json.load(f)
            if not str(ctx.guild.id) in w:
                return await ctx.send("Na tym serwerze nie była ustawiona wiadomość powitalna.")

            w[str(ctx.guild.id)]['channel'] = "off"
            w[str(ctx.guild.id)]['msg'] = "off"

        with open("welcome.json", "w") as f:
            json.dump(w, f, indent=4)

        await ctx.send("Wyłączono wiadomość powitalną na tym serwerze.")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        try:
            with open("bay.json", "r") as f:
                w = json.load(f)
                if not str(member.guild.id) in w:
                    return

                c = w[str(member.guild.id)]['channel']
                m = w[str(member.guild.id)]['msg']

            m = m.replace("<>", member.name)
            m = m.replace("[]", member.mention)
            m = m.replace("{}", str(len(member.guild.members)))
            m = m.replace("@", "@\u200b")
            await member.guild.get_channel(c).send(m)

        except:
            return

    @set.command(description="Ustawia wiadmość pożegnalną", usage="set leavemsg (kanał) (wiadomość)")
    async def leavemsg(self, ctx, channel: discord.TextChannel, *, arg):
        if not functions.check(ctx, "admin", "set"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `admin.set`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
          
        with open("bay.json", "r") as f:
            w = json.load(f)
            if not str(ctx.guild.id) in w:
                w[str(ctx.guild.id)] = ctx.guild.id
                w[str(ctx.guild.id)] = {}

            if not str(channel.id) in w:
                w[str(ctx.guild.id)]['channel'] = channel.id
                w[str(ctx.guild.id)]['msg'] = arg

            w[str(ctx.guild.id)] = ctx.guild.id
            w[str(ctx.guild.id)] = {}
            w[str(ctx.guild.id)]['channel'] = channel.id
            w[str(ctx.guild.id)]['msg'] = arg

        with open("bay.json", "w") as f:
            json.dump(w, f, indent=4)

        await ctx.send(f"Ustawiono `{arg}` jako wiadomość pożegnalna na kanał {channel.mention}.")

    @set.command(description="Wyłącza wiadomość pożegnalną", usage="set offleavemsg")
    async def offleavemsg(self, ctx):
        if not functions.check(ctx, "admin", "set"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `admin.set`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
          
        with open("bay.json", "r") as f:
            w = json.load(f)
            if not str(ctx.guild.id) in w:
                return await ctx.send("Na tym serwerze nie była ustawiona wiadomość pożegnalna.")

            w[str(ctx.guild.id)]['channel'] = "off"
            w[str(ctx.guild.id)]['msg'] = "off"

        with open("bay.json", "w") as f:
            json.dump(w, f, indent=4)

        await ctx.send("Wyłączono wiadomość pożegnalną na tym serwerze.")

    @set.command(description="Po wejściu na serwer użytkownik dostaje role", usage="set autorole (rola)")
    async def autorole(self, ctx, *, role: discord.Role):
        if not functions.check(ctx, "admin", "set"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `admin.set`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
          
        with open("autorola.json", "r") as f:
            a = json.load(f)

            a[str(ctx.guild.id)] = role.id

        with open("autorola.json", "w") as f:
            json.dump(a, f, indent=4)

        await ctx.send(f"Ustawiono `{role}` na autorole na ten serwer.")

    @set.command(description="Wyłącza autorole", usage="set offautorole")
    async def offautorole(self, ctx):
        if not functions.check(ctx, "admin", "set"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `admin.set`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
          
        with open("autorola.json", "r") as f:
            a = json.load(f)
            
            del a[str(ctx.guild.id)]

        with open("autorola.json", "w") as f:
            json.dump(a, f, indent=4)

        await ctx.send(f"Wyłączono autorole na tym serwerze.")

    @set.command(description="Wyłącza przeklinanie na serwerze", usage="set offbadwords")
    async def offbadwords(self, ctx):
        if not functions.check(ctx, "admin", "set"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `admin.set`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
          
        with open("censor.json", "r") as f:
            c = json.load(f)

            if not str(ctx.guild.id) in c:
                c[str(ctx.guild.id)] = "on"

            c[str(ctx.guild.id)] = "on"

        with open("censor.json", "w") as f:
            json.dump(c, f, indent=4)

        await ctx.send("Włączono usuwanie wulgaryzmów.")

    @set.command(description="Włącza przeklinanie na serwerze", usage="set onbadwords")
    async def onbadwords(self, ctx):
        if not functions.check(ctx, "admin", "set"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `admin.set`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
          
        with open("censor.json", "r") as f:
            c = json.load(f)

            if not str(ctx.guild.id) in c:
                c[str(ctx.guild.id)] = "off"

            c[str(ctx.guild.id)] = "off"

        with open("censor.json", "w") as f:
            json.dump(c, f, indent=4)

        await ctx.send("Wyłączono usuwanie wulgaryzmów.")

    @set.command(description="Wyłącza wysyłanie zaproszeń na serwerze", usage="set offinvites")
    async def offinvites(self, ctx):
        if not functions.check(ctx, "admin", "set"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `admin.set`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
          
        with open("antyinvites.json", "r") as f:
            ai = json.load(f)
            ai[str(ctx.guild.id)] = True

        with open("antyinvites.json", "w") as f:
            json.dump(ai, f, indent=4)

        await ctx.send("Włączono usuwanie zaproszeń.")

    @set.command(description="Włącza wysyłanie zaproszeń na serwerze", usage="set oninvites")
    async def oninvites(self, ctx):
        if not functions.check(ctx, "admin", "set"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `admin.set`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
          
        with open("antyinvites.json", "r") as f:
            ai = json.load(f)
            del ai[str(ctx.guild.id)]

        with open("antyinvites.json", "w") as f:
            json.dump(ai, f, indent=4)

        await ctx.send("Wyłączono usuwanie zaproszeń.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        try:
            with open("customcmd.json", "r") as f:
                c = json.load(f)

                cmd = c[str(message.guild.id)][message.content]['komenda']
                msg = c[str(message.guild.id)][message.content]['msg']

            if message.content == cmd:
                msg = msg.replace("<>", str(message.author.name))
                msg = msg.replace("[]", str(message.author.mention))

                await message.channel.send(msg)
        
        except:
            return
        
    @set.command(description="Ustawia cleverbota", usage="set cleverbot (kanał)")
    async def cleverbot(self, ctx, channel: discord.TextChannel):
        if not functions.check(ctx, "admin", "set"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `admin.set`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
          
        with open("cleverbot.json", "r") as f:
            cleverbot = json.load(f)
            
            cleverbot[str(ctx.guild.id)] = channel.id
            
        with open("cleverbot.json", "w") as f:
            json.dump(cleverbot, f, indent=4)
            
        await ctx.send(f"Ustawiono kanał z cleverbotem na {channel.mention}")
        
    @set.command(description="Wyłącza cleverbota", usage="set offcleverbot")
    async def offcleverbot(self, ctx):
        if not functions.check(ctx, "admin", "set"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `admin.set`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
          
        with open("cleverbot.json", "r") as f:
            cleverbot = json.load(f)
            
            del cleverbot[str(ctx.guild.id)]
            
        with open("cleverbot.json", "w") as f:
            json.dump(cleverbot, f, indent=4)
            
        await ctx.send("Wyłączono cleverbota")
          
def setup(client):
    client.add_cog(Administracja(client))
    print("Załadowano administracja")