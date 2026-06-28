# ============================================================
#   GINGERY DISCORD BOT  •  v0.3.0
#   Made by @GingerLawyer97
# ============================================================

import os
import random
import time
import asyncio
import logging

import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View
from dotenv import load_dotenv

import database as db

# ── Logging ───────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("Gingery")

# ── Config ────────────────────────────────────────────────────
load_dotenv()

VERSION    = "0.3.0"
BOT_COLOR  = 0x9B59B6
INVITE_URL = (
    "https://discord.com/oauth2/authorize"
    "?client_id=1226467038113828884"
    "&permissions=962073020480&integration_type=0&scope=bot"
)
SUPPORT_URL = "https://discord.gg/CFUHkHsmSe"
TOPGG_URL   = "https://top.gg/bot/1226467038113828884"
THUMBNAIL   = "https://share.creavite.co/666c1a52506029c631efc84b.gif"

# XP awarded per game outcome
XP = {"win": 30, "loss": 5, "correct": 20, "played": 5}

# Coin rewards per game outcome
COINS = {"win": 50, "loss": 5, "correct": 30, "played": 3}

# ── Bot ───────────────────────────────────────────────────────
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=".", intents=intents)

# ── UI helpers ────────────────────────────────────────────────

def promo_view() -> View:
    v = View(timeout=None)
    v.add_item(Button(label="Invite Bot",  url=INVITE_URL, emoji="🤖"))
    v.add_item(Button(label="Vote for us", url=TOPGG_URL,  emoji="⭐"))
    return v

def links_view() -> View:
    v = View(timeout=None)
    v.add_item(Button(label="Support",    url=SUPPORT_URL, emoji="💬"))
    v.add_item(Button(label="Invite Bot", url=INVITE_URL,  emoji="🤖"))
    v.add_item(Button(label="Vote",       url=TOPGG_URL,   emoji="⭐"))
    return v

def embed(title: str, description: str = "", color: int = BOT_COLOR) -> discord.Embed:
    return discord.Embed(title=title, description=description, color=color)

async def maybe_promo(interaction: discord.Interaction) -> None:
    if random.random() < 0.25:
        await interaction.followup.send(
            "Enjoying Gingery? **Invite it** or **vote** to support!",
            view=promo_view(), ephemeral=True,
        )

def reward_line(coins_: int, xp_: int) -> str:
    return f"\n\n🪙 **+{coins_} coins** · ⭐ **+{xp_} XP**"

def pct(wins: int, played: int) -> str:
    return f"{round(wins / played * 100)}%" if played else "—"

# ── Game reward helper ────────────────────────────────────────

def record_game(
    user_id: int, guild_id: int, username: str,
    played_col: str, win_col: str | None, won: bool
) -> tuple[int, int]:
    """
    Ensures user exists, bumps played/win counters, awards coins + XP.
    Returns (coins_awarded, xp_awarded).
    """
    db.ensure_user(user_id, guild_id, username)
    db.increment_stat(user_id, guild_id, played_col)
    if won and win_col:
        db.increment_stat(user_id, guild_id, win_col)

    c = COINS["win"] if won else COINS["loss"]
    x = XP["win"]    if won else XP["loss"]
    db.increment_stat(user_id, guild_id, "coins",    c)
    db.increment_stat(user_id, guild_id, "total_xp", x)
    return c, x

# ── Data ──────────────────────────────────────────────────────

TRIVIA = [
    {"q": "What is the capital of France?",                        "a": "Paris"},
    {"q": "What is the largest planet in our solar system?",       "a": "Jupiter"},
    {"q": "Who painted the Mona Lisa?",                            "a": "Leonardo da Vinci"},
    {"q": "What is the main ingredient in guacamole?",             "a": "Avocado"},
    {"q": "What is the chemical symbol for water?",                "a": "H2O"},
    {"q": "What is the largest mammal in the world?",              "a": "Blue Whale"},
    {"q": "What is the largest organ in the human body?",          "a": "Skin"},
    {"q": "What is the smallest country in the world?",            "a": "Vatican City"},
    {"q": "What is the largest bird in the world?",                "a": "Ostrich"},
    {"q": "What is the smallest continent?",                       "a": "Australia"},
    {"q": "What is the largest desert in the world?",              "a": "Sahara Desert"},
    {"q": "What is the capital of Italy?",                         "a": "Rome"},
    {"q": "What is the highest mountain in the world?",            "a": "Mount Everest"},
    {"q": "What is the largest ocean in the world?",               "a": "Pacific Ocean"},
    {"q": "What is the longest river in the world?",               "a": "Nile River"},
    {"q": "What is the most widely spoken language?",              "a": "Mandarin Chinese"},
    {"q": "Who was the first person to walk on the moon?",         "a": "Neil Armstrong"},
    {"q": "What is the main ingredient in hummus?",                "a": "Chickpeas"},
    {"q": "What is the currency of the United Kingdom?",           "a": "Pound Sterling"},
    {"q": "Who is known as the 'Father of Computers'?",           "a": "Charles Babbage"},
    {"q": "What is the tallest building in the world?",            "a": "Burj Khalifa"},
    {"q": "What is the chemical symbol for gold?",                 "a": "Au"},
    {"q": "What is the national flower of Japan?",                 "a": "Cherry Blossom"},
    {"q": "Who invented the telephone?",                           "a": "Alexander Graham Bell"},
    {"q": "What is the largest coral reef system?",                "a": "Great Barrier Reef"},
    {"q": "What is the fastest land animal?",                      "a": "Cheetah"},
    {"q": "Who wrote Hamlet?",                                     "a": "William Shakespeare"},
    {"q": "What is the hardest natural substance on Earth?",       "a": "Diamond"},
    {"q": "What is the smallest planet in our solar system?",      "a": "Mercury"},
    {"q": "What is the most popular sport in the world?",          "a": "Soccer"},
    {"q": "What is the smallest bone in the human body?",          "a": "Stapes"},
    {"q": "What is the world's largest landlocked country?",       "a": "Kazakhstan"},
    {"q": "What is the longest-running US animated TV show?",      "a": "The Simpsons"},
    {"q": "What is the largest lake in the world?",                "a": "Caspian Sea"},
    {"q": "What is the capital of Japan?",                         "a": "Tokyo"},
]

