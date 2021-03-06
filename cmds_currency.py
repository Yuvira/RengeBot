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
	server = message.guild
	
	# profile
	if (args[0].lower() == 'profile'):
				
		# set profile description
		if (len(args) > 1 and (args[1].lower() == 'desc' or args[1].lower() == 'description')):
			if (len(args) > 2):
				data = await load_profile(member, conn, cur)
				if (args[1].lower() == 'desc'):
					data[2] = umsg[13:]
				else:
					data[2] = umsg[20:]
				if len(data[2]) > 500:
					await channel.send('I couldn\'t set your description because i\'s over 500 characters!')
					return
				await save_profile(data, conn, cur)
				await channel.send('Description set to `' + data[2] + '`!')
			else:
				await channel.send('You need to enter a description!')
				
		# show profile
		else:
			
			# get user being profiled
			user = member
			if (len(message.mentions) > 0):
				user = message.mentions[0]
			elif (len(args) > 1):
				try:
					user = await client.fetch_user(args[1])
				except:
					m = discord.utils.find(lambda u: args[1].lower() in u.display_name.lower(), server.members)
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
				embed = discord.Embed(title = user.display_name + '\'s profile', type = 'rich', description = data[2] + '\n\n**Credits**\n' + data[3] + '\n\n**Reputation**\n' + data[4] + '\n\n**Waifus**' + waifu, colour = user.colour)
			except:
				embed = discord.Embed(title = user.display_name + '\'s profile', type = 'rich', description = data[2] + '\n\n**Credits**\n' + data[3] + '\n\n**Reputation**\n' + data[4] + '\n\n**Waifus**' + waifu)
			if (user.avatar_url == ''):
				avatar = str(user.default_avatar_url)
			else:
				avatar = str(user.avatar_url)
				avatar = avatar.replace('?size=1024', '')
			embed.set_thumbnail(url = avatar)
			await channel.send(content = None, embed = embed)
			
	# daily
	if (args[0].lower() == 'daily'):
		
		# check ratelimit
		rl = await load_ratelimit(member, conn, cur)
		t = int(time.time()) - rl[1]
		if (t > 86400):
		
			# add 100 credits to profile
			data = await load_profile(member, conn, cur)
			data[3] = str(int(data[3]) + 100)
			await save_profile(data, conn, cur)
			
			# update ratelimit
			rl[1] = int(time.time())
			await save_ratelimit(rl, conn, cur)
			await channel.send('You have received your daily 100 credits!')
			
		# show time remaining
		else:
			msg = 'Slow down! Your daily credits aren\'t ready yet!\nYou can get your next daily in '
			t = 86400 - t
			msg = msg + str(int(t/3600)) + ' hours, '
			t = t % 3600
			msg = msg + str(int(t/60)) + ' minutes, '
			t = t % 60
			msg = msg + str(t) + ' seconds'
			await channel.send(msg)
			
	# loot
	if (args[0].lower() == 'loot'):
		
		# check ratelimit
		rl = await load_ratelimit(member, conn, cur)
		t = int(time.time()) - rl[2]
		if (t > 300):
		
			# get random credits and update profile
			loot = int(random.random() * 40) - 10
			if (loot > 0):
				data = await load_profile(member, conn, cur)
				data[3] = str(int(data[3]) + loot)
				await save_profile(data, conn, cur)
			
			# update ratelimit
			rl[2] = int(time.time())
			await save_ratelimit(rl, conn, cur)
			if (loot > 0):
				await channel.send('You looted a whole ' + str(loot) + ' credits!')
			else:
				await channel.send('You couldn\'t find anything to loot!')
			
		# show time remaining
		else:
			msg = 'Slow down! You just looted not that long ago!\nYou can loot again in '
			t = 300 - t
			msg = msg + str(int(t/60)) + ' minutes, '
			t = t % 60
			msg = msg + str(t) + ' seconds'
			await channel.send(msg)
			
	# transfer
	if (args[0].lower() == 'transfer'):
		if (len(args) == 3):
			if (len(message.mentions) == 1):
				if (is_int(args[2])):
					if (int(args[2]) > 0):
						usr1 = await load_profile(member, conn, cur)
						if (int(args[2]) <= int(usr1[3])):
							usr2 = await load_profile(message.mentions[0], conn, cur)
							if (usr1[0] != usr2[0]):
								usr1[3] = str(int(usr1[3]) - int(args[2]))
								usr2[3] = str(int(usr2[3]) + int(args[2]))
								await save_profile(usr1, conn, cur)
								await save_profile(usr2, conn, cur)
								if (message.mentions[0] == server.me):
									await channel.send('Thank you for your donation of ' + args[2] + ' credits!')
								else:
									await channel.send('Successfully transferred ' + args[2] + ' credits to ' + message.mentions[0].name + '!')
							else:
								await channel.send('You can\'t transfer to yourself!')
						else:
							await channel.send('You don\'t have that much money!')
					else:
						await channel.send('You can\'t transfer negative credits!')
				else:
					await channel.send('Invalid transfer amount!')
			else:
				await channel.send('You need to mention one user!')
		else:
			await channel.send('Incorrect number of arguments!')
			
	# rep
	if (args[0].lower() == 'rep'):
		
		# check ratelimit
		rl = await load_ratelimit(member, conn, cur)
		t = int(time.time()) - rl[3]
		if (t > 86400):
		
			#add rep
			if (len(args) == 2):
				if (len(message.mentions) == 1):
					if (message.mentions[0] != message.author):
						data = await load_profile(message.mentions[0], conn, cur)
						data[4] = str(int(data[4]) + 1)
						await save_profile(data, conn, cur)
						rl[3] = int(time.time())
						await save_ratelimit(rl, conn, cur)
						await channel.send('Gave rep to ' + message.mentions[0].name + '!')
					else:
						await channel.send('You can\'t rep yourself!')
				else:
					await channel.send('You need to mention someone!')
			else:
				await channel.send('You need to mention someone!')
			
		# show time remaining
		else:
			msg = 'Slow down! You can\'t rep yet!\nYou can give rep again in '
			t = 86400 - t
			msg = msg + str(int(t/3600)) + ' hours, '
			t = t % 3600
			msg = msg + str(int(t/60)) + ' minutes, '
			t = t % 60
			msg = msg + str(t) + ' seconds'
			await channel.send(msg)
			
	# get global richest users
	if (args[0].lower() == 'richest'):
		msg = 'Top Ten'
		if (len(args) > 1):
			if (args[1].lower() == 'rep'):
				cur.execute('SELECT * FROM profiles ORDER BY CAST(rep AS INTEGER) DESC LIMIT 10')
				for a in range(0,10):
					t = cur.fetchone()
					msg = msg + '\n' + str(a + 1) + '. **' + t[1] + '** - ' + str(t[4])
				embed = discord.Embed(title = 'Global Most Reputable Users', type = 'rich', description = msg)
				await channel.send(content = None, embed = embed)
		else:
			cur.execute('SELECT * FROM profiles ORDER BY CAST(credits AS INTEGER) DESC LIMIT 10')
			for a in range(0,10):
				t = cur.fetchone()
				msg = msg + '\n' + str(a + 1) + '. **' + t[1] + '** - $' + str(t[3])
			embed = discord.Embed(title = 'Global Richest Users', type = 'rich', description = msg)
			await channel.send(content = None, embed = embed)
			
	# return user balance
	if (args[0].lower() == 'balance' or args[0].lower() == 'bal'):
	
		# get user being checked
		user = member
		if (len(message.mentions) > 0):
			user = message.mentions[0]
		elif (len(args) > 1):
			try:
				user = await client.fetch_user(args[1])
			except:
				m = discord.utils.find(lambda u: args[1].lower() in u.display_name.lower(), server.members)
				if (m != None):
					user = m
					
		# load data
		data = await load_profile(user, conn, cur)
		
		# display data
		if (member == message.author):
			await channel.send(user.display_name + ' has ' + data[3] + ' credits!')
		else:
			await channel.send(user.display_name + ' has ' + data[3] + ' credits!')
