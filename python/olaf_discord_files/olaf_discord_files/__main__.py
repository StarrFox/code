import os
import asyncio

import discord
import dotenv

dotenv.load_dotenv()

wizspoil = discord.Object(id=1015677559020724264)
token = os.environ["DISCORD_TOKEN"]


class OlafExample(discord.Client):
    async def setup_hook(self):
        command_tree.copy_global_to(guild=wizspoil)
        await command_tree.sync(guild=wizspoil)


client = OlafExample(intents=discord.Intents.all())
command_tree = discord.app_commands.CommandTree(client)


@command_tree.command()
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(
        "content",
        file=discord.File("to_send.txt")
        )


@command_tree.context_menu()
async def clickme(interaction: discord.Interaction, message: discord.Message):
    await interaction.response.send_message(
        f"Hello {message.id=}",
        file=discord.File("to_send.txt")
        )


def main():
    client.run(token)


if __name__ == "__main__":
    main()
