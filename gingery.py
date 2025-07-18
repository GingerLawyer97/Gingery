# GINGERY DISCORD BOT
# Made by @GingerLawyer97
version = '0.2.4'
#
# ------------------------ LIBRARIES ------------------------ #

import os
from os import name, path
import discord
from discord import app_commands, message
from discord.app_commands.transformers import InlineTransformer
from discord.ext import commands
from discord.ui import Button, View
import random
from random import randrange
import time
import asyncio
import json
import mysql.connector
from dotenv import load_dotenv

# ------------------------ SETUP ------------------------ #

# Intents of the Bot
intents = discord.Intents.default()
intents.message_content = True

# Bot Instance
client = commands.Bot(command_prefix=['.'], intents=intents)

# ------------------------ STARTUP ------------------------ #

load_dotenv()

# Database Connection
username = os.environ['dbUser']
password = os.environ['dbPass']

db = mysql.connector.connect(
    host="mysql.db.bot-hosting.net",
    user=username,
    password=password,
    database="s97085_Statistics"
)

def connectToDB():
    db = mysql.connector.connect(
        host="mysql.db.bot-hosting.net",
        user=username,
        password=password,
        database="s97085_Statistics"
    )

cursor = db.cursor()

@client.event
async def on_ready():

    print('Gingery has connected to Discord!')
    # Sync Slash Commands
    await client.tree.sync()

    total_servers = 0

    for guild in client.guilds:
        total_servers += 1

    print(f"Total Servers: {total_servers}")
    # Status of the Bot
    await client.change_presence(status=discord.Status.idle,
                                 activity=discord.Activity(
                                     type=discord.ActivityType.playing,
                                     name=f"in {total_servers} Servers"))

# ------- LISTS/VARIABLES/PREDEFINED FUNCTIONS ------- #

trivia_questions = [{
    "question": "What is the capital of France?",
    "answer": "Paris"
}, {
    "question": "What is the largest planet in our solar system?",
    "answer": "Jupiter"
}, {
    "question": "Who painted the Mona Lisa?",
    "answer": "Leonardo da Vinci"
}, {
    "question": "What is the main ingredient in guacamole?",
    "answer": "Avocado"
}, {
    "question": "What is the chemical symbol for water?",
    "answer": "H2O"
}, {
    "question": "What is the largest mammal in the world?",
    "answer": "Blue Whale"
}, {
    "question": "What is the largest organ in the human body?",
    "answer": "Skin"
}, {
    "question": "What is the smallest country in the world?",
    "answer": "Vatican City"
}, {
    "question": "What is the largest bird in the world?",
    "answer": "Ostrich"
}, {
    "question": "What is the smallest continent in the world?",
    "answer": "Australia"
}, {
    "question": "What is the largest desert in the world?",
    "answer": "Sahara Desert"
}, {
    "question": "What is the capital of Italy?",
    "answer": "Rome"
}, {
    "question": "What is the highest mountain in the world?",
    "answer": "Mount Everest"
}, {
    "question": "What is the largest ocean in the world?",
    "answer": "Pacific Ocean"
}, {
    "question": "What is the longest river in the world?",
    "answer": "Nile River"
}, {
    "question": "What is the largest lake in the world?",
    "answer": "Caspian Sea"
}, {
    "question": "What is the most populous country in the world?",
    "answer": "China"
}, {
    "question": "What is the hottest continent in the world?",
    "answer": "Africa"
}, {
    "question": "What is the coldest continent in the world?",
    "answer": "Antarctica"
}, {
    "question": "What is the largest island in the world?",
    "answer": "Greenland"
}, {
    "question": "What is the smallest state in the US?",
    "answer": "Rhode Island"
}, {
    "question": "What is the largest state in the US?",
    "answer": "Alaska"
}, {
    "question": "What is the capital of Japan?",
    "answer": "Tokyo"
}, {
    "question": "What is the fastest land animal?",
    "answer": "Cheetah"
}, {
    "question": "Who wrote 'Hamlet'?",
    "answer": "William Shakespeare"
}, {
    "question": "What is the hardest natural substance on Earth?",
    "answer": "Diamond"
}, {
    "question": "What is the smallest planet in our solar system?",
    "answer": "Mercury"
}, {
    "question": "What is the most widely spoken language in the world?",
    "answer": "Mandarin Chinese"
}, {
    "question": "Who was the first person to walk on the moon?",
    "answer": "Neil Armstrong"
}, {
    "question": "What is the main ingredient in hummus?",
    "answer": "Chickpeas"
}, {
    "question": "What is the currency of the United Kingdom?",
    "answer": "Pound Sterling"
}, {
    "question": "What is the most popular sport in the world?",
    "answer": "Soccer (Football)"
}, {
    "question": "Who is known as the 'Father of Computers'?",
    "answer": "Charles Babbage"
}, {
    "question": "What is the tallest building in the world?",
    "answer": "Burj Khalifa"
}, {
    "question":
    "What is the primary ingredient in traditional Japanese miso soup?",
    "answer": "Miso paste"
}, {
    "question": "What is the name of the longest-running Broadway show?",
    "answer": "The Phantom of the Opera"
}, {
    "question": "What is the smallest bone in the human body?",
    "answer": "Stapes (in the ear)"
}, {
    "question": "What is the most consumed beverage in the world?",
    "answer": "Water"
}, {
    "question": "What is the chemical symbol for gold?",
    "answer": "Au"
}, {
    "question": "What is the national flower of Japan?",
    "answer": "Cherry Blossom"
}, {
    "question": "Who invented the telephone?",
    "answer": "Alexander Graham Bell"
}, {
    "question": "What is the world's largest landlocked country?",
    "answer": "Kazakhstan"
}, {
    "question": "What is the highest-grossing film of all time?",
    "answer": "Avatar"
}, {
    "question": "What is the name of the longest river in the United States?",
    "answer": "Missouri River"
}, {
    "question": "What is the largest coral reef system in the world?",
    "answer": "Great Barrier Reef"
}, {
    "question": "What is the main ingredient in the dish 'paella'?",
    "answer": "Rice"
}, {
    "question":
    "What is the longest-running television show in the United States?",
    "answer": "The Simpsons"
}]

