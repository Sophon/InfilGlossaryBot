import discord
import string_utils
from discord.ext import commands


def create_embed(title, item, color, author, avatar):
    tags, string = string_utils.search_and_replace(item["def"])

    embed = discord.Embed(
        title=title,
        description=string,
        color=color
    )
    embed.set_author(name=author, icon_url=avatar)

    if 'games' in item:
        embed.add_field(name="Games", value=item["games"], inline=True)

    if 'altterm' in item:
        embed.add_field(name="Synonyms", value=item["altterm"], inline=True)

    if 'video' in item:
        link = string_utils.create_gfycat_link(item["video"][0])
        embed.add_field(name="Gif", value=string_utils.wrap_link(link), inline=False)

    embed.add_field(name="Source", value=string_utils.create_source(searched_term=title), inline=False)

    return embed, create_action_row_from_tags(tags)


def create_action_row_from_tags(tags):
    buttons = []
    for tag in tags:
        buttons.append(discord.ui.Button(label=tag))

    return buttons


