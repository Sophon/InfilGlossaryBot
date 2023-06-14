import threading

import discord
from discord.ext import commands
import infil_glossary
import constants
import logger
import discord_util


def main():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='!', intents=intents, activity=discord.Game(name="!glossary [TERM]"))
    my_glossary = infil_glossary.get_full_glossary()

    @bot.command()
    async def glossary(ctx, *, message):
        item = infil_glossary.search_dictionary(my_glossary, message)
        embed = discord_util.create_embed(
            title=message,
            item=item,
            color=discord.Color.blue(),
            author=ctx.author.display_name,
            avatar=ctx.author.avatar.url
        )
        await ctx.send(embed=embed)

    bot.run(constants.TOKEN)


function = infil_glossary.search_dictionary
rate = constants.RATE_OF_LOGGING_IN_SECONDS
log_to_file = True
filename = "log.txt"
background_thread = threading.Thread(target=logger.log_call_count_of, args=(function, rate, log_to_file, filename,))

background_thread.start()
main()

