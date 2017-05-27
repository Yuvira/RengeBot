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
				embed = discord.Embed(title='Profile Command', type='rich', description='**Usage:**\n`$profile` - Displays your profile\n`$profile desc <description>` - Set the description for your profile')
				await client.send_message(channel, content=None, embed=embed)
			else:
				await client.send_message(channel, 'That command does not exist!')
		else:
			embed = discord.Embed(title='Renge Help', type='rich', description='Use `$help <command>` for usage\n**Action Commands:**\n`shrug` `sugoi`\n**Profile Commands:**\n`profile`\n**Moderation Commands:**\n`kick` `ban`\n**Info Commands:**\n`help` `about` `request`')
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
			embed = discord.Embed(title='About Renge', type='rich', description='Renge is a small bot but constantly growing with new commands and community suggestions!\n\nCreated by Yuvira#7842\n\n**Version:** 0.1.5\n**Servers:** ' + str(t1) + '\n**Users:** ' + str(t2) + '\n\n[Invite Link](https://discordapp.com/oauth2/authorize?client_id=309002800703078400&scope=bot&permissions=271641670)\n[Support Guild](https://discord.gg/9ZxCkvv)')
			embed.set_thumbnail(url=client.user.avatar_url)
			await client.send_message(channel, content=None, embed=embed)
			
	# request
	if (args[0] == 'request'):
		if (umsg == 'request'):
			await client.send_message(channel, 'You need to specify something to request!')
		else:
			await client.send_message(request_channel, 'Request from `' + member.name + '#' + member.discriminator + '`: ' + umsg[8:])
			await client.send_message(channel, 'Request sent! The creator will DM you if your suggestion is added')
