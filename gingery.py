import os
from os import name
import discord
from discord import app_commands
from discord.ext import commands
import random
from random import randrange
import time
import asyncio

# Intents of the Bot
intents = discord.Intents.default()
intents.message_content = True

# Bot Instance
client = commands.Bot(command_prefix=['.'], intents=intents)

# If the Bot goes Online
@client.event
async def on_ready():
    
    print('Gingery has connected to Discord!')
    # Sync Slash Commands
    await client.tree.sync()
    # Status of the Bot
    await client.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.listening,name="!about"))

trivia_questions = [
    {"question": "What is the capital of France?", "answer": "Paris"},
    {"question": "What is the largest planet in our solar system?", "answer": "Jupiter"},
    {"question": "Who painted the Mona Lisa?", "answer": "Leonardo da Vinci"},
    {"question": "What is the main ingredient in guacamole?", "answer": "Avocado"},
    {"question": "What is the chemical symbol for water?", "answer": "H2O"},
    {"question": "What is the largest mammal in the world?", "answer": "Blue Whale"},
    {"question": "What is the largest organ in the human body?", "answer": "Skin"},
    {"question": "What is the smallest country in the world?", "answer": "Vatican City"},
    {"question": "What is the largest bird in the world?", "answer": "Ostrich"},
    {"question": "What is the smallest continent in the world?", "answer": "Australia"},
    {"question": "What is the largest desert in the world?", "answer": "Sahara Desert"},
    {"question": "What is the capital of Italy?", "answer": "Rome"},
    {"question": "What is the highest mountain in the world?", "answer": "Mount Everest"},
    {"question": "What is the largest ocean in the world?", "answer": "Pacific Ocean"},
    {"question": "What is the longest river in the world?", "answer": "Nile River"},
    {"question": "What is the largest lake in the world?", "answer": "Caspian Sea"},
    {"question": "What is the most populous country in the world?", "answer": "China"},
    {"question": "What is the hottest continent in the world?", "answer": "Africa"},
    {"question": "What is the coldest continent in the world?", "answer": "Antarctica"},
    {"question": "What is the largest island in the world?", "answer": "Greenland"},
    {"question": "What is the smallest state in the US?", "answer": "Rhode Island"},
    {"question": "What is the largest state in the US?", "answer": "Alaska"},
    {"question": "What is the capital of Japan?", "answer": "Tokyo"},
    {"question": "What is the fastest land animal?", "answer": "Cheetah"},
    {"question": "Who wrote 'Hamlet'?", "answer": "William Shakespeare"},
    {"question": "What is the hardest natural substance on Earth?", "answer": "Diamond"},
    {"question": "What is the smallest planet in our solar system?", "answer": "Mercury"},
    {"question": "What is the most widely spoken language in the world?", "answer": "Mandarin Chinese"},
    {"question": "Who was the first person to walk on the moon?", "answer": "Neil Armstrong"},
    {"question": "What is the main ingredient in hummus?", "answer": "Chickpeas"},
    {"question": "What is the currency of the United Kingdom?", "answer": "Pound Sterling"},
    {"question": "What is the most popular sport in the world?", "answer": "Soccer (Football)"},
    {"question": "Who is known as the 'Father of Computers'?", "answer": "Charles Babbage"},
    {"question": "What is the tallest building in the world?", "answer": "Burj Khalifa"},
    {"question": "What is the primary ingredient in traditional Japanese miso soup?", "answer": "Miso paste"},
    {"question": "What is the name of the longest-running Broadway show?", "answer": "The Phantom of the Opera"},
    {"question": "What is the smallest bone in the human body?", "answer": "Stapes (in the ear)"},
    {"question": "What is the most consumed beverage in the world?", "answer": "Water"},
    {"question": "What is the chemical symbol for gold?", "answer": "Au"},
    {"question": "What is the national flower of Japan?", "answer": "Cherry Blossom"},
    {"question": "Who invented the telephone?", "answer": "Alexander Graham Bell"},
    {"question": "What is the world's largest landlocked country?", "answer": "Kazakhstan"},
    {"question": "What is the highest-grossing film of all time?", "answer": "Avatar"},
    {"question": "What is the name of the longest river in the United States?", "answer": "Missouri River"},
    {"question": "What is the largest coral reef system in the world?", "answer": "Great Barrier Reef"},
    {"question": "What is the main ingredient in the dish 'paella'?", "answer": "Rice"},
    {"question": "What is the longest-running television show in the United States?", "answer": "The Simpsons"}
]