riddle_questions = [{
    "question":
    "I have keys but open no locks. I have space but no room. You can enter, but you can't go outside. What am I?",
    "answer": "A keyboard"
}, {
    "question":
    "I can fly without wings. I can cry without eyes. Whenever I go, darkness flies. What am I?",
    "answer": "A cloud"
}, {
    "question":
    "I am not alive, but I grow. I don't have lungs, but I need air. I don't have a mouth, but water kills me. What am I?",
    "answer": "Fire"
}, {
    "question": "I can be cracked, made, told, and played. What am I?",
    "answer": "A joke"
}, {
    "question": "The more you take, the more you leave behind. What am I?",
    "answer": "Footsteps"
}, {
    "question": "I shave every day, but my beard stays the same. What am I?",
    "answer": "A barber"
}, {
    "question":
    "I am not alive, but I can grow; I don't have eyes, but I will cry; I don't have wings, but I will fly. What am I?",
    "answer": "A storm"
}, {
    "question": "I go in hard and come out soft. You blow me hard. What am I?",
    "answer": "Chewing gum"
}, {
    "question":
    "I am always hungry, I must always be fed. The finger I touch will soon turn red. What am I?",
    "answer": "Fire"
}, {
    "question":
    "I turn once, what is out will not get in. I turn again, what is in will not get out. What am I?",
    "answer": "A key"
}, {
    "question":
    "I can be long or short; I can be grown or bought; I can be painted or left bare; I can be round or square. What am I?",
    "answer": "Nails"
}, {
    "question": "I have a head, a tail, but no body. What am I?",
    "answer": "A coin"
}, {
    "question": "I can be cracked, made, told, and played. What am I?",
    "answer": "A joke"
}, {
    "question":
    "I am an odd number. Take away one letter and I become even. What am I?",
    "answer": "Seven"
}, {
    "question": "I am full of holes, but I can hold water. What am I?",
    "answer": "A sponge"
}, {
    "question":
    "I can travel around the world while staying in a corner. What am I?",
    "answer": "A stamp"
}, {
    "question":
    "I am light as a feather, yet the strongest man can't hold me for much more than a minute. What am I?",
    "answer": "Breath"
}, {
    "question":
    "I am not alive, but I can grow; I don't have eyes, but I will cry; I don't have wings, but I will fly. What am I?",
    "answer": "A storm"
}, {
    "question": "I can be cracked, made, told, and played. What am I?",
    "answer": "A joke"
}, {
    "question":
    "I am taken from a mine, and shut up in a wooden case, from which I am never released, and yet I am used by almost every person. What am I?",
    "answer": "Pencil lead"
}]

WORDS = [
    'python', 'discord', 'programming', 'bot', 'server', 'message', 'channel',
    'role', 'algorithm', 'array', 'attribute', 'boolean', 'byte', 'class',
    'compiler', 'condition', 'constant', 'constructor', 'data', 'debug', 'default', 'development', 'dictionary', 'document', 'element',
    'encryption', 'exception', 'expression', 'file', 'framework', 'function',
    'hexadecimal', 'index', 'inheritance', 'input', 'integer', 'interface',
    'iteration', 'json', 'keyword', 'lambda', 'library', 'loop', 'method',
    'module', 'namespace', 'object', 'operator', 'parameter', 'pointer',
    'polymorphism', 'procedure', 'process', 'protocol', 'queue', 'recursion',
    'reference', 'script', 'software', 'stack', 'string', 'syntax', 'thread',
    'variable', 'version', 'virtual', 'bytecode', 'callback', 'cast', 'char',
    'client', 'closure', 'code', 'compile', 'compute', 'concatenate',
    'concurrent', 'context', 'control', 'cookie', 'cryptography', 'daemon',
    'dataframe', 'datetime', 'debugger', 'declaration', 'decorator',
    'decrement', 'delimiter', 'deployment', 'destructor', 'directive',
    'dynamic', 'entity', 'enumeration', 'environment', 'equality', 'event',
    'execute', 'extension', 'facet', 'factory', 'field', 'filesystem',
    'filter', 'flag', 'float', 'flush', 'frontend', 'generic', 'global',
    'hash', 'heap', 'host', 'http', 'identifier', 'immutable',
    'implementation', 'import', 'increment', 'indexer', 'inherit', 'instance',
    'interpreter', 'iterator', 'literal', 'macro', 'mapper', 'memory',
    'metadata', 'middleware', 'mutable', 'network', 'null', 'numeric',
    'operand', 'operation', 'optional', 'override', 'package', 'parse',
    'parser', 'partition', 'payload', 'permutation', 'polymorphic', 'port',
    'property', 'proxy', 'random', 'register', 'repository', 'request',
    'response', 'result', 'return', 'runtime', 'scalar', 'schema', 'scope',
    'serializer', 'service', 'session', 'socket', 'source', 'specification',
    'stacktrace', 'state', 'statement', 'storage', 'stream', 'structure',
    'subroutine', 'system', 'tag', 'template', 'token', 'transaction',
    'transform', 'trigger', 'tuple', 'unit', 'update', 'url', 'utility',
    'validation', 'value', 'vector', 'void', 'wrapper', 'yield', 'accessor',
    'adapter', 'aggregate', 'alias', 'allocation', 'anchor', 'animation',
    'annotation', 'argument', 'arithmetic', 'assertion', 'asynchronous',
    'atomic', 'audience', 'authentication', 'authorization', 'autonomous',
    'backup', 'balance', 'bandwidth', 'benchmark', 'binary', 'binding',
    'bitwise', 'blob', 'bootstrap', 'boundary', 'broker', 'buffer', 'bundler',
    'bus', 'cache', 'certificate', 'character', 'checksum', 'cipher', 'clone',
    'cluster', 'codec', 'coefficient', 'collaboration', 'collection', 'column',
    'commit', 'comparison', 'compile-time', 'compression', 'concurrency',
    'configuration', 'connect', 'container', 'coordinate', 'coroutine',
    'coverage', 'credential', 'cryptographic', 'cursor', 'cycle', 'dataset',
    'decision', 'decryption', 'deflate', 'definition', 'deferred',
    'delegation', 'dependency', 'dereference', 'descriptor', 'design',
    'deterministic', 'developer', 'diagnostic', 'differential', 'diffusion'
]

