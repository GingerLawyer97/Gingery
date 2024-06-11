import os
import discord
from discord.ext import commands
import random
from random import randrange
import json
import time
import asyncio

os.chdir("C:\\Users\\parmo\\Documents\\GingeryPy")

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix=['!'], intents=intents)

@client.event
async def on_ready():
    print('GingeryPy has connected to Discord!')
    await client.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.listening, name="!help"))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Help Command
    if message.content.startswith('!help'):
        embedvar = discord.Embed(title=">>>> HELP <<<<", description="List of Commands to use the Bot:")
        embedvar.add_field(name="`!coinflip`", value="- Flip's a Coin.")
        embedvar.add_field(name="`!rolladice`", value="- Roll's a Dice.")
    
    # Roll a Dice Command    
    if message.content.startswith('!rolladice'):
        radnum = randrange(0,7) 
        await message.channel.send("The Number is... ")
        time.sleep(1)
        await message.channel.send(radnum)

    # Coin Flip Command
    if message.content.startswith('!coinflip'):
        coinflip = randrange(-1,2)
        await message.channel.send("Flipping... ")
        time.sleep(2)
        if coinflip == 1:
            await message.channel.send("Heads!")
        else:
            await message.channel.send("Tails!")
            
client.run("")
