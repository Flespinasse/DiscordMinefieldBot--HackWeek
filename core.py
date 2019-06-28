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
import asyncio

import chf
import config

discord_emojis = dict()
discord_emojis[1] = "<:m1:593002785608433672>"
discord_emojis[2] = '<:m2:593002786203893760>'
discord_emojis[3] = '<:m3:593002786250162197>'
discord_emojis[4] = '<:m4:593002786531049472>'

bot = commands.Bot(command_prefix=config.botPrefix)
bot.load_extension('Minesweeper')
bot.load_extension('RockPaperScissors')

bot.remove_command('help')


@bot.event
async def on_connect():
    print("Connected to Discord")

@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user} ; {bot.user.id}")

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"```Python\n{error}```")
    raise error

@bot.event
async def on_guild_join(guild):
	await guild.owner.send("Hey! Thanks for adding me in your guild! My prefix is `ms.`, check out the games I have!")

@bot.command(aliases=['howtoplay', 'rules'])
async def game_rules(ctx, *, game_name=None):
    if not game_name:
        await ctx.send(embed=chf.game_rule_list())
        return
    await ctx.send(embed=chf.game_rule_complete(game_name))

@bot.command(name='help')
async def _help(ctx, *, command=None):
    if not command:
        await ctx.send(embed=chf.help_list())
        return
    await ctx.send(embed=chf.help_complete(command))

@bot.command()
async def reload_all(ctx):
    if ctx.author.id == 332857848252071938:
        bot.reload_extension('Minesweeper')
        await ctx.send('All extensions have been reloaded')

@bot.command()
@commands.cooldown(1, 86400, type=commands.BucketType.user)
async def suggestion(ctx, *, idea):
	if not suggestion:
		await ctx.send("Please send me your suggestion within the next 3 minutes!")

		def suggestionMessage(message):
			return message.author == ctx.author
		content = None
		try:
			message = await bot.wait_for('message', timeout=180.0, check=suggestionMessage)
			content=message.content
		except asyncio.TimeoutError:
			await ctx.send("You timed out!")
			return
		suggestion = content
	
	async with ctx.channel.typing():
		embed = discord.Embed(title=f"{ctx.author.name} has a suggestion. Vote now!", description=idea, color=0x4287f5)
		embed.set_footer(text="Vote with ✅/❌ | Votes are open for 24 hours")
		suggestionMessage = await bot.get_guild(config.officialGuildID).get_channel(config.suggestionsChannel).send(embed=embed)
		await suggestionMessage.add_reaction('✅')
		await suggestionMessage.add_reaction('❌')
		await ctx.send("Your suggestion has been sent to the developers!")
	await asyncio.sleep(86400) #1 day time = 86400 seconds
	suggestionMessage = await bot.get_guild(config.officialGuildID).get_channel(config.suggestionsChannel).fetch_message(suggestionMessage.id)
	if (suggestionMessage.reactions[0].count / suggestionMessage.reactions[1].count) > 1:
		embed=discord.Embed(title=f"The community seems hyped by {ctx.author.name}'s suggestion", description="The developers will read the suggestion and maybe add in the bot if it is possible.", color=0x1ec718)
		embed.add_field(name="Suggestion", value=idea)
		await bot.get_guild(config.officialGuildID).get_channel(config.suggestionsAnswers).send(embed=embed)
	else:
		embed=discord.Embed(title=f"{ctx.author.name}'s suggestion has been rejected by the community and the developers", color=0xf74420)
		embed.add_field(name="Suggestion", value=idea)
		await bot.get_guild(config.officialGuildID).get_channel(config.suggestionsAnswers).send(embed=embed)
    

@bot.command(aliases=['joinus', 'supportserver', 'supportlink', 'officialserverlink'])
async def invite(ctx):
	embed=discord.Embed(title="Developers' server", description="https://discord.gg/SxyWxWq")
	embed.set_footer(text="By joining our server you may get extra perms in future games")
	await ctx.send(embed=embed)

