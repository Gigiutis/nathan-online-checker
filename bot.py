import discord
import requests
import asyncio

# ====== CONFIG ======
DISCORD_TOKEN = "MTQ2NTgxMTEyNzA1MjAwOTc0NQ.G-MiDE.Yg5csObvNz_5NeOZ0OYRKKCkz5FXCrUBiOfES0"

ROBLOX_USER_ID = 4064551172
CHANNEL_ID = 1273004876040900691

PING_USERS = [
    1273004876040900691,         # Discord user ID 1
    528285160383447041,         # Discord user ID 2
    1001310599071936603          # Discord user ID 3
]
# ====================

intents = discord.Intents.default()
client = discord.Client(intents=intents)

last_status = False  # False = offline, True = online

async def check_roblox_status():
    global last_status
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)

    while not client.is_closed():
        response = requests.post(
            "https://presence.roblox.com/v1/presence/users",
            json={"userIds": [ROBLOX_USER_ID]}
        )

        presence = response.json()["userPresences"][0]["userPresenceType"]
        online = presence != 0  # 0 = offline

        if online and not last_status:
            mentions = " ".join(f"<@{uid}>" for uid in PING_USERS)
            await channel.send(f"{mentions} Roblox account is ONLINE")

        last_status = online
        await asyncio.sleep(60)  # check every 60 seconds

@client.event
async def on_ready():
    print("Bot is running")
    client.loop.create_task(check_roblox_status())

client.run(DISCORD_TOKEN)
