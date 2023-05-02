import discord
import requests
import bot
from discord.ext import commands
import riot


def get_response(message:str)-> str:
    p_message = message.lower()

    if p_message == 'hello':
        return 'Shut up'





