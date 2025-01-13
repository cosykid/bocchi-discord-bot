import discord
import os
import random
from dotenv import load_dotenv
from discord import app_commands

# Other files
from gpt import send_request
from duel import register_duel_command

# IGNORE ALL FLASK CODE IT'S JUST THERE FOR DEPLOYMENT

from flask import Flask
import asyncio
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return 'Bot is running!'

def run_flask():
    # Get the PORT environment variable set by Render
    port = os.getenv('PORT', 5000)  # Default to 5000 if not set
    app.run(host='0.0.0.0', port=port)

#######################################################

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

load_dotenv()
TOKEN = os.getenv("TOKEN") # Discord bot token
DELETED_GIF = 'https://tenor.com/view/bocchi-the-rock-deleted-delete-i-saw-what-you-deleted-we-saw-what-you-deleted-gif-3336587386229376638'

@client.event
async def on_ready():
    register_duel_command(tree, client) # register duel command with the command tree
    await tree.sync(guild=discord.Object(id=1080458538087890965)) #sync commands to discord
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if client.user in message.mentions: 
        response = await send_request(message.content)
        await message.channel.send(response)

@client.event
async def on_message_edit(before, after):
    # Ignore if the content did not change
    if before.content == after.content:
        return
    await on_message_change (before)

@client.event
async def on_message_delete(message):
    await on_message_change (message)

# Helper function which handles both message deletion and edit events
async def on_message_change(message):
    if message.author == client.user:
        return
    
    # Catches the deleted/edited message in a 1 in 6 chance, otherwise send bocchi gif
    if random.randint(1, 6) == 3:
        await message.channel.send(f'{message.author.mention}\n> {message.content}')
    else:
        await message.channel.send(DELETED_GIF)

if __name__ == "__main__":
    # Start the Flask server in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Start the Discord bot (async)
    asyncio.run(client.run(TOKEN))
