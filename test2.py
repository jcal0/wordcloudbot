import discord
from discord.ext import commands
import json
import nltk
import re
import logging
import os
from dotenv import load_dotenv
from datetime import datetime
import json
import pytz
from gptpy import eval_gm_data
from compare_dicts import compare

load_dotenv()
logging.basicConfig(level=logging.INFO)

# Initialize the NLTK data
nltk.download("punkt")

# Set up the bot client
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = commands.Bot(command_prefix="-", intents=intents)
channel_id = 1116762669232439408

@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")
    print("Executing...")

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

@client.command()
async def gmpolice(ctx):
    data, auth_lookup = await download_messages()
    #data is currently a dict

    with open("output.txt", "w") as file:
        file.write(json.dumps(data)) # writes to file as a json string

    logging.info('awaiting gpt response')
    logging_message_discord = f"```Getting today's messages from good-morning channel, and sending to ChatGPT for evaluation...```"
    await ctx.send(logging_message_discord)
    gpt_response = eval_gm_data(data)
    gpt_response_context = f"```\nGPT evaluation:\n{gpt_response}\n\n model used:gpt-3.5-turbo\n```"  
    #gpt response is a json
    gpt_response = json.loads(gpt_response)
    #now response is a dict
    logging.info(gpt_response)
    member_dict, count = members()

    # formatted_content = f"```{json.dumps(member_dict, indent=4)}```"
    # await ctx.send(formatted_content)
    # await ctx.send(f'number of members: {count}')

    processed_dict = compare(auth_lookup,gpt_response,member_dict)
    good_morning_sayers = []
    good_morning_naysayers = []
    # formattedprocessed_dict = f"```{json.dumps(member_dict, indent=4)}```"
    for key,value in processed_dict.items():
        if value:
            good_morning_sayers.append(key)
        else:
            good_morning_naysayers.append(key)

    array_sayers = "\n".join(str(item) for item in good_morning_sayers)
    formatted_sayers = f"```\nPeople who love the morning:\n\n{array_sayers}\n```"  
    await ctx.send(formatted_sayers)

    array_naysayers = "\n".join(str(item) for item in good_morning_naysayers)
    formatted_naysayers = f"```\nPeople who did NOT say Good Morning:\n\n{array_naysayers}\n```"  
    await ctx.send(formatted_naysayers)
    await ctx.send(gpt_response_context)


def members():
    member_dict = {}
    count = 0
    for guild in client.guilds:
        channel = guild.get_channel(channel_id)
        members = channel.guild.members
        for member in members:
            name = (member.name+'#'+member.discriminator)
            member_dict[name] = False
            count+=1
        break
    return member_dict, count



# Function to download messages to a JSON file
async def download_messages():
    for guild in client.guilds:
        channel = guild.get_channel(channel_id)
        if channel is not None:
            # Get the current date
            today = datetime.now(pytz.timezone('America/Los_Angeles')).date()
           
            dict = {}
            auth_lookup = {}
            # Fetch all messages in the channel
            inst = 0
            async for message in channel.history(limit=None):
                message_date = message.created_at.date()
                if message_date == today:
                    inst+=1
                    auth_lookup[inst] = str(message.author)
                    dict.update({inst:{'content':message.content, 'evaluation':''}})

            return dict, auth_lookup
        break

# Run the bot with your bot token
token = os.getenv("DISCORD_BOT_TOKEN")
client.run(token)
download_messages()