WORDS = ['python', 'discord', 'programming', 'bot', 'server', 'message', 'channel', 'role', 'algorithm', 'array', 'attribute', 'boolean', 'byte', 'class', 'compiler', 'condition', 'constant', 'constructor', 
    'data', 'database', 'debug', 'default', 'development', 'dictionary', 'document', 'element', 'encryption', 'exception', 
    'expression', 'file', 'framework', 'function', 'hexadecimal', 'index', 'inheritance', 'input', 'integer', 'interface', 
    'iteration', 'json', 'keyword', 'lambda', 'library', 'loop', 'method', 'module', 'namespace', 'object', 'operator', 
    'parameter', 'pointer', 'polymorphism', 'procedure', 'process', 'protocol', 'queue', 'recursion', 'reference', 'script', 
    'software', 'stack', 'string', 'syntax', 'thread', 'variable', 'version', 'virtual', 'bytecode', 'callback', 'cast', 
    'char', 'client', 'closure', 'code', 'compile', 'compute', 'concatenate', 'concurrent', 'context', 'control', 'cookie', 
    'cryptography', 'daemon', 'dataframe', 'datetime', 'debugger', 'declaration', 'decorator', 'decrement', 'delimiter', 
    'deployment', 'destructor', 'directive', 'dynamic', 'entity', 'enumeration', 'environment', 'equality', 'event', 'execute', 
    'extension', 'facet', 'factory', 'field', 'filesystem', 'filter', 'flag', 'float', 'flush', 'frontend', 'generic', 'global', 
    'hash', 'heap', 'host', 'http', 'identifier', 'immutable', 'implementation', 'import', 'increment', 'indexer', 'inherit', 
    'instance', 'interpreter', 'iterator', 'literal', 'macro', 'mapper', 'memory', 'metadata', 'middleware', 'mutable', 'network', 
    'null', 'numeric', 'operand', 'operation', 'optional', 'override', 'package', 'parse', 'parser', 'partition', 'payload', 
    'permutation', 'polymorphic', 'port', 'property', 'proxy', 'random', 'register', 'repository', 'request', 'response', 'result', 
    'return', 'runtime', 'scalar', 'schema', 'scope', 'serializer', 'service', 'session', 'socket', 'source', 'specification', 
    'stacktrace', 'state', 'statement', 'storage', 'stream', 'structure', 'subroutine', 'system', 'tag', 'template', 'token', 
    'transaction', 'transform', 'trigger', 'tuple', 'unit', 'update', 'url', 'utility', 'validation', 'value', 'vector', 'void', 
    'wrapper', 'yield', 'accessor', 'adapter', 'aggregate', 'alias', 'allocation', 'anchor', 'animation', 'annotation', 'argument', 
    'arithmetic', 'assertion', 'asynchronous', 'atomic', 'audience', 'authentication', 'authorization', 'autonomous', 'backup', 
    'balance', 'bandwidth', 'benchmark', 'binary', 'binding', 'bitwise', 'blob', 'bootstrap', 'boundary', 'broker', 'buffer', 
    'bundler', 'bus', 'cache', 'certificate', 'character', 'checksum', 'cipher', 'clone', 'cluster', 'codec', 'coefficient', 
    'collaboration', 'collection', 'column', 'commit', 'comparison', 'compile-time', 'compression', 'concurrency', 'configuration', 
    'connect', 'container', 'coordinate', 'coroutine', 'coverage', 'credential', 'cryptographic', 'cursor', 'cycle', 'dataset', 
    'decision', 'decryption', 'deflate', 'definition', 'deferred', 'delegation', 'dependency', 'dereference', 'descriptor', 'design', 
    'deterministic', 'developer', 'diagnostic', 'differential', 'diffusion' ]

eight_ball_responses = [
    "It is certain.",
    "It is decidedly so.",
    "Without a doubt.",
    "Yes – definitely.",
    "You may rely on it.",
    "As I see it, yes.",
    "Most likely.",
    "Outlook good.",
    "Yes.",
    "Signs point to yes.",
    "Reply hazy, try again.",
    "Ask again later.",
    "Better not tell you now.",
    "Cannot predict now.",
    "Concentrate and ask again.",
    "Don't count on it.",
    "My reply is no.",
    "My sources say no.",
    "Outlook not so good.",
    "Very doubtful."
]