RIDDLES = [
    {"q": "I have keys but open no locks. I have space but no room. What am I?",            "a": "A keyboard"},
    {"q": "I can fly without wings. I can cry without eyes. What am I?",                    "a": "A cloud"},
    {"q": "I'm not alive but I grow; I need air but have no lungs; water kills me. What am I?", "a": "Fire"},
    {"q": "The more you take, the more you leave behind. What am I?",                       "a": "Footsteps"},
    {"q": "I shave every day, but my beard stays the same. What am I?",                     "a": "A barber"},
    {"q": "I have a head, a tail, but no body. What am I?",                                 "a": "A coin"},
    {"q": "I am an odd number. Take away a letter and I become even. What am I?",           "a": "Seven"},
    {"q": "I am full of holes but can hold water. What am I?",                              "a": "A sponge"},
    {"q": "I can travel around the world while staying in a corner. What am I?",            "a": "A stamp"},
    {"q": "Light as a feather, yet no man can hold me for long. What am I?",                "a": "Breath"},
    {"q": "I go in hard and come out soft. What am I?",                                     "a": "Chewing gum"},
    {"q": "I turn once — what's out won't get in. I turn again — what's in won't get out. What am I?", "a": "A key"},
]

EIGHT_BALL = [
    "It is certain.", "It is decidedly so.", "Without a doubt.",
    "Yes — definitely.", "You may rely on it.", "As I see it, yes.",
    "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.",
    "Reply hazy, try again.", "Ask again later.", "Better not tell you now.",
    "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.",
    "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful.",
]

TRUTHS = [
    "What is your biggest fear?",
    "What is the most embarrassing thing you've done in public?",
    "Have you ever cheated in a game?",
    "What is your biggest regret?",
    "What is a secret you've never told anyone?",
    "Have you ever stolen something?",
    "What is the most unusual habit you have?",
    "Have you ever let someone else take the blame for something you did?",
    "What is the most outrageous lie you've ever told?",
    "Have you ever snooped through someone's belongings?",
    "What is the weirdest thing you've ever eaten?",
    "What is the worst thing you've said to someone?",
]

DARES = [
    "Do 10 push-ups right now!",
    "Sing the chorus of your favourite song out loud.",
    "Do your best impression of a famous person.",
    "Do a silly dance for one minute.",
    "Speak in a funny accent until your next turn.",
    "Try to lick your elbow.",
    "Act like a monkey until your next turn.",
    "Text a random contact in your phone and say 'I see you'.",
    "Do your best chicken dance.",
    "Let the group give you a new nickname for the rest of the game.",
]

FACTS = [
    "Honey never spoils — archaeologists found 3,000-year-old honey in Egyptian tombs that's still edible.",
    "Bananas are berries, but strawberries are not.",
    "Octopuses have three hearts.",
    "A day on Venus is longer than a year on Venus.",
    "Wombat poop is cube-shaped.",
    "The Eiffel Tower can be 15 cm taller in summer due to thermal expansion.",
    "Humans share approximately 60% of their DNA with bananas.",
    "The shortest war in history lasted 38 minutes — Britain vs Zanzibar, 1896.",
    "Kangaroos can't walk backward.",
    "A group of flamingos is called a flamboyance.",
    "Dolphins have names for each other.",
    "A jiffy is an actual unit of time: 1/100th of a second.",
    "Cleopatra lived closer in time to the moon landing than to the Great Pyramid's construction.",
    "Scotland's national animal is the unicorn.",
    "Butterflies taste with their feet.",
    "The smell of freshly cut grass is a plant distress signal.",
    "The electric chair was invented by a dentist.",
    "Cows have best friends and become stressed when separated.",
]

JOKES = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "Why did the scarecrow win an award? He was outstanding in his field!",
    "What do you call fake spaghetti? An impasta.",
    "Why did the bicycle fall over? It was two-tired.",
    "Why don't programmers like nature? It has too many bugs.",
    "What do you call a bear with no teeth? A gummy bear.",
    "Why did the coffee file a police report? It got mugged.",
    "What did one ocean say to the other? Nothing, they just waved.",
    "Why did the tomato turn red? It saw the salad dressing.",
    "Why was the broom late? It swept in.",
    "What do you call a pile of cats? A meowtain.",
    "Why don't eggs tell jokes? They might crack up.",
]