@bot.command(aliases=['bug_report', 'report_a_bug'])
@commands.cooldown(3, 21600, type=commands.BucketType.user)
async def bugreport(ctx):
	bugEmbed = await ctx.send(embed=discord.Embed(title="what is the bug impact on the gameplay/bot?", description=":one:: Minor, :two:: Medium, :three:: Major, :four:: GAME BREAKING").set_footer(text="A minor bug can be a letter missing in a text, as a Game-breaking bug can make a game crash. Major and medium bugs are bugs that show up in-game but don't ruin it. Major is for important bugs in-game, but not game-breaking ones."))

	def bug_react(reaction):
		if str(reaction.emoji) == discord_emojis[1]:
			return reaction.user_id == ctx.author.id
		elif str(reaction.emoji) == discord_emojis[2]:
			return reaction.user_id == ctx.author.id
		elif str(reaction.emoji) == discord_emojis[3]:
			return reaction.user_id == ctx.author.id
		elif str(reaction.emoji) == discord_emojis[4]:
			return reaction.user_id == ctx.author.id
	
	await bugEmbed.add_reaction(discord_emojis[1])
	await bugEmbed.add_reaction(discord_emojis[2])
	await bugEmbed.add_reaction(discord_emojis[3])
	await bugEmbed.add_reaction(discord_emojis[4])

	how_important = None
	try:
		reaction = await bot.wait_for('raw_reaction_add', timeout=60.0, check=bug_react)
		how_important = reaction
	except asyncio.TimeoutError:
		await bugEmbed.edit(embed=discord.Embed(title="Timeout", description="You timed out. Bug report cancelled.", color=discord.Colour(0xff0000)))
		return
	color = None
	bugMessage = None
	await bugEmbed.clear_reactions()
	if str(how_important.emoji) == discord_emojis[1]:
		color = discord.Colour(0x88ff00)
		bugMessage = "Report minor bug"
	elif str(how_important.emoji) == discord_emojis[2]:
		color = discord.Colour(0xffff00)
		bugMessage = "Report medium bug"
	elif str(how_important.emoji) == discord_emojis[3]:
		color = discord.Colour(0xff8800)
		bugMessage = "Report major bug"
	elif str(how_important.emoji) == discord_emojis[4]:
		color = discord.Colour(0xff0000)
		bugMessage = "Report game-breaking bug"
	
	await bugEmbed.edit(embed=discord.Embed(title=bugMessage, description="What did you do before the bug happened?", color=color))
	def bugstep(message):
		return message.author == ctx.author
	
	how_happen = None
	try:
		message = await bot.wait_for('message', timeout=180.0, check=bugstep)
		how_happen = message.content
	except asyncio.TimeoutError:
		await bugEmbed.edit(embed=discord.Embed(title="Timeout", description="You timed out. Bug report cancelled", color=discord.Colour(0xff0000)))
		return
	await bugEmbed.edit(embed=discord.Embed(title=bugMessage, description="What did you expect to happen?", color=color))

	what_happen_expect = None
	try:
		message = await bot.wait_for('message', timeout=180.0, check=bugstep)
		what_happen_expect = message.content
	except asyncio.TimeoutError:
		await bugEmbed.edit(embed=discord.Embed(title="Timeout", description="You timed out. Bug report cancelled", color=discord.Colour(0xff0000)))
		return
	await bugEmbed.edit(embed=discord.Embed(title=bugMessage, description="What happened?", color=color))

	what_happen_real = None
	try:
		message = await bot.wait_for('message', timeout=180.0, check=bugstep)
		what_happen_real = message.content
	except asyncio.TimeoutError:
		await bugEmbed.edit(embed=discord.Embed(title="Timeout", description="You timed out. Bug report cancelled", color=discord.Colour(0xff0000)))
		return
	
	finalembed=discord.Embed(title=bugMessage, description="Are these informations correct?", color=color)
	finalembed.add_field(name="What were you doing before the bug?", value=how_happen)
	finalembed.add_field(name="Result expected?", value=what_happen_expect)
	finalembed.add_field(name="Result got?", value=what_happen_real)
	await bugEmbed.edit(embed=finalembed)
	await bugEmbed.add_reaction('✅')
	await bugEmbed.add_reaction('❌')

	def correct_check(reaction):
		if reaction.emoji.name == '✅':
			return reaction.user_id == ctx.author.id
		elif reaction.emoji.name == '❌':
			return reaction.user_id == ctx.author.id
	
	choice = None
	try:
		reaction = await bot.wait_for('raw_reaction_add', timeout=60.0, check=correct_check)
		choice = reaction
	except asyncio.TimeoutError:
		await bugEmbed.edit(embed=discord.Embed(title="Timeout", description="You timed out. Bug report cancelled", color=discord.Colour(0xff0000)))
		return
	if choice.emoji.name == '✅':
		async with ctx.channel.typing():
			finalembed=discord.Embed(title=bugMessage.replace("Report ", ""), description="A bug has been reported!", color=color)
			finalembed.add_field(name="What were you doing before the bug?", value=how_happen)
			finalembed.add_field(name="Result expected?", value=what_happen_expect)
			finalembed.add_field(name="Result got?", value=what_happen_real)
			finalembed.set_footer(text=f"Bug reported by {ctx.author.name} ; {ctx.author.id}")
			finalEmbedMSG = await bot.get_guild(config.officialGuildID).get_channel(config.bugChannel).send(embed=finalembed)
			await finalEmbedMSG.add_reaction('✅')
			await finalEmbedMSG.add_reaction('❌')
			await ctx.send(":thumbsup: Your bug has been reported and will be treated as soon as the devs can. **Please open your DMs so they can contact you if further information is needed**")
			return
	elif choice.emoji.name == '❌':
		await ctx.send("Please re-invoke the command")
		return

@bot.command(aliases=['info'])
async def about(ctx):
	embed=discord.Embed(title="About the bot", description="Devs/Bot info", color=discord.Colour(0x00ff00))
	embed.add_field(name="Main Coder", value="Raoul1808", inline=True)
	embed.add_field(name="Sub-Coders", value="Joquliina\nMaddyFace43v3r", inline=True)
	embed.add_field(name="Bot Prefix", value=config.botPrefix)
	embed.add_field(name="Bot Version", value=config.botVersion, inline=True)
	embed.add_field(name="Programming language + Library used", value=f"Python 3.6.X\nDiscord.py v{discord.__version__}", inline=True)
	embed.add_field(name="Guilds", value=len(bot.guilds))
	embed.add_field(name="Commands", value="8", inline=True)
	embed.set_thumbnail(url=bot.user.avatar_url)
	await ctx.send(embed=embed)

async def is_dev(ctx):
	return str(ctx.author.id) in ['545671764185841665', '354872019818381313', '332857848252071938']

@bot.command()
@commands.check(is_dev)
async def contact(ctx, userID, *, message):
	await bot.get_user(int(userID)).send(message)
	await ctx.send("Message successfully sent")

        

bot.run(config.TOKEN)
