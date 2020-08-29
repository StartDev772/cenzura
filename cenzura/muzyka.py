import discord
from discord.ext import commands
import asyncio
import itertools
import sys
import traceback
from async_timeout import timeout
from functools import partial
from youtube_dl import YoutubeDL
import json
import functions

ytdlopts = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpegopts = {
    'before_options': '-nostdin',
    'options': '-vn'
}

ytdl = YoutubeDL(ytdlopts)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, requester):
        super().__init__(source)
        self.requester = requester

        self.title = data.get('title')
        self.web_url = data.get('webpage_url')

    def __getitem__(self, item: str):
        return self.__getattribute__(item)

    @classmethod
    async def create_source(cls, ctx, search: str, *, loop, download=False):
        loop = loop or asyncio.get_event_loop()

        to_run = partial(ytdl.extract_info, url=search, download=download)
        data = await loop.run_in_executor(None, to_run)

        if 'entries' in data:
            data = data['entries'][0]

        await ctx.send(f'Dodano `{data["title"]}` do kolejki')

        if download:
            source = ytdl.prepare_filename(data)
        else:
            return {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title']}

        return cls(discord.FFmpegPCMAudio(source), data=data, requester=ctx.author)

    @classmethod
    async def regather_stream(cls, data, *, loop):
        loop = loop or asyncio.get_event_loop()
        requester = data['requester']

        to_run = partial(ytdl.extract_info, url=data['webpage_url'], download=False)
        data = await loop.run_in_executor(None, to_run)

        return cls(discord.FFmpegPCMAudio(data['url']), data=data, requester=requester)


class MusicPlayer:
    __slots__ = ('bot', '_guild', '_channel', '_cog', 'queue', 'next', 'current', 'np', 'volume')

    def __init__(self, ctx):
        self.bot = ctx.bot
        self._guild = ctx.guild
        self._channel = ctx.channel
        self._cog = ctx.cog

        self.queue = asyncio.Queue()
        self.next = asyncio.Event()

        self.np = None
        self.volume = .5
        self.current = None

        ctx.bot.loop.create_task(self.player_loop())

    async def player_loop(self):
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            self.next.clear()

            try:
                async with timeout(300):
                    source = await self.queue.get()
            except asyncio.TimeoutError:
                return self.destroy(self._guild)

            if not isinstance(source, YTDLSource):
                try:
                    source = await YTDLSource.regather_stream(source, loop=self.bot.loop)
                except Exception as e:
                    await self._channel.send(f'Wystąpił nieoczekiwany błąd!')
                    continue

            source.volume = self.volume
            self.current = source

            self._guild.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
            self.np = await self._channel.send(f'Teraz gram `{source.title}`')
            await self.next.wait()

            source.cleanup()
            self.current = None

            try:
                await self.np.delete()
            except discord.HTTPException:
                pass

    def destroy(self, guild):
        return self.bot.loop.create_task(self._cog.cleanup(guild))

class Muzyka(commands.Cog):
    __slots__ = ('bot', 'players')

    def __init__(self, bot):
        self.bot = bot
        self.players = {}

    async def cleanup(self, guild):
        try:
            await guild.voice_client.disconnect()
        except AttributeError:
            pass

        try:
            del self.players[guild.id]
        except KeyError:
            pass

    async def __local_check(self, ctx):
        if not ctx.guild:
            raise commands.NoPrivateMessage
        return True

        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    def get_player(self, ctx):
        try:
            player = self.players[ctx.guild.id]
        except KeyError:
            player = MusicPlayer(ctx)
            self.players[ctx.guild.id] = player

        return player

    @commands.command(description="Bot dołącza na kanał głosowy", usage="join")
    async def join(self, ctx):
        if not functions.check(ctx, "muzyka", "join"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `muzyka.join`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)

        channel = ctx.author.voice.channel

        vc = ctx.voice_client

        if vc:
            if vc.channel.id == channel.id:
                return
            
            await vc.move_to(channel)
        else:
            await channel.connect()

        try:
            await ctx.guild.me.edit(deafen=True)
        except:
            pass

        await ctx.send('Dołączyłem na kanał')

    @commands.command(description="Zaczyna grać muzyke", usage="play (muzyka)")
    async def play(self, ctx, *, search: str):
        if not functions.check(ctx, "muzyka", "play"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `muzyka.play`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)

        await ctx.trigger_typing()

        vc = ctx.voice_client

        if not vc:
            await ctx.invoke(self.join)

        player = self.get_player(ctx)
        source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop, download=False)

        await player.queue.put(source)

    @commands.command(description="Pomija muzyke", usage="skip")
    async def skip(self, ctx):
        if not functions.check(ctx, "muzyka", "skip"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `muzyka.skip`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)

        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('Na obecną chwile nic nie gram')

        if vc.is_paused():
            pass
        elif not vc.is_playing():
            return

        vc.stop()
        await ctx.send(f'Pominięto muzyke')

    @commands.command(description="Pokazuje kolejke", usage="queue")
    async def queue(self, ctx):
        if not functions.check(ctx, "muzyka", "queue"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `muzyka.queue`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)

        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('Nie jestem na żadnym kanale!')

        player = self.get_player(ctx)
        if player.queue.empty():
            return await ctx.send('Nie ma żadnych piosenek w kolejce')

        upcoming = list(itertools.islice(player.queue._queue, 0, 5))

        fmt = '\n'.join(f'[{_["title"]}]({_["webpage_url"]})' for _ in upcoming)
        embed = discord.Embed(title="Kolejka na tym serwerze:", description=fmt, color=discord.Color.red())

        await ctx.send(embed=embed)

    @commands.command(description="Pokazuje aktualnie graną muzyke", usage="nowplaying", aliases=["np"])
    async def nowplaying(self, ctx):
        if not functions.check(ctx, "muzyka", "nowplaying"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `muzyka.nowplaying`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)

        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('Nie jestem na żadnym kanale!')

        player = self.get_player(ctx)
        if not player.current:
            return await ctx.send('Na obecną chwile nic nie gra!')

        try:
            await player.np.delete()
        except discord.HTTPException:
            pass

        player.np = await ctx.send(f'Teraz gram `{vc.source.title}`')

    @commands.command(description="Ustawia głośność", usage="volume (głośność)")
    async def volume(self, ctx, *, vol: float):
        if not functions.check(ctx, "muzyka", "volume"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `muzyka.volume`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)

        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('Nie jestem na żadnym kanale!')

        player = self.get_player(ctx)

        if vc.source:
            vc.source.volume = vol / 100

        player.volume = vol / 100
        await ctx.send(f'Ustawiono głośność na {vol}%')

    @commands.command(description="Bot wychodzi z kanału głosowego", usage="leave", aliases=["stop"])
    async def leave(self, ctx):
        if not functions.check(ctx, "muzyka", "leave"):
            e = discord.Embed(title="Nie masz uprawnień", description="Nie posiadasz uprawnień `muzyka.leave`", color=discord.Color.red())
            e.set_footer(text="Uprawnienie administratora może edytować permisje do różnych ról (komenda perm)")
            return await ctx.send(embed=e)

        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('Nie jestem na żadnym kanale!')

        await self.cleanup(ctx.guild)
        await ctx.send("Rozłączyłem sie z kanału")

def setup(bot):
    bot.add_cog(Muzyka(bot))
    print("Załadowano muzyka")