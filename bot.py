import discord
import responses
import requests
from discord.ext import commands



def get_live_game(account_id):
    live_game_url = 'https://na1.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/'+ account_id + '?api_key=' + riot_key
    resp = requests.get(live_game_url)
    game_data = resp.json()
    participants = game_data['participants']
    return participants

riot_key = 'RGAPI-047d424c-91e8-4efa-bbcc-1db31e0b38ad'

def get_sum_info(sum_name):
    summoner_name_url = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"+ sum_name+ "?api_key="+ riot_key
    resp = requests.get(summoner_name_url)
    sum_info = resp.json()
    return sum_info

def embed(name,sum_level,profile_icon):
    Summmoner_embed = discord.Embed(title = name, description=sum_level)
    Summmoner_embed.set_thumbnail(url = profile_icon)
    return Summmoner_embed

## The following embeds are for a live game scenario
def players_embed(name, profile_icon, champ_icon, team):
    live_game = discord.Embed( title= name, description= "Team:" + str(team))
    live_game.set_thumbnail(url = profile_icon)
    live_game.set_image(url = champ_icon)
    return live_game



TOKEN ='MTEwMjY1NTUxMzYwMDIwNDk0MQ.GWFUry.84XWG3igoA_1v8esoJms2jpW1TyuEkbNYOK5is'
async def send_message(message, user_message, is_private):
    try:
        response = responses.get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


def run_discord_bot():
    TOKEN = 'MTEwMjY1NTUxMzYwMDIwNDk0MQ.GWFUry.84XWG3igoA_1v8esoJms2jpW1TyuEkbNYOK5is'
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f'{username} said: "{user_message}"({channel})')

        if user_message[0] == "#":
            user_message = user_message[1:]
            await send_message(message,user_message,is_private= True)
        if user_message[0] == '!':
            sum_name = user_message[1:]
            sum_info = get_sum_info(sum_name)
            name = sum_info['name']
            sum_level = "Level: " + str(sum_info['summonerLevel'])
            profile_icon = "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/profile-icons/" + str(
                sum_info['profileIconId']) + ".jpg"
            sum_embed = embed(name,sum_level,profile_icon)
            await message.channel.send(embed=sum_embed)

        if user_message[0:4] == 'live':

            sum_name = user_message[5:]
            sum_info = get_sum_info(sum_name)
            account_id = sum_info['id']
            participants = get_live_game(account_id)
            for player in participants:
                champ_icon = "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/" +str(player['championId']) + '.png'
                profile_icon = "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/profile-icons/" + str(
                player['profileIconId']) + ".jpg"
                team = int(player['teamId']/100)
                name = player['summonerName']
                live_game_embed = players_embed(name, profile_icon, champ_icon, team)
                await message.channel.send(embed=live_game_embed)







        else:
            await send_message(message, user_message, is_private = False)




    client.run(TOKEN)

