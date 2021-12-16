import os
import discord
import random
import requests
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()

TOKEN=os.getenv("DISCORD_TOKEN")

API_KEY =  ''

bot = commands.Bot(command_prefix="!")



@bot.command(name="game")
async def match_history(ctx, summoner_name):
    API_ENDPOINT = requests.get(f'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={API_KEY}')
    summoner_info = (API_ENDPOINT.json())
    summoner_id = summoner_info["id"]

    API_ENDPOINT2 = requests.get(f'https://na1.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{summoner_id}?api_key={API_KEY}')
    game_info = API_ENDPOINT2.json()

    blue_side_list = []
    red_side_list = []
    for i in range(len(game_info["participants"])):
        team = (game_info["participants"][i])
        if team["teamId"] == 100:
            blue_team_id = team["summonerId"]
            blue_side_list.append(blue_team_id)
        else:
            red_team_id = team["summonerId"]
            red_side_list.append(red_team_id)
    

    team_1_player_details = []
    team_2_player_details = []
    for item in blue_side_list:
        API_ENDPOINT3 = requests.get(f'https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/{item}?api_key={API_KEY}')
        player_data_blue = API_ENDPOINT3.json()
        print(player_data_blue)
        for i in range(len(player_data_blue)):
            if(player_data_blue[i]["queueType"] == "RANKED_SOLO_5x5"):
                team_1_player_details.append({"Summoner": player_data_blue[i]['summonerName'], "Tier": player_data_blue[i]["tier"], "Rank": player_data_blue[i]["rank"]})
            


    for item in red_side_list:
        API_ENDPOINT4 = requests.get(f'https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/{item}?api_key={API_KEY}')
        player_data_red = API_ENDPOINT4.json()
        for i in range(len(player_data_red)):
            
            if(player_data_red[i]["queueType"] == "RANKED_SOLO_5x5" ):
                team_2_player_details.append({"Summoner": player_data_red[i]['summonerName'], "Tier": player_data_red[i]["tier"], "Rank": player_data_red[i]["rank"]})

    print(red_side_list)

    formatted_string = "Blue Team: \n"
    for element in team_1_player_details:
        formatted_string += "Summoner Name: " + element["Summoner"] + " | " + "Rank: " + element["Tier"] + " " + element["Rank"] + "\n"
    
    formatted_string += "\nRed Team: \n"

    for element in team_2_player_details:
        formatted_string += "Summoner Name: " + element["Summoner"] + " | " + "Rank: " + element["Tier"]  + " " + element["Rank"] + "\n"

    print(formatted_string)

    resp = formatted_string
    await ctx.send(resp)

bot.run(TOKEN)

