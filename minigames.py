import discord
from discord.ext import commands
import random
from random import randrange
import time
import asyncio

trivia_questions = [
    {"question": "What is the capital of France?", "answer": "Paris"},
    {"question": "What is the largest planet in our solar system?", "answer": "Jupiter"},
    {"question": "Who painted the Mona Lisa?", "answer": "Leonardo da Vinci"},
    {"question": "What is the main ingredient in guacamole?", "answer": "Avocado"},
    {"question": "What is the chemical symbol for water?", "answer": "H2O"}
]

# Help Command
async def help_cmd(channel):
    embedvar = discord.Embed(
        title="========= HELP =========",
        description="List of Commands to use the Bot:")
    embedvar.add_field(name="`!coinflip`", value="- Flip's a Coin.", inline = False)
    embedvar.add_field(name="`!rolladice`", value="- Roll's a Dice.", inline = False)
    embedvar.add_field(name="`!rps <rock/paper/scissors>`", value="- Plays Rock, Paper, Scissors with the Bot.", inline=False)
    embedvar.add_field(name="`!highlow`", value="- Plays a Number Guessing game with the Bot.", inline=False)
    embedvar.add_field(name="`!scramble`", value="- Plays a Word Scramble game with the Bot.", inline=False)
    embedvar.add_field(name="`!trivia`", value="- Plays a Trivia game with the Bot.", inline=False)

    await channel.send(embed=embedvar)

# Roll a Dice
async def rolladice(channel):
  radnum = randrange(0, 7)
  await channel.send("The Number is... ")
  time.sleep(1)
  await channel.send(radnum)

# Flip a Coin
async def coinflip(channel):
  coinflip = randrange(-1, 2)
  await channel.send("Flipping... ")
  time.sleep(2)
  if coinflip == 1:
      await channel.send("Heads!")
  else:
      await channel.send("Tails!")

# Rock Paper Scissors
async def rps(channel, user_choice, message):
  if message.content == '!rps':
      return
  else:
    choices = ['rock', 'paper', 'scissors']
    user_choice = message.content.split(' ')[1].lower()  # Extract user's choice

    if user_choice not in choices:
        await channel.send('Invalid choice! Please choose either rock, paper, or scissors.')
        return

    bot_choice = random.choice(choices)

    if user_choice == bot_choice:
        await channel.send(f'Both chose {user_choice}. It\'s a tie!')
    elif (user_choice == 'rock' and bot_choice == 'scissors') or \
        (user_choice == 'paper' and bot_choice == 'rock') or \
        (user_choice == 'scissors' and bot_choice == 'paper'):
        await channel.send(f'You chose {user_choice} and I chose {bot_choice}. You win!')
    else:
        await channel.send(f'You chose {user_choice} and I chose {bot_choice}. I win!')

# High Low Game
async def highlow(channel, message, client, author):
    number = random.randint(1, 100) # Generate a random number between 1 and 100

    await channel.send('I have chosen a number between 1 and 100. Try to guess it! You have 7 attempts.')

    def highlow_check(msg):
        return msg.author == message.author and msg.channel == message.channel

    # Allow the user to guess the number within 7 attempts
    for _ in range(7):
        try:
            guess = await client.wait_for('message', check=highlow_check, timeout=30)
            guess = int(guess.content)

            if guess < number:
                await channel.send('Too low! Try again.')
            elif guess > number:
                await channel.send('Too high! Try again.')
            else:
                await channel.send(f'Congratulations {author}! You guessed it right!')
                return
        except ValueError:
            await channel.send('Invalid input! Please enter a number.')
        except asyncio.TimeoutError:
            await channel.send('Time\'s up! You didn\'t guess the number in time. The number was {}.'.format(number))
            return

    await channel.send('You have used all your attempts. The number was {}.'.format(number))

# Word Scramble Game
async def scramble(channel, message, client):
    WORDS = ['python', 'discord', 'programming', 'bot', 'server', 'message', 'channel', 'role']

    word = random.choice(WORDS)
    scrambled_word = ''.join(random.sample(word, len(word)))
    await channel.send(f'Unscramble this word: **{scrambled_word}**')

    def scramble_check(m):
        return m.author == message.author and m.channel == channel

    try:
        user_guess = await client.wait_for('message', check=scramble_check, timeout=15)
    except asyncio.TimeoutError:
        await channel.send('Time is up! You took too long to answer.')
        return

    if user_guess.content.lower() == word:
        await channel.send(f'Congratulations {message.author.mention}! You guessed the word correctly.')
    else:
        await channel.send(f'Sorry {message.author.mention}, the correct word was: **{word}**.')

# Trivia Game
async def trivia(channel, message, client):
    question = random.choice(trivia_questions)
    await channel.send(question["question"])

    def check(msg):
        return msg.author == message.author and msg.channel == channel

    try:
        answer = await client.wait_for('message', timeout=20.0, check=check)
    except asyncio.TimeoutError:
        await channel.send('Time\'s up! The correct answer was: {}'.format(question["answer"]))
    else:
        if answer.content.lower() == question["answer"].lower():
            await channel.send('Correct!')
        else:
            await channel.send('Incorrect! The correct answer was: {}'.format(question["answer"]))