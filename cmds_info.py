# import
import discord
import time
import datetime
import platform
from renge_utils import set_string_size

# info cmds
async def cmds_info(message, umsg, client):
	
	# args/variables
	args = umsg.split(' ')
	channel = message.channel
	member = message.author
	request_channel = discord.Object('315103432581185536')
	bot_version = '0.3.6'
	
	# help
	if (args[0] == 'help'):
		
		# contextual help
		if (len(args) > 1):
			if (args[1] == 'help'):
				embed = discord.Embed(title='Help Command', type='rich', description='**Usage:**\n`$help` - Shows the command list')
				await client.send_message(channel, content=None, embed=embed)
			elif (args[1] == 'about'):
				embed = discord.Embed(title='About Command', type='rich', description='**Usage:**\n`$about` - Shows info about the bot')
				await client.send_message(channel, content=None, embed=embed)
			elif (args[1] == 'info'):
				embed = discord.Embed(title='Info Command', type='rich', description='**Usage:**\n`$info` - Shows technical & bot information')
				await client.send_message(channel, content=None, embed=embed)
			elif (args[1] == 'invite'):
				embed = discord.Embed(title='Invite Command', type='rich', description='**Usage:**\n`$invite` - Display a link to invite Renge to your server')
				await client.send_message(channel, content=None, embed=embed)
			elif (args[1] == 'support'):
				embed = discord.Embed(title='Support Command', type='rich', description='**Usage:**\n`$support` - Display a link to the support guild')
				await client.send_message(channel, content=None, embed=embed)
			elif (args[1] == 'ping'):
				embed = discord.Embed(title='Ping Command', type='rich', description='**Usage:**\n`$ping` - Ping Renge')
				await client.send_message(channel, content=None, embed=embed)
			elif (args[1] == 'avatar'):
				embed = discord.Embed(title='Avatar Command', type='rich', description='**Usage:**\n`$avatar` - View your avatar\n`$avatar <@mention>` - View avatar of a mentioned user')
				await client.send_message(channel, content=None, embed=embed)
			elif (args[1] == 'request'):
				embed = discord.Embed(title='Request Command', type='rich', description='**Usage:**\n`$request` - Send a request to the developer')
				await client.send_message(channel, content=None, embed=embed)
			elif (args[1] == 'shrug'):
				embed = discord.Embed(title='Shrug Command', type='rich', description='**Usage:**\n`$shrug` - Shrug')
				await client.send_message(channel, content=None, embed=embed)
			elif (args[1] == 'sugoi'):
				embed = discord.Embed(title='Sugoi Command', type='rich', description='**Usage:**\n`$sugoi` - SUGOI!')
				await client.send_message(channel, content=None, embed=embed)
			elif (args[1] == 'kick'):
				embed = discord.Embed(title='Kick Command', type='rich', description='**Usage:**\n`$kick <@mentions> <reason>` - Kicks one or more mentioned users with optional reason')
				await client.send_message(channel, content=None, embed=embed)
			elif (args[1] == 'ban'):
				embed = discord.Embed(title='Ban Command', type='rich', description='**Usage:**\n`$ban <@mentions>` - Bans one or more monetioned users\n`$ban <@mentions> <days>` - Bans mentioned user(s) and deletes messages from the past given number of days')
				await client.send_message(channel, content=None, embed=embed)
			elif (args[1] == 'prune'):
				embed = discord.Embed(title='Prune Command', type='rich', description='**Usage:**\n`$prune <amount>` - Deletes a given number (5 to 99) of messages (default 99 if more or no amount specified)\n`$prune bot <amount>` - Deletes a given number of bot commands and responses')
				await client.send_message(channel, content=None, embed=embed)
			elif (args[1] == 'profile'):
				embed = discord.Embed(title='Profile Command', type='rich', description='**Usage:**\n`$profile` - Displays your profile\n`$profile <@mention>` - Show the profile of a mentioned user\n`$profile <nickname>` - Show the profile of a user with that name in the current server\n`$profile <id>` - Show the profile of a user with a given id\n`$profile desc <description>` - Set the description for your profile')
				await client.send_message(channel, content=None, embed=embed)
			elif (args[1] == 'rep'):
				embed = discord.Embed(title='Rep Command', type='rich', description='**Usage:**\n`$rep <@mention>` - Give rep to a mentioned user (Can be used once every 24 hours)')
				await client.send_message(channel, content=None, embed=embed)
			elif (args[1] == 'daily'):
				embed = discord.Embed(title='Daily Command', type='rich', description='**Usage:**\n`$daily` - Gives you 100 free credits every 24 hours')
				await client.send_message(channel, content=None, embed=embed)
			elif (args[1] == 'loot'):
				embed = discord.Embed(title='Loot Command', type='rich', description='**Usage:**\n`$loot` - Loots a random number of credits every 5 minutes')
				await client.send_message(channel, content=None, embed=embed)
			elif (args[1] == 'roulette'):
				embed = discord.Embed(title='Roulette Command', type='rich', description='Allows up to four people at a time to play a game of casino roulette\n**Usage:**\n`$roulette bet <amount> <type>` - Bets an amount on a certain value (bet types listed below)\n`$roulette quick <amount> <type>` - Plays an instant game for one person\n`$roulette cancel` - Cancels your current bet\n`$roulette spin` - Spin the roulette wheel\n**Bet Types:**\n`red/black` - Bets on the red or black colour (Payout 1:1)\n`odd/even` - Bets on odd or even numbers (Payout 1:1)\n`high/low` - Bets on high (19-36) or low (1-18) numbers (Payout 1:1)\n`column <#>` - Bet on column 1, 2 or 3 (Payout 2:1)\n`dozen <#>` - Bet on first (1-12), second (13-24) or third (25-36) dozen (Payout 2:1)\n**Note:**\nDue to input limitations, only outside bets are currently allowed. Inside bets may be added in future')
				await client.send_message(channel, content=None, embed=embed)
			elif (args[1] == 'richest'):
				embed = discord.Embed(title='Richest Command', type='rich', description='**Usage:**\n`$richest` - Retrieves the top ten richest users\n`$richest rep` - Retrieves the top ten users with the most rep')
				await client.send_message(channel, content=None, embed=embed)
			elif (args[1] == 'transfer'):
				embed = discord.Embed(title='Transfer Command', type='rich', description='**Usage:**\n`$transfer <@mention> <amount>` - Transfer a given amount to a mentioned user')
				await client.send_message(channel, content=None, embed=embed)
			elif (args[1] == 'waifu'):
				embed = discord.Embed(title='Waifu Command', type='rich', description='**Usage:**\n`$waifu add <@mention>` - Add the mentioned user as one of your waifus\n`$waifu rem <number>` - Remove the waifu at the given postion (1-5, in order seen on profile)')
				await client.send_message(channel, content=None, embed=embed)
			elif (args[1] == 'sotd'):
				embed = discord.Embed(title='Song of the Day Command', type='rich', description="**Usage:**\n`$sotd` - Display today's song of the day (links to SoundCloud)\n`$sotd url` - Displays just the song url so the player gets embedded into Discord")
				await client.send_message(channel, content=None, embed=embed)
			else:
				await client.send_message(channel, 'That command does not exist!')
		
		# command list
		else:
			embed = discord.Embed(title='Renge Help', type='rich', description='Use `$help <command>` for usage')
			embed.add_field(name="Info Commands:",value="`help` `invite` `support` `about` `info` `ping` `avatar` `request`",inline=False)
			if not message.server is None:
				embed.add_field(name="Moderation Commands:",value="`ban` `kick` `prune`",inline=False)
			embed.add_field(name="Action Commands:",value="`shrug` `sugoi`",inline=False)
			embed.add_field(name="Currency Commands:",value="`profile` `rep` `daily` `loot` `transfer` `richest`",inline=False)
			embed.add_field(name="Game Commands:",value="`roulette`",inline=False)
			embed.add_field(name="Misc Commands:",value='`waifu` `sotd`')
			await client.send_message(channel, content=None, embed=embed)
	
	# invite
	if (args[0] == 'invite'):
		await client.send_message(channel, "You can invite me to your server here! https://polr.me/rengebot")
	
	# support
	if (args[0] == 'support'):
		await client.send_message(channel, "You can join the support guild here! https://discord.gg/9ZxCkvv")
	
	# about
	if (args[0] == 'about'):
		if (umsg == 'about'):
			t1 = 0
			t2 = 0
			for server in client.servers:
				t1 += 1
				for member in server.members:
					t2 += 1
			embed = discord.Embed(title='About Renge', type='rich', description='Renge is a small bot but constantly growing with new commands and community suggestions!\n\nCreated by Yuvira\n\n**Version:** ' + bot_version + '\n**Servers:** ' + str(t1) + '\n**Users:** ' + str(t2) + '\n\n[Invite Link](http://polr.me/rengebot)\n[Support Guild](https://discord.gg/9ZxCkvv)')
			embed.set_thumbnail(url=client.user.avatar_url)
			await client.send_message(channel, content=None, embed=embed)
	
	# ping
	if (args[0] == 'ping'):
		before = datetime.datetime.utcnow()
		ping_msg = await client.send_message(channel, 'Pinging...')
		ping = (datetime.datetime.utcnow() - before) * 1000
		before2 = time.monotonic()
		await (await client.ws.ping())
		after = time.monotonic()
		ping2 = (after - before2) * 1000
		await client.edit_message(ping_msg, new_content='Ping! Message received! `Ping: {:.2f}ms'.format(ping.total_seconds()) + ' Websocket: {0:.0f}ms`'.format(ping2))
		
	# avatar
	if (args[0] == 'avatar'):
		
		# mention avatar
		if (len(message.mentions) > 0):
			avatar = None
			if (message.mentions[0].avatar_url == ''):
				avatar = message.mentions[0].default_avatar_url
			else:
				avatar = message.mentions[0].avatar_url
				avatar = avatar.replace(".webp?size=1024", ".png?size=512")
				avatar = avatar.replace(".gif?size=1024", ".gif")
			embed = discord.Embed(title=message.mentions[0].display_name + "'s avatar!", type='rich', description='Click [here](' + avatar + ')!')
			embed.set_image(url=avatar)
			await client.send_message(channel, content=None, embed=embed)
		
		# user's avatar
		else:
			avatar = None
			if (member.avatar_url == ''):
				avatar = member.default_avatar_url
			else:
				avatar = member.avatar_url
				avatar = avatar.replace(".webp?size=1024", ".png?size=512")
				avatar = avatar.replace(".gif?size=1024", ".gif")
			embed = discord.Embed(title='Your avatar!', type='rich', description='Click [here](' + avatar + ')!')
			embed.set_image(url=avatar)
			await client.send_message(channel, content=None, embed=embed)
		
	# request
	if (args[0] == 'request'):
		if (umsg == 'request'):
			await client.send_message(channel, 'You need to specify something to request!')
		else:
			await client.send_message(request_channel, 'Request from `' + member.name + '#' + member.discriminator + '`: ' + umsg[8:])
			await client.send_message(channel, 'Request sent! The creator will DM you if your suggestion is added')

	# info
	if (args[0] == 'info'):
		before = time.monotonic()
		await (await client.ws.ping())
		after = time.monotonic()
		ping = (after - before) * 1000
		server_count = 0
		member_count = 0
		channel_count = 0
		for guild in client.servers:
			server_count += 1
			for chan in guild.channels:
				channel_count += 1
			for member in guild.members:
				member_count += 1
		msg = "```============[ Technical Info ]============\n"
		msg += "::DiscordPY Version :: " + set_string_size(str(discord.__version__), 17) + "::\n"
		msg += "::Python Version    :: " + set_string_size(str(platform.python_version()), 17) + "::\n"
		msg += "::Websocket Ping    :: " + set_string_size("{0:.0f}ms".format(ping), 17) + "::\n"
		msg += "==============[ Renge Info ]==============\n"
		msg += "::Bot Version       :: " + set_string_size(str(bot_version), 17) + "::\n"
		msg += "::Guilds            :: " + set_string_size(str(server_count), 17) + "::\n"
		msg += "::Users             :: " + set_string_size(str(member_count), 17) + "::\n"
		msg += "::Channels          :: " + set_string_size(str(channel_count), 17) + "::\n"
		msg += "==========================================```"
		await client.send_message(channel, msg)
