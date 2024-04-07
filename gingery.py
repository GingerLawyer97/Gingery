# This example requires the 'message_content' intent.

import discord
from discord import app_commands

intents = discord.Intents.default()
client = discord.Client(intents=intents)

intents.message_content = True
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

# Add the guild ids in which the slash command will appear.
# If it should be in all, remove the argument, but note that
# it will take some time (up to an hour) to register the
# command if it's for all guilds.
@tree.command(
    name="commandname",
    description="My first application Command",
    # guild=discord.Object(id=12417128931)
)
async def first_command(interaction):
    await interaction.response.send_message("Hello!")

@client.event
async def on_ready():
    await tree.sync()
    print("Ready!")

client.run('MTIyNjQ2NzAzODExMzgyODg4NA.GZDDBi.R6Pu3j0LA0FcN8SdlzTWYua98Par-fOmOaPw0U')