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
import random
import asyncio

scis = '<:victory_hand:594115983728443392>'
rock = '✊'
paper = '✋'

def who_wins_round(com, player):
	"""
	1 is rock, 2 is paper, 3 is rock
	"""
	if com == "1":
		if player == "1":
			return "Rock", "Rock", "Draw"
		elif player == "2":
			return "Rock", "Paper", "You"
		elif player == "3":
			return "Rock", "Scissors", "Me"
	elif com == "2":
		if player == "1":
			return "Paper", "Rock", "Me"
		elif player == "2":
			return "Paper", "Paper", "Draw"
		elif player == "3":
			return "Paper", "Scissors", "You"
	elif com == "3":
		if player == "1":
			return "Scissors", "Rock", "You"
		if player == "2":
			return "Scissors", "Paper", "Me"
		if player == "3":
			return "Scissors", "Scissors", "Draw"

class RockPaperScissors(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command(aliases=['rockpaperscissors', 'rpsgame', 'rps_game', 'rock_paper_scissors'])
	@commands.cooldown(1, 60, type=commands.BucketType.user)
	async def rockgame(self, ctx):
		game_embed = await ctx.send(embed=discord.Embed(title="Please send me a number of points", description="The number of points should be between 3 and 30")) 
		def ask_points(message):
			return message.author == ctx.author
		
		choice = None
		try:
			message = await self.bot.wait_for('message', timeout=60.0, check=ask_points)
			choice = message
		except asyncio.TimeoutError:
			await game_embed.edit(embed=discord.Embed(title="Timeout", description="You took too many time to give me amount of points", color=discord.Colour(0xff0000)))
			return
		try:
			if int(choice.content) < 3 or int(choice.content) > 30:
				raise Exception
			points = int(choice.content)
		except Exception:
			await game_embed.edit(embed=discord.Embed(title="Points not valid", description="You gave me an incorrect number of points. I will set the number of points to 10.", color=discord.Colour(0xff0000)))
			points = 10
		await game_embed.add_reaction(rock)
		await game_embed.add_reaction(paper)
		await game_embed.add_reaction(scis)
		player = 0
		com = 0

		def round_choice(reaction):
			if reaction.emoji.name == rock:
				return reaction.user_id == ctx.author.id
			elif reaction.emoji.name == paper:
				return reaction.user_id == ctx.author.id
			elif str(reaction.emoji) == scis:
				return reaction.user_id == ctx.author.id
		
		player_last = "X"
		com_last = "X"
		round_last = "X"
		win_colour = 0x00a6ff
		while True:
			embed=discord.Embed(title="Rock, Paper, Scissors", description=f"{rock} = Rock, {paper} = Paper, {scis} = Scissors", color=discord.Colour(win_colour))
			embed.add_field(name="Me (computer)", value=f"Points: {str(com)}", inline=True)
			embed.add_field(name=ctx.author.name, value=f"Points: {str(player)}", inline=True)
			embed.add_field(name="Last Round", value=f"You: {player_last}\nMe: {com_last}\nWinner: {round_last}")
			embed.set_footer(text=f"Beat me! First to {str(points)} wins!")
			await game_embed.edit(embed=embed)

			choice = None
			try:
				reaction = await self.bot.wait_for('raw_reaction_add', timeout=60.0, check=round_choice)
				choice = reaction.emoji
			except asyncio.TimeoutError:
				await ctx.send(f"{ctx.author.mention} took too many time to respond. Game stopped.")
				return
			com_play = str(random.randint(1,3))
			if str(choice.name) == rock:
				await game_embed.remove_reaction(choice, ctx.author)
				player_play = "1"
			elif str(choice.name) == paper:
				await game_embed.remove_reaction(choice, ctx.author)
				player_play = "2"
			elif str(choice) == scis:
				await game_embed.remove_reaction(scis, ctx.author)
				player_play = "3"
			player_last, com_last, round_last = who_wins_round(com_play, player_play)
			if round_last == "You":
				round_last = ctx.author.name
				player += 1
				win_colour = 0x00ff00
			elif round_last == "Me":
				com += 1
				win_colour = 0xff0000
			else:
				win_colour = 0x00a6ff
			
			if com == points:
				embed=discord.Embed(title="I won!", description=f"{ctx.author.name}: {str(player)}", color=discord.Colour(win_colour))
				await game_embed.edit(embed=embed)
				return
			elif player == points:
				embed=discord.Embed(title="You won!", description=f"Me: {str(com)}", color=discord.Colour(win_colour))
				await game_embed.edit(embed=embed)
				return




def setup(bot):
	bot.add_cog(RockPaperScissors(bot))