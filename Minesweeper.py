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

import random
import discord
import asyncio
from discord.ext import commands


discord_emojis = dict()
discord_emojis[0] = "<:bl:593002788141924362>"
discord_emojis[1] = "<:m1:593002785608433672>"
discord_emojis[2] = '<:m2:593002786203893760>'
discord_emojis[3] = '<:m3:593002786250162197>'
discord_emojis[4] = '<:m4:593002786531049472>'
discord_emojis[5] = '<:m5:593002786828845066>'
discord_emojis[6] = '<:m6:593002786745090084>'
discord_emojis[7] = '<:m7:593002787684614160>'
discord_emojis[8] = '<:m8:593002788221485060>'
discord_emojis['*'] = ':bomb:'
discord_emojis['hidden'] = '<:hi:593049329455988736>'
discord_emojis['hidden_selected'] = '<:hs:593049277425778688>'
discord_emojis['flag'] = '<:fh:593000706882011146>'
discord_emojis['flag_selected'] = '<:fs:593050119830634496>'
discord_emojis['no_flag'] = '<:nf:594096281287131166>'
discord_emojis['reveal'] = '<:ms_reveal_action:593000706760507413>'
discord_emojis['flag_action'] = '<:flag_action:593049972799176726>'
discord_emojis['mine_revealed'] = '<:go:593091244041830400>'
discord_emojis['mine_not_found'] = '<:mn:593099503683239936>'



def print_grid(grid): #Debug Grid print
    resultat = ""
    for l in grid:
        for t in l:
            resultat += str(t)
        resultat += '\n'
    return resultat

def print_discord(grid, gtype):
    resultat = ""
    resultat += "Grid:\n"
    for l in grid:
        for t in l:
            if gtype == 'spoiler':
                resultat += '||'+discord_emojis[t]+'||'
            elif gtype == 'interactive':
                resultat += discord_emojis[t]
        resultat += '\n'
    return resultat

def generate_grid(size: int):
    return [[0 for i in range(size)] for i in range(size)]

def generate_grid_public(size: int):
    return [['hidden' for i in range(size)] for i in range(size)]