QUOTES = [
    "The only limit to our realization of tomorrow is our doubts of today. — FDR",
    "The best way to predict the future is to invent it. — Alan Kay",
    "Life is 10% what happens to us and 90% how we react to it. — Charles Swindoll",
    "Get busy living or get busy dying. — Stephen King",
    "You only live once, but if you do it right, once is enough. — Mae West",
    "Your time is limited — don't waste it living someone else's life. — Steve Jobs",
    "Not how long, but how well you have lived is the main thing. — Seneca",
    "Turn your wounds into wisdom. — Oprah Winfrey",
    "Everything negative is an opportunity for me to rise. — Kobe Bryant",
    "The unexamined life is not worth living. — Socrates",
]

WOULD_YOU_RATHER = [
    ("Have the ability to fly", "Have the ability to be invisible"),
    ("Be able to teleport anywhere", "Be able to read minds"),
    ("Have unlimited money", "Have unlimited time"),
    ("Live without music", "Live without television"),
    ("Be feared by all", "Be loved by all"),
    ("Be constantly tired", "Be constantly hungry"),
    ("Have a photographic memory", "Be able to forget anything at will"),
    ("Live on the Moon", "Live on Mars"),
    ("Be able to speak all languages", "Be able to play all instruments"),
    ("Have the power to heal others", "Have the power to heal yourself"),
    ("Always be 10 minutes late", "Always be 20 minutes early"),
    ("Be able to breathe underwater", "Be able to walk through walls"),
]

THIS_OR_THAT = [
    "Cats or Dogs?", "Tea or Coffee?", "Summer or Winter?",
    "Pizza or Burger?", "Movies or Books?", "Morning or Night?",
    "Beach or Mountains?", "Sweet or Savory?", "Android or iOS?",
    "Rain or Snow?", "Chocolate or Vanilla?", "Call or Text?",
    "Comedy or Drama?", "Netflix or YouTube?", "Board Games or Video Games?",
    "Camping or Hotel?", "Flying or Driving?", "Sunrise or Sunset?",
    "Spicy or Mild?", "Money or Fame?",
]

STORY_PROMPTS = [
    "The night sky cracked open with a flash, and something fell from the stars.",
    "As the train pulled away, she realised her suitcase was still on the platform.",
    "He found an old locked diary in the attic — one that had his name on it.",
    "Every mirror in the house reflected a different version of her.",
    "The letter arrived 20 years late, but it still changed everything.",
    "Nobody ever returned from the forest after midnight — until now.",
    "She woke up with no memory and a note in her hand: 'Trust no one.'",
    "The painting in the museum blinked at her.",
    "The last message on the phone read: 'Don't answer the door.'",
    "The radio started playing a station that hadn't broadcast in 50 years.",
    "He stepped into the elevator, but it didn't stop on any known floor.",
    "Each book in the library was filled with stories from her dreams.",
]

COPY_PASTE_SENTENCES = [
    "The ubiquitous nature of technological advancements is profound.",
    "Quantum mechanics often challenges our perception of reality.",
    "Ephemeral beauty is fleeting but intensely captivating.",
    "The juxtaposition of modernism and tradition creates unique architectural designs.",
    "Exemplifying resilience in adversity demonstrates remarkable fortitude.",
    "The ceaseless march of progress reshapes every corner of civilisation.",
    "Serendipitous discoveries have often driven the greatest scientific breakthroughs.",
]

SCRAMBLE_WORDS = [
    "python", "discord", "programming", "algorithm", "boolean",
    "compiler", "recursion", "inheritance", "polymorphism", "cryptography",
    "asynchronous", "concurrency", "authentication", "serializer", "middleware",
    "decorator", "coroutine", "abstraction", "dependency", "refactoring",
]

BEATS     = {"rock": "scissors", "paper": "rock", "scissors": "paper"}
RPS_EMOJI = {"rock": "🪨", "paper": "📄", "scissors": "✂️"}

# ── XP → Level ────────────────────────────────────────────────

def xp_to_level(xp: int) -> tuple[int, int, int]:
    """Returns (level, xp_into_level, xp_needed_for_next)."""
    level = 0
    while xp >= (needed := 100 * (level + 1)):
        xp    -= needed
        level += 1
    return level, xp, 100 * (level + 1)

# ── Startup ───────────────────────────────────────────────────

@bot.event
async def on_ready():
    try:
        db.init_pool()
        db.create_tables()
        log.info("Database ready.")
    except Exception as e:
        log.critical(f"DB setup failed: {e}")

    await bot.tree.sync()
    total = len(bot.guilds)
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(
            type=discord.ActivityType.playing,
            name=f"/help | In {total} servers",
        ),
    )
    log.info(f"Gingery v{VERSION} online — {total} server(s).")

@bot.event
async def on_command_error(ctx, error):
    log.error(f"Command error: {error}")

# ════════════════════════════════════════════════════════════
#   INFO COMMANDS
# ════════════════════════════════════════════════════════════

@bot.tree.command(name="about", description="Learn about Gingery.")
async def about(interaction: discord.Interaction):
    log.info(f"/about — {interaction.user}")
    e = discord.Embed(
        title="About Gingery 🤖",
        description=(
            "Gingery is an open-source Discord bot built with Python.\n"
            "It brings **mini-games, trivia, riddles, an economy, and more** to your server.\n\n"
            "Use `/help` to see all commands.\n\n"
            "_Gingery is in active development — report bugs in our support server!_"
        ),
        color=BOT_COLOR,
    )
    e.set_thumbnail(url=THUMBNAIL)
    e.add_field(name="Version",   value=f"`{VERSION}`",        inline=True)
    e.add_field(name="Servers",   value=f"`{len(bot.guilds)}`", inline=True)
    e.add_field(name="Developer", value="`GingerLawyer97`",     inline=True)
    e.set_footer(text="Gingery • Made with ❤️ in Python")
    await interaction.response.send_message(embed=e, view=links_view())


