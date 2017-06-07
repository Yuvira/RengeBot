# import
import discord
import time
import random
import sqlite3
from renge_utils import load_profile
from renge_utils import save_profile
from renge_utils import load_ratelimit
from renge_utils import save_ratelimit
from renge_utils import is_int

# info cmds
async def cmds_currency(message, umsg, client, conn, cur):
	
	# args/variables
	args = umsg.split(' ')
	channel = message.channel
	member = message.author
	
	# profile
	if (args[0] == 'profile'):
		
		# show other person's profile
		if (len(args) == 2 and len(message.mentions) > 0):
		
			# load data
			data = await load_profile(message.mentions[0], conn, cur)
			
			# display data
			embed = discord.Embed(title=message.mentions[0].name + "'s profile", type='rich', description=data[2] + '\n\n**Credits**\n' + str(data[3]), colour=message.mentions[0].colour)
			if (message.mentions[0].avatar_url == ''):
				embed.set_thumbnail(url=message.mentions[0].default_avatar_url)
			else:
				embed.set_thumbnail(url=message.mentions[0].avatar_url)
			await client.send_message(channel, content=None, embed=embed)
				
		# profile commands
		elif (len(args) > 1):
			
			# load data
			data = await load_profile(member, conn, cur)
			
			# description set
			if (args[1] == 'desc'):
				if (len(args) > 2):
					data[2] = umsg[13:]
					await client.send_message(channel, 'Description set to `' + data[2] + '`!')
				else:
					await client.send_message(channel, 'You need to enter a description!')
		
			# save profile
			await save_profile(member, data, conn, cur)
		
		# show profile
		else:
			
			# load data
			data = await load_profile(member, conn, cur)
			
			# display data
			embed = discord.Embed(title=member.name + "'s profile", type='rich', description=data[2] + '\n\n**Credits**\n' + str(data[3]), colour=member.colour)
			if (member.avatar_url == ''):
				embed.set_thumbnail(url=member.default_avatar_url)
			else:
				embed.set_thumbnail(url=member.avatar_url)
			await client.send_message(channel, content=None, embed=embed)
			
	# daily
	if (args[0] == 'daily'):
		
		# check ratelimit
		rl = await load_ratelimit(member, conn, cur)
		t = int(time.time()) - rl[2]
		if (t > 86400):
		
			# add 100 credits to profile
			data = await load_profile(member, conn, cur)
			data[3] = data[3] + 100
			if (data[3] > 9200000000000000000):
				data[3] = 9200000000000000000
				await client.send_message(channel, ':tada: Good job, ' + member.name + ", you reached the credit limit. Hope you're proud of yourself")
			await save_profile(member, data, conn, cur)
			
			# update ratelimit
			rl[2] = int(time.time())
			await save_ratelimit(member, rl, conn, cur)
			await client.send_message(channel, 'You have received your daily 100 credits!')
			
		# show time remaining
		else:
			msg = "Slow down! Your daily credits aren't ready yet!\nYou can get your next daily in "
			t = 86400 - t
			msg = msg + str(int(t/3600)) + ' hours, '
			t = t % 3600
			msg = msg + str(int(t/60)) + ' minutes, '
			t = t % 60
			msg = msg + str(t) + ' seconds'
			await client.send_message(channel, msg)
			
	# loot
	if (args[0] == 'loot'):
		
		# check ratelimit
		rl = await load_ratelimit(member, conn, cur)
		t = int(time.time()) - rl[3]
		if (t > 300):
		
			# get random credits and update profile
			loot = int(random.random() * 40) - 10
			if (loot > 0):
				data = await load_profile(member, conn, cur)
				data[3] = data[3] + loot
				if (data[3] > 9200000000000000000):
					data[3] = 9200000000000000000
					await client.send_message(channel, ':tada: Good job, ' + member.name + ", you reached the credit limit. Hope you're proud of yourself")
				await save_profile(member, data, conn, cur)
			
			# update ratelimit
			rl[3] = int(time.time())
			await save_ratelimit(member, rl, conn, cur)
			if (loot > 0):
				await client.send_message(channel, 'You looted a whole ' + str(loot) + ' credits!')
			else:
				await client.send_message(channel, "You couldn't find anything to loot")
			
		# show time remaining
		else:
			msg = "Slow down! You just looted not that long ago!\nYou can loot again in "
			t = 300 - t
			msg = msg + str(int(t/60)) + ' minutes, '
			t = t % 60
			msg = msg + str(t) + ' seconds'
			await client.send_message(channel, msg)
			
	# transfer
	if (args[0] == 'transfer'):
		if (len(args) == 3):
			if (len(message.mentions) == 1):
				if (is_int(args[2])):
					if (int(args[2]) > 0):
						usr1 = await load_profile(member, conn, cur)
						if (int(args[2]) <= usr1[3]):
							usr2 = await load_profile(message.mentions[0], conn, cur)
								if (usr1[0] != usr2[0]):
								usr1[3] -= int(args[2])
								usr2[3] += int(args[2])
								await save_profile(member, usr1, conn, cur)
								await save_profile(message.mentions[0], usr2, conn, cur)
								await client.send_message(channel, 'Successfully transferred ' + args[2] + ' credits to ' + message.mentions[0].name + '!')
							else:
								await client.send_message(channel, "You can't transfer to yourself!")
						else:
							await client.send_message(channel, "You don't have that much money!")
					else:
						await client.send_message(channel, "You can't transfer negative credits!")
				else:
					await client.send_message(channel, 'Invalid transfer amount!')
			else:
				await client.send_message(channel, 'You need to mention one user!')
		else:
			await client.send_message(channel, 'Incorrect number of arguments!')
			
	# get global richest users
	if (args[0] == 'richest'):
		msg = 'Top Ten'
		cur.execute('SELECT * FROM profiles ORDER BY credits DESC')
		for a in range(0,10):
			t = cur.fetchone()
			msg = msg + '\n' + str(a+1) + '. ' + t[1] + ' - $' + str(t[3])
		embed = discord.Embed(title='Global Richest Users', type='rich', description=msg)
		await client.send_message(channel, content=None, embed=embed)
