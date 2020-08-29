import discord
from discord.ext import commands
import json

class Sranks(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.Cog.listener()
    async def on_message(self, msg):
        with open("sranks.json", "r") as f:
            sranks = json.load(f)

            if not str(msg.guild.id) in sranks:
                sranks[str(msg.guild.id)] = {}

            if not str(msg.guild.get_role(msg.guild.id)) in sranks[str(msg.guild.id)]:
                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))] = {}
                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["fun"] = {}
                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["admin"] = {}
                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["level"] = {}
                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["glevel"] = {}
                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["inne"] = {}
                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["muzyka"] = {}

                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["fun"]["ping"] = True
                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["fun"]["ascii"] = True
                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["fun"]["cat"] = True
                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["fun"]["dog"] = True
                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["fun"]["panda"] = True
                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["fun"]["coinflip"] = True
                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["fun"]["rnumber"] = True
                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["fun"]["rchoice"] = True
                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["fun"]["love"] = True
                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["fun"]["howgay"] = True
                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["fun"]["avatar"] = True
                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["fun"]["servericon"] = True
                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["fun"]["slap"] = True
                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["fun"]["kiss"] = True
                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["fun"]["hug"] = True
                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["fun"]["8ball"] = True
                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["fun"]["google"] = True
                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["fun"]["cleverbot"] = True
                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["fun"]["whois"] = True
                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["fun"]["achievement"] = True

                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["admin"]["userinfo"] = True
                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["admin"]["serverinfo"] = True
                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["admin"]["kick"] = False
                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["admin"]["ban"] = False
                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["admin"]["warn"] = False
                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["admin"]["warns"] = False
                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["admin"]["removewarn"] = False
                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["admin"]["clearwarns"] = False
                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["admin"]["clear"] = False
                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["admin"]["set"] = False

                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["level"]["level"] = False
                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["level"]["lvlon"] = False
                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["level"]["lvloff"] = False
                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["level"]["levels"] = False

                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["glevel"]["glvlon"] = False
                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["glevel"]["glvloff"] = False

                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["inne"]["snipe"] = False
                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["inne"]["cmd"] = False

                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["muzyka"]["join"] = True
                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["muzyka"]["leave"] = True
                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["muzyka"]["play"] = True
                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["muzyka"]["queue"] = True
                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["muzyka"]["skip"] = False
                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["muzyka"]["volume"] = False
                sranks[str(msg.guild.id)][str(msg.guild.get_role(msg.guild.id))]["muzyka"]["nowplaying"] = True

        with open("sranks.json", "w") as f:
            json.dump(sranks, f, indent=4)

    @commands.command(description="Pokazuje liste uprawnień", usage="perms [rola]")
    async def perms(self, ctx, rola=None):
        rola = rola or "@everyone"
        permissions = []
        with open("sranks.json", "r") as f:
            sranks = json.load(f)

            for category in sranks[str(ctx.guild.id)][rola]:
                for command in sranks[str(ctx.guild.id)][rola][category]:
                    if sranks[str(ctx.guild.id)][rola][category][command]:
                        permissions.append("`" + command + "`")
                        
            e = discord.Embed(title=f"Permisje roli {rola}:", description=", ".join(permissions), color=discord.Color.red())
            await ctx.send(embed=e)

    @commands.group(description="Lista komend perm", usage="perm", invoke_without_command=True)
    async def perm(self, ctx):
        if ctx.author.guild_permissions.administrator:
            e = discord.Embed(title="Serwerowe rangi:", description="> `perm permlist`, `perm add (rola) (permisja)`, `perm remove (rola) (permisja)`, `perm delete (rola)`", color=discord.Color.red())
            return await ctx.send(embed=e)

        e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `sranks.perm`", color=discord.Color.red())
        await ctx.send(embed=e)

    @perm.command(description="Pokazuje liste dostępnych uprawnień w bocie", usage="perm permlist")
    async def permlist(self, ctx):
        if ctx.author.guild_permissions.administrator:
            e = discord.Embed(title="Dostępne permisje:", color=discord.Color.red())
            e.add_field(name="4Fun:", value="> `fun.ping`, `fun.ascii`, `fun.cat`, `fun.dog`, `fun.panda`, `fun.coinflip`, `fun.rnumber`, `fun.rchoice`, `fun.love`, `fun.howgay`, `fun.avatar`, `fun.servericon`, `fun.slap`, `fun.kiss`, `fun.hug`, `fun.8ball`, `fun.cleverbot`, `fun.whois`, `fun.achievement`", inline=False)
            e.add_field(name="Administracja:", value="> `admin.userinfo`, `admin.serverinfo`, `admin.kick`, `admin.ban`, `admin.warn`, `admin.warns`, `admin.removewarn`, `admin.clearwarns`, `admin.clear`, `admin.set`", inline=False)
            e.add_field(name="Muzyka:", value="> `muzyka.join`, `muzyka.play`, `muzyka.leave`, `muzyka.skip`, `muzyka.queue`, `muzyka.volume`, `muzyka.nowplaying`")
            e.add_field(name="Levele:", value="> `level.level`, `level.lvlon`, `level.lvloff`, `level.levels`", inline=False)
            e.add_field(name="Globalne levele:", value="> `glevel.glvlon`, `glevel.glvloff`", inline=False)
            e.add_field(name="Inne:", value="> `inne.snipe`, `inne.cmd`")
            return await ctx.send(embed=e)
            
        e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `sranks.perm`", color=discord.Color.red())
        await ctx.send(embed=e)

    @perm.command(description="Usuwa role z bazy danych", usage="perm delete (rola)")
    async def delete(self, ctx, name: discord.Role):
        if ctx.author.guild_permissions.administrator:
            with open("sranks.json", "r") as f:
                sranks = json.load(f)
                
                name = name.name

                del sranks[str(ctx.guild.id)][name]

            with open("sranks.json", "w") as f:
                json.dump(sranks, f, indent=4)

            return await ctx.send(f"Usunięto `{name}`")
        
        e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `sranks.perm`", color=discord.Color.red())
        await ctx.send(embed=e)

    @perm.command(description="Dodaje permisje do roli", usage="perm add (rola) (permisja)", aliases=["+"])
    async def add(self, ctx, rola: discord.Role, permission):
        if ctx.author.guild_permissions.administrator:
            with open("sranks.json", "r") as f:
                sranks = json.load(f)
                
                rola = rola.name

                if not rola in sranks[str(ctx.guild.id)]:
                    sranks[str(ctx.guild.id)][rola] = {}
                    sranks[str(ctx.guild.id)][rola]["fun"] = {}
                    sranks[str(ctx.guild.id)][rola]["admin"] = {}
                    sranks[str(ctx.guild.id)][rola]["level"] = {}
                    sranks[str(ctx.guild.id)][rola]["glevel"] = {}
                    sranks[str(ctx.guild.id)][rola]["inne"] = {}
                    sranks[str(ctx.guild.id)][rola]["muzyka"] = {}

                    sranks[str(ctx.guild.id)][rola]["fun"]["ping"] = True
                    sranks[str(ctx.guild.id)][rola]["fun"]["ascii"] = True
                    sranks[str(ctx.guild.id)][rola]["fun"]["cat"] = True
                    sranks[str(ctx.guild.id)][rola]["fun"]["dog"] = True
                    sranks[str(ctx.guild.id)][rola]["fun"]["panda"] = True
                    sranks[str(ctx.guild.id)][rola]["fun"]["coinflip"] = True
                    sranks[str(ctx.guild.id)][rola]["fun"]["rnumber"] = True
                    sranks[str(ctx.guild.id)][rola]["fun"]["rchoice"] = True
                    sranks[str(ctx.guild.id)][rola]["fun"]["love"] = True
                    sranks[str(ctx.guild.id)][rola]["fun"]["howgay"] = True
                    sranks[str(ctx.guild.id)][rola]["fun"]["avatar"] = True
                    sranks[str(ctx.guild.id)][rola]["fun"]["servericon"] = True
                    sranks[str(ctx.guild.id)][rola]["fun"]["slap"] = True
                    sranks[str(ctx.guild.id)][rola]["fun"]["kiss"] = True
                    sranks[str(ctx.guild.id)][rola]["fun"]["hug"] = True
                    sranks[str(ctx.guild.id)][rola]["fun"]["8ball"] = True
                    sranks[str(ctx.guild.id)][rola]["fun"]["google"] = True
                    sranks[str(ctx.guild.id)][rola]["fun"]["cleverbot"] = True
                    sranks[str(ctx.guild.id)][rola]["fun"]["whois"] = True
                    sranks[str(ctx.guild.id)][rola]["fun"]["achievement"] = True

                    sranks[str(ctx.guild.id)][rola]["admin"]["userinfo"] = True
                    sranks[str(ctx.guild.id)][rola]["admin"]["serverinfo"] = True
                    sranks[str(ctx.guild.id)][rola]["admin"]["kick"] = False
                    sranks[str(ctx.guild.id)][rola]["admin"]["ban"] = False
                    sranks[str(ctx.guild.id)][rola]["admin"]["warn"] = False
                    sranks[str(ctx.guild.id)][rola]["admin"]["warns"] = False
                    sranks[str(ctx.guild.id)][rola]["admin"]["removewarn"] = False
                    sranks[str(ctx.guild.id)][rola]["admin"]["clearwarns"] = False
                    sranks[str(ctx.guild.id)][rola]["admin"]["clear"] = False
                    sranks[str(ctx.guild.id)][rola]["admin"]["set"] = False

                    sranks[str(ctx.guild.id)][rola]["level"]["level"] = False
                    sranks[str(ctx.guild.id)][rola]["level"]["lvlon"] = False
                    sranks[str(ctx.guild.id)][rola]["level"]["lvloff"] = False
                    sranks[str(ctx.guild.id)][rola]["level"]["levels"] = False

                    sranks[str(ctx.guild.id)][rola]["glevel"]["glvlon"] = False
                    sranks[str(ctx.guild.id)][rola]["glevel"]["glvloff"] = False

                    sranks[str(ctx.guild.id)][rola]["inne"]["snipe"] = False
                    sranks[str(ctx.guild.id)][rola]["inne"]["cmd"] = False

                    sranks[str(ctx.guild.id)][rola]["muzyka"]["join"] = True
                    sranks[str(ctx.guild.id)][rola]["muzyka"]["leave"] = True
                    sranks[str(ctx.guild.id)][rola]["muzyka"]["play"] = True
                    sranks[str(ctx.guild.id)][rola]["muzyka"]["queue"] = True
                    sranks[str(ctx.guild.id)][rola]["muzyka"]["skip"] = False
                    sranks[str(ctx.guild.id)][rola]["muzyka"]["volume"] = False
                    sranks[str(ctx.guild.id)][rola]["muzyka"]["nowplaying"] = True

                sranks[str(ctx.guild.id)][rola][permission.split(".")[0]][permission.split(".")[1]] = True

            with open("sranks.json", "w") as f:
                json.dump(sranks, f, indent=4)

            return await ctx.send(f"Dodano permisje `{permission}` do roli `{rola}`")

        e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `sranks.perm`", color=discord.Color.red())
        await ctx.send(embed=e)

    @perm.command(description="Usuwa permisje z roli", usage="perm remove (rola) (permisja)", aliases=["-"])
    async def remove(self, ctx, rola: discord.Role, permission):
        if ctx.author.guild_permissions.administrator:
            with open("sranks.json", "r") as f:
                sranks = json.load(f)
                
                rola = rola.name

                sranks[str(ctx.guild.id)][rola][permission.split(".")[0]][permission.split(".")[1]] = False

            with open("sranks.json", "w") as f:
                json.dump(sranks, f, indent=4)

            return await ctx.send(f"Usunięto permisje `{permission}` z roli `{rola}`")

        e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `sranks.perm`", color=discord.Color.red())
        await ctx.send(embed=e)

def setup(client):
    client.add_cog(Sranks(client))
    print("Załadowano sranks")