@bot.tree.command(name="help", description="See all available commands.")
async def help_cmd(interaction: discord.Interaction):
    log.info(f"/help — {interaction.user}")
    e = discord.Embed(title="📖 Gingery Commands", color=BOT_COLOR)
    e.set_thumbnail(url=THUMBNAIL)
    e.add_field(name="ℹ️ Info", inline=False, value=(
        "`/about` · About the bot\n"
        "`/help`  · This menu\n"
        "`/invite`· Invite link"
    ))
    e.add_field(name="🎮 Games", inline=False, value=(
        "`/trivia`            · Trivia question\n"
        "`/riddle`            · Riddle challenge\n"
        "`/highlow`           · Guess the number (7 tries)\n"
        "`/scramble`          · Unscramble a word\n"
        "`/copypaste`         · Typing speed challenge\n"
        "`/rockpaperscissors` · RPS vs the bot"
    ))
    e.add_field(name="🎲 Random", inline=False, value=(
        "`/rolladice`      · Roll a dice\n"
        "`/coinflip`       · Flip a coin\n"
        "`/8ball`          · Ask the magic 8-ball\n"
        "`/fact`           · Random fun fact\n"
        "`/joke`           · Random joke\n"
        "`/quote`          · Inspirational quote\n"
        "`/wouldyourather` · Would you rather…?\n"
        "`/thisorthat`     · This or that?\n"
        "`/truthordare`    · Truth or Dare\n"
        "`/story`          · Story starter prompt"
    ))
    e.add_field(name="📊 Profile & Economy", inline=False, value=(
        "`/profile`     · Your full profile card\n"
        "`/stats`       · Detailed game stats\n"
        "`/leaderboard` · Server leaderboards\n"
        "`/daily`       · Claim your daily coins\n"
        "`/balance`     · Check your coin balance"
    ))
    e.set_footer(text=f"Gingery v{VERSION} • Games award coins & XP!")
    await interaction.response.send_message(embed=e)


@bot.tree.command(name="invite", description="Invite Gingery to your server.")
async def invite(interaction: discord.Interaction):
    log.info(f"/invite — {interaction.user}")
    e = embed("🤖 Invite Gingery", f"[Click here to invite the bot!]({INVITE_URL})")
    await interaction.response.send_message(embed=e, view=links_view())

# ════════════════════════════════════════════════════════════
#   RANDOM / FUN COMMANDS  (no DB tracking needed)
# ════════════════════════════════════════════════════════════

@bot.tree.command(name="8ball", description="Ask the magic 8-ball a question.")
@app_commands.describe(question="Your yes/no question")
async def ball(interaction: discord.Interaction, question: str):
    log.info(f"/8ball — {interaction.user}")
    e = embed("🎱 Magic 8-Ball", f"**You asked:** {question}\n\n🔮 {random.choice(EIGHT_BALL)}")
    await interaction.response.send_message(embed=e)
    await maybe_promo(interaction)


@bot.tree.command(name="rolladice", description="Roll a six-sided dice.")
async def rolladice(interaction: discord.Interaction):
    log.info(f"/rolladice — {interaction.user}")
    result = random.randint(1, 6)
    faces  = {1:"⚀",2:"⚁",3:"⚂",4:"⚃",5:"⚄",6:"⚅"}
    e = embed("🎲 Dice Roll", f"{interaction.user.mention} rolled a **{result}** {faces[result]}")
    await interaction.response.send_message(embed=e)
    await maybe_promo(interaction)


@bot.tree.command(name="coinflip", description="Flip a coin.")
async def coinflip(interaction: discord.Interaction):
    log.info(f"/coinflip — {interaction.user}")
    result = random.choice(["Heads 🪙", "Tails 🔄"])
    e = embed("🪙 Coin Flip", f"{interaction.user.mention} flipped **{result}**!")
    await interaction.response.send_message(embed=e)
    await maybe_promo(interaction)


@bot.tree.command(name="fact", description="Get a random fun fact.")
async def fact(interaction: discord.Interaction):
    e = embed("💡 Fun Fact", random.choice(FACTS))
    await interaction.response.send_message(embed=e)
    await maybe_promo(interaction)


@bot.tree.command(name="joke", description="Get a random joke.")
async def joke(interaction: discord.Interaction):
    e = embed("😂 Joke", random.choice(JOKES))
    await interaction.response.send_message(embed=e)
    await maybe_promo(interaction)


@bot.tree.command(name="quote", description="Get an inspirational quote.")
async def quote(interaction: discord.Interaction):
    e = embed("✨ Quote", f"_{random.choice(QUOTES)}_")
    await interaction.response.send_message(embed=e)
    await maybe_promo(interaction)


@bot.tree.command(name="story", description="Get a story-starter prompt.")
async def story(interaction: discord.Interaction):
    e = embed("📖 Story Starter", random.choice(STORY_PROMPTS))
    e.set_footer(text="Continue the story by typing your next sentence!")
    await interaction.response.send_message(embed=e)
    await maybe_promo(interaction)


