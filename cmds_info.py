# import
import discord
import time
import datetime
import platform
from renge_utils import set_string_size

# info cmds
async def cmds_info(message, umsg, startup, client):
	
	# args/variables
	args = umsg.split(' ')
	channel = message.channel
	member = message.author
	server = message.guild
	request_channel = client.get_channel(315103432581185536)
	bot_version = '1.0.0'
	
	# help
	if (args[0].lower() == 'help'):
		
		# contextual help
		if (len(args) > 1):
			embed = ''
			if (args[1].lower() == 'help'):
				embed = discord.Embed(title='Help Command', type='rich', description='**Usage:**\n`$help` - Shows the command list')
			elif (args[1].lower() == 'about'):
				embed = discord.Embed(title='About Command', type='rich', description='**Usage:**\n`$about` - Shows info about the bot')
			elif (args[1].lower() == 'info'):
				embed = discord.Embed(title='Info Command', type='rich', description='**Usage:**\n`$info` - Shows technical & bot information')
			elif (args[1].lower() == 'invite'):
				embed = discord.Embed(title='Invite Command', type='rich', description='**Usage:**\n`$invite` - Displays helpful links including one for inviting Renge to your own server')
			elif (args[1].lower() == 'support'):
				embed = discord.Embed(title='Support Command', type='rich', description='**Usage:**\n`$support` - Displays helpful links including an invite to the support server')
			elif (args[1].lower() == 'ping'):
				embed = discord.Embed(title='Ping Command', type='rich', description='**Usage:**\n`$ping` - Ping Renge')
			elif (args[1].lower() == 'avatar'):
				embed = discord.Embed(title='Avatar Command', type='rich', description='**Usage:**\n`$avatar` - View your avatar\n`$avatar <mention>` - View avatar of a mentioned user\n`$avatar <name>` - View the avatar of a user with that name in the current server\n`$avatar <id>` - View the avatar of a user with a given id')
			elif (args[1].lower() == 'request'):
				embed = discord.Embed(title='Request Command', type='rich', description='**Usage:**\n`$request` - Send a request to the developer')
			elif (args[1].lower() == 'shrug'):
				embed = discord.Embed(title='Shrug Command', type='rich', description='**Usage:**\n`$shrug` - Shrug')
			elif (args[1].lower() == 'sugoi'):
				embed = discord.Embed(title='Sugoi Command', type='rich', description='**Usage:**\n`$sugoi` - SUGOI!')
			elif (args[1].lower() == 'pat'):
				embed = discord.Embed(title='Pat Command', type='rich', description='**Usage:**\n`$pat <mention(s)>` - Give someone a well-deserved pat')
			elif (args[1].lower() == 'hug'):
				embed = discord.Embed(title='Hug Command', type='rich', description='**Usage:**\n`$hug <mention(s)>` - Give a special someone a warm hug')
			elif (args[1].lower() == 'pout'):
				embed = discord.Embed(title='Pout Command', type='rich', description='**Usage:**\n`$pout` - Pout\n`$pout <mention(s)>` - Pout at someone')
			elif (args[1].lower() == 'slap'):
				embed = discord.Embed(title='Slap Command', type='rich', description='**Usage:**\n`$slap <mention(s)>` - Give someone a good smack')
			elif (args[1].lower() == 'stare'):
				embed = discord.Embed(title='Stare Command', type='rich', description='**Usage:**\n`$stare <mention(s)>` - Get someone to notice you')
			elif (args[1].lower() == 'nom'):
				embed = discord.Embed(title='Nom Command', type='rich', description='**Usage:**\n`$nom` - Eat something\n`$nom <mention(s)>` - Eat some*one*')
			elif (args[1].lower() == 'prefix'):
				embed = discord.Embed(title='Custom Prefix Command', type='rich', description='**Usage:**\n`$prefix` - Display the server\'s custom prefix\n`$prefix set <prefix>` - Set the server\'s custom prefix\n`$prefix reset` - Remove the server\'s custom prefix\n**Note:**\nSetting or resetting the server\'s custom prefix requires the `Manage Server` permission')
			elif (args[1].lower() == 'welcome'):
				embed = discord.Embed(title='Welcome Message Command', type='rich', description='**Usage:**\n`$welcome` - Display the server\'s welcome message\n`$welcome set <channel> <message>` - Set the server\'s welcome message\n`$welcome reset` - Remove the server\'s welcome message\n**Note:**\nYou can use `!user.mention!` and `!user.name!` as placeholders for the new user\'s mention/name\n**Note:**\nSetting or resetting the server\'s welcome message requires the `Manage Server` permission')
			elif (args[1].lower() == 'leave'):
				embed = discord.Embed(title='Leave Message Command', type='rich', description='**Usage:**\n`$leave` - Display the server\'s leave message\n`$leave set <channel> <message>` - Set the server\'s leave message\n`$leave reset` - Remove the server\'s leave message\n**Note:**\nYou can use `!user.mention!` and `!user.name!` as placeholders for the old user\'s mention/name\n**Note:**\nSetting or resetting the server\'s leave message requires the `Manage Server` permission')
			elif (args[1].lower() == 'autorole'):
				embed = discord.Embed(title='Autorole Command', type='rich', description='**Usage:**\n`$autorole` - Display the server\'s active autorole\n`$autorole set <role>` - Set the server\'s autorole\n`$autorole reset` - Remove the server\'s autorole\n**Note:**\nAn autorole is a role that is automatically applied to any new member who joins the server')
			elif (args[1].lower() == 'kick'):
				embed = discord.Embed(title='Kick Command', type='rich', description='**Usage:**\n`$kick <mention(s)> <reason>` - Kicks one or more mentioned users with optional reason')
			elif (args[1].lower() == 'ban'):
				embed = discord.Embed(title='Ban Command', type='rich', description='**Usage:**\n`$ban <mention(s)>` - Bans one or more mentioned users\n`$ban <mention(s)> <days>` - Bans mentioned user(s) and deletes messages from the past given number of days')
			elif (args[1].lower() == 'prune'):
				embed = discord.Embed(title='Prune Command', type='rich', description='**Usage:**\n`$prune <amount>` - Deletes a given number (5 to 99) of messages (default 99 if more or no amount specified)\n`$prune bot <amount>` - Deletes a given number of bot commands and responses')
			elif (args[1].lower() == 'profile'):
				embed = discord.Embed(title='Profile Command', type='rich', description='**Usage:**\n`$profile` - Displays your profile\n`$profile <mention>` - Show the profile of a mentioned user\n`$profile <name>` - Show the profile of a user with that name in the current server\n`$profile <id>` - Show the profile of a user with a given id\n`$profile description <description>` - Set the description for your profile')
			elif (args[1].lower() == 'rep'):
				embed = discord.Embed(title='Rep Command', type='rich', description='**Usage:**\n`$rep <mention>` - Give rep to a mentioned user (Can be used once every 24 hours)')
			elif (args[1].lower() == 'daily'):
				embed = discord.Embed(title='Daily Command', type='rich', description='**Usage:**\n`$daily` - Gives you 100 free credits every 24 hours')
			elif (args[1].lower() == 'loot'):
				embed = discord.Embed(title='Loot Command', type='rich', description='**Usage:**\n`$loot` - Loots a random number of credits every 5 minutes')
			elif (args[1].lower() == 'richest'):
				embed = discord.Embed(title='Richest Command', type='rich', description='**Usage:**\n`$richest` - Retrieves the top ten richest users\n`$richest rep` - Retrieves the top ten users with the most rep')
			elif (args[1].lower() == 'transfer'):
				embed = discord.Embed(title='Transfer Command', type='rich', description='**Usage:**\n`$transfer <mention> <amount>` - Transfer a given amount to a mentioned user')
			elif (args[1].lower() == 'balance'):
				embed = discord.Embed(title='Balance Command', type='rich', description='**Usage:**\n`$balance` - Displays your total credits\n`$balance <mention>` - Show a mentioned user\'s total credits\n`$balance <name>` - Show the credits of a user with that name in the current server\n`$balance <id>` - Show the credits of a user with a given id\n')
			elif (args[1].lower() == 'roulette'):
				embed = discord.Embed(title='Roulette Command', type='rich', description='**Usage:**\n`$roulette <amount> <bet type>` - Bet credits on roulette\n**Bet Types:**\n`red/black` - Bets on the red or black colour (Payout 1:1)\n`odd/even` - Bets on odd or even numbers (Payout 1:1)\n`high/low` - Bets on high (19-36) or low (1-18) numbers (Payout 1:1)\n`column <#>` - Bet on column 1, 2 or 3 (Payout 2:1)\n`dozen <#>` - Bet on first (1-12), second (13-24) or third (25-36) dozen (Payout 2:1)\n**Note:**\nDue to input limitations, only outside bets are currently allowed. Inside bets may be added in future')
			elif (args[1].lower() == 'slots'):
				embed = discord.Embed(title='Slots Command', type='rich', description='**Usage:**\n`$slots <amount>` - Bet credits on the slot machine\n**Payouts:**\n:cherries: - 2x Bet amount\n:rice_ball: - 3x Bet amount\n:butterfly: - 5x Bet amount\n:cherry_blossom: - 10x Bet amount\n:dollar: - 25x Bet amount\n:gem: - 50x Bet amount\n')
			elif (args[1].lower() == 'waifu'):
				embed = discord.Embed(title='Waifu Command', type='rich', description='**Usage:**\n`$waifu add <mention>` - Add the mentioned user as one of your waifus\n`$waifu remove <number>` - Remove the waifu at the given postion (1-5, in order seen on profile)')
			elif (args[1].lower() == 'sotd'):
				embed = discord.Embed(title='Song of the Day Command', type='rich', description='**Usage:**\n`$sotd` - Display today\'s song of the day (links to SoundCloud)\n`$sotd url` - Displays just the song url so the player gets embedded into Discord')
			elif (args[1].lower() == 'anime'):
				embed = discord.Embed(title='Anime Command', type='rich', description='**Usage:**\n`$anime <title>` - Search AniList for an anime')
			elif (args[1].lower() == 'manga'):
				embed = discord.Embed(title='Manga Command', type='rich', description='**Usage:**\n`$manga <title>` - Search AniList for a manga')
			elif (args[1].lower() == '8ball'):
				embed = discord.Embed(title='Magic 8-Ball Command', type='rich', description='**Usage:**\n`$8ball <question>` - Ask the Magic 8-Ball a question')
			if (embed == ''):
				await channel.send('That command does not exist!')
			else:
				await channel.send(content = None, embed = embed)
		
		# command list
		else:
			embed = discord.Embed(title = 'Renge Help', type = 'rich', description = 'Use `$help <command>` for usage')
			embed.add_field(name = 'Info Commands:', value = '`help` `invite` `support` `about` `info` `ping` `avatar` `request`', inline = False)
			if not message.guild is None:
				embed.add_field(name = 'Management Commands:', value = '`prefix` `welcome` `leave` `autorole`',inline = False)
				embed.add_field(name = 'Moderation Commands:', value = '`ban` `kick` `prune`', inline = False)
			embed.add_field(name = 'Action Commands:',value = '`pat` `hug` `pout` `slap` `stare` `nom` `shrug` `sugoi`',inline = False)
			embed.add_field(name = 'Currency Commands:',value = '`profile` `rep` `daily` `loot` `transfer` `richest` `balance`',inline = False)
			embed.add_field(name = 'Game Commands:',value = '`roulette` `slots`',inline = False)
			embed.add_field(name = 'Misc Commands:',value = '`anime` `manga` `sotd` `waifu` `8ball`')
			await channel.send(content = None, embed = embed)
	
	# invite/support
	if (args[0].lower() == 'invite' or args[0].lower() == 'support'):
		embed = discord.Embed(title = 'Helpful Links', type = 'rich', description = '[Invite Link](http://polr.me/rengebot)\n[Support Guild](https://discord.gg/9ZxCkvv)\n[GitHub Repo](https://github.com/Yuvira/RengeBot)')
		embed.set_thumbnail(url = client.user.avatar_url)
		await channel.send(content = None, embed = embed)
	
	# about
	if (args[0].lower() == 'about'):
		t1 = 0
		t2 = 0
		for server in client.guilds:
			t1 += 1
			for member in server.members:
				t2 += 1
		embed = discord.Embed(title = 'About Renge', type = 'rich', description = 'Renge is a small bot but constantly growing with new commands and community suggestions!\n\nCreated by Yuvira\n\n**Version:** ' + bot_version + '\n**Servers:** ' + str(t1) + '\n**Users:** ' + str(t2) + '\n\n[Invite Link](http://polr.me/rengebot)\n[Support Guild](https://discord.gg/9ZxCkvv)\n[GitHub Repo](https://github.com/Yuvira/RengeBot)')
		embed.set_thumbnail(url = client.user.avatar_url)
		await channel.send(content = None, embed = embed)
	
	# ping
	if (args[0].lower() == 'ping'):
		before = datetime.datetime.utcnow()
		ping_msg = await channel.send('Pinging...')
		ping = (datetime.datetime.utcnow() - before) * 1000
		before2 = time.monotonic()
		await (await client.ws.ping())
		after = time.monotonic()
		ping2 = (after - before2) * 1000
		await ping_msg.edit(content = 'Ping! Message received! `Ping: {:.2f}ms'.format(ping.total_seconds()) + ' Websocket: {0:.0f}ms`'.format(ping2))
		
	# avatar
	if (args[0].lower() == 'avatar'):
		
		# get user to retrieve avatar from
		user = member
		name = 'Your'
		if (len(message.mentions) > 0):
			user = message.mentions[0]
		elif (len(args) > 1):
			try:
				user = await client.fetch_user(args[1])
			except:
				m = discord.utils.find(lambda u: args[1].lower() in u.display_name.lower(), server.members)
				if (m != None):
					user = m
		if (user != member):
			name = user.display_name + '\'s'
		
		# get avatar
		avatar = None
		if (str(user.avatar_url) == ''):
			avatar = str(user.default_avatar_url)
		else:
			avatar = str(user.avatar_url)
			avatar = avatar.replace('.webp?size=1024', '.png?size=512')
			avatar = avatar.replace('.gif?size=1024', '.gif')
		embed = discord.Embed(title = name + ' avatar!', type = 'rich', description = 'Click [here](' + avatar + ')!')
		embed.set_image(url = avatar)
		await channel.send(content = None, embed = embed)
		
	# request
	if (args[0].lower() == 'request'):
		if (len(args) > 1):
			await request_channel.send('Request from `' + member.name + '#' + member.discriminator + '`: ' + umsg[8:])
			await channel.send('Request sent! The creator will DM you if your suggestion is added')
		else:
			await channel.send('You need to specify something to request!')

	# info
	if (args[0].lower() == 'info'):
		before = time.monotonic()
		await (await client.ws.ping())
		after = time.monotonic()
		ping = (after - before) * 1000
		server_count = 0
		member_count = 0
		channel_count = 0
		for guild in client.guilds:
			server_count += 1
			for chan in guild.channels:
				channel_count += 1
			for member in guild.members:
				member_count += 1
		t = time.time() - startup
		uptime = str(int(t/86400)) + 'd '
		t = t % 86400
		uptime = uptime + str(int(t/3600)) + 'h '
		t = t % 3600
		uptime = uptime + str(int(t/60)) + 'm '
		t = t % 60
		uptime = uptime + str(int(t)) + 's'
		msg = '```============[ Technical Info ]============\n'
		msg += '::DiscordPY Version :: ' + set_string_size(str(discord.__version__), 17) + '::\n'
		msg += '::Python Version    :: ' + set_string_size(str(platform.python_version()), 17) + '::\n'
		msg += '::Websocket Ping    :: ' + set_string_size('{0:.0f}ms'.format(ping), 17) + '::\n'
		msg += '==============[ Renge Info ]==============\n'
		msg += '::Bot Version       :: ' + set_string_size(str(bot_version), 17) + '::\n'
		msg += '::Guilds            :: ' + set_string_size(str(server_count), 17) + '::\n'
		msg += '::Users             :: ' + set_string_size(str(member_count), 17) + '::\n'
		msg += '::Channels          :: ' + set_string_size(str(channel_count), 17) + '::\n'
		msg += '::Uptime            :: ' + set_string_size(uptime, 17) + '::\n'
		msg += '==========================================```'
		await channel.send(msg)
