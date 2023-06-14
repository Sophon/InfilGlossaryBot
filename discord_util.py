import discord
import utils


def create_embed(title, item, color, author, avatar):
    embed = discord.Embed(
        title=title,
        description=item["def"],
        color=color
    )
    embed.set_author(name=author, icon_url=avatar)

    if 'games' in item:
        embed.add_field(name="Games", value=item["games"], inline=True)

    if 'altterm' in item:
        embed.add_field(name="Synonyms", value=item["altterm"], inline=True)

    if 'video' in item:
        link = utils.create_gfycat_link(item["video"][0])
        embed.add_field(name="Gif", value=utils.wrap_link(link), inline=False)

    embed.add_field(name="Source", value=utils.create_source(searched_term=title), inline=False)

    return embed