@bot.tree.command(name="truthordare", description="Get a Truth or a Dare.")
@app_commands.describe(choice="Choose truth or dare")
@app_commands.choices(choice=[
    app_commands.Choice(name="Truth", value="truth"),
    app_commands.Choice(name="Dare",  value="dare"),
])
async def truthordare(interaction: discord.Interaction, choice: app_commands.Choice[str]):
    if choice.value == "truth":
        e = embed("🤔 Truth", random.choice(TRUTHS))
    else:
        e = embed("😈 Dare", random.choice(DARES))
    await interaction.response.send_message(embed=e)
    await maybe_promo(interaction)


@bot.tree.command(name="wouldyourather", description="A Would You Rather question.")
async def wyr(interaction: discord.Interaction):
    a, b = random.choice(WOULD_YOU_RATHER)
    e = discord.Embed(title="🤷 Would You Rather…?", color=BOT_COLOR)
    e.add_field(name="Option A 🅰️", value=a, inline=False)
    e.add_field(name="Option B 🅱️", value=b, inline=False)
    await interaction.response.send_message(embed=e)
    await maybe_promo(interaction)


@bot.tree.command(name="thisorthat", description="A This or That question.")
async def thisorthat(interaction: discord.Interaction):
    e = embed("❓ This or That?", random.choice(THIS_OR_THAT))
    await interaction.response.send_message(embed=e)
    await maybe_promo(interaction)

# ════════════════════════════════════════════════════════════
#   GAME COMMANDS  (DB-tracked)
# ════════════════════════════════════════════════════════════

@bot.tree.command(name="trivia", description="Answer a trivia question and earn coins.")
async def trivia(interaction: discord.Interaction):
    log.info(f"/trivia — {interaction.user}")
    item = random.choice(TRIVIA)
    e = embed("🧠 Trivia", f"**{item['q']}**\n\nYou have **30 seconds** to answer!")
    e.set_footer(text="Type your answer in this channel.")
    await interaction.response.send_message(embed=e)

    def check(m):
        return m.author == interaction.user and m.channel == interaction.channel

    try:
        msg = await bot.wait_for("message", check=check, timeout=30)
    except asyncio.TimeoutError:
        await interaction.followup.send(embed=embed(
            "⏰ Time's Up!", f"The answer was **{item['a']}**.", color=0xE74C3C
        ))
        return

    won = msg.content.strip().lower() == item["a"].lower()
    c, x = record_game(
        interaction.user.id, interaction.guild_id, str(interaction.user),
        "trivia_played", "trivia_wins", won
    )

    if won:
        await interaction.followup.send(embed=embed(
            "✅ Correct!",
            f"The answer was **{item['a']}**. Great job!" + reward_line(c, x),
            color=0x2ECC71,
        ))
    else:
        await interaction.followup.send(embed=embed(
            "❌ Incorrect",
            f"Your answer: `{msg.content}`\nCorrect answer: **{item['a']}**" + reward_line(c, x),
            color=0xE74C3C,
        ))
    await maybe_promo(interaction)


@bot.tree.command(name="riddle", description="Solve a riddle and earn coins.")
async def riddle(interaction: discord.Interaction):
    log.info(f"/riddle — {interaction.user}")
    item = random.choice(RIDDLES)
    e = embed("🔍 Riddle", f"_{item['q']}_\n\nYou have **30 seconds**!")
    e.set_footer(text="Type your answer in this channel.")
    await interaction.response.send_message(embed=e)

    def check(m):
        return m.author == interaction.user and m.channel == interaction.channel

    try:
        msg = await bot.wait_for("message", check=check, timeout=30)
    except asyncio.TimeoutError:
        await interaction.followup.send(embed=embed(
            "⏰ Time's Up!", f"The answer was **{item['a']}**.", color=0xE74C3C
        ))
        return

    won = msg.content.strip().lower() == item["a"].lower()
    c, x = record_game(
        interaction.user.id, interaction.guild_id, str(interaction.user),
        "riddle_played", "riddle_wins", won
    )

    if won:
        await interaction.followup.send(embed=embed(
            "✅ Correct!",
            f"The answer was **{item['a']}**. Very clever!" + reward_line(c, x),
            color=0x2ECC71,
        ))
    else:
        await interaction.followup.send(embed=embed(
            "❌ Incorrect",
            f"Your answer: `{msg.content}`\nCorrect answer: **{item['a']}**" + reward_line(c, x),
            color=0xE74C3C,
        ))
    await maybe_promo(interaction)


@bot.tree.command(name="rockpaperscissors", description="Play Rock Paper Scissors vs the bot.")
@app_commands.choices(choice=[
    app_commands.Choice(name="Rock",     value="rock"),
    app_commands.Choice(name="Paper",    value="paper"),
    app_commands.Choice(name="Scissors", value="scissors"),
])
async def rps(interaction: discord.Interaction, choice: app_commands.Choice[str]):
    log.info(f"/rps — {interaction.user}")
    bot_pick = random.choice(list(BEATS))
    player   = choice.value
    line = (
        f"{interaction.user.mention} chose **{player.title()}** {RPS_EMOJI[player]}\n"
        f"I chose **{bot_pick.title()}** {RPS_EMOJI[bot_pick]}\n\n"
    )

    if player == bot_pick:
        title = "🤝 It's a Tie!"
        line += "Nobody wins this round."
        won   = False
    elif BEATS[player] == bot_pick:
        title = "🏆 You Win!"
        line += "Well played!"
        won   = True
    else:
        title = "💀 You Lose!"
        line += "Better luck next time!"
        won   = False

    await interaction.response.defer()
    c, x = record_game(
        interaction.user.id, interaction.guild_id, str(interaction.user),
        "rps_played", "rps_wins", won
    )
    await interaction.followup.send(embed=embed(title, line + reward_line(c, x)))
    await maybe_promo(interaction)


