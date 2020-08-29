import ast
import discord
from discord.ext import commands
import json
import asyncio
import config

def insert_returns(body):
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)
        
class Developerskie(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.command(description="Wywołuje skrypt", usage="eval (kod)")
    async def eval(self, ctx, *, cmd):
        if ctx.author.id in config.owners:
            try:
                fn_name = "_eval_expr"

                cmd = cmd.strip("` ")

                cmd = "\n".join(f"    {i}" for i in cmd.splitlines())

                body = f"async def {fn_name}():\n{cmd}"

                parsed = ast.parse(body)
                body = parsed.body[0].body

                insert_returns(body)

                env = {
                    'bot': ctx.bot,
                    'discord': discord,
                    'commands': commands,
                    'ctx': ctx,
                    '__import__': __import__
                }

                exec(compile(parsed, filename="<ast>", mode="exec"), env)

                result = (await eval(f"{fn_name}()", env))
                msg = await ctx.send(result)
            except Exception as e:
                msg = await ctx.send(f"```{e}```")
                
            def check(r, m):
                return m == ctx.author and str(r.emoji) == "⏹️" and r.message.id == msg.id
            
            try:
                await msg.add_reaction("⏹️")
                await self.bot.wait_for("reaction_add", check=check, timeout=120)
                return await msg.delete()
            except:
                return
          
        e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `developerskie.eval`", color=discord.Color.red())
        await ctx.send(embed=e)

    @commands.command(description="Ładuje cog", usage="load (cog)")
    async def load(self, ctx, *, arg):
        if ctx.author.id in config.owners:
            try:
                self.bot.load_extension(arg)
                return await ctx.send(f"Załadowano `{arg}`")
            except Exception as e:
                return await ctx.send(f"```{e}```")
        
        e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `developerskie.load`", color=discord.Color.red())
        await ctx.send(embed=e)
            
    @commands.command(description="Wyłącza cog", usage="unload (cog)")
    async def unload(self, ctx, *, arg):
        if ctx.author.id in config.owners:
            try:
                self.bot.unload_extension(arg)
                return await ctx.send(f"Wyłączono `{arg}`")
            except Exception as e:
                return await ctx.send(f"```{e}```")

        e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `developerskie.unload`", color=discord.Color.red())
        await ctx.send(embed=e)

    @commands.command(description="Wyłącza i włącza cog", usage="reload (cog)")
    async def reload(self, ctx, *, arg):
        if ctx.author.id in config.owners:
            try:
                self.bot.reload_extension(arg)
                return await ctx.send(f"Przeładowano `{arg}`")
            except Exception as e:
                return await ctx.send(f"```{e}```")

        e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `developerskie.reload`", color=discord.Color.red())
        await ctx.send(embed=e)

    @commands.command(description="Sortuje pomoc", usage="sorthelp")
    async def sorthelp(self, ctx):
        if ctx.author.id in config.owners:
            try:
                extensions = ["fun", "admin", "muzyka", "lvls", "inne", "sranks", "info", "pomoc", "dblistatest", "developerskie", "eventy", "status", "handler", "jishaku"]
                [self.bot.reload_extension(extension) for extension in extensions]
                return await ctx.send(f"Ułożono cogi w pomocy")
            except Exception as e:
                return await ctx.send(f"```{e}```")

        e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `developerskie.sorthelp`", color=discord.Color.red())
        await ctx.send(embed=e)
    
def setup(client):
    client.add_cog(Developerskie(client))
    print("Załadowano developerskie")