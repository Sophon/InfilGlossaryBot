import threading

import discord
from discord.ext import commands
import infil_glossary
import constants
import discord_util
import utils


async def output(message, glossary):
    term = utils.remove_tag(message.content)
    item = infil_glossary.search_dictionary(glossary, term)
    embed = discord_util.create_embed(
        title=term,
        item=item,
        color=discord.Color.blue(),
        author=message.author.display_name,
        avatar=message.author.avatar.url
    )
    await message.channel.send(embed=embed)


def main():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(
        command_prefix=commands.when_mentioned,
        intents=intents,
        activity=discord.Game(name="@me [TERM]")
    )
    my_glossary = infil_glossary.get_full_glossary()

    @bot.event
    async def on_message(message):
        user = bot.user
        if message.author.bot is False and user.mentioned_in(message) and len(message.content) >= len(user.mention) + 1:
            await output(message, my_glossary)

    bot.run(constants.TOKEN)


main()

