# import
import discord

# info cmds
async def cmds_mod(message, umsg, client):
	
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
			msg = "Kicked "
			for i in range(0, len(message.mentions)):
				if server.me.top_role.position > message.mentions[i].top_role.position:
					if member.top_role.position > message.mentions[i].top_role.position:
						try:
							try:
								await client.send_message(message.mentions[i], 'You were kicked from **' + server.name + '** by **' + str(member) + '**')
							except:
								pass
							await client.kick(message.mentions[i])
							msg += "`{}` ".format(str(message.mentions[i]))
						except:
							await client.send_message(channel, "Something happened while trying to kick the member :<")
					else:
						await client.send_message(channel, "You can't kick someone with a higher role than you!")
				else:
					await client.send_message(channel, "I can't kick that person because they have a role higher than me!")
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
						except:
							await client.send_message(channel, "Something happened while trying to ban the member.") # this shouldnt happen
					else:
						await client.send_message(channel, "Can't allow you to ban someone with a higher role than you.")
				else:
					await client.send_message(channel, "I can't ban that person because they have a role higher than me.")
			await client.send_message(channel, msg + "and deleted **" + str(t) + "** days of messages.")
