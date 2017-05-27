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
		if (channel.permissions_for(server.me).kick_members == False):
			await client.send_message(channel, 'I do not have permissions to kick!')
		elif (channel.permissions_for(member).kick_members == False):
			await client.send_message(channel, 'You do not have permissions to kick!')
		elif (len(message.mentions) < 1):
			await client.send_message(channel, 'You must mention the person(s) to kick!')
		else:
			check = 0
			rrole = len(role_hierarchy)
			t = server.me.top_role
			for a in range(0, len(server.role_hierarchy)):
				if (t == role_hierarchy[a]):
					rrole = a
			for a in range(0, len(message.mentions)):
				t = message.mentions[a].top_role
				for a in range(0, len(server.role_hierarchy)):
					if (t == role_hierarchy[a]):
						if (a <= rrole):
							check = 1
			if (check == 0):
				msg = 'Kicked '
				for a in range(0, len(message.mentions)):
					msg = msg + '`' + message.mentions[a].name + '` '
					private_channel = server.get_member(message.mentions[a].id)
					try:
						await client.send_message(private_channel, 'You were kicked from **' + server.name + '** by **' + member.name + '**')
					except HTTPException:
						pass
				for a in range(0, len(message.mentions)):
					await client.kick(message.mentions[a])
			else:
				msg = 'Failed to kick! My role is lower than one or more of the mentioned users!'
			await client.send_message(channel, msg)
	
	# ban
	if (args[0] == 'ban'):
		t = 0
		if (channel.permissions_for(server.me).ban_members == False):
			await client.send_message(channel, 'I do not have permissions to ban!')
		elif (channel.permissions_for(member).ban_members == False):
			await client.send_message(channel, 'You do not have permissions to ban!')
		elif (len(message.mentions) < 1):
			await client.send_message(channel, 'You must mention the person(s) to ban!')
		else:
			check = 0
			rrole = len(role_hierarchy)
			t = server.me.top_role
			for a in range(0, len(server.role_hierarchy)):
				if (t == role_hierarchy[a]):
					rrole = a
			for a in range(0, len(message.mentions)):
				t = message.mentions[a].top_role
				for a in range(0, len(server.role_hierarchy)):
					if (t == role_hierarchy[a]):
						if (a <= rrole):
							check = 1
			try:
				t = int(args[len(args)-1])
			except ValueError:
				t = 0
			if (check == 0):
				msg = 'Banned '
				for a in range(0, len(message.mentions)):
					msg = msg + '`' + message.mentions[a].name + '` '
					private_channel = server.get_member(message.mentions[a].id)
					try:
						await client.send_message(private_channel, 'You were banned from **' + server.name + '** by **' + member.name + '**')
					except HTTPException:
						pass
				for a in range(0, len(message.mentions)):
					await client.ban(message.mentions[a], delete_message_days=t)
				await client.send_message(channel, msg + 'and deleted their messages from the past ' + str(t) + ' days')
			else:
				await client.send_message(channel, 'Failed to ban! My role is lower than one or more of the mentioned users!')
