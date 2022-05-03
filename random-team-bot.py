import discord
import random
import re


client = discord.Client()

champs = []
with open('champions.txt') as f:
    for line in f:
        champs.append(line.strip())

def mentions_bot_name(mentions):
    for mention in mentions:
        if mention.name == client.user.display_name:
            return True
    return False

def get_random_teams(blue, red):
    temp_champs = champs.copy()
    chosen_champs = random.sample(temp_champs, red+blue)
    red_champs, blue_champs = chosen_champs[0:blue], chosen_champs[blue:]
    return [red_champs, blue_champs]

async def handle_message(message):
    generate_game_pattern = re.compile(f"@{client.user.display_name} [1-5]v[1-5]")
    if generate_game_pattern.match(message.clean_content):
        teams = get_random_teams(int(message.clean_content[24]), int(message.clean_content[26]))
        blue_team_string = '\n'.join(teams[0])
        red_team_string = '\n'.join(teams[1])
        await message.channel.send(f'BLUE TEAM:\n{blue_team_string}')
        await message.channel.send(f'RED TEAM:\n{red_team_string}')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if len(message.mentions) > 0 and mentions_bot_name(message.mentions):
        await handle_message(message)

client.run('DISCORD_APP_KEY')