eight_ball_responses = [
    "It is certain.", "It is decidedly so.", "Without a doubt.",
    "Yes – definitely.", "You may rely on it.", "As I see it, yes.",
    "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.",
    "Reply hazy, try again.", "Ask again later.", "Better not tell you now.",
    "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.",
    "My reply is no.", "My sources say no.", "Outlook not so good.",
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
    "Try to lick your elbow.", "Speak in an accent for the next three rounds.",
    "Post an embarrassing photo of yourself on social media.",
    "Let the person to your left draw on your face with a pen.",
    "Do 20 push-ups.", "Wear a funny hat for the rest of the game.",
    "Text a random contact in your phone and say 'I see you'.",
    "Eat a raw onion slice.", "Let someone tickle you for 30 seconds.",
    "Do your best chicken dance outside on the lawn.",
    "Act like a monkey until your next turn.",
    "Run around the outside of the house three times.",
    "Let someone give you a temporary tattoo with a marker.",
    "Pretend to be the person to your right for the next 10 minutes."
]

facts = [
    "The longest river in the world is the Nile, stretching over 6,650 kilometers (4,130 miles).",
    "The smallest bone in the human body is the stapes bone in the middle ear.",
    "Honey never spoils; archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still edible.",
    "Bananas are berries, but strawberries are not.",
    "Octopuses have three hearts.",
    "A day on Venus is longer than a year on Venus.",
    "Wombat poop is cube-shaped.",
    "The Eiffel Tower can be 15 cm taller during the summer due to thermal expansion.",
    "There are more stars in the universe than grains of sand on all the Earth's beaches.",
    "Humans share approximately 60% of their DNA with bananas.",
    "A bolt of lightning contains enough energy to toast 100,000 slices of bread.",
    "The shortest war in history was between Britain and Zanzibar on August 27, 1896. Zanzibar surrendered after 38 minutes.",
    "Kangaroos can't walk backward.",
    "A group of flamingos is called a 'flamboyance'.",
    "The longest time between two twins being born is 87 days.",
    "There are more public libraries in the U.S. than McDonald's restaurants.",
    "Dolphins have names for each other.",
    "A jiffy is an actual unit of time: 1/100th of a second.",
    "The longest word in the English language is 189,819 letters long and would take you three and a half hours to pronounce.",
    "Cleopatra lived closer in time to the moon landing than to the construction of the Great Pyramid of Giza.",
    "A single cloud can weigh more than a million pounds.",
    "The inventor of the Pringles can is now buried in one.",
    "Cows have best friends and can become stressed when they are separated.",
    "Scotland's national animal is the unicorn.",
    "Butterflies can taste with their feet.",
    "There are more fake flamingos in the world than real ones.",
    "The smell of freshly cut grass is actually a plant distress call.",
    "Humans are the only animals that blush.",
    "There are more possible iterations of a game of chess than there are atoms in the known universe.",
    "The electric chair was invented by a dentist."
]

joke_ = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "Why don't skeletons fight each other? They don't have the guts.",
    "What do you call fake spaghetti? An impasta.",
    "Why did the math book look sad? Because it had too many problems.",
    "How does a penguin build its house? Igloos it together.",
    "Why can't you give Elsa a balloon? Because she will let it go.",
    "What do you call a fish with no eyes? Fsh.",
    "Why don't oysters share their pearls? Because they're shellfish.",
    "What do you get when you cross a snowman and a vampire? Frostbite.",
    "Why did the bicycle fall over? Because it was two-tired.",
    "What do you call cheese that isn't yours? Nacho cheese.",
    "Why did the golfer bring two pairs of pants? In case he got a hole in one.",
    "Why don't some couples go to the gym? Because some relationships don't work out.",
    "What do you call a bear with no teeth? A gummy bear.",
    "Why did the coffee file a police report? It got mugged.",
    "How do you catch a squirrel? Climb into a tree and act like a nut.",
    "What did one ocean say to the other ocean? Nothing, they just waved.",
    "Why are ghosts bad at lying? Because they are too transparent.",
    "What do you get when you cross a snowman and a dog? Frostbite.",
    "Why was the math book sad? It had too many problems.",
    "Why did the tomato turn red? Because it saw the salad dressing.",
    "Why did the stadium get hot after the game? All the fans left.",
    "Why don't programmers like nature? It has too many bugs.",
    "What do you get when you cross a vampire with a snowman? Frostbite.",
    "Why did the chicken join a band? Because it had the drumsticks.",
    "Why was the broom late? It swept in.",
    "What do you call a pile of cats? A meowtain.",
    "Why did the scarecrow become a successful neurosurgeon? He was outstanding in his field.",
    "Why don't eggs tell jokes? They might crack up."
]

questions_wyr = [
    ("Have the ability to fly", "Have the ability to be invisible"),
    ("Be able to teleport anywhere", "Be able to read minds"),
    ("Have unlimited money", "Have unlimited time"),
    ("Live without music", "Live without television"),
    ("Be feared by all", "Be loved by all"),
    ("Know the history of every object you touch",
     "Be able to talk to animals"),
    ("Be constantly tired", "Be constantly hungry"),
    ("Never use social media again", "Never watch another movie or TV show"),
    ("Live in a world without technology", "Live in a world without nature"),
    ("Be able to control fire", "Be able to control water"),
    ("Have the power of super strength", "Have the power of super speed"),
    ("Only be able to whisper", "Only be able to shout"),
    ("Have a photographic memory", "Be able to forget anything you want"),
    ("Live on the moon", "Live on Mars"),
    ("Be able to time travel to the past",
     "Be able to time travel to the future"),
    ("Have a personal chef", "Have a personal chauffeur"),
    ("Always be 10 minutes late", "Always be 20 minutes early"),
    ("Be able to talk to plants", "Be able to talk to electronic devices"),
    ("Be famous but always be watched", "Be rich but always be alone"),
    ("Have a rewind button for your life",
     "Have a pause button for your life"),
    ("Be able to speak all languages",
     "Be able to play all musical instruments"),
    ("Have the power to heal others", "Have the power to heal yourself"),
    ("Never eat your favorite food again",
     "Only eat your favorite food for the rest of your life"),
    ("Always have bad breath", "Always have body odor"),
    ("Be able to breathe underwater", "Be able to walk through walls")
]