truths = [
    "What is your biggest fear?",
    "What is the most embarrassing thing you've done in public?",
    "Have you ever cheated in a game?",
    "What is the most daring thing you've ever done?",
    "Have you ever lied to get out of trouble?",
    "What is your biggest regret?",
    "What is a secret you've never told anyone?",
    "Have you ever stolen something?",
    "What is the most ridiculous thing you've ever done on a dare?",
    "What is your biggest insecurity?",
    "What is the worst thing you've ever said to someone?",
    "Have you ever faked being sick to skip school or work?",
    "What is the most awkward date you've ever been on?",
    "Have you ever had a crush on a friend's partner?",
    "What is the most expensive thing you've ever broken?",
    "Have you ever been caught in a lie?",
    "What is the weirdest thing you've ever eaten?",
    "Have you ever been in a physical fight?",
    "What is the most unusual habit you have?",
    "What is something you're afraid to lose?",
    "Have you ever let someone else take the blame for something you did?",
    "What is the most outrageous lie you've ever told?",
    "Have you ever snooped through someone's phone or belongings?"
]

dares = [
    "Do 10 pushups right now!",
    "Sing the chorus of your favorite song out loud.",
    "Do your best impression of a famous person.",
    "Let someone write a word on your forehead in marker.",
    "Do a silly dance for one minute.",
    "Speak in a funny voice until your next turn.",
    "Eat a spoonful of a condiment of your choice.",
    "Let someone in the group redo your hairstyle.",
    "Wear socks on your hands for the next 10 minutes.",
    "Try to lick your elbow.",
    "Speak in an accent for the next three rounds.",
    "Post an embarrassing photo of yourself on social media.",
    "Let the person to your left draw on your face with a pen.",
    "Do 20 push-ups.",
    "Wear a funny hat for the rest of the game.",
    "Text a random contact in your phone and say 'I see you'.",
    "Eat a raw onion slice.",
    "Let someone tickle you for 30 seconds.",
    "Do your best chicken dance outside on the lawn.",
    "Act like a monkey until your next turn.",
    "Run around the outside of the house three times.",
    "Let someone give you a temporary tattoo with a marker.",
    "Pretend to be the person to your right for the next 10 minutes."
]

