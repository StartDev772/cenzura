import json

def check(ctx, category, cmd):
    rank = ctx.author.top_role.name
    with open("sranks.json", "r") as f2:
        sranks = json.load(f2)
        
        if not rank in sranks[str(ctx.guild.id)]:
            rank = "@everyone"
          
    return ctx.author.guild_permissions.administrator or sranks[str(ctx.guild.id)][rank][category][cmd]