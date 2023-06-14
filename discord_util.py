import discord
import utils


def create_embed(title, item, color, author, avatar):
    embed = discord.Embed(
        title=title,
        description=item["def"],
        color=color
    )
    embed.set_author(name=author, icon_url=avatar)

    if item["games"]:
        embed.add_field(name="Games", value=item["games"], inline=True)

    if item["altterm"]:
        embed.add_field(name="Synonyms", value=item["altterm"], inline=True)

    embed.add_field(name="Source", value=utils.create_source(searched_term=title), inline=False)

    return embed



