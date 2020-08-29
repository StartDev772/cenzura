import discord
from discord.ext import commands, tasks
import random
import json
import os
import config

def get_prefix(client, message):
    if not message.guild:
        return commands.when_mentioned_or(";")(client, message)

    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    if str(message.guild.id) not in prefixes:
        return commands.when_mentioned_or(";")(client, message)

    prefix = prefixes[str(message.guild.id)]
    return commands.when_mentioned_or(prefix)(client, message)

client = commands.AutoShardedBot(command_prefix = get_prefix)
client.remove_command('help')
os.environ["JISHAKU_NO_UNDERSCORE"] = "true"

extensions = ["fun", "admin", "muzyka", "lvls", "inne", "sranks", "info", "pomoc", "dblistatest", "developerskie", "eventy", "status", "handler", "jishaku"]
[client.load_extension(cog) for cog in extensions]

@client.event
async def on_ready():
    print("ONLINE")
    
client.run(config.token)