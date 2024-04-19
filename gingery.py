import os
import discord
from discord.ext import commands
import random
from random import randrange
import json
import time

os.chdir("C:\\Users\\parmo\\Documents\\GingeryPy")

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix=['!'], intents=intents)

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('with your mom'))
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Help Command
    if message.content.startswith('!help'):
        await message.channel.send(">>>>>> **HELP** <<<<<<\n\n*List of Commands:*\n\n> `!coinflip` - Flips a Coin!\n> `!rolladice` - Rolls a Dice!\n> `!yesno` - Says either Yes or No.")
    
    # Roll a Dice Command    
    if message.content.startswith('!rolladice'):
        radnum = randrange(0,7) 
        await message.channel.send("The Number is... ")
        time.sleep(1)
        await message.channel.send(radnum)

    # Coin Flip Command
    if message.content.startswith('!coinflip'):
        coinflip = randrange(-1,2)
        await message.channel.send("FLipping... ")
        time.sleep(2)
        if coinflip == 1:
            await message.channel.send("Heads!")
        else:
            await message.channel.send("Tails!")

    

client.run("MTIyNjQ2NzAzODExMzgyODg4NA.GL_kq4.Qvb9L5iXPzQC5cvCdGfeDpTQ7cj9EM5xi6eq8g")