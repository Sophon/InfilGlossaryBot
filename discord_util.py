import discord


def create_embed(title, item, color, author, avatar):
    embed = discord.Embed(
        title=title,
        description=item["def"],
        color=color
    )
    embed.set_author(name=author, icon_url=avatar)

    embed.add_field(name="Games", value=item["games"], inline=True)

    return embed



