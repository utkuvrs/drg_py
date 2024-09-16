import discord
import json
import os
import requests

from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Get the token from the .env file
TOKEN = os.getenv('TOKEN')

# Initialize the bot
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Function to format the JSON data into a string
def format_json(json_data):
    message = ""
    for dive_type, dive_info in json_data['Deep Dives'].items():
        message += f"**{dive_type}**\n"
        message += f"Biome: {dive_info['Biome']}\n"
        message += f"Code Name: {dive_info['CodeName']}\n"
        for stage in dive_info['Stages']:
            message += f"  Stage ID: {stage['id']}\n"
            message += f"  Length: {stage['Length']}\n"
            message += f"  Complexity: {stage['Complexity']}\n"
            message += f"  Primary Objective: {stage['PrimaryObjective']}\n"
            message += f"  Secondary Objective: {stage['SecondaryObjective']}\n"
            if 'MissionWarnings' in stage:
                message += f"  Mission Warnings: {', '.join(stage['MissionWarnings'])}\n"
            if 'MissionMutator' in stage:
                message += f"  Mission Mutator: {stage['MissionMutator']}\n"
            message += "\n"
    return message

# Event listener for when the bot has connected to Discord
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

# Event listener for when a message is sent in a channel
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Check if the message contains a URL
    if 'http' in message.content:
        try:
            # Extract the URL from the message content
            url = message.content

            # Fetch the JSON data from the URL
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad status codes
            json_data = response.json()

            # Format the fetched JSON data
            formatted_message = format_json(json_data)
            await message.channel.send(formatted_message)
        except requests.RequestException as e:
            await message.channel.send(f"Failed to fetch JSON: {e}")
        except json.JSONDecodeError:
            await message.channel.send("Failed to parse JSON")

# Run the bot
client.run(TOKEN)
