import discord


def create_embed(term, message, color, author, avatar):
    embed = discord.Embed(
        title=term,
        description=message,
        color=color
    )
    embed.set_author(name=author, icon_url=avatar)
    return embed



