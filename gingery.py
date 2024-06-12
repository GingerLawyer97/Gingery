import os
import discord
from discord.ext import commands
import random
from random import randrange
import time
import asyncio

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix=['!'], intents=intents)


@client.event
async def on_ready():
    print('Gingery has connected to Discord!')
    await client.change_presence(status=discord.Status.idle,
                                 activity=discord.Activity(
                                     type=discord.ActivityType.listening,
                                     name="!help"))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Help Command
    if message.content.startswith('!help'):
        print("Help Command Executed by " + str(message.author))
        embedvar = discord.Embed(
            title="========= HELP =========",
            description="List of Commands to use the Bot:")
        embedvar.add_field(name="`!coinflip`", value="- Flip's a Coin.", inline = False)
        embedvar.add_field(name="`!rolladice`", value="- Roll's a Dice.", inline = False)
        embedvar.add_field(name="`!rps <rock/paper/scissors>`", value="- Plays Rock, Paper, Scissors with the Bot.", inline = False)
        embedvar.add_field(name="`!highlow`", value="- Plays a Number Guessing game with the Bot.", inline = False)
        embedvar.add_field(name="`!scramble`", value="- Plays a Word Scramble game with the Bot.", inline = False)
        await message.channel.send(embed=embedvar)

    # Roll a Dice Command
    if message.content.startswith('!rolladice'):
        print("Rolladice Command Executed by " + str(message.author))
        radnum = randrange(0, 7)
        await message.channel.send("The Number is... ")
        time.sleep(1)
        await message.channel.send(radnum)

    # Coin Flip Command
    if message.content.startswith('!coinflip'):
        print("Coinflip Command Executed by " + str(message.author))
        coinflip = randrange(-1, 2)
        await message.channel.send("Flipping... ")
        time.sleep(2)
        if coinflip == 1:
            await message.channel.send("Heads!")
        else:
            await message.channel.send("Tails!")

    # Rock Paper Scissors Command
    if message.content.startswith('!rps'):
        print("Rock Paper Scissors Command Executed by " + str(message.author))
        if message.content == '!rps':
            return
        else:
            choices = ['rock', 'paper', 'scissors']
            user_choice = message.content.split(' ')[1].lower()  # Extract user's choice

            if user_choice not in choices:
                await message.channel.send('Invalid choice! Please choose either rock, paper, or scissors.')
                return

            bot_choice = random.choice(choices)

            if user_choice == bot_choice:
                await message.channel.send(f'Both chose {user_choice}. It\'s a tie!')
            elif (user_choice == 'rock' and bot_choice == 'scissors') or \
                (user_choice == 'paper' and bot_choice == 'rock') or \
                (user_choice == 'scissors' and bot_choice == 'paper'):
                await message.channel.send(f'You chose {user_choice} and I chose {bot_choice}. You win!')
            else:
                await message.channel.send(f'You chose {user_choice} and I chose {bot_choice}. I win!')

    # HighLow Command
    if message.content.startswith('!highlow'):
        print("HighLow Command Executed by " + str(message.author))
        number = random.randint(1, 100) # Generate a random number between 1 and 100

        await message.channel.send('I have chosen a number between 1 and 100. Try to guess it! You have 7 attempts.')

        def check(msg):
            return msg.author == message.author and msg.channel == message.channel

        # Allow the user to guess the number within 7 attempts
        for _ in range(7):
            try:
                guess = await client.wait_for('message', check=check, timeout=30)
                guess = int(guess.content)

                if guess < number:
                    await message.channel.send('Too low! Try again.')
                elif guess > number:
                    await message.channel.send('Too high! Try again.')
                else:
                    await message.channel.send('Congratulations! You guessed it right!')
                    return
            except ValueError:
                await message.channel.send('Invalid input! Please enter a number.')
            except asyncio.TimeoutError:
                await message.channel.send('Time\'s up! You didn\'t guess the number in time. The number was {}.'.format(number))
                return

        await message.channel.send('You have used all your attempts. The number was {}.'.format(number))

    # Word Scramble Command
    print("Word Scramble Command Executed by " + str(message.author))
    if message.author == client.user:
            return

    if message.content.startswith('!scramble'):
        WORDS = ['python', 'discord', 'programming', 'bot', 'server', 'message', 'channel', 'role']

        word = random.choice(WORDS)
        scrambled_word = ''.join(random.sample(word, len(word)))
        await message.channel.send(f'Unscramble this word: **{scrambled_word}**')

        def check(m):
            return m.author == message.author and m.channel == message.channel

        try:
            user_guess = await client.wait_for('message', check=check, timeout=15)
        except asyncio.TimeoutError:
            await message.channel.send('Time is up! You took too long to answer.')
            return

        if user_guess.content.lower() == word:
            await message.channel.send(f'Congratulations {message.author.mention}! You guessed the word correctly.')
        else:
            await message.channel.send(f'Sorry {message.author.mention}, the correct word was: **{word}**.')

token = os.environ['TOKEN']
client.run(token)