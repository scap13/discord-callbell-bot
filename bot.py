import discord
import requests
import asyncio
from datetime import datetime, timedelta

TOKEN_DISCORD = "IL_TUO_TOKEN_DISCORD"
CALLBELL_API_KEY = "LA_TUA_API_KEY"
CALLBELL_URL = "https://api.callbell.eu/v1/statistics/teams"  # da adattare in base al tuo caso
DISCORD_CHANNEL_ID = 123456789012345678  # ID del canale dove inviare le statistiche

intents = discord.Intents.default()
client = discord.Client(intents=intents)

async def get_callbell_stats():
    headers = {"Authorization": f"Bearer {CALLBELL_API_KEY}"}
    response = requests.get(CALLBELL_URL, headers=headers)

    if response.status_code == 200:
        data = response.json()

        # Esempio di dati (da adattare in base alla risposta reale dell’API)
        ordini = data["teams"]["ordini"]["messages_received"]
        preventivi = data["teams"]["preventivi"]["messages_received"]
        totale = ordini + preventivi
        return ordini, preventivi, totale
    else:
        print("Errore API:", response.status_code)
        return 0, 0, 0

async def send_stats():
    ordini, preventivi, totale = await get_callbell_stats()
    channel = client.get_channel(DISCORD_CHANNEL_ID)

    oggi = datetime.now().strftime("%d/%m/%Y")
    msg = (
        f"📊 **Statistiche Callbell - {oggi}**\n"
        f"• Team Ordini: **{ordini}** messaggi\n"
        f"• Team Preventivi: **{preventivi}** messaggi\n"
        f"• Totale: **{totale}** messaggi"
    )

    await channel.send(msg)

async def scheduler():
    while True:
        now = datetime.now()
        target = now.replace(hour=17, minute=30, second=0, microsecond=0)
        if now > target:
            target += timedelta(days=1)
        wait_time = (target - now).total_seconds()
        await asyncio.sleep(wait_time)
        await send_stats()

@client.event
async def on_ready():
    print(f"{client.user} connesso.")
    client.loop.create_task(scheduler())

client.run(TOKEN_DISCORD)
