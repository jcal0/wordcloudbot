import discord
from discord.ext import commands
import json
import nltk
import re
import logging
import os
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)


# Initialize the NLTK data
nltk.download("punkt")

# Set up the bot client
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = commands.Bot(command_prefix="-", intents=intents)

@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")


@client.event
async def on_command_error(ctx, error):
    print(f"An error occurred: {error}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    print(f"Message received from {message.author}: {message.content}")
    print(f"Message type: {type(message.content)}")

    await client.process_commands(message)


    

# Function to process messages and create word frequency count
async def create_wordcloud(messages):
    text = ""
    for message in messages:
        if message.author == client.user:  # Skip the bot's own messages
            continue
        text += message.content + " "
    tokens = nltk.word_tokenize(text)
    
    # Filter tokens to exclude symbols, mentions, and bot commands
    filtered_tokens = [token for token in tokens if re.match(r'^[A-Za-z]+$', token) and not token.startswith('-')]

    freq_dist = nltk.FreqDist(filtered_tokens)
    top_words = freq_dist.most_common(20)
    wordcloud = ""
    for word, count in top_words:
        wordcloud += f"{word} ({count})\n"
    return wordcloud


# Function to download messages to a JSON file
def download_messages(messages):
    message_list = []
    for message in messages:
        message_dict = {
            "author": str(message.author),
            "content": message.content,
            "timestamp": str(message.created_at)
        }
        message_list.append(message_dict)
    with open("messages.json", "w") as outfile:
        json.dump(message_list, outfile)
    print("Messages downloaded to messages.json")

# Command to create a wordcloud and download messages

@client.command()
async def wordcloud(ctx):
    server_messages = []
    messages_per_channel = 100
    total_messages_scraped = 0
    for channel in ctx.guild.text_channels:
        # Check if the bot has permission to read messages in the channel
        if channel.permissions_for(ctx.guild.me).read_message_history:
            logging.info(f"Fetching messages from channel: {channel.name}")
            message_count = 0
            async for message in channel.history(limit=messages_per_channel):
                server_messages.append(message)
                message_count += 1
                total_messages_scraped +=1
            logging.info(f"Fetched {message_count} messages from channel: {channel.name}")

    wordcloud = await create_wordcloud(server_messages)
    await ctx.send(f"Top 20 words in the last {total_messages_scraped} messages:\n{wordcloud}")
    download_messages(server_messages)

@client.command()
async def ping(ctx):
    await ctx.send("Pong!")

# Run the bot with your bot token
token = os.getenv("DISCORD_BOT_TOKEN")
client.run(token)