quotes = [
    ("The only limit to our realization of tomorrow is our doubts of today. - Franklin D. Roosevelt"
     ),
    ("In the end, we will remember not the words of our enemies, but the silence of our friends. - Martin Luther King Jr."
     ), ("The best way to predict the future is to invent it. - Alan Kay"),
    ("Life is 10% what happens to us and 90% how we react to it. - Charles R. Swindoll"
     ), ("The purpose of our lives is to be happy. - Dalai Lama"),
    ("Get busy living or get busy dying. - Stephen King"),
    ("You only live once, but if you do it right, once is enough. - Mae West"),
    ("Many of life's failures are people who did not realize how close they were to success when they gave up. - Thomas A. Edison"
     ),
    ("If you want to live a happy life, tie it to a goal, not to people or things. - Albert Einstein"
     ),
    ("Never let the fear of striking out keep you from playing the game. - Babe Ruth"
     ),
    ("Money and success don’t change people; they merely amplify what is already there. - Will Smith"
     ),
    ("Your time is limited, so don’t waste it living someone else’s life. - Steve Jobs"
     ),
    ("Not how long, but how well you have lived is the main thing. - Seneca"),
    ("If life were predictable it would cease to be life, and be without flavor. - Eleanor Roosevelt"
     ),
    ("The whole secret of a successful life is to find out what is one’s destiny to do, and then do it. - Henry Ford"
     ),
    ("In order to write about life first you must live it. - Ernest Hemingway"
     ),
    ("The big lesson in life, baby, is never be scared of anyone or anything. - Frank Sinatra"
     ),
    ("Sing like no one’s listening, love like you’ve never been hurt, dance like nobody’s watching, and live like it’s heaven on earth. - Mark Twain"
     ),
    ("Curiosity about life in all of its aspects, I think, is still the secret of great creative people. - Leo Burnett"
     ),
    ("Life is not a problem to be solved, but a reality to be experienced. - Soren Kierkegaard"
     ), ("The unexamined life is not worth living. - Socrates"),
    ("Turn your wounds into wisdom. - Oprah Winfrey"),
    ("The way I see it, if you want the rainbow, you gotta put up with the rain. - Dolly Parton"
     ),
    ("Do all the good you can, for all the people you can, in all the ways you can, as long as you can. - Hillary Clinton"
     ),
    ("Don’t settle for what life gives you; make life better and build something. - Ashton Kutcher"
     ),
    ("Everything negative – pressure, challenges – is all an opportunity for me to rise. - Kobe Bryant"
     ), ("I like criticism. It makes you strong. - LeBron James"),
    ("You never really learn much from hearing yourself speak. - George Clooney"
     ),
    ("Life imposes things on you that you can’t control, but you still have the choice of how you’re going to live through this. - Celine Dion"
     ),
    ("Life is never easy. There is work to be done and obligations to be met – obligations to truth, to justice, and to liberty. - John F. Kennedy"
     ), ("Live for each second without hesitation. - Elton John")
]

questions_tort = [
    ("Cats or Dogs?"),
    ("Tea or Coffee?"),
    ("Summer or Winter?"),
    ("Pizza or Burger?"),
    ("Movies or Books?"),
    ("Morning or Night?"),
    ("Beach or Mountains?"),
    ("Sweet or Savory?"),
    ("Facebook or Twitter?"),
    ("Android or iOS?"),
    ("Rain or Snow?"),
    ("Chocolate or Vanilla?"),
    ("Call or Text?"),
    ("Comedy or Drama?"),
    ("Singing or Dancing?"),
    ("Hamburgers or Hotdogs?"),
    ("Netflix or YouTube?"),
    ("Pen or Pencil?"),
    ("Board Games or Video Games?"),
    ("Camping or Hotel?"),
    ("Flying or Driving?"),
    ("Superman or Batman?"),
    ("Sunrise or Sunset?"),
    ("Spicy or Mild?"),
    ("Fruits or Vegetables?"),
    ("Shopping Online or In-Store?"),
    ("Cardio or Weightlifting?"),
    ("Money or Fame?"),
    ("Dinosaurs or Dragons?"),
    ("Robots or Aliens?"),
]

sentences = [
    "The ubiquitous nature of technological advancements is profound.",
    "Quantum mechanics often challenges our perception of reality.",
    "Ephemeral beauty is fleeting but intensely captivating.",
    "The juxtaposition of modernism and tradition creates unique architectural designs.",
    "Exemplifying resilience in adversity demonstrates remarkable fortitude."
]

story = [
    "The night sky cracked open with a flash, and something fell from the stars.",
    "As the train pulled away, she realized her suitcase was still on the platform.",
    "He found an old, locked diary hidden in the attic—one that had his name on it.",
    "Every mirror in the house reflected a different version of her.",
    "The letter arrived 20 years late, but it still changed everything.",
    "Nobody ever returned from the forest after midnight—until now.",
    "She woke up with no memory and a note in her hand: 'Trust no one.'",
    "The town disappeared from the map, but not from his memories.",
    "He could hear music coming from the walls, and no one else could.",
    "The painting in the museum blinked at her.",
    "Every morning, the calendar reset to the same date.",
    "The last message on the phone read: 'Don’t answer the door.'",
    "She wasn’t alone on the island—someone had lit a fire.",
    "He was born with a map on his palm—and today it started glowing.",
    "The vending machine dispensed a note that read: 'You’re being watched.'",
    "They told her not to press the red button. She did anyway.",
    "The dog came home with a key tied around its neck.",
    "The radio started playing a station that hadn’t broadcast in 50 years.",
    "He stepped into the elevator, but it didn’t stop on any known floor.",
    "Each book in the library was filled with stories from her dreams."
]

button1 = Button(label="Support Server",
     url="https://discord.gg/7sdx7PAtRh")

