# import
import discord
import sqlite3
from renge_utils import load_profile
from renge_utils import save_profile
from renge_utils import is_int

# misc cmds
async def cmds_misc(message, umsg, client, conn, cur):
	
	# args/variables
	args = umsg.split(' ')
	channel = message.channel
	member = message.author
	
	# song of the day
	if (args[0] == 'sotd'):
		try:
			cur.execute('SELECT * FROM sotd ORDER BY rowid ASC LIMIT 1')
			t = cur.fetchone()
			if (len(args) > 1 and args[1] == 'url'):
				await client.send_message(channel, t[2])
			else:
				embed = discord.Embed(title="Song of the Day", description=t[0] + ' - ' + t[1], url=t[2])
				embed.set_thumbnail(url=t[3])
				await client.send_message(channel, content=None, embed=embed)
		except:
			await client.send_message(channel, "Something went wrong (there probably isn't a song of the day queued)!")
	
	# waifu
	if (args[0] == 'waifu'):
		if (len(args) > 1):
			
			# add
			if (args[1] == 'add'):
				if (len(args) > 2 and len(message.mentions) == 1):
					if (message.mentions[0].id != member.id):
						check1 = False
						pos = 0
						data = await load_profile(member, conn, cur)
						for a in range(9,4,-1):
							if (data[a] == message.mentions[0].id):
								check1 = True
							elif (data[a] == None):
								pos = a
						if (check1 == False):
							if (pos > 0):
								t = await load_profile(message.mentions[0], conn, cur)
								await save_profile(t, conn, cur)
								data[pos] = t[0]
								await save_profile(data, conn, cur)
								await client.send_message(channel, 'Congratulations! **' + message.mentions[0].name + '** is now your waifu!')
							else:
								await client.send_message(channel, 'You have too many waifus already (max 5)!')
						else:
							await client.send_message(channel, 'That person is already your waifu!')
					else:
						await client.send_message(channel, "You can't be your own waifu!")
				else:
					await client.send_message(channel, 'You must mention one user!')
					
			# remove
			elif (args[1] == 'rem' or args[1] == "rm"):
				if (len(args) > 2):
					if (is_int(args[2])):
						if (int(args[2]) > 0 and int(args[2]) < 6):
							data = await load_profile(member, conn, cur)
							if (data[int(args[2])+4] != None):
								try:
									t = await load_profile(data[int(args[2])+4], conn, cur)
									for a in range(int(args[2])+4,9):
										data[a] = data[a+1]
									data[9] = None
									await save_profile(data, conn, cur)
									await client.send_message(channel, '**' + t[1] + '** is no longer your waifu!')
								except:
									for a in range(int(args[2])+4,9):
										data[a] = data[a+1]
									data[9] = None
									await save_profile(data, conn, cur)
									await client.send_message(channel, 'Waifu removed!')
							else:
								await client.send_message(channel, 'There are no waifus at that position!')
						else:
							await client.send_message(channel, 'Invalid number, need 1-5!')
					else:
						await client.send_message(channel, "That isn't a number!")
				else:
					await client.send_message(channel, 'You must specify a waifu to remove (1-5)!')
