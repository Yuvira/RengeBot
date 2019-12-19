# import
import discord
import sqlite3
import random
import requests
import json
import html
from renge_utils import load_profile
from renge_utils import save_profile
from renge_utils import is_int

# parse dates in yyyy-mm-dd format to text
def get_date(date):
	args = date.split('-')
	s = ''
	str = ''
	if args[1] == '1': str = 'Jan'
	elif args[1] == '2': str = 'Feb'
	elif args[1] == '3': str = 'Mar'
	elif args[1] == '4': str = 'Apr'
	elif args[1] == '5': str = 'May'
	elif args[1] == '6': str = 'Jun'
	elif args[1] == '7': str = 'Jul'
	elif args[1] == '8': str = 'Aug'
	elif args[1] == '9': str = 'Sept'
	elif args[1] == '10': str = 'Oct'
	elif args[1] == '11': str = 'Nov'
	elif args[1] == '12': str = 'Dec'
	if (str == ''):
		s = 'Ongoing'
	else:
		s = str + ' ' + args[1] + ', ' + args[0]
	return s
	
# get format
def get_format(format):
	s = ''
	if format == 'TV': s = 'TV'
	if format == 'TV_SHORT': s = 'Short'
	if format == 'MOVIE': s = 'Movie'
	if format == 'SPECIAL': s = 'Special'
	if format == 'OVA': s = 'OVA'
	if format == 'ONA': s = 'ONA'
	if format == 'MUSIC': s = 'Music'
	if format == 'MANGA': s = 'Manga'
	if format == 'NOVEL': s = 'Novel'
	if format == 'ONE_SHOT': s = 'One-Shot'
	return s