button2 = Button(
    label="Invite Bot",
    url=
    "https://discord.com/oauth2/authorize?client_id=1226467038113828884&permissions=962073020480&integration_type=0&scope=bot"
)

button3 = Button(label="Vote",
                 url="https://top.gg/bot/1226467038113828884")

# Recording data to Database
def cmdexecuted(user):
    cursor.execute("SELECT * FROM stats WHERE username='" + str(user) + "'")
    result = cursor.fetchone()
    if result:
        print(f"Record already exists for {user}.")
        cursor.execute("UPDATE stats SET totalCommands=totalCommands + 1 WHERE username='" + str(user) + "'")
        db.commit()
    else:
        # Insert new record
        insert_sql = "INSERT INTO stats (username, totalCommands) VALUES (%s, %s)"
        cursor.execute(insert_sql, (str(user), 0))
        db.commit()
        print("New record inserted.")
    
# ------------------------ ADMIN ONLY COMMANDS ------------------------ #

# List of allowed server IDs
ALLOWED_GUILD_IDS = [1256973532462710936, 1268165953443856495]

# ------------------------ SLASH COMMANDS ------------------------ #


# About Slash Command
@client.tree.command(name='about', description='Description about the bot.')
async def about(interaction: discord.Interaction):
    print("About Command Executed by " + str(interaction.user))

    connectToDB()
    cmdexecuted(interaction.user)

    embedvar = discord.Embed(
        title="About Gingery",
        description=
        ("Gingery is a open source discord bot, **made using Python**, that provides various **minigames** for your discord server members to play with! \n\n Type `.help` to see the list of commands. \n\n `Note: Gingery is still in development, so expect bugs and glitches. You can report a bug by creating a ticket in our support server.` \n\n Developed by **GingerLawyer97**."
         ))
    embedvar.set_thumbnail(
        url='https://share.creavite.co/666c1a52506029c631efc84b.gif')
    embedvar.set_footer(text=f'Version {version}')

    # Create a view and add the buttons to it
    view = View()
    view.add_item(button1)
    view.add_item(button2)
    view.add_item(button3)

    await interaction.response.send_message(embed=embedvar, view=view)


# Help Slash Command
@client.tree.command(name='help', description='List of commands.')
async def help(interaction: discord.Interaction, page: str):
    print("Help Command Executed by " + str(interaction.user))

    connectToDB()
    cmdexecuted(interaction.user)

    choices = ['1', '2', '3']

    if page not in choices:
        await interaction.response.send_message(
            f"Invalid Choice! Please choose an page number.\nExample: `/help 1`"
        )
        return

    if page == '1':
        embedvar = discord.Embed(
            title="HELP", description="List of Commands to use the Bot:")
        embedvar.add_field(name="`.about`",
                           value="- Description About the Bot",
                           inline=False)
        embedvar.add_field(name="`.coinflip`",
                           value="- Flip's a Coin.",
                           inline=False)
        embedvar.add_field(name="`.rolladice`",
                           value="- Roll's a Dice.",
                           inline=False)
        embedvar.add_field(name="`.rps <rock/paper/scissors>`",
                           value="- Plays Rock, Paper, Scissors with the Bot.",
                           inline=False)
        embedvar.add_field(
            name="`.highlow`",
            value="- Plays a Number Guessing game with the Bot.",
            inline=False)
        embedvar.add_field(name="`.scramble`",
                           value="- Plays a Word Scramble game with the Bot.",
                           inline=False)
        embedvar.add_field(name="`.trivia`",
                           value="- The Bot asks you a Question.",
                           inline=False)
        embedvar.set_footer(text="Page 1/3")
        await interaction.response.send_message(embed=embedvar)

    if page == '2':
        embedvar2 = discord.Embed(
            title="HELP", description="List of Commands to use the Bot:")
        embedvar2.add_field(name="`.riddle`",
                            value="- The Bot asks you a Riddle.",
                            inline=False)
        embedvar2.add_field(name="`.8ball <question>`",
                            value="- Ask the Bot a question.",
                            inline=False)
        embedvar2.add_field(name="`.td <truth/dare>`",
                            value="- The Bot asks you a Truth or Dare.",
                            inline=False)
        embedvar2.add_field(name="`.fact`",
                            value="- The Bot gives you a random Fact.",
                            inline=False)
        embedvar2.add_field(name="`.joke`",
                            value="- The Bot tells you a random Joke.",
                            inline=False)
        embedvar2.add_field(name="`.quote`",
                            value="- The Bot gives you a random Quote.",
                            inline=False)
        embedvar2.add_field(
            name="`.wyr`",
            value="- The Bot asks you a Would You Rather Question.",
            inline=False)
        embedvar2.set_footer(text="Page 2/3")
        await interaction.response.send_message(embed=embedvar2)

    if page == '3':
        embedvar3 = discord.Embed(
            title="HELP", description="List of Commands to use the Bot:")
        embedvar3.add_field(
            name="`.tort`",
            value="- The Bot asks you a This or That Question.",
            inline=False)
        embedvar3.add_field(
            name="`.copypaste`",
            value=
            "- Copy & Paste a random sentence while trying to get the best time.",
            inline=False)
        embedvar3.add_field(name="`.stats`",
            value="- Shows your Statistics.",
            inline=False)
        embedvar3.add_field(name="`.invite`",
                            value="- Invite the Bot to your Server.",
                            inline=False)
        embedvar3.set_footer(text="Page 3/3")
        await interaction.response.send_message(embed=embedvar3)


# Roll a Dice Slash Command
@client.tree.command(name='rolladice', description='Roll a dice.')
async def rolladice(interaction: discord.Interaction):
    print("Rolladice Command Executed by " + str(interaction.user))

    connectToDB()
    cmdexecuted(interaction.user)

    radnum = randrange(1, 7)
    await interaction.response.send_message(embed = discord.Embed(
        title=f"{interaction.user} rolled a Dice!",
        description=f"The Dice rolled a **{radnum}**!"
    ))
    
    if random.random() < 0.25:
        view = View()
        view.add_item(button2)
        view.add_item(button3)
        await interaction.followup.send(
            "Dont forget to **Invite the Bot to your server** and **Vote** for it!",
            view=view,
            ephemeral=True)


