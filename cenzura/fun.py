import discord
from discord.ext import commands
from discord import File
import random
import urllib.parse
import asyncio
import json
import os
import aiohttp
from pyfiglet import Figlet
import async_cleverbot as ac
import requests
from PIL import Image
from dblista import DBLista
import functions
import config

class Fun(commands.Cog):
    def __init__(self, client):
        self.bot = client
    
    @commands.command(description="Pokazuje ping", usage="ping")
    async def ping(self, ctx):
        if not functions.check(ctx, "fun", "ping"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `fun.ping`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
          
        await ctx.send(f"""
```
       Ping!       Pong!
 0 🏓          |             0
/|   ---------------------  /|\\
/ \\   |                 |   / \\
              {round(self.bot.latency * 1000)}ms
```
        """)
        
    @commands.command(description="Wysyła link google", usage="google (zapytanie)", aliases=["g"])
    async def google(self, ctx, *, search):
        if not functions.check(ctx, "fun", "google"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `fun.google`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
          
        embed = discord.Embed(
            colour = discord.Colour.red()
        )
          
        embed.add_field(name='Twój wynik wyszukiwania:', value=f'[{search}](https://google.com/search?q={urllib.parse.quote_plus(search)})', inline=False)
        embed.set_footer(text=f'Wywołane przez {ctx.author.id}')

        await ctx.send(embed=embed)
            
    @commands.command(description="Orzeł czy reszka", usage="coinflip")
    async def coinflip(self, ctx):
        if not functions.check(ctx, "fun", "coinflip"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `fun.coinflip`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
          
        choices = ["Orzeł", "Reszka"]
        los = random.choice(choices)
        await ctx.send(los)
        
    @commands.command(description="Losuje liczbe", usage="rnumber (od) (do)")
    async def rnumber(self, ctx, a: int, b: int):
        if not functions.check(ctx, "fun", "rnumber"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `fun.rnumber`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
          
        los = random.randint(a, b)
        await ctx.send(los)
        
    @commands.command(description="Pokazuje avatar", usage="avatar [osoba]")
    async def avatar(self, ctx, member: discord.User=None):
        if not functions.check(ctx, "fun", "avatar"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `fun.avatar`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
          
        member = member or ctx.author
          
        async with ctx.typing():
            avatar = requests.get(f"https://cdn.discordapp.com/avatars/{member.id}/{member.avatar}.png").content
            open("member.png", "wb").write(avatar)
            
            await ctx.send(file=File("member.png"))
            os.remove("member.png")
        
    @commands.command(description="Pokazuje w ilu procentach osoby sie kochają", usage="love (osoba) [osoba]", aliases=["ship"])
    async def love(self, ctx, m: discord.User, me: discord.User=None):
        if not functions.check(ctx, "fun", "love"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `fun.love`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
          
        los = random.randint(0,100)
    
        me = me or ctx.author

        los = random.randint(0, 100)
        
        async with ctx.typing():
            open("member1.png", "wb").write(requests.get(m.avatar_url).content)
            open("member2.png", "wb").write(requests.get(me.avatar_url).content)
        	
            para = Image.open("para.png")
            member1 = Image.open("member1.png")
            member2 = Image.open("member2.png")
            
            member1.thumbnail((300, 300))
            member2.thumbnail((300, 300))
            
            para.paste(member1, (360, 250))
            para.paste(member2, (890, 180))
            
            para.save("ship.png")
            
            await ctx.send(f"**{m.name}** + **{me.name}** = **{m.name[:round(len(m.name) / 2)].lower()}{me.name[round(len(me.name) / 2):].lower()}**\nIch miłość jest równa **{los}%**!", file=discord.File("ship.png"))
            os.remove("member1.png")
            os.remove("member2.png")
            os.remove("ship.png")
        
    @commands.command(description="Odpowiada na pytanie", usage="8ball (pytanie)", aliases=["8ball"])
    async def _8ball(self, ctx, *, arg):
        if not functions.check(ctx, "fun", "8ball"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `fun.8ball`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
          
        answer = random.choice("Tak, Nie, Możliwe że tak, Możliwe że nie, Możliwe lecz nie wiem, Raczej tak, Raczej nie, Oczywiście że tak, Oczywiście że nie, Na pewno tak, Na pewno nie".split(", "))
        await ctx.send(f":8ball: | **{answer}**")
   
    @commands.command(description="Losuje tekst z podanych", usage="rchoice (a) | (b) | (c) itd.")
    async def rchoice(self, ctx, *, arg):
        if not functions.check(ctx, "fun", "rchoice"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `fun.rchoice`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
          
        wybory = arg.split(" | ")
        los = random.choice(wybory)
        e = discord.Embed(description=los, color=discord.Color.red())
        e.set_footer(text=f"Wywołane przez {ctx.author.id}")
        await ctx.send(embed=e)
        
    @commands.command(description="Pokazuje ikone serwera", usage="servericon")
    async def servericon(self, ctx):
        if not functions.check(ctx, "fun", "servericon"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `fun.servericon`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
            
        async with ctx.typing():
            icon = requests.get(f"{ctx.author.guild.icon_url}?height=100&width=100").content
            open("icon.png", "wb").write(icon)
            await ctx.send(file=File("icon.png"))
            os.remove("icon.png")
        
    @commands.command(description="Uderza osobe", usage="slap (osoba)")
    async def slap(self, ctx, member: discord.User):
        if not functions.check(ctx, "fun", "slap"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `fun.slap`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
  
        async with ctx.typing():
            img1 = requests.get("https://nekos.life/api/v2/img/slap").json()
            img2 = requests.get(img1["url"]).content
            open("slap.gif", "wb").write(img2)
            await ctx.send(f"**{ctx.author.name}** uderzył **{member.name}**!", file=File("slap.gif"))
            os.remove("slap.gif")
                    
    @commands.command(description="Całuje osobe", usage="kiss (osoba)")
    async def kiss(self, ctx, member: discord.User):
        if not functions.check(ctx, "fun", "kiss"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `fun.kiss`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
          
        async with ctx.typing():
            img1 = requests.get("https://nekos.life/api/kiss").json()
            img2 = requests.get(img1["url"]).content
            open("kiss.gif", "wb").write(img2)
            await ctx.send(f"**{ctx.author.name}** pocałował **{member.name}**!", file=File("kiss.gif"))
            os.remove("kiss.gif")
                    
    @commands.command(description="Przytula osobe", usage="hug (osoba)")
    async def hug(self, ctx, member: discord.User):
        if not functions.check(ctx, "fun", "hug"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `fun.hug`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
          
        async with ctx.typing():
            img1 = requests.get("https://nekos.life/api/hug").json()
            img2 = requests.get(img1["url"]).content
            open("hug.gif", "wb").write(img2)
            await ctx.send(f"**{ctx.author.name}** przytulił **{member.name}**!", file=File("hug.gif"))
            os.remove("hug.gif")

    @commands.command(description="Pokazuje losowe zdjęcie kota", usage="cat")
    async def cat(self, ctx):
        if not functions.check(ctx, "fun", "cat"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `fun.cat`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
          
        async with ctx.typing():
            img1 = requests.get("https://some-random-api.ml/img/cat").json()
            img2 = requests.get(img1["link"]).content
                
            open("cat.png", "wb").write(img2)
            await ctx.send(file=File("cat.png"))
            os.remove("cat.png")

    @commands.command(description="Pokazuje losowe zdjęcie psa", usage="dog")
    async def dog(self, ctx):
        if not functions.check(ctx, "fun", "dog"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `fun.dog`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
                
        async with ctx.typing():
            img1 = requests.get("https://some-random-api.ml/img/dog").json()
            img2 = requests.get(img1["link"]).content
                
            open("dog.png", "wb").write(img2)
            await ctx.send(file=File("dog.png"))
            os.remove("dog.png")

    @commands.command(description="Generuje tekst w ascii", usage="ascii (tekst)")
    async def ascii(self, ctx, *, arg):
        if not functions.check(ctx, "fun", "ascii"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `fun.ascii`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
          
        await ctx.send("```" + Figlet().renderText(arg) + "```")

    @commands.command(description="Pokazuje losowe zdjęcie pandy", usage="panda")
    async def panda(self, ctx):
        if not functions.check(ctx, "fun", "panda"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `fun.panda`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
                
        async with ctx.typing():
            img1 = requests.get("https://some-random-api.ml/img/panda").json()
            img2 = requests.get(img1["link"]).content
                
            open("panda.png", "wb").write(img2)
            await ctx.send(file=File("panda.png"))
            os.remove("panda.png")
                
    @commands.command(description="Rozmowa z cleverbotem (tylko angielski)", usage="cleverbot (tekst)", aliases=["cb"])
    async def cleverbot(self, ctx, *, arg):
        if not functions.check(ctx, "fun", "cleverbot"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `fun.cleverbot`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
      
        cb = ac.Cleverbot(config.cleverbot)
        async with ctx.typing():
            response = await cb.ask(arg)
            await ctx.send(response.text)
            
    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot:
            return
          
        with open("cleverbot.json", "r") as f:
            cleverbot = json.load(f)
            
            if str(msg.guild.id) in cleverbot:
                if msg.channel.id == cleverbot[str(msg.guild.id)]:
                    cb = ac.Cleverbot(config.cleverbot)
                    async with msg.channel.typing():
                        response = await cb.ask(msg.content)
                        await msg.channel.send(response.text)

    @commands.command(description="Zabawa w zgadywanie nicku po avatarze", usage="whois", aliases=["ktoto", "who"])
    async def whois(self, ctx):
        if not functions.check(ctx, "fun", "whois"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `fun.whois`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
          
        def check(m):
            return m.channel == ctx.channel and m.author.id != 705552952600952960

        w = []

        for m in ctx.guild.members:
            w.append(m.name)
        
        los = random.choice(w)

        for member in ctx.guild.members:
            if member.name == los:
                e=discord.Embed(title="Kto to jest", color=member.color)
                e.set_image(url=member.avatar_url)
                
                await ctx.send(embed=e)

                try:
                    msg = await self.bot.wait_for("message", check=check, timeout=10.0)
                    
                    if msg.author.bot:
                        return
                        
                    if msg.content == los:
                        return await ctx.send(f"Tak, to jest awatar osoby `{los}`!".replace("@", "@\u200b"))

                    await ctx.send(f"Nie, to nie `{msg.content}` tylko `{los}`. Koniec gry".replace("@", "@\u200b"))

                except asyncio.TimeoutError:
                    await ctx.send("Nikt nie zgadł na czas.")
        
    @commands.command(description="Pokazuje w ilu procentach jest sie gejem", usage="howgay [osoba]")
    async def howgay(self, ctx, member: discord.User=None):
        if not functions.check(ctx, "fun", "howgay"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `fun.howgay`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
          
        member = member or ctx.author
            
        await ctx.send(f"{member.name} jest gejem w {random.randint(0, 100)}%!")
        
    @commands.command(description="Wysyła obrazek \"Achievement Get!\"", usage="achievement (tekst)", aliases=["mc"])
    async def achievement(self, ctx, *, arg):
        if not functions.check(ctx, "fun", "achievement"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `fun.achievement`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)
          
        if len(arg) > 23:
            return await ctx.send("Wiadomość przekroczyła limit znaków (`limit 23`)")
        
        async with ctx.typing():
            arg = arg.replace(" ", "+").replace("ś", "s").replace("ę", "e").replace("ż", "z").replace("ź", "z").replace("ł", "l").replace("ó", "o").replace("ą", "a").replace("ć", "c").replace("Ś", "S").replace("Ę", "E").replace("Ż", "Z").replace("Ź", "Z").replace("Ł", "L").replace("Ó", "O").replace("Ą", "A").replace("Ć", "C")
            img = requests.get(f"https://minecraftskinstealer.com/achievement/{random.randint(1, 40)}/Achievement+Get%21/{arg}").content
            open("achievement.png", "wb").write(img)
            await ctx.send(file=File("achievement.png"))
            os.remove("achievement.png")
    
def setup(client):
    client.add_cog(Fun(client))
    print("Załadowano fun")
