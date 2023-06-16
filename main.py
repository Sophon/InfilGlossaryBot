import discord
from discord import app_commands
from discord.ext import commands
import constants
import discord_client


def main():
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


main()
