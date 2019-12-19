# import
import discord
import asyncio

# info cmds
async def cmds_mod(message, umsg, prefix, client):
	
	# args/variables
	args = umsg.split(' ')
	channel = message.channel
	server = message.guild
	member = message.author
	
	# kick
	if (args[0].lower() == 'kick'):
		if (server.me.guild_permissions.kick_members == False):
			await channel.send('I don\'t have permission to kick!')
		elif (member.guild_permissions.kick_members == False):
			await channel.send('You don\'t have permission to kick!')
		elif (len(message.mentions) < 1):
			await channel.send('You must mention the person(s) to kick!')
		else:
			test = False
			msg = 'Kicked'
			reason = ''
			for a in range(len(message.mentions) + 1, len(args)):
				reason += ' ' + args[a]
			for u in message.mentions:
				if (server.me.top_role.position > u.top_role.position):
					if (member.top_role.position > u.top_role.position):
						try:
							await u.kick()
							msg += ' `' + u.display_name + '`'
							test = True
							try:
								await u.send('You were kicked from **' + server.name + '** by **' + member.display_name + '**:' + reason)
							except:
								pass
						except:
							await channel.send('Failed to kick `' + u.display_name + '`!')
					else:
						await channel.send('`' + u.display_name + '` has a higher role than you!')
				else:
					await channel.send('`' + u.display_name + '` has a higher role than me!')
			if (test == True):
				await channel.send(msg)
	
	# ban
	if (args[0].lower() == 'ban'):
		if (server.me.guild_permissions.ban_members == False):
			await channel.send('I don\'t have permission to ban!')
		elif (member.guild_permissions.ban_members == False):
			await channel.send('You don\'t have permission to ban!')
		elif (len(message.mentions) < 1):
			await channel.send('You must mention the person(s) to ban!')
		else:
			try:
				t = int(args[len(args) - 1])
			except ValueError:
				t = 0
			test = False
			msg = 'Banned'
			for u in message.mentions:
				if (server.me.top_role.position > u.top_role.position):
					if (member.top_role.position > u.top_role.position):
						try:
							await u.ban(delete_message_days = t)
							msg += ' `' + u.display_name + '`'
							test = True
							try:
								await u.send('You were banned from **' + server.name + '** by **' + member.display_name + '**')
							except:
								pass
						except:
							await channel.send('Failed to ban `' + u.display_name + '`!')
					else:
						await channel.send('`' + u.display_name + '` has a higher role than you!')
				else:
					await channel.send('`' + u.display_name + '` has a higher role than me!')
			if (test == True):
				await channel.send(msg + ' and deleted **' + str(t) + '** days of messages')
				
	# prune
	if (args[0].lower() == 'prune'):
		if (server.me.guild_permissions.manage_messages == False):
			await channel.send('I don\'t have permission to manage messages!')
		elif (member.guild_permissions.manage_messages == False):
			await channel.send('You don\'t have permission to manage messages!')
		elif (len(args) < 2):
			await channel.send('You need to specify the number of messages to prune!')
		else:
			bot = False
			num = 0
			if args[1].lower() == 'bot':
				bot = True
				if (len(args) < 3):
					num = 99
				else:
					try:
						num = int(args[2])
					except ValueError:
						await channel.send('That\'s not a number!')
						return
			else:
				try:
					num = int(args[1])
				except ValueError:
					await channel.send('That\'s not a number!')
					return
			mgs = []
			async for x in channel.history(limit = num + 1):
				if (bot == True):
					if (x.author.bot or x.content.lower().startswith(prefix)):
						mgs.append(x)
				else:
					mgs.append(x)
			try:
				await channel.delete_messages(mgs)
			except discord.HTTPException:
				await channel.send('Failed to prune (messages are probably too old)!')
				return
			m = '` messages!'
			if (bot == True):
				m = '` bot messages & bot calls!'
			pruned = await channel.send('Deleted `' + str(len(mgs)-1) + m)
			await asyncio.sleep(5)
			try:
				await pruned.delete()
			except discord.NotFound:
				pass
