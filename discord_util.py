import discord


def create_embed(term, message, color, url=""):
    embed = discord.Embed(
        title=term,
        url=url,
        description=message,
        color=color
    )
    return embed
