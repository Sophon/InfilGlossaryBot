import discord
from discord import app_commands
from discord.ext import commands
import infil_glossary
import constants
import discord_util
import utils


async def output_embed(ctx, term, glossary, author, avatar):
    item = infil_glossary.search_dictionary(glossary, utils.remove_tag(term))
    embed = discord_util.create_embed(
        title=term,
        item=item,
        color=discord.Color.blue(),
        author=author,
        avatar=avatar
    )

    await ctx.channel.send(embed=embed)


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
    async def on_ready():
        print(f"Bot is ready. Logged in as {bot.user.name}")
        try:
            synced = await bot.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(e)

    @bot.event
    async def on_message(message):
        user = bot.user
        if message.author.bot is False and user.mentioned_in(message) and len(message.content) >= len(user.mention) + 1:
            await output_embed(
                ctx=message,
                term=message.content,
                glossary=my_glossary,
                author=message.author.display_name,
                avatar=message.author.avatar.url
            )

    @bot.tree.command(name="glossary")
    @app_commands.describe(term="term to search")
    async def glossary(interaction: discord.Interaction, term: str):
        await output_embed(
            ctx=interaction,
            term=term,
            glossary=my_glossary,
            author=interaction.user.display_name,
            avatar=interaction.user.avatar.url
        )

    bot.run(constants.TOKEN)


main()