def mines(grid, nb_mines):
    remaining_tiles=[(nb//len(grid),nb%len(grid)) for nb in range(len(grid)**2)]
    for i in range(int(nb_mines)):
        ligne, colonne = remaining_tiles.pop(random.randint(0,(len(grid)*len(grid))-1-i))
        grid[ligne][colonne] = 1
    return None

def extract(grid, tile):
    l, t = tile
    resultat = 0
    for line in range(max(l-1,0),1 + min(l+1,len(grid)-1)):
        for tile in range(max(t-1,0),1 + min(t+1,len(grid)-1)):
            if grid[l][t] == 1:
                return '*'
            else:
                resultat += grid[line][tile]
    return resultat

def calculate(grid):
    calcul_grid = generate_grid(len(grid))
    for line in range(len(grid)):
        for tile in range(len(grid)):
            calcul_grid[line][tile] = extract(grid, (line, tile))
    return calcul_grid

def look_for_zeros(grid, grid_pub, tile, win_rules):
    l, t = tile
    if grid[l][t] != 0:
        return
    tiles_done = []
    tiles_todo = []
    tiles_todo.append((l, t))
    while len(tiles_todo) > 0:
        l, t = tiles_todo.pop(0)
        for line in range(max(l-1,0),1 + min(l+1,len(grid)-1)):
            for tile in range(max(t-1,0),1 + min(t+1,len(grid)-1)):
                if grid[line][tile] == 0:
                    if (line, tile) not in tiles_done:
                        tiles_todo.append((line, tile))
                        tiles_done.append((line, tile))
                if grid_pub[line][tile] == 'hidden':
                    win_rules['tiles_left']-=1
                if grid_pub[line][tile] == 'flag':
                    win_rules['flags_wrong'] -= 1
                    win_rules['tiles_left'] -= 1
                grid_pub[line][tile] = grid[line][tile]
    return grid, grid_pub, win_rules

def reveal_process(grid, grid_priv, tile, win_rules):
    l, t = tile
    if grid[l][t] == 'flag':
        if grid_priv[l][t] != '*':
            win_rules['flags_wrong'] -= 1
    if grid_priv[l][t] == 0:
        grid_priv, grid, win_rules = look_for_zeros(grid_priv, grid, (l, t), win_rules)
    elif grid_priv[l][t] == '*':
        win_rules['mine_revealed'] = [True, (l, t)]
    else:
        grid[l][t] = grid_priv[l][t]
        win_rules['tiles_left'] -= 1

    return grid, grid_priv, win_rules


def flag_action(grid, grid_priv, tile, win_rules):
    l, t = tile
    grid[l][t] = 'flag'
    if grid_priv[l][t] == '*':
        win_rules['flags_right'] -= 1
    else:
        win_rules['flags_wrong'] += 1

    return grid, grid_priv, win_rules


def gameover_show(grid, grid_priv, tile):
    ligne, colonne = tile
    grid[ligne][colonne] = 'mine_revealed'
    resultat = "Grid:\n"
    for l in range(len(grid)):
        for t in range(len(grid)):
            if grid[l][t] == 'mine_revealed':
                resultat += discord_emojis['mine_revealed']
            elif grid_priv[l][t] == '*':
                if grid[l][t] == 'flag':
                    resultat += discord_emojis['flag']
                else:
                    resultat += discord_emojis['mine_not_found']
            elif grid[l][t] == 'flag':
                if grid_priv[l][t] != '*':
                    resultat += discord_emojis['no_flag']
            else:
                resultat += discord_emojis[grid[l][t]]
        resultat += '\n'
    return resultat

def win_show(grid, grid_priv):
    resultat = "Grid:\n"
    for l in range(len(grid)):
        for t in range(len(grid)):
            if grid_priv[l][t] == '*':
                resultat += discord_emojis['flag']
            else:
                resultat += discord_emojis[grid_priv[l][t]]


class Minesweeper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    
    @commands.command(name='minesweeper', aliases=['msgame', 'minegame'])
    async def _minesweeper(self, ctx, nb_mines=None):
        game_ask = await ctx.send(f"Would you want to play **spoiler version** {discord_emojis['hidden']} or **interactive version** {discord_emojis['reveal']} ?")
        await game_ask.add_reaction(discord_emojis['reveal'])
        await game_ask.add_reaction(discord_emojis['hidden'])

        def game_ask_check(reaction):
            if reaction.user_id == ctx.author.id and str(reaction.emoji) == str(discord_emojis["reveal"]) and reaction.message_id == game_ask.id:
                return "Interactive"
            elif reaction.user_id == ctx.author.id and str(reaction.emoji) == str(discord_emojis['hidden']) and reaction.message_id == game_ask.id:
                return "Classic"

        choice = None
        try:
            reaction = await self.bot.wait_for('raw_reaction_add', timeout=60.0, check=game_ask_check)
            choice = reaction
        except asyncio.TimeoutError:
            await ctx.send(f"{ctx.author.mention} took too many time to respond. Game request cancelled")
            return
        else:
            if str(choice.emoji) == discord_emojis['hidden']:
                try:
                    if int(nb_mines) > 45 or int(nb_mines) < 12:
                        await ctx.send("Number of mines should be between 12 and 45. Randomizing amount...")
                        nb_mines = random.randint(12,45)
                except Exception:
                    await ctx.send("Number of mines not given. Randomizing between 12 and 45...")
                    nb_mines = random.randint(12,45)
                base = generate_grid(9)
                mines(base, nb_mines)
                priv = calculate(base)
                await ctx.send(print_discord(priv, 'spoiler'))
                return
            elif str(choice.emoji) == discord_emojis['reveal']:
                try:
                    if int(nb_mines) > 45 or int(nb_mines) < 12:
                        await ctx.send("Number of mines should be between 12 and 45. Randomizing amount...")
                        nb_mines = random.randint(12,45)
                except Exception:
                    await ctx.send("Number of mines not given. Randomizing between 12 and 45...")
                    nb_mines = random.randint(12,45)
                base = generate_grid(9)
                mines(base, nb_mines)
                priv = calculate(base)
                public = generate_grid_public(9)
                game_board = await ctx.send("Preparing board...")
                await ctx.send("Send me tile coordinates (must look like this: `1,1` ; `9,9` ; `5,7` ; `y,x` ; etc...)\nDon't forget to read the **minesweeper rules** before playing.\nTo stop playing, type `cancel` or `stop`. Please note that **your game won't be resumed later if you stop playing**.\nYou can pause the game by doing `pause`. This allows you to \"save your game\" up to 10 minutes. After this time limit, your game will be deleted.")
                    
                print(print_grid(priv))

                def coordinates_wait(m):
                    return m.author == ctx.author and m.channel == ctx.message.channel

                win_rules = dict()
                win_rules["tiles_left"] = 81-int(nb_mines)
                win_rules["flags_right"] = int(nb_mines)
                win_rules["flags_wrong"] = 0
                win_rules['mine_revealed'] = [False, (0, 0)]
                while True:
                    print(win_rules)
                    if win_rules['mine_revealed'][0] == True:
                        await game_board.edit(content=gameover_show(public, priv, win_rules['mine_revealed'][1]))
                        await ctx.send("Game over")
                        return
                    await game_board.edit(content=print_discord(public, 'interactive'))

                    message = None
                    try:
                        m = await self.bot.wait_for('message', timeout=180.0, check=coordinates_wait)
                        message = m
                    except asyncio.TimeoutError:
                        await ctx.send(f"{ctx.author.mention} took too many time to respond. Game stopped.")
                        return
                    if message.content == "pause":
                        pause_msg = await ctx.send("Game has been paused. You have 10 minutes before the game is cancelled/stopped.")
                        def pause_game_check(reaction):
                            return reaction.user_id == ctx.author.id and str(reaction.emoji.name) == '✅' and pause_msg.id == reaction.message_id
                        await pause_msg.add_reaction('✅')
                        try:
                            m = await self.bot.wait_for('raw_reaction_add', timeout=600.0, check=pause_game_check)
                            await pause_msg.delete()
                        except asyncio.TimeoutError:
                            await pause_msg.edit(content=f"{ctx.author.mention}, your pause time has exceeded 10 minutes. Your game has been cancelled to save bot memory.")
                            return
                    elif message.content == "stop" or message.content == "cancel":
                        await ctx.send(f"{ctx.author.mention}, your game has been stopped.")
                        return
                    else:
                        try:
                            ligne, nani, colonne = tuple(message.content)
                            ligne = int(ligne) - 1
                            colonne = int(colonne) - 1
                            if ligne > 8 or colonne > 8 or ligne < 0 or colonne < 0:
                                raise Exception
                            await message.delete()
                        except Exception:
                            nope_message = await ctx.send("Invalid user input")
                            await asyncio.sleep(2)
                            await nope_message.delete()
                        else:
                            if public[ligne][colonne] == priv[ligne][colonne]:
                                nope_message = await ctx.send(embed=discord.Embed(description="__You must select a **hidden** or **flagged** tile__"))
                                await asyncio.sleep(2.5)
                                await nope_message.delete()
                            elif public[ligne][colonne] == 'hidden':
                                public[ligne][colonne] = 'hidden_selected'
                                await game_board.edit(content=print_discord(public, 'interactive'))
                                embed=discord.Embed(title="What would you want to do?")
                                embed.add_field(name="Reveal tile", value=f"React with {discord_emojis['reveal']}", inline=True)
                                embed.add_field(name="Flag the tile", value=f"React with {discord_emojis['flag_action']}", inline=True)
                                embed.set_footer(text="Wrong tile? Click on the ❌ reaction!")
                                embed_choice = await ctx.send(embed=embed)
                                await embed_choice.add_reaction(discord_emojis['reveal'])
                                await embed_choice.add_reaction(discord_emojis['flag_action'])
                                await embed_choice.add_reaction('❌')
                                def action_check(reaction):
                                    if reaction.user_id == ctx.author.id and str(reaction.emoji) == discord_emojis["reveal"] and reaction.message_id == embed_choice.id:
                                        return True
                                    elif reaction.user_id == ctx.author.id and str(reaction.emoji) == discord_emojis['flag_action'] and reaction.message_id == embed_choice.id:
                                        return True
                                    elif reaction.user_id == ctx.author.id and str(reaction.emoji.name) == '❌' and reaction.message_id == embed_choice.id:
                                        return True
                                reaction = None
                                try:
                                    r = await self.bot.wait_for('raw_reaction_add', timeout=180.0, check=action_check)
                                    reaction = r
                                except asyncio.TimeoutError:
                                    await ctx.send(f"{ctx.author.mention} took too many time to respond. Game stopped.")
                                else:
                                    if str(reaction.emoji) == discord_emojis['reveal']:
                                        public, priv, win_rules = reveal_process(public, priv, (ligne, colonne), win_rules)
                                    elif str(reaction.emoji) == discord_emojis['flag_action']:
                                        public, priv, win_rules = flag_action(public, priv, (ligne, colonne), win_rules)
                                    elif str(reaction.emoji.name) == '❌':
                                        public[ligne][colonne] = 'hidden'
                                    await embed_choice.delete()

                            elif public[ligne][colonne] == 'flag':
                                public[ligne][colonne] = 'flag_selected'
                                await game_board.edit(content=print_discord(public, "interactive"))
                                embed=discord.Embed(title="What would you want to do?")
                                embed.add_field(name="Reveal tile", value=f"React with {discord_emojis['reveal']}", inline=True)
                                embed.set_footer(text="Wrong tile? Click on the ❌ reaction!")
                                embed_choice = await ctx.send(embed=embed)
                                await embed_choice.add_reaction(discord_emojis['reveal'])
                                await embed_choice.add_reaction('❌')
                                def action_check(reaction):
                                    if reaction.user_id == ctx.author.id and str(reaction.emoji) == discord_emojis["reveal"] and reaction.message_id == embed_choice.id:
                                        return True
                                    elif reaction.user_id == ctx.author.id and str(reaction.emoji.name) == '❌' and reaction.message_id == embed_choice.id:
                                        return True
                                reaction = None
                                try:
                                    r = await self.bot.wait_for('raw_reaction_add', timeout=180.0, check=action_check)
                                    reaction = r
                                except asyncio.TimeoutError:
                                    await ctx.send(f"{ctx.author.mention} took too many time to respond. Game stopped.")
                                else:
                                    if str(reaction.emoji) == discord_emojis['reveal']:
                                        public, priv, win_rules = reveal_process(public, priv, (ligne, colonne), win_rules)
                                    elif str(reaction.emoji.name) == '❌':
                                        public[ligne][colonne] = 'flag'
                                    await embed_choice.delete()
                        if win_rules['tiles_left'] == 0:
                            await ctx.send("All tiles have been revealed. Congratulations, you won!")
                            await game_board.edit(content=win_show(public, priv))
                            return
                        elif win_rules['flags_right'] == 0:
                            if win_rules['flags_wrong'] == 0:
                                await game_board.edit(content=win_show(public, priv))
                                await ctx.send("All mines have been flagged. Congratulations, you won!")
                                return









def setup(bot):
    bot.add_cog(Minesweeper(bot))