# get status
def get_status(status):
	s = ''
	if status == 'FINISHED': s = 'Finished'
	if status == 'RELEASING': s = 'Active'
	if status == 'NOT_YET_RELEASED': s = 'Unreleased'
	if status == 'CANCELLED': s = 'Cancelled'
	return s

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
				await channel.send(t[2])
			else:
				embed = discord.Embed(title = 'Song of the Day', description = t[0] + ' - ' + t[1], url = t[2])
				embed.set_thumbnail(url = t[3])
				await channel.send(content = None, embed = embed)
		except:
			await channel.send('Something went wrong (there probably isn\'t a song of the day queued)!')
	
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
						for a in range(9, 4, -1):
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
								await channel.send('Congratulations! **' + message.mentions[0].name + '** is now your waifu!')
							else:
								await channel.send('You have too many waifus already (max 5)!')
						else:
							await channel.send('That person is already your waifu!')
					else:
						await channel.send('You can\'t be your own waifu!')
				else:
					await channel.send('You must mention one user!')
					
			# remove
			elif (args[1].lower() == 'remove' or args[1].lower() == 'rem' or args[1].lower() == 'rm'):
				if (len(args) > 2):
					if (is_int(args[2])):
						if (int(args[2]) > 0 and int(args[2]) < 6):
							data = await load_profile(member, conn, cur)
							if (data[int(args[2]) + 4] != None):
								try:
									t = await load_profile(data[int(args[2]) + 4], conn, cur)
									for a in range(int(args[2]) + 4,9):
										data[a] = data[a + 1]
									data[9] = None
									await save_profile(data, conn, cur)
									await channel.send('**' + t[1] + '** is no longer your waifu!')
								except:
									for a in range(int(args[2]) + 4,9):
										data[a] = data[a + 1]
									data[9] = None
									await save_profile(data, conn, cur)
									await channel.send('Waifu removed!')
							else:
								await channel.send('There is no waifu at that number!')
						else:
							await channel.send('Invalid number, need 1-5!')
					elif (args[2].lower() == 'all'):
						data = await load_profile(member, conn, cur)
						if (data[5] != None):
							for a in range(5, 10):
								data[a] = None
							await save_profile(data, conn, cur)
							await channel.send('All waifus removed!')
					else:
						await channel.send('That isn\'t a number or `all`!')
				else:
					await channel.send('You must specify a waifu to remove (1-5)!')
			
			# invalid action
			else:
				await channel.send('That\'s not something you can do with your waifus!')
					
	# anime lookup
	if (args[0].lower() == 'anime'):
		if (len(args) > 1):
			
			# setup query
			query = '''
			query ($search: String) {
				Media (search: $search, type:ANIME) {
					id
					title {
						romaji
						english
					}
					description
					format
					status
					startDate {
						year
						month
						day
					}
					endDate {
						year
						month
						day
					}
					episodes
					averageScore
					coverImage {
						medium
					}
				}
			}
			'''
			
			# set search query
			variables = {
				'search': umsg[6:]
			}
			
			# get response and load to json
			url = 'https://graphql.anilist.co'
			response = requests.post(url, json = {'query': query, 'variables': variables})
			j = json.loads(response.text)
			
			# send data
			try:
				data = j['data']['Media']
				desc = data['description'].replace('<br>', '')
				embed = discord.Embed(title = data['title']['romaji'], description = html.unescape(desc), url = 'https://anilist.co/anime/' + str(data['id']))
				embed.add_field(name = 'Format', value=get_format(data['format']), inline = True)
				embed.add_field(name = 'Episodes', value=str(data['episodes']), inline = True)
				embed.add_field(name = 'Status', value=get_status(data['status']), inline = True)
				embed.add_field(name = 'Rating', value=str(data['averageScore'])[0] + '.' + str(data['averageScore'])[1], inline = True)
				embed.add_field(name = 'Aired', value=get_date(str(data['startDate']['year']) + '-' + str(data['startDate']['month']) + '-' + str(data['startDate']['day'])), inline = True)
				embed.add_field(name = 'Ended', value=get_date(str(data['endDate']['year']) + '-' + str(data['endDate']['month']) + '-' + str(data['endDate']['day'])), inline = True)
				embed.add_field(name = 'English Title', value=data['title']['english'], inline = True)
				embed.set_thumbnail(url = data['coverImage']['medium'])
				await channel.send(content = None, embed = embed)
			except:
				await channel.send('Anime not found!')
			
		else:
			await channel.send('You need to specify an anime to look for!')
					
	# manga lookup
	if (args[0].lower() == 'manga'):
		if (len(args) > 1):
			
			# setup query
			query = '''
			query ($search: String) {
				Media (search: $search, type:MANGA) {
					id
					title {
						romaji
						english
					}
					description
					format
					status
					startDate {
						year
						month
						day
					}
					endDate {
						year
						month
						day
					}
					chapters
					volumes
					averageScore
					coverImage {
						medium
					}
				}
			}
			'''
			
			# set search query
			variables = {
				'search': umsg[6:]
			}
			
			# get response and load to json
			url = 'https://graphql.anilist.co'
			response = requests.post(url, json = {'query': query, 'variables': variables})
			j = json.loads(response.text)
			
			# send data
			try:
				data = j['data']['Media']
				desc = data['description'].replace('<br>', '')
				embed = discord.Embed(title = data['title']['romaji'], description = html.unescape(desc), url = 'https://anilist.co/manga/' + str(data['id']))
				embed.add_field(name = 'Format', value=get_format(data['format']), inline = True)
				embed.add_field(name = 'Volumes/Chapters', value=str(data['volumes']) + '/' + str(data['chapters']), inline = True)
				embed.add_field(name = 'Status', value=get_status(data['status']), inline = True)
				embed.add_field(name = 'Rating', value=str(data['averageScore'])[0] + '.' + str(data['averageScore'])[1], inline = True)
				embed.add_field(name = 'Aired', value=get_date(str(data['startDate']['year']) + '-' + str(data['startDate']['month']) + '-' + str(data['startDate']['day'])), inline = True)
				embed.add_field(name = 'Ended', value=get_date(str(data['endDate']['year']) + '-' + str(data['endDate']['month']) + '-' + str(data['endDate']['day'])), inline = True)
				embed.add_field(name = 'English Title', value=data['title']['english'], inline = True)
				embed.set_thumbnail(url = data['coverImage']['medium'])
				await channel.send(content = None, embed = embed)
			except:
				await channel.send('Manga not found!')
			
		else:
			await channel.send('You need to specify an anime to look for!')
	
	# magic 8 ball
	if (args[0].lower() == '8ball'):
		if (len(args) > 1):
			s = ':8ball: '
			t = int(random.random() * 23)
			if t == 0: s += 'It is certain'
			elif t == 1: s += 'It is decidedly so'
			elif t == 2: s += 'Without a doubt'
			elif t == 3: s += 'Yes, definitely'
			elif t == 4: s += 'You can rely on it'
			elif t == 5: s += 'You can count on it'
			elif t == 6: s += 'As I see it, yes'
			elif t == 7: s += 'Most likely'
			elif t == 8: s += 'Outlook is good'
			elif t == 9: s += 'Yes'
			elif t == 10: s += 'Signs point to yes'
			elif t == 11: s += 'Absolutely'
			elif t == 12: s += 'Reply hazy, try again'
			elif t == 13: s += 'Ask again later'
			elif t == 14: s += 'Better not tell you now'
			elif t == 15: s += 'Cannot predict now'
			elif t == 16: s += 'Concentrate and ask again'
			elif t == 17: s += 'Don\'t count on it'
			elif t == 18: s += 'I think not'
			elif t == 19: s += 'My sources say no'
			elif t == 20: s += 'Outlook is not so good'
			elif t == 21: s += 'Very doubtful'
			elif t == 22: s += 'No'
			await channel.send(s)
		else:
			await channel.send('You need to ask a question!')
