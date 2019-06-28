 ######################################################################## 
#                                                                        #
#          ####    ###   #####   #####   #####   #####   ####            #
#          #   #    #    #       #       #   #   #   #   #   #           #
#          #   #    #    #       #       #   #   #   #   #   #           #
#          #   #    #    #####   #       #   #   #####   #   #           #
#          #   #    #        #   #       #   #   # #     #   #           #
#          #   #    #        #   #       #   #   #  #    #   #           #
#          ####    ###   #####   #####   #####   #   #   ####            #
#                                                                        #
#    #   #   #####   #####   #   #      #   #   #####   #####   #   #    #
#    #   #   #   #   #       #  ##      #   #   #       #       #  ##    #
#    #####   #####   #       ###        # # #   ####    ####    ###      #
#    #   #   #   #   #       #  ##      # # #   #       #       #  ##    #
#    #   #   #   #   #####   #   #      #####   #####   #####   #   #    #
#                                                                        #
 ######################################################################## 

import discord
from discord.ext import commands
import os

def read_file_content(file, path):
    return [i.rstrip() for i in open(os.path.join(path, file), 'r').readlines()]

def game_rule_complete(game_name):
    try:
        game_rule = read_file_content(f"{game_name}.gamerule", os.path.join(os.getcwd(), 'game_rules'))
        embed=discord.Embed(title=f"Rules - {game_rule[0]}")
    except FileNotFoundError:
        return discord.Embed(title="Rules", description="This game doesn't exist!").set_footer(text="Make sure you respect the caps of the game which you cant the rules from")
    for i in range((len(game_rule)//2)-2):
        embed.add_field(name=game_rule[(i*2)+2], value=game_rule[(i*2)+3], inline=False)
    return embed

def game_rule_list():
    path = os.path.join(os.getcwd(), 'game_rules')
    embed = discord.Embed(title="Rules - List")
    for file in os.listdir(path):
        if file.endswith('.gamerule'):
            game_rule = read_file_content(file, path)
            embed.add_field(name=game_rule[0], value=game_rule[1], inline=True)
    return embed

def help_list():
    path = os.path.join(os.getcwd(), 'help')
    embed = discord.Embed(title="Help - Command List")
    for file in os.listdir(path):
        if file.endswith('.hlp'):
            help_file = read_file_content(file, path)
            embed.add_field(name=help_file[1], value=help_file[3], inline=True)
    return embed

def help_complete(help_name):
    try:
        help_file = read_file_content(f'{help_name}.hlp', os.path.join(os.getcwd(), 'help'))
        embed = discord.Embed(title=f"{help_file[0]} - Help")
    except FileNotFoundError:
        return discord.Embed(title="Help", description="This command does not exist!")
    embed.add_field(name="Name", value=help_file[1], inline=True)
    embed.add_field(name="Aliases", value=help_file[2], inline=True)
    embed.add_field(name="Description", value=help_file[4], inline=False)
    embed.add_field(name="Syntax", value=help_file[5], inline=True)
    embed.set_footer(text="In the syntax, <> are required arguments, [] are optional")
    return embed