# Coin Flip Slash Command
@client.tree.command(name='coinflip', description='Flips a Coin.')
async def coinflip(interaction: discord.Interaction):
    print("Coinflip Command Executed by " + str(interaction.user))

    connectToDB()
    cmdexecuted(interaction.user)
    
    coinflip = randrange(-1, 2)
    if coinflip == 1:
        await interaction.response.send_message(embed = discord.Embed(
            title=f"{interaction.user} Flipped a Coin!",
            description=f"The Coin landed on **Heads**!"
        ))
    else:
        await interaction.response.send_message(embed = discord.Embed(
                                                    title=f"{interaction.user} Flipped a Coin!",
                                                    description=f"The Coin landed on **Tails**!"
                                                ))

    if random.random() < 0.25:
        view = View()
        view.add_item(button2)
        view.add_item(button3)
        await interaction.followup.send(
            "Dont forget to **Invite the Bot to your server** and **Vote** for it!",
            view=view,
            ephemeral=True)


# Rock Paper Scissors Slash Command
@client.tree.command(name='rockpaperscissors', description='Play Rock Paper Scissors with the Bot.')
@app_commands.choices(choice=[
    app_commands.Choice(name="Rock", value="rock"),
    app_commands.Choice(name="Paper", value="paper"),
    app_commands.Choice(name="Scissors", value="scissors"),
    ])
async def rps(interaction: discord.Interaction, choice: app_commands.Choice[str]):
    print("RPS Command Executed by " + str(interaction.user))

    connectToDB()
    cmdexecuted(interaction.user)

    bot_choices = ['rock', 'paper', 'scissors']
    bot_choice = random.choice(bot_choices)

    if choice.value == bot_choice:
        await interaction.response.send_message(embed = discord.Embed(
            title="Tie!",
            description="Both choose the same thing!"
        ))
    elif (choice.value == 'rock' and bot_choice == 'scissors') or \
        (choice.value == 'paper' and bot_choice == 'rock') or \
        (choice.value == 'scissors' and bot_choice == 'paper'):
        await interaction.response.send_message(embed = discord.Embed(
            title="You Win!",
            description=f"You choose `{choice.value}` and the Bot choose `{bot_choice}`!"
        ))
    else:
        await interaction.response.send_message(embed = discord.Embed(
            title="You Lose!",
            description=f"You choose `{choice.value}` and the Bot choose `{bot_choice}`!"
        ))

    if random.random() < 0.25:
        view = View()
        view.add_item(button2)
        view.add_item(button3)
        await interaction.followup.send(
            "Dont forget to **Invite the Bot to your server** and **Vote** for it!",
            view=view,
            ephemeral=True)


# High Low Slash Command
@client.tree.command(name='highlow', description='Play High Low with the Bot.')
async def highlow(interaction: discord.Interaction):
    print("HighLow Command Executed by " + str(interaction.user))

    connectToDB()
    cmdexecuted(interaction.user)

    number = random.randint(1,
                            100)  # Generate a random number between 1 and 100

    await interaction.response.send_message(embed = discord.Embed(
        title="Guess the Number!",
        description="I'm thinking of a number between 1 and 100. Try to guess it!"
    ))

    def highlow_check(msg):
        return msg.author == interaction.user and msg.channel == interaction.channel

    # Allow the user to guess the number within 7 attempts
    for _ in range(7):
        try:
            guess = await client.wait_for('message',
                                          check=highlow_check,
                                          timeout=30)
            guess = int(guess.content)

            if guess < number:
                await interaction.followup.send('Too low! Try again.')
            elif guess > number:
                await interaction.followup.send('Too high! Try again.')
            elif guess == number:
                await interaction.followup.send(embed = discord.Embed(
                    title="You Win!",
                    description=f"You guessed it right! The Number was: `{number}`!"
                ))
                return
        except ValueError:
            await interaction.followup.send(
                'Invalid input! Please enter a number.')
        except asyncio.TimeoutError:
            await interaction.followup.send(embed = discord.Embed(
                title="Time's Up!",
                description="You took too long to guess. The number was: `{number}`!"
            ))
            return

    await interaction.followup.send(embed = discord.Embed(
        title="You Lose!",
        description=f"You ran out of attempts. The number was: `{number}`!"
    ))
    
    if random.random() < 0.25:
        view = View()
        view.add_item(button2)
        view.add_item(button3)
        await interaction.followup.send(
            "Dont forget to **Invite the Bot to your server** and **Vote** for it!",
            view=view,
            ephemeral=True)


# Word Scramble Slash Command
@client.tree.command(name='scramble',
                     description='The Bot gives you a Word to Unscramble.')
async def scramble(interaction: discord.Interaction):
    print("Scramble Command Executed by " + str(interaction.user))

    connectToDB()
    cmdexecuted(interaction.user)

    word = random.choice(WORDS)
    scrambled_word = ''.join(random.sample(word, len(word)))
    await interaction.response.send_message(embed = discord.Embed(
        title="Unscramble the Word!",
        description=f"Unscramble the following word: `{scrambled_word}`!"
    ))

    def scramble_check(m):
        return m.author == interaction.user and m.channel == interaction.channel

    try:
        user_guess = await client.wait_for('message',
                                           check=scramble_check,
                                           timeout=30)
    except asyncio.TimeoutError:
        await interaction.followup.send(embed = discord.Embed(
            title="Time's Up!",
            description=f"You took too long to unscramble the word. The word was: `{word}`!"
        ))
        return

    if user_guess.content.lower() == word:
        await interaction.followup.send(embed = discord.Embed(
            title="You Win!",
            description=f"Congratulations! You unscrambled the word correctly. The word was: `{word}`!"
        ))
    else:
        await interaction.followup.send(embed = discord.Embed(
            title="You Lose!",
            description=f"Sorry, that's not the correct word. The word was: `{word}`!"
        ))
    
    if random.random() < 0.25:
        view = View()
        view.add_item(button2)
        view.add_item(button3)
        await interaction.followup.send(
            "Dont forget to **Invite the Bot to your server** and **Vote** for it!",
            view=view,
            ephemeral=True)


