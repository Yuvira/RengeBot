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
	server = message.server
	
	# profile
	if (args[0] == 'profile'):
				
		# set profile description
		if (len(args) > 1 and args[1] == 'desc'):
			if (len(args) > 2):
				data = await load_profile(member, conn, cur)
				data[2] = umsg[13:]
				if len(data[2]) > 500:
					await client.send_message(channel, "I couldn't set your description because it is over 500 characters!")
					return
				await save_profile(data, conn, cur)
				await client.send_message(channel, 'Description set to `' + data[2] + '`!')
			else:
				await client.send_message(channel, 'You need to enter a description!')
				
		# show profile
		else:
			
			# get user being profiled
			user = member
			if (len(message.mentions) > 0):
				user = message.mentions[0]
			elif (len(args) > 1):
				check = True
				if (is_int(args[1])):
					try:
						user = await client.get_user_info(args[1])
					except:
						check = False
				else:
					check = False
				if (check == False):
					m = discord.utils.find(lambda u: args[1] in u.display_name.lower(), server.members)
					if (m != None):
						user = m
		
			# load data
			data = await load_profile(user, conn, cur)
			
			# load waifus
			waifu = ''
			for a in range(5,10):
				if (data[a] != None):
					t = await load_profile(data[a], conn, cur)
					waifu = waifu + '\n' + t[1]
			if (waifu == ''):
				waifu = '\nNone'
			
			# display data
			try:
				embed = discord.Embed(title=user.display_name + "'s profile", type='rich', description=data[2] + '\n\n**Credits**\n' + str(data[3]) + '\n\n**Reputation**\n' + str(data[4]) + '\n\n**Waifus**' + waifu, colour=user.colour)
			except:
				embed = discord.Embed(title=user.display_name + "'s profile", type='rich', description=data[2] + '\n\n**Credits**\n' + str(data[3]) + '\n\n**Reputation**\n' + str(data[4]) + '\n\n**Waifus**' + waifu)
			if (user.avatar_url == ''):
				avatar = user.default_avatar_url
			else:
				avatar = user.avatar_url
				avatar = avatar.replace("?size=1024", "")
			embed.set_thumbnail(url=avatar)
			await client.send_message(channel, content=None, embed=embed)
			
	# daily
	if (args[0] == 'daily'):
		
		# check ratelimit
		rl = await load_ratelimit(member, conn, cur)
		t = int(time.time()) - rl[1]
		if (t > 86400):
		
			# add 100 credits to profile
			data = await load_profile(member, conn, cur)
			data[3] = data[3] + 100
			if (data[3] > 9200000000000000000):
				data[3] = 9200000000000000000
				await client.send_message(channel, ':tada: Good job, ' + member.name + ", you reached the credit limit. Hope you're proud of yourself")
			await save_profile(data, conn, cur)
			
			# update ratelimit
			rl[1] = int(time.time())
			await save_ratelimit(rl, conn, cur)
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
		t = int(time.time()) - rl[2]
		if (t > 300):
		
			# get random credits and update profile
			loot = int(random.random() * 40) - 10
			if (loot > 0):
				data = await load_profile(member, conn, cur)
				data[3] += loot
				if (data[3] > 9200000000000000000):
					data[3] = 9200000000000000000
					await client.send_message(channel, ':tada: Good job, ' + member.name + ", you reached the credit limit. Hope you're proud of yourself")
				await save_profile(data, conn, cur)
			
			# update ratelimit
			rl[2] = int(time.time())
			await save_ratelimit(rl, conn, cur)
			if (loot > 0):
				await client.send_message(channel, 'You looted a whole ' + str(loot) + ' credits!')
			else:
				await client.send_message(channel, "You couldn't find anything to loot!")
			
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
								await save_profile(usr1, conn, cur)
								await save_profile(usr2, conn, cur)
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
			
	# rep
	if (args[0] == 'rep'):
		
		# check ratelimit
		rl = await load_ratelimit(member, conn, cur)
		t = int(time.time()) - rl[3]
		if (t > 86400):
		
			#add rep
			if (len(args) == 2):
				if (len(message.mentions) == 1):
					if (message.mentions[0] != message.author):
						data = await load_profile(message.mentions[0], conn, cur)
						data[4] = data[4] + 1
						await save_profile(data, conn, cur)
						rl[3] = int(time.time())
						await save_ratelimit(rl, conn, cur)
						await client.send_message(channel, 'Gave rep to ' + message.mentions[0].name + '!')
					else:
						await client.send_message(channel, "You can't rep yourself!")
				else:
					await client.send_message(channel, 'You need to mention one user!')
			else:
				await client.send_message(channel, 'Incorrect number of arguments!')
			
		# show time remaining
		else:
			msg = "Slow down! You can't rep yet!\nYou can give rep again in "
			t = 86400 - t
			msg = msg + str(int(t/3600)) + ' hours, '
			t = t % 3600
			msg = msg + str(int(t/60)) + ' minutes, '
			t = t % 60
			msg = msg + str(t) + ' seconds'
			await client.send_message(channel, msg)
			
	# get global richest users
	if (args[0] == 'richest'):
		msg = 'Top Ten'
		if (len(args) > 1):
			if (args[1] == 'rep'):
				cur.execute('SELECT * FROM profiles ORDER BY rep DESC LIMIT 10')
				for a in range(0,10):
					t = cur.fetchone()
					msg = msg + '\n' + str(a+1) + '. **' + t[1] + '** - ' + str(t[4])
				embed = discord.Embed(title='Global Most Reputable Users', type='rich', description=msg)
				await client.send_message(channel, content=None, embed=embed)
		else:
			cur.execute('SELECT * FROM profiles ORDER BY credits DESC LIMIT 10')
			for a in range(0,10):
				t = cur.fetchone()
				msg = msg + '\n' + str(a+1) + '. **' + t[1] + '** - $' + str(t[3])
			embed = discord.Embed(title='Global Richest Users', type='rich', description=msg)
			await client.send_message(channel, content=None, embed=embed)
			
	# return user balance
	if (args[0] == 'balance'):
	
		# get user being checked
		user = member
		if (len(message.mentions) > 0):
			user = message.mentions[0]
		elif (len(args) > 1):
			check = True
			if (is_int(args[1])):
				try:
					user = await client.get_user_info(args[1])
				except:
					check = False
			else:
				check = False
			if (check == False):
				m = discord.utils.find(lambda u: args[1] in u.display_name.lower(), server.members)
				if (m != None):
					user = m
					
		# load data
		data = await load_profile(user, conn, cur)
		
		# display data
		if (member == message.author):
			await client.send_message(channel, user.display_name + ' has ' + str(data[3]) + ' credits!')
		else:
			await client.send_message(channel, user.display_name + ' has ' + str(data[3]) + ' credits!')