@bot.tree.command(name="highlow", description="Guess the number within 7 attempts.")
async def highlow(interaction: discord.Interaction):
    log.info(f"/highlow — {interaction.user}")
    number = random.randint(1, 100)

    e = embed(
        "🔢 Guess the Number!",
        "I'm thinking of a number between **1** and **100**.\n"
        "You have **7 attempts** and **30 s** per guess."
    )
    await interaction.response.send_message(embed=e)
    db.ensure_user(interaction.user.id, interaction.guild_id, str(interaction.user))

    def check(m):
        return m.author == interaction.user and m.channel == interaction.channel

    won = False
    for attempt in range(1, 8):
        try:
            msg   = await bot.wait_for("message", check=check, timeout=30)
            guess = int(msg.content.strip())
        except asyncio.TimeoutError:
            await interaction.followup.send(embed=embed(
                "⏰ Time's Up!", f"The number was **{number}**.", color=0xE74C3C
            ))
            return
        except ValueError:
            await interaction.followup.send("Please enter a valid whole number.")
            continue

        remaining = 7 - attempt
        if guess < number:
            await interaction.followup.send(f"📈 **Too low!** ({remaining} attempt(s) left)")
        elif guess > number:
            await interaction.followup.send(f"📉 **Too high!** ({remaining} attempt(s) left)")
        else:
            won = True
            c, x = record_game(
                interaction.user.id, interaction.guild_id, str(interaction.user),
                "highlow_played", "highlow_wins", True
            )
            await interaction.followup.send(embed=embed(
                "🏆 You Win!",
                f"You guessed **{number}** in {attempt} attempt(s)!" + reward_line(c, x),
                color=0x2ECC71,
            ))
            await maybe_promo(interaction)
            return

    c, x = record_game(
        interaction.user.id, interaction.guild_id, str(interaction.user),
        "highlow_played", None, False
    )
    await interaction.followup.send(embed=embed(
        "💀 Out of Attempts!",
        f"The number was **{number}**." + reward_line(c, x),
        color=0xE74C3C,
    ))
    await maybe_promo(interaction)


@bot.tree.command(name="scramble", description="Unscramble a word and earn coins.")
async def scramble(interaction: discord.Interaction):
    log.info(f"/scramble — {interaction.user}")
    word    = random.choice(SCRAMBLE_WORDS)
    jumbled = list(word)
    while "".join(jumbled) == word:
        random.shuffle(jumbled)
    scrambled_word = "".join(jumbled)

    e = embed("🔀 Word Scramble", f"Unscramble this: **`{scrambled_word}`**\n\nYou have **30 seconds**!")
    await interaction.response.send_message(embed=e)

    def check(m):
        return m.author == interaction.user and m.channel == interaction.channel

    try:
        msg = await bot.wait_for("message", check=check, timeout=30)
    except asyncio.TimeoutError:
        await interaction.followup.send(embed=embed(
            "⏰ Time's Up!", f"The word was **{word}**.", color=0xE74C3C
        ))
        return

    won = msg.content.strip().lower() == word
    c, x = record_game(
        interaction.user.id, interaction.guild_id, str(interaction.user),
        "scramble_played", "scramble_wins", won
    )

    if won:
        await interaction.followup.send(embed=embed(
            "✅ Correct!", f"The word was **{word}**. Nice one!" + reward_line(c, x), color=0x2ECC71
        ))
    else:
        await interaction.followup.send(embed=embed(
            "❌ Wrong!", f"Your answer: `{msg.content}`\nThe word was: **{word}**" + reward_line(c, x),
            color=0xE74C3C,
        ))
    await maybe_promo(interaction)


_cp_timers: dict = {}

@bot.tree.command(name="copypaste", description="Type a sentence as fast as possible.")
async def copypaste(interaction: discord.Interaction):
    log.info(f"/copypaste — {interaction.user}")
    sentence = random.choice(COPY_PASTE_SENTENCES)

    e = embed(
        "⌨️ Copy-Paste Challenge",
        f"Type this sentence as fast as you can:\n\n> {sentence}\n\nYou have **30 seconds**."
    )
    await interaction.response.send_message(embed=e)
    db.ensure_user(interaction.user.id, interaction.guild_id, str(interaction.user))
    _cp_timers[interaction.user.id] = time.perf_counter()

    def check(m):
        return m.author == interaction.user and m.channel == interaction.channel

    try:
        msg = await bot.wait_for("message", check=check, timeout=30)
    except asyncio.TimeoutError:
        _cp_timers.pop(interaction.user.id, None)
        await interaction.followup.send(embed=embed(
            "⏰ Time's Up!", "You ran out of time.", color=0xE74C3C
        ))
        return

    elapsed = time.perf_counter() - _cp_timers.pop(interaction.user.id, time.perf_counter())
    db.increment_stat(interaction.user.id, interaction.guild_id, "copypaste_played")

    if msg.content.strip() == sentence:
        is_pb = db.update_best_copypaste(interaction.user.id, interaction.guild_id, elapsed)
        c, x  = COINS["win"], XP["win"]
        db.increment_stat(interaction.user.id, interaction.guild_id, "coins",    c)
        db.increment_stat(interaction.user.id, interaction.guild_id, "total_xp", x)

        pb_line = "\n🏅 **New personal best!**" if is_pb else ""
        await interaction.followup.send(embed=embed(
            "✅ Correct!",
            f"You typed it in **{elapsed:.3f} seconds**! 🚀{pb_line}" + reward_line(c, x),
            color=0x2ECC71,
        ))
    else:
        await interaction.followup.send(embed=embed(
            "❌ Wrong!",
            f"That wasn't quite right.\n\nExpected:\n> {sentence}",
            color=0xE74C3C,
        ))
    await maybe_promo(interaction)