# Trivia Slash Command
@client.tree.command(name='trivia', description='The Bots asks you a question')
async def trivia(interaction: discord.Interaction):
    print("Trivia Command Executed by " + str(interaction.user))

    connectToDB()
    cmdexecuted(interaction.user)

    question = random.choice(trivia_questions)
    await interaction.response.send_message(embed = discord.Embed(
        title="Trivia Question!",
        description=f"The Question is: `{question['question']}`!"
    ))

    def check(msg):
        return msg.author == interaction.user and msg.channel == interaction.channel

    try:
        answer = await client.wait_for('message', timeout=30, check=check)
    except asyncio.TimeoutError:
        await interaction.followup.send(embed = discord.Embed(
            title="Time's Up!",
            description=f"You took too long to answer the question. The answer was: `{question['answer']}`!"
        ))
    else:
        if answer.content.lower() == question["answer"].lower():
            await interaction.followup.send(embed = discord.Embed(
                title="Correct!",
                description=f"Congratulations! You answered correctly. The answer was: `{question['answer']}`!"
            ))
            
        else:
            await interaction.followup.send(embed = discord.Embed(
                title="Incorrect!",
                description=f"Sorry, that's not the correct answer. The answer was: `{question['answer']}`!"
            ))
    
    if random.random() < 0.25:
        view = View()
        view.add_item(button2)
        view.add_item(button3)
        await interaction.followup.send(
            "Dont forget to **Invite the Bot to your server** and **Vote** for it!",
            view=view,
            ephemeral=True)


# Riddle Slash Command
@client.tree.command(name='riddle', description='The Bot asks you a Riddle.')
async def riddle(interaction: discord.Interaction):
    print("Riddle Command Executed by " + str(interaction.user))

    connectToDB()
    cmdexecuted(interaction.user)

    question = random.choice(riddle_questions)
    await interaction.response.send_message(embed = discord.Embed(
        title="Riddle!",
        description=f"The Riddle is: `{question['question']}`!"
    ))

    def check(msg):
        return msg.author == interaction.user and msg.channel == interaction.channel

    try:
        answer = await client.wait_for('message', timeout=30, check=check)
    except asyncio.TimeoutError:
        await interaction.followup.send(embed = discord.Embed(
            title="Time's Up!",
            description=f"You took too long to answer the riddle. The answer was: `{question['answer']}`!"
        ))
    else:
        if answer.content.lower() == question["answer"].lower():
            await interaction.followup.send(embed = discord.Embed(
                title="Correct!",
                description=f"Congratulations! You answered correctly. The answer was: `{question['answer']}`!"
            ))
        else:
            await interaction.followup.send(embed = discord.Embed(
                title="Incorrect!",
                description=f"Sorry, that's not the correct answer. The answer was: `{question['answer']}`!"
            ))
    
    if random.random() < 0.25:
        view = View()
        view.add_item(button2)
        view.add_item(button3)
        await interaction.followup.send(
            "Dont forget to **Invite the Bot to your server** and **Vote** for it!",
            view=view,
            ephemeral=True)


# 8Ball Slash Command
@client.tree.command(name='8ball', description='Ask the Bot a Question.')
async def ball(interaction: discord.Interaction, question: str):
    print("8ball Command Executed by " + str(interaction.user))

    connectToDB()
    cmdexecuted(interaction.user)

    response = random.choice(eight_ball_responses)
    await interaction.response.send_message(embed = discord.Embed(
        title="8Ball!",
        description=f"You asked: `{question}`\nThe Bot's Answer is: `{response}`"
    ))
    
    if random.random() < 0.25:
        view = View()
        view.add_item(button2)
        view.add_item(button3)
        await interaction.followup.send(
            "Dont forget to **Invite the Bot to your server** and **Vote** for it!",
            view=view,
            ephemeral=True)


# Truth or Dare Slash Command
@client.tree.command(name='truthordare', description='The Bot gives you a Truth or a Dare.')
async def truthordare(interaction: discord.Interaction, choice: str):
    print("TD Command Executed by " + str(interaction.user))

    connectToDB()
    cmdexecuted(interaction.user)

    choices = ['truth', 'dare']

    if choice not in choices:
        await interaction.response.send_message(
            f"Invalid Choice! Please choose either truth or dare.\nExample: `/truthordare truth`"
        )
        return

    if choice == 'truth':
        await interaction.response.send_message(embed = discord.Embed(
            title="Truth!",
            description=f"Truth Question: `{random.choice(truths)}`"
        ))
    elif choice == 'dare':
        await interaction.response.send_message(embed = discord.Embed(
            title="Dare!",
            description=f"Dare: `{random.choice(dares)}`"
        ))
    
    if random.random() < 0.25:
        view = View()
        view.add_item(button2)
        view.add_item(button3)
        await interaction.followup.send(
            "Dont forget to **Invite the Bot to your server** and **Vote** for it!",
            view=view,
            ephemeral=True)


# Fact Slash Command
@client.tree.command(name='fact', description='The Bot tells you a Fact.')
async def fact(interaction: discord.Interaction):
    print("Fact Command Executed by " + str(interaction.user))

    connectToDB()
    cmdexecuted(interaction.user)

    fact = random.choice(facts)
    await interaction.response.send_message(embed = discord.Embed(
        title="Here's an Random Fact!",
        description=f"Fact: `{fact}`"
    ))
    
    if random.random() < 0.25:
        view = View()
        view.add_item(button2)
        view.add_item(button3)
        await interaction.followup.send(
            "Dont forget to **Invite the Bot to your server** and **Vote** for it!",
            view=view,
            ephemeral=True)


# Joke Slash Command
@client.tree.command(name='joke', description='The Bot tells you a Joke.')
async def jokes(interaction: discord.Interaction):
    print("Joke Command Executed by " + str(interaction.user))

    connectToDB()
    cmdexecuted(interaction.user)

    joke = random.choice(joke_)
    await interaction.response.send_message(embed = discord.Embed(
        title="Here's an Random Joke!",
        description=f"Joke: `{joke}`"
    ))
    
    if random.random() < 0.25:
        view = View()
        view.add_item(button2)
        view.add_item(button3)
        await interaction.followup.send(
            "Dont forget to **Invite the Bot to your server** and **Vote** for it!",
            view=view,
            ephemeral=True)


