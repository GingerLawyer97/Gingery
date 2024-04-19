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

client = commands.Bot(command_prefix=['!'])

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

    # Yes or No Command
    if message.content.startswith('!yesno'):
        yesno = int(randrange(-1,2))
    if yesno == 1:
        await message.channel.send("Yes")
    else:
        await message.channel.send("No")

@client.command()
async def coinflip(ctx):
    coinflip = randrange(-1,2)
    await message.channel.send("FLipping... s")
    time.sleep(2)
    if coinflip == 1:
        await ctx.send("Heads!")
    else:
        await ctx.send("Tails!")

    

client.run(os.getenv('TOKEN'))