# Text Commands
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # About Command
    if message.content.startswith('.about'):
        print("About Command Executed by " + str(message.author))
        embedvar = discord.Embed(
            title="About Gingery",
            description=("Gingery is a Discord bot, **made using Python**, that provides various **minigames** for your discord server members to play with! \n\n Type `.help` to see the list of commands. \n\n Discord Server: https://discord.gg/7sdx7PAtRh \n\n `Note: Gingery is still in development, so expect bugs and glitches. You can Report me a Bug by sending me a DM (@gingerlawyer97).` \n\n Developed by **GingerLawyer97**."))
        embedvar.set_thumbnail(url='https://share.creavite.co/666c1a52506029c631efc84b.gif')
        embedvar.set_footer(text='Version 0.1.3')

        await message.channel.send(embed=embedvar)

    # Help Command
    if message.content.startswith('.help'):
        print("Help Command Executed by " + str(message.author))
        embedvar = discord.Embed(
            title="HELP",
            description="List of Commands to use the Bot:")
        embedvar.add_field(name="`.about`", value="- Description About the Bot", inline=False)
        embedvar.add_field(name="`.coinflip`", value="- Flip's a Coin.", inline = False)
        embedvar.add_field(name="`.rolladice`", value="- Roll's a Dice.", inline = False)
        embedvar.add_field(name="`.rps <rock/paper/scissors>`", value="- Plays Rock, Paper, Scissors with the Bot.", inline=False)
        embedvar.add_field(name="`.highlow`", value="- Plays a Number Guessing game with the Bot.", inline=False)
        embedvar.add_field(name="`.scramble`", value="- Plays a Word Scramble game with the Bot.", inline=False)
        embedvar.add_field(name="`.trivia`", value="- The Bot asks you a Question.", inline=False)
        embedvar.add_field(name="`.8ball <question>`", value="- Ask the Bot a question.", inline=False)
        embedvar.add_field(name="`.td <truth/dare>`", value="- The Bot asks you a Truth or Dare.", inline=False)

        await message.channel.send(embed=embedvar)

    # Roll a Dice Command
    if message.content.startswith('.rolladice'):
        print("Rolladice Command Executed by " + str(message.author))
        radnum = randrange(0, 7)
        await message.channel.send("The Number is... ")
        await message.channel.send(radnum)

    # Coin Flip Command    
    if message.content.startswith('.coinflip'):
        print("Coinflip Command Executed by " + str(message.author))
        coinflip = randrange(-1, 2)
        if coinflip == 1:
            await message.channel.send("Its a Head!")
        else:
            await message.channel.send("Its a Tail!")

    # Rock Paper Scissors Command
    if message.content.startswith('.rps'):
        print("RPS Command Executed by " + str(message.author))
        if message.content == '.rps':
            await message.channel.send(f"Invalid Choice! Please choose either rock, paper, or scissors.\nExample: `.rps rock`")
            return
        else:
            choices = ['rock', 'paper', 'scissors']
            user_choice = message.content.split(' ')[1].lower()  # Extract user's choice

            if user_choice not in choices:
                await message.channel.send(f'Invalid choice! Please choose either rock, paper, or scissors.\nExample: `.rps rock`')
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
    if message.content.startswith('.highlow'):
        print("HighLow Command Executed by " + str(message.author))
        number = random.randint(1, 100) # Generate a random number between 1 and 100

        await message.channel.send('I have chosen a number between 1 and 100. Try to guess it! You have 7 attempts.')

        def highlow_check(msg):
            return msg.author == message.author and msg.channel == message.channel

        # Allow the user to guess the number within 7 attempts
        for _ in range(7):
            try:
                guess = await client.wait_for('message', check=highlow_check, timeout=30)
                guess = int(guess.content)

                if guess < number:
                    await message.channel.send('Too low! Try again.')
                elif guess > number:
                    await message.channel.send('Too high! Try again.')
                else:
                    await message.channel.send(f'Congratulations {message.author}! You guessed it right!')
                    return
            except ValueError:
                await message.channel.send('Invalid input! Please enter a number.')
            except asyncio.TimeoutError:
                await message.channel.send('Time\'s up! You didn\'t guess the number in time. The number was {}.'.format(number))
                return

        await message.channel.send('You have used all your attempts. The number was {}.'.format(number))

    # Word Scramble Command
    if message.content.startswith('.scramble'):
        print("Scramble Command Executed by " + str(message.author))
        word = random.choice(WORDS)
        scrambled_word = ''.join(random.sample(word, len(word)))
        await message.channel.send(f'Unscramble this word: **{scrambled_word}**')

        def scramble_check(m):
            return m.author == message.author and m.channel == message.channel

        try:
            user_guess = await client.wait_for('message', check=scramble_check, timeout=30)
        except asyncio.TimeoutError:
            await message.channel.send('Time is up! You took too long to answer.')
            return

        if user_guess.content.lower() == word:
            await message.channel.send(f'Congratulations {message.author.mention}! You guessed the word correctly.')
        else:
            await message.channel.send(f'Sorry {message.author.mention}, the correct word was: **{word}**.')

    # Trivia Game Command
    if message.content.startswith('.trivia'):
        print("Trivia Command Executed by " + str(message.author))
        question = random.choice(trivia_questions)
        await message.channel.send(question["question"])

        def check(msg):
            return msg.author == message.author and msg.channel == message.channel

        try:
            answer = await client.wait_for('message', timeout=30, check=check)
        except asyncio.TimeoutError:
            await message.channel.send('Time\'s up! The correct answer was: {}'.format(question["answer"]))
        else:
            if answer.content.lower() == question["answer"].lower():
                await message.channel.send('Correct!')
            else:
                await message.channel.send('Incorrect! The correct answer was: {}'.format(question["answer"]))

    # 8-Ball Command
    if message.content.startswith('.8ball'):
        print("8ball Command Executed by " + str(message.author))
        if message.content == '.8ball':
            await message.channel.send(f"Please ask a question.\nExample: `.8ball Is Gingery the best?`")
            return
        else:
            response = random.choice(eight_ball_responses)
            await message.channel.send(f'{response}')

    # Truth or Dare Command
    if message.content.startswith('.td'):
        print("TD Command Executed by " + str(message.author))
        if message.content == '.td':
            await message.channel.send(f"Invalid Choice! Please choose either truth or dare.\nExample: `.td truth`")
            return
        else:
            choices = ['truth', 'dare']
            user_choice = message.content.split(' ')[1].lower()  # Extract user's choice

            if user_choice not in choices:
                await  message.channel.send(f"Invalid Choice! Please choose either truth or dare.\nExample: `.td truth`")
                return
            
            if user_choice == 'truth':
                await message.channel.send(random.choice(truths))
            elif user_choice == 'dare':
                await message.channel.send(random.choice(dares))
        
# Token
token = os.environ['TOKEN']
client.run(token)