# ════════════════════════════════════════════════════════════
#   PROFILE & ECONOMY
# ════════════════════════════════════════════════════════════

@bot.tree.command(name="profile", description="View your full Gingery profile card.")
@app_commands.describe(member="The user to look up (defaults to you)")
async def profile(interaction: discord.Interaction, member: discord.Member = None):
    target = member or interaction.user
    log.info(f"/profile — {interaction.user} → {target}")
    await interaction.response.defer()

    db.ensure_user(target.id, interaction.guild_id, str(target))
    row = db.get_stats(target.id, interaction.guild_id)
    if not row:
        await interaction.followup.send("Could not load profile. Play a game first!", ephemeral=True)
        return

    level, xp_in, xp_next = xp_to_level(row["total_xp"])
    bar_filled = round((xp_in / xp_next) * 10)
    bar = "█" * bar_filled + "░" * (10 - bar_filled)

    total_wins   = row["trivia_wins"] + row["highlow_wins"] + row["scramble_wins"] + row["rps_wins"] + row["riddle_wins"]
    total_played = row["trivia_played"] + row["highlow_played"] + row["scramble_played"] + row["rps_played"] + row["riddle_played"]

    e = discord.Embed(title=f"🎮 {target.display_name}'s Profile", color=BOT_COLOR)
    e.set_thumbnail(url=target.display_avatar.url)
    e.add_field(name="⭐ Level",   value=f"**{level}** `[{bar}]`\n{xp_in}/{xp_next} XP", inline=False)
    e.add_field(name="🪙 Coins",   value=f"**{row['coins']:,}**",      inline=True)
    e.add_field(name="⭐ Total XP",value=f"**{row['total_xp']:,}**",   inline=True)
    e.add_field(name="🏆 Overall", value=f"{total_wins}W / {total_played}P ({pct(total_wins, total_played)})", inline=True)
    e.add_field(name="🧠 Trivia",  value=f"{row['trivia_wins']}W / {row['trivia_played']}P",     inline=True)
    e.add_field(name="🔍 Riddle",  value=f"{row['riddle_wins']}W / {row['riddle_played']}P",     inline=True)
    e.add_field(name="🔢 HighLow", value=f"{row['highlow_wins']}W / {row['highlow_played']}P",   inline=True)
    e.add_field(name="🔀 Scramble",value=f"{row['scramble_wins']}W / {row['scramble_played']}P", inline=True)
    e.add_field(name="✂️ RPS",     value=f"{row['rps_wins']}W / {row['rps_played']}P",           inline=True)
    if row["best_copypaste"] and row["best_copypaste"] > 0:
        e.add_field(name="⌨️ Best Typing", value=f"{row['best_copypaste']:.3f}s", inline=True)
    e.set_footer(text=f"Member since {row['joined_at'].strftime('%d %b %Y')} · Gingery v{VERSION}")
    await interaction.followup.send(embed=e)


@bot.tree.command(name="stats", description="View detailed game stats.")
@app_commands.describe(member="The user to look up (defaults to you)")
async def stats(interaction: discord.Interaction, member: discord.Member = None):
    target = member or interaction.user
    log.info(f"/stats — {interaction.user} → {target}")
    await interaction.response.defer()

    db.ensure_user(target.id, interaction.guild_id, str(target))
    row = db.get_stats(target.id, interaction.guild_id)
    if not row:
        await interaction.followup.send("No stats yet — play some games first!", ephemeral=True)
        return

    e = discord.Embed(title=f"📊 {target.display_name}'s Stats", color=BOT_COLOR)
    e.set_thumbnail(url=target.display_avatar.url)
    e.add_field(name="🧠 Trivia",   value=f"{row['trivia_wins']}W / {row['trivia_played']}P\n({pct(row['trivia_wins'],   row['trivia_played'])} win rate)",   inline=True)
    e.add_field(name="🔍 Riddle",   value=f"{row['riddle_wins']}W / {row['riddle_played']}P\n({pct(row['riddle_wins'],   row['riddle_played'])} win rate)",   inline=True)
    e.add_field(name="🔢 High-Low", value=f"{row['highlow_wins']}W / {row['highlow_played']}P\n({pct(row['highlow_wins'], row['highlow_played'])} win rate)", inline=True)
    e.add_field(name="🔀 Scramble", value=f"{row['scramble_wins']}W / {row['scramble_played']}P\n({pct(row['scramble_wins'],row['scramble_played'])} win rate)",inline=True)
    e.add_field(name="✂️ RPS",      value=f"{row['rps_wins']}W / {row['rps_played']}P\n({pct(row['rps_wins'],       row['rps_played'])} win rate)",      inline=True)
    if row["best_copypaste"] and row["best_copypaste"] > 0:
        e.add_field(name="⌨️ Best Typing", value=f"{row['best_copypaste']:.3f}s\n({row['copypaste_played']} runs)", inline=True)
    e.add_field(name="🪙 Coins",    value=f"{row['coins']:,}",    inline=True)
    e.add_field(name="⭐ Total XP", value=f"{row['total_xp']:,}", inline=True)
    e.set_footer(text=f"Gingery v{VERSION}")
    await interaction.followup.send(embed=e)


