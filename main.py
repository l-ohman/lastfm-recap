import os
from dotenv import load_dotenv
import discord
from embeds import create_embed


load_dotenv()
discord_token = os.getenv("DISCORD_TOKEN")


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if not message.content.startswith("$lastfm"):
        return
    args = message.content.split()
    embed = create_embed(args)
    await message.channel.send(embed=embed)


client.run(discord_token)
