import os
import discord
from discord.ext import tasks, commands
from datetime import datetime
import pytz

# Config
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("POST_CHANNEL_ID"))
TIMEZONE = os.getenv("TIMEZONE", "Europe/Rome")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot connesso come {bot.user}")
    daily_task.start()

@tasks.loop(minutes=1)
async def daily_task():
    now = datetime.now(pytz.timezone(TIMEZONE))
    # Controlla se è 17:30
    if now.hour == 17 and now.minute == 30:
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            await channel.send("📊 Ecco le statistiche giornaliere (demo)!")
        else:
            print("❌ Canale non trovato")

bot.run(DISCORD_TOKEN)