@bot.tree.command(name="balance", description="Check your coin balance.")
@app_commands.describe(member="The user to check (defaults to you)")
async def balance(interaction: discord.Interaction, member: discord.Member = None):
    log.info(f"/balance — {interaction.user}")
    target = member or interaction.user
    await interaction.response.defer()
    db.ensure_user(target.id, interaction.guild_id, str(target))
    row = db.get_stats(target.id, interaction.guild_id)
    coins = row["coins"] if row else 0
    e = embed("🪙 Coin Balance", f"{target.mention} has **{coins:,} coins**.")
    await interaction.followup.send(embed=e)


@bot.tree.command(name="daily", description="Claim your daily coins reward.")
async def daily(interaction: discord.Interaction):
    log.info(f"/daily — {interaction.user}")
    await interaction.response.defer()
    db.ensure_user(interaction.user.id, interaction.guild_id, str(interaction.user))
    result = db.claim_daily(interaction.user.id, interaction.guild_id)

    if result["claimed"]:
        streak  = result["streak"]
        coins_  = result["coins"]
        fire    = "🔥 " if streak > 1 else ""
        e = embed(
            "🎁 Daily Reward Claimed!",
            f"You received **{coins_:,} coins**!\n\n"
            f"{fire}**Streak: {streak} day(s)**\n"
            f"_Longer streaks = more coins (up to 500/day)_",
            color=0x2ECC71,
        )
        e.set_footer(text="Come back tomorrow to keep your streak!")
    else:
        e = embed(
            "⏳ Already Claimed",
            f"You already claimed your daily reward today.\n"
            f"Come back **tomorrow** to continue your {result['streak']}-day streak!",
            color=0xE74C3C,
        )
    await interaction.followup.send(embed=e)

# ════════════════════════════════════════════════════════════
#   LEADERBOARD
# ════════════════════════════════════════════════════════════

@bot.tree.command(name="leaderboard", description="View the server leaderboard.")
@app_commands.describe(category="Which stat to rank by")
@app_commands.choices(category=[
    app_commands.Choice(name="🪙 Coins",          value="coins"),
    app_commands.Choice(name="⭐ Total XP",        value="total_xp"),
    app_commands.Choice(name="🧠 Trivia Wins",     value="trivia"),
    app_commands.Choice(name="🔍 Riddle Wins",     value="riddle"),
    app_commands.Choice(name="🔢 High-Low Wins",   value="highlow"),
    app_commands.Choice(name="🔀 Scramble Wins",   value="scramble"),
    app_commands.Choice(name="✂️ RPS Wins",        value="rps"),
    app_commands.Choice(name="⌨️ Best Typing",     value="copypaste"),
])
async def leaderboard(interaction: discord.Interaction, category: app_commands.Choice[str] = None):
    cat = category.value if category else "coins"
    log.info(f"/leaderboard ({cat}) — {interaction.user}")
    await interaction.response.defer()

    rows, label = db.get_leaderboard(interaction.guild_id, cat, limit=10)
    user_rank   = db.get_rank(interaction.user.id, interaction.guild_id, cat)

    if not rows:
        await interaction.followup.send(
            embed=embed("📊 Leaderboard", "No data yet — play some games first!"),
            ephemeral=True,
        )
        return

    medals = {1: "🥇", 2: "🥈", 3: "🥉"}
    lines  = []
    for row in rows:
        rank   = row["rank"]
        medal  = medals.get(rank, f"`#{rank}`")
        value  = f"{row['value']:.3f}s" if cat == "copypaste" else f"{int(row['value']):,}"
        lines.append(f"{medal} **{row['username']}** — {value}")

    desc = "\n".join(lines)
    if user_rank:
        desc += f"\n\n_Your rank: **#{user_rank}**_"

    e = embed(f"🏆 {label} Leaderboard", desc)
    e.set_footer(text=f"{interaction.guild.name} · Gingery v{VERSION}")
    await interaction.followup.send(embed=e)

# ════════════════════════════════════════════════════════════
#   ADMIN COMMANDS
# ════════════════════════════════════════════════════════════

@bot.tree.command(name="dbtest", description="[Admin] Test the database connection.")
@app_commands.checks.has_permissions(administrator=True)
async def dbtest(interaction: discord.Interaction):
    log.info(f"/dbtest — {interaction.user}")
    await interaction.response.defer(ephemeral=True)
    ok, info = db.ping()
    if ok:
        e = discord.Embed(title="✅ Database Connected", description=f"**Server:** {info}", color=0x2ECC71)
    else:
        e = discord.Embed(title="❌ Database Error", description=f"`{info}`", color=0xE74C3C)
    await interaction.followup.send(embed=e, ephemeral=True)

# ── Run ───────────────────────────────────────────────────────
bot.run(os.environ["TESTTOKEN"])