# Quote Slash Command
@client.tree.command(name='quote', description='The Bot tells you a Quote.')
async def quote(interaction: discord.Interaction):
    print("Quote Command Executed by " + str(interaction.user))

    connectToDB()
    cmdexecuted(interaction.user)

    # Choose a Random Qoute
    quote = random.choice(quotes)
    # Send the Quote
    await interaction.response.send_message(embed = discord.Embed(
        title="Here's an Random Quote!",
        description=f"Quote: `{quote}`"
    ))
    
    if random.random() < 0.25:
        view = View()
        view.add_item(button2)
        view.add_item(button3)
        await interaction.followup.send(
            "Dont forget to **Invite the Bot to your server** and **Vote** for it!",
            view=view,
            ephemeral=True)


# Would you Rather Slash Command
@client.tree.command(
    name='wouldyourather',
    description='The Bot asks you a Would You Rather Question.')
async def wyr(interaction: discord.Interaction):
    print("Would You Rather Command Executed by " + str(interaction.user))

    connectToDB()
    cmdexecuted(interaction.user)

    # Choose a random question
    question = random.choice(questions_wyr)

    # Create the embed message
    embedwyr = discord.Embed(title="**Would You Rather**")
    embedwyr.add_field(name="Option 1", value=question[0], inline=False)
    embedwyr.add_field(name="Option 2", value=question[1], inline=False)

    # Send the message and capture the sent message object
    message = await interaction.response.send_message(embed=embedwyr)
    
    if random.random() < 0.25:
        view = View()
        view.add_item(button2)
        view.add_item(button3)
        await interaction.followup.send(
            "Dont forget to **Invite the Bot to your server** and **Vote** for it!",
            view=view,
            ephemeral=True)


# This or That Slash Command
@client.tree.command(name='thisorthat',
                     description='The Bot asks you a This or That Question.')
async def tort(interaction: discord.Interaction):
    print(f"This or that Command Executed by {interaction.user}")

    connectToDB()
    cmdexecuted(interaction.user)

    question = random.choice(questions_tort)
    embed = discord.Embed(title="This or That", description=f"{random.choice(questions_tort)}")

    message = await interaction.response.send_message(embed=embed)
    
    if random.random() < 0.25:
        view = View()
        view.add_item(button2)
        view.add_item(button3)
        await interaction.followup.send(
            "Dont forget to **Invite the Bot to your server** and **Vote** for it!",
            view=view,
            ephemeral=True)


copypastestopwatch = {}


# Copy Paste Slash Command
@client.tree.command(
    name='copypaste',
    description=
    'Copy & Paste a random sentence while trying to get the best time.')
async def copypaste(interaction: discord.Interaction):
    print("Copy Paste Game Command Executed by " + str(interaction.user))

    connectToDB()
    cmdexecuted(interaction.user)
        
    user_id = interaction.user
    sentence = random.choice(sentences)
    await interaction.response.send_message(embed = discord.Embed(
        title="Copy Paste!",
        description=f"Type the following sentence as fast as you can:\n`{sentence}`"
    ))
    copypastestopwatch[user_id] = time.time()

    def copypaste_check(msg):
        return msg.author == interaction.user and msg.channel == interaction.channel

    answer = await client.wait_for('message',
                                   check=copypaste_check,
                                   timeout=30)
    answer = str(answer.content)

    if answer == sentence:
        start_time = copypastestopwatch.pop(user_id)
        elapsed_time = time.time() - start_time
        await interaction.followup.send(embed = discord.Embed(
            title="You got it right!",
            description=f"in {elapsed_time:.3f} seconds"
        ))
    else:
        await interaction.followup.send(embed = discord.Embed(
            title="Wrong!",
            description=f"The sentence you copied was wrong! The Sentence was: `{sentence}`"
        ))

    if random.random() < 0.25:
        view = View()
        view.add_item(button2)
        view.add_item(button3)
        await interaction.followup.send(
            "Dont forget to **Invite the Bot to your server** and **Vote** for it!",
            view=view,
            ephemeral=True)

# Story Slash Command
@client.tree.command(name='story', description='The Bot starts a random story.')
async def radnomStory(interaction: discord.Interaction):
    print("Story Command Executed by " + str(interaction.user))

    connectToDB()
    cmdexecuted(interaction.user)

    random_story = random.choice(story)
    storyEmbed = discord.Embed(
        title="Start a story!",
        description=random_story
    )
    storyEmbed.set_footer(text="Continue the story by typing your own sentence.")
    await interaction.response.send_message(embed = storyEmbed)

    if random.random() < 0.25:
        view = View()
        view.add_item(button2)
        view.add_item(button3)
        await interaction.followup.send(
            "Dont forget to **Invite the Bot to your server** and **Vote** for it!",
            view=view,
            ephemeral=True)

# Invite Slash Command
@client.tree.command(name='invite',
                     description='Invite the Bot to your server')
async def invite(interaction: discord.Interaction):
    print("Invite Command Executed by " + str(interaction.user))

    connectToDB()
    cmdexecuted(interaction.user)

    await interaction.response.send_message(
        f"# Invite the Bot to your server: \n\n - **INVITE LINK**: https://discord.com/oauth2/authorize?client_id=1226467038113828884&permissions=962073020480&integration_type=0&scope=bot"
    )

# Stats Slash Command
@client.tree.command(name='stats', description='Shows your statistics.')
async def stats(interaction: discord.Interaction):
    print("Stats Command Executed by " + str(interaction.user))
    cursor.execute("SELECT * FROM stats WHERE username='" + str(interaction.user) + "'")
    stats = cursor.fetchone()
    totalCommands = stats[1]
    if stats:
        embedvar = discord.Embed(
            title="Statistics",
            description=
            f"**Total Commands Executed by {interaction.user}:** `{totalCommands}`"
        )
        await interaction.response.send_message(embed=embedvar)
    else:
        await interaction.response.send_message("**You have not executed any commands yet. (The Statistics command is not counted as a command obv.)**")

# ------------------------ TOKEN ------------------------ #

token = os.environ['TOKEN']
client.run(token)