# import
import discord
import sqlite3
import random
import urllib.request
import urllib.parse
import xml.etree.ElementTree
import base64
import html
from renge_utils import load_profile
from renge_utils import save_profile
from renge_utils import is_int

# parse dates in yyyy-mm-dd format to text
async def get_date(date):
	args = date.split('-')
	str = ''
	if args[1] == '01': str='Jan'
	elif args[1] == '02': str='Feb'
	elif args[1] == '03': str='Mar'
	elif args[1] == '04': str='Apr'
	elif args[1] == '05': str='May'
	elif args[1] == '06': str='Jun'
	elif args[1] == '07': str='Jul'
	elif args[1] == '08': str='Aug'
	elif args[1] == '09': str='Sept'
	elif args[1] == '10': str='Oct'
	elif args[1] == '11': str='Nov'
	elif args[1] == '12': str='Dec'
	if (args[2].startswith('0')): args[2]=args[2][1]
	str = str + ' ' + args[1] + ', ' + args[0]
	return str

# misc cmds
async def cmds_misc(message, umsg, client, conn, cur):
	
	# args/variables
	args = umsg.split(' ')
	channel = message.channel
	member = message.author
	
	# song of the day
	if (args[0].lower() == 'sotd'):
		try:
			cur.execute('SELECT * FROM sotd ORDER BY rowid ASC LIMIT 1')
			t = cur.fetchone()
			if (len(args) > 1 and args[1].lower() == 'url'):
				await client.send_message(channel, t[2])
			else:
				embed = discord.Embed(title="Song of the Day", description=t[0] + ' - ' + t[1], url=t[2])
				embed.set_thumbnail(url=t[3])
				await client.send_message(channel, content=None, embed=embed)
		except:
			await client.send_message(channel, "Something went wrong (there probably isn't a song of the day queued)!")
	
	# waifu
	if (args[0].lower() == 'waifu'):
		if (len(args) > 1):
			
			# add
			if (args[1].lower() == 'add'):
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
			elif (args[1].lower() == 'rem' or args[1].lower() == "rm"):
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
								await client.send_message(channel, 'There is no waifu at that number!')
						else:
							await client.send_message(channel, 'Invalid number, need 1-5!')
					elif (args[2].lower() == 'all'):
						data = await load_profile(member, conn, cur)
						if (data[5] != None):
							for a in range(5,10):
								data[a] = None
							await save_profile(data, conn, cur)
							await client.send_message(channel, 'All waifus removed!')
					else:
						await client.send_message(channel, "That isn't a number or `all`!")
				else:
					await client.send_message(channel, 'You must specify a waifu to remove (1-5)!')
					
	# anime lookup
	if (args[0].lower() == 'anime'):
		if (len(args) > 1):
			try:
				userpass = base64.b64encode(b'username:password').decode('ascii')
				req = urllib.request.Request(
					'https://myanimelist.net/api/anime/search.xml?' + urllib.parse.urlencode({'q': umsg[6:]}), 
					data=None, 
					headers={'Authorization': 'Basic ' + userpass}
				)
				with urllib.request.urlopen(req) as url:
					root = xml.etree.ElementTree.parse(url).getroot()
					desc = root[0][10].text.replace('<br />', '')
					embed = discord.Embed(title=root[0][1].text, description=html.unescape(desc), url='https://myanimelist.net/anime/' + root[0][0].text)
					embed.add_field(name='Type', value=root[0][6].text, inline=True)
					embed.add_field(name='Episodes', value=root[0][4].text, inline=True)
					embed.add_field(name='Status', value=root[0][7].text, inline=True)
					embed.add_field(name='Rating', value=root[0][5].text, inline=True)
					embed.add_field(name='Aired', value=await get_date(root[0][8].text), inline=True)
					embed.add_field(name='Ended', value=await get_date(root[0][9].text), inline=True)
					embed.add_field(name='English Title', value=root[0][2].text, inline=False)
					embed.set_thumbnail(url=root[0][11].text)
					await client.send_message(channel, content=None, embed=embed)
			except:
				await client.send_message(channel, 'Anime not found!')
		else:
			await client.send_message(channel, 'You need to specify an anime to look for!')
	
	# magic 8 ball
	if (args[0].lower() == '8ball'):
		if (len(args) > 1):
			str = ':8ball: '
			t = int(random.random() * 23)
			if t == 0: str=str + 'It is certain'
			elif t == 1: str=str + 'It is decidedly so'
			elif t == 2: str=str + 'Without a doubt'
			elif t == 3: str=str + 'Yes, definitely'
			elif t == 4: str=str + 'You can rely on it'
			elif t == 5: str=str + 'You can count on it'
			elif t == 6: str=str + 'As I see it, yes'
			elif t == 7: str=str + 'Most likely'
			elif t == 8: str=str + 'Outlook is good'
			elif t == 9: str=str + 'Yes'
			elif t == 10: str=str + 'Signs point to yes'
			elif t == 11: str=str + 'Absolutely'
			elif t == 12: str=str + 'Reply hazy, try again'
			elif t == 13: str=str + 'Ask again later'
			elif t == 14: str=str + 'Better not tell you now'
			elif t == 15: str=str + 'Cannot predict now'
			elif t == 16: str=str + 'Concentrate and ask again'
			elif t == 17: str=str + "Don't count on it"
			elif t == 18: str=str + 'I think not'
			elif t == 19: str=str + 'My sources say no'
			elif t == 20: str=str + 'Outlook is not so good'
			elif t == 21: str=str + 'Very doubtful'
			elif t == 22: str=str + 'No'
			await client.send_message(channel, str)
		else:
			await client.send_message(channel, 'You need to ask a question!')
