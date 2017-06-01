# import
import discord
import glob

# info cmds
async def cmds_info(message, umsg, client):
	
	# args/variables
	args = umsg.split(' ')
	channel = message.channel
	member = message.author
	request_channel = discord.Object('315103432581185536')
	
	# help
	if (args[0] == 'help'):
		if (len(args) > 1):
			if (args[1] == 'help'):
				embed = discord.Embed(title='Help Command', type='rich', description='**Usage:**\n`$help` - Shows the command list')
				await client.send_message(channel, content=None, embed=embed)
			elif (args[1] == 'about'):
				embed = discord.Embed(title='About Command', type='rich', description='**Usage:**\n`$about` - Shows info about the bot')
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
				embed = discord.Embed(title='Kick Command', type='rich', description='**Usage:**\n`$kick <mentions>` - Kicks one or more mentioned users')
				await client.send_message(channel, content=None, embed=embed)
			elif (args[1] == 'ban'):
				embed = discord.Embed(title='Ban Command', type='rich', description='**Usage:**\n`$ban <mentions>` - Bans one or more monetioned users\n`$ban <mentions> <days>` - Bans mentioned user(s) and deletes messages from the past given number of days')
				await client.send_message(channel, content=None, embed=embed)
			elif (args[1] == 'profile'):
				embed = discord.Embed(title='Profile Command', type='rich', description='**Usage:**\n`$profile` - Displays your profile\n`$profile <@mention>` - Show the profile of someone else\n`$profile desc <description>` - Set the description for your profile')
				await client.send_message(channel, content=None, embed=embed)
			elif (args[1] == 'daily'):
				embed = discord.Embed(title='Daily Command', type='rich', description='**Usage:**\n`$daily` - Gives you 100 free credits every 24 hours')
				await client.send_message(channel, content=None, embed=embed)
			elif (args[1] == 'loot'):
				embed = discord.Embed(title='Loot Command', type='rich', description='**Usage:**\n`$loot` - Loots a random number of credits every 5 minutes')
				await client.send_message(channel, content=None, embed=embed)
			elif (args[1] == 'profile'):
				embed = discord.Embed(title='Roulette Command', type='rich', description='Allows up to four people at a time to play a game of casino roulette\n**Usage:**\n`$roulette bet <amount> <type>` - Bets an amount on a certain value (bet types listed below)\n`$roulette cancel` - Cancels your current bet\n`$roulette spin` - Spin the roulette wheel\n**Bet Types:**\n`red/green` - Bets on the red or green colour (Payout 1:1)\n`odd/even` - Bets on odd or even numbers (Payout 1:1)\n`high/low` - Bets on high (19-36) or low (1-18) numbers (Payout 1:1)\n`column <#>` - Bet on column 1, 2 or 3 (Payout 2:1)\n`dozen <#>` - Bet on first (1-12), second (13-24) or third (25-36) dozen (Payout 2:1)\n**Note:**\nDue to limitations, only outside bets are currently allowed. Inside bets may be added in future')
				await client.send_message(channel, content=None, embed=embed)
			else:
				await client.send_message(channel, 'That command does not exist!')
		else:
			embed = discord.Embed(title='Renge Help', type='rich', description='Use `$help <command>` for usage\n**Action Commands:**\n`shrug` `sugoi`\n**Profile Commands:**\n`profile` `daily` `loot`\n**Game Commands:**\n`roulette`\n**Moderation Commands:**\n`kick` `ban`\n**Info Commands:**\n`help` `about` `request`')
			await client.send_message(channel, content=None, embed=embed)
	
	# about
	if (args[0] == 'about'):
		if (umsg == 'about'):
			t1 = 0
			t2 = 0
			for server in client.servers:
				t1 += 1
				for member in server.members:
					t2 += 1
			embed = discord.Embed(title='About Renge', type='rich', description='Renge is a small bot but constantly growing with new commands and community suggestions!\n\nCreated by Yuvira#7842\n\n**Version:** 0.2.0\n**Servers:** ' + str(t1) + '\n**Users:** ' + str(t2) + '\n\n[Invite Link](https://discordapp.com/oauth2/authorize?client_id=309002800703078400&scope=bot&permissions=271641670)\n[Support Guild](https://discord.gg/9ZxCkvv)')
			embed.set_thumbnail(url=client.user.avatar_url)
			await client.send_message(channel, content=None, embed=embed)
			
	# request
	if (args[0] == 'request'):
		if (umsg == 'request'):
			await client.send_message(channel, 'You need to specify something to request!')
		else:
			await client.send_message(request_channel, 'Request from `' + member.name + '#' + member.discriminator + '`: ' + umsg[8:])
			await client.send_message(channel, 'Request sent! The creator will DM you if your suggestion is added')
