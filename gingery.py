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
        name="help",
        description="Shows all the commands for the Bot"
)

async def help(interaction):
    await interaction.response.send_message("List of Commands:\n1. /hello\n2. /rolladice\n3. /yesorno\n4. /flipacoin")

@tree.command(
        name="highlow",
        description="Guess the Number"
)

async def highlow(interaction):
    highlownum = randrange(0,101)
    print(highlownum)
    tries = 10
    await interaction.response.send_message("Guessing a Number...")
    time.sleep(2)
    await interaction.followup.send("Try guessing the Number I Guessed. You have 10 tries.")
    async def on_message(message):
        if message.content.startswith(highlownum):
            print("guessed number")
            await message.channel.send("You Guessed the Number!")

@tree.command(
        name="flipacoin",
        description="Flip's a Coin"
)

async def flipacoin(interaction):
    coinflip = randrange(-1,2)
    await interaction.response.send_message("Flipping a Coin...")
    time.sleep(2)
    if coinflip == 1:
        await interaction.followup.send("Heads!")
    else:
        await interaction.followup.send("Tails!")

@tree.command(
        name="yesorno",
        description="Says either Yes or No"
)

async def yesorno(interaction):
    yesno = randrange(-1,2)
    if yesno == 1:
        await interaction.response.send_message("Yes")
    else:
        await interaction.response.send_message("No")

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