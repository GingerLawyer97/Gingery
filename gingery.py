import time
import random
from random import randrange
import discord
from discord import app_commands

intents = discord.Intents.default()
client = discord.Client(intents=intents)

intents.message_content = True
tree = app_commands.CommandTree(client)

# Add the guild ids in which the slash command will appear.
# If it should be in all, remove the argument, but note that
# it will take some time (up to an hour) to register the
# command if it's for all guilds.
# guild=discord.Object(id=12417128931)

@tree.command(
        name="rolladice",
        description="Rolls a Dice"
)

async def rolladice(interaction):
    radnum = randrange(0,7) 
    await interaction.response.send_message("The Number is... ")
    time.sleep(1)
    await interaction.followup.send(radnum)

@tree.command(
    name="hello",
    description="Say Hello to the Bot",
)
async def hello(interaction):
    await interaction.response.send_message("Hello!")

@client.event
async def on_ready():
    await tree.sync()
    print(f'We have logged in as {client.user}')

client.run('MTIyNjQ2NzAzODExMzgyODg4NA.GL_kq4.Qvb9L5iXPzQC5cvCdGfeDpTQ7cj9EM5xi6eq8g')