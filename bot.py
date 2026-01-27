import discord
import requests
import asyncio
import os

# ===== LOAD ENV VARIABLES =====
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
ROBLOX_USER_ID = int(os.environ["ROBLOX_USER_ID"])
CHANNEL_ID = int(os.environ["CHANNEL_ID"])
# ==============================

# dummy placeholder Discord user IDs (replace later if you want)
PING_USERS = [
    123456789012345678,
    987654321098765432,
    555666777888999000
]

intents = discord.Intents.default()
client = discord.Client(intents=intents)

last_presence = -1
# presence values:
# 0 = offline
# 1 = online
# 2 = in game
# 3 = studio

async def check_roblox_status():
    global last_presence
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)

    while not client.is_closed():
        try:
            r = requests.post(
                "https://presence.roblox.com/v1/presence/users",
                json={"userIds": [ROBLOX_USER_ID]},
                timeout=10
            )

            presence = r.json()["userPresences"][0]["userPresenceType"]
            mentions = " ".join(f"<@{uid}>" for uid in PING_USERS)

            # went ONLINE
            if presence == 1 and last_presence != 1:
                await channel.send(f"Nathan is online {mentions}")

            # started PLAYING
            if presence == 2 and last_presence != 2:
                await channel.send(f"Nathan is playing {mentions}")

            last_presence = presence

        except Exception as e:
            print("Roblox check error:", e)

        await asyncio.sleep(60)  # check every 60 seconds

@client.event
async def on_ready():
    print("Bot running")
    client.loop.create_task(check_roblox_status())

client.run(DISCORD_TOKEN)

