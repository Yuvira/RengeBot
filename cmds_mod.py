# import
import discord
import asyncio

# info cmds
async def cmds_mod(message, umsg, prefix, client):
	
	# args/variables
	args = umsg.split(' ')
	channel = message.channel
	server = message.server
	member = message.author
	
	# kick
	if (args[0] == 'kick'):
		if (server.me.server_permissions.kick_members == False):
			await client.send_message(channel, 'I do not have permissions to kick!')
		elif (member.server_permissions.kick_members == False):
			await client.send_message(channel, 'You do not have permissions to kick!')
		elif (len(message.mentions) < 1):
			await client.send_message(channel, 'You must mention the person(s) to kick!')
		else:
			test = False
			msg = "Kicked "
			for i in range(0, len(message.mentions)):
				if server.me.top_role.position > message.mentions[i].top_role.position:
					if member.top_role.position > message.mentions[i].top_role.position:
						try:
							try:
								reason = ''
								t = 1 + len(message.mentions)
								for a in range(t, len(args)):
									reason += ' ' + args[a]
								await client.send_message(message.mentions[i], 'You were kicked from **' + server.name + '** by **' + str(member) + '**:' + reason)
							except:
								pass
							await client.kick(message.mentions[i])
							msg += "`{}` ".format(str(message.mentions[i]))
							test = True
						except:
							await client.send_message(channel, "Something happened, failed to kick!")
					else:
						await client.send_message(channel, "You can't kick someone with a higher role than you!")
				else:
					await client.send_message(channel, "I can't kick that person because they have a role higher than me!")
			if (test == True):
				await client.send_message(channel, msg)
	
	# ban
	if (args[0] == 'ban'):
		t = 0
		if (server.me.server_permissions.ban_members == False):
			await client.send_message(channel, 'I do not have permissions to ban!')
		elif (member.server_permissions.ban_members == False):
			await client.send_message(channel, 'You do not have permissions to ban!')
		elif (len(message.mentions) < 1):
			await client.send_message(channel, 'You must mention the person(s) to ban!')
		else:
			test = False
			try:
				t = int(args[len(args)-1])
			except ValueError:
				t = 0
			msg = "Banned "
			for i in range(0, len(message.mentions)):
				if server.me.top_role.position > message.mentions[i].top_role.position:
					if member.top_role.position > message.mentions[i].top_role.position:
						try:
							try:
								await client.send_message(message.mentions[i], 'You were banned from **' + server.name + '** by **' + str(member) + '**')
							except:
								pass
							await client.ban(message.mentions[i],delete_message_days=t)
							msg += "`{}` ".format(str(message.mentions[i]))
							test = True
						except:
							await client.send_message(channel, "Something happened, failed to ban!")
					else:
						await client.send_message(channel, "You can't ban someone with a higher role than you!")
				else:
					await client.send_message(channel, "I can't ban that person because they have a role higher than me!")
			if (test == True):
				await client.send_message(channel, msg + "and deleted **" + str(t) + "** days of messages")
				
	# prune
	if (args[0] == 'prune'):
		if (server.me.server_permissions.manage_messages == False):
			await client.send_message(channel, "I do not have permissions to manage messages!")
		elif (member.server_permissions.manage_messages == False):
			await client.send_message(channel, 'You do not have permissions to manage messages!')
		elif (len(args) < 2):
			await client.send_message(channel, "You need to specify the number of messages to prune!")
		else:
			if args[1] == 'bot':
				num = 0
				if (len(args) < 3):
					num = 99
				else:
					try:
						num = int(args[2])
					except ValueError:
						await client.send_message(channel, "That's not a number!")
						return
					if num < 5:
						await client.send_message(channel, "That's too few messages!")
						return
					if num > 99:
						num = 99
				mgs = []
				async for x in client.logs_from(channel, limit=num+2):
					if x.author.bot or x.content.lower().startswith(prefix):
						mgs.append(x)
				try:
					await client.delete_messages(mgs)
				except discord.HTTPException:
					await client.send_message(channel, "Failed to prune, messages are probably too old")
					return
				pruned = await client.send_message(channel, "Deleted `" + str(len(mgs)-1) + "` bot messages & bot calls")
				await asyncio.sleep(5)
				try:
					await client.delete_message(pruned)
				except discord.NotFound:
					pass
			else:
				try:
					num = int(args[1])
				except ValueError:
					await client.send_message(channel, "That's not a number or `bot`!")
					return
				if num < 5:
					await client.send_message(channel, "That's too few messages!")
					return
				if num > 99:
					num = 99
				mgs = []
				async for x in client.logs_from(channel, limit=num+1):
					mgs.append(x)
				try:
					await client.delete_messages(mgs)
				except discord.HTTPException:
					await client.send_message(channel, "Failed to prune, messages are probably too old")
					return
				pruned = await client.send_message(channel, "Deleted `" + str(len(mgs)-1) + "` messages")
				await asyncio.sleep(5)
				try:
					await client.delete_message(pruned)
				except discord.NotFound:
					pass
	
