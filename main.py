import discord
from discord import app_commands
from discord.ext import commands
import infil_glossary
import constants
import discord_util
import string_utils
import discord_client


def output_embed(term, glossary, author, avatar):
    term = string_utils.remove_mention_tag(term)
    item = infil_glossary.search_dictionary(glossary, term)
    return discord_util.create_embed(
        title=term,
        item=item,
        color=discord.Color.blue(),
        author=author,
        avatar=avatar
    )


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

    # TAG COMMAND
    @bot.event
    async def on_message(message):
        user = bot.user
        if message.author.bot is False and user.mentioned_in(message) and len(message.content) >= len(user.mention) + 1:
            embed, action_row = output_embed(
                term=message.content,
                glossary=my_glossary,
                author=message.author.display_name,
                avatar=message.author.avatar.url
            )
            await message.channel.send(embed=embed, components=action_row)

    # SLASH COMMAND
    @bot.tree.command(name="glossary")
    @app_commands.describe(term="term to search")
    async def glossary(interaction: discord.Interaction, term: str):
        embed, action_row = output_embed(
            term=term,
            glossary=my_glossary,
            author=interaction.user.display_name,
            avatar=interaction.user.avatar.url
        )
        await interaction.response.send_message(embed=embed, components=action_row)

    bot.run(constants.TOKEN)


def main_2():
    intents = discord.Intents.default()
    client = discord_client.DiscordClient(
        command_prefix=commands.when_mentioned,
        intents=intents,
        activity=discord.Game(name="@me [TERM]")
    )

    @client.tree.command(name="glossary")
    @app_commands.describe(term="term to search")
    async def glossary(interaction: discord.Interaction, term: str):
        embed = client.embed_from_interaction(
            query=term,
            author_name=interaction.user.display_name,
            author_avatar=interaction.user.avatar.url
        )

        await interaction.response.send_message(embed=embed)

    client.run(constants.TOKEN)


main_2()
