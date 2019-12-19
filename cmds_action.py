# import
import discord
import urllib.request
import json

# load weeb images
async def get_image(client, channel, type, head, text):
	req = urllib.request.Request(
		'https://rra.ram.moe/i/r?type=' + type, 
		data = None, 
		headers = {'token'}
	)
	with urllib.request.urlopen(req) as url:
		data = json.loads(url.read().decode())
		embed = discord.Embed(title = head, description = text, type = 'rich')
		embed.set_image(url = 'https://rra.ram.moe' + data['path'])
		await channel.send(content = None, embed = embed)
		
# list users
async def list_mentions(users):
	text = ''
	if (len(users) > 2):
		text = '**' + users[0].display_name + '**'
		for a in range (1,len(users)-1):
			text = text + ', **' + users[a].display_name + '**'
		text = text + ' and **' + users[len(users)-1].display_name + '**'
	elif (len(users) > 1):
		text = '**' + users[0].display_name + '** and **' + users[1].display_name + '**'
	else:
		text = '**' + users[0].display_name + '**'
	return text

# info cmds
async def cmds_action(message, umsg, client):
	
	# args/variables
	args = umsg.split(' ')
	channel = message.channel
	member = message.author
	
	# pat
	if (args[0].lower() == 'pat'):
		if (len(message.mentions) > 0):
			if (len(message.mentions) == 1 and message.mentions[0] == member):
				await get_image(client, channel, 'pat', 'Pat', '*Pats you*')
			else:
				list = await list_mentions(message.mentions)
				await get_image(client, channel, 'pat', 'Pat', '**' + member.display_name + '**' + ' is patting ' + list)
		else:
			await channel.send('You need to mention someone to pat!')
	
	# hug
	if (args[0].lower() == 'hug'):
		if (len(message.mentions) > 0):
			if (len(message.mentions) == 1 and message.mentions[0] == member):
				await get_image(client, channel, 'hug', 'Hug', '*Hugs you*')
			else:
				list = await list_mentions(message.mentions)
				await get_image(client, channel, 'hug', 'Hug', '**' + member.display_name + '**' + ' is hugging ' + list)
		else:
			await channel.send('You need to mention someone to hug!')
	
	# pout
	if (args[0].lower() == 'pout'):
		if (len(message.mentions) > 0):
			if (len(message.mentions) == 1 and message.mentions[0] == member):
				await get_image(client, channel, 'pout', 'Pout', '*Pouts at you*')
			else:
				list = await list_mentions(message.mentions)
				await get_image(client, channel, 'pout', 'Pout', '**' + member.display_name + '**' + ' is pouting at ' + list)
		else:
			await get_image(client, channel, 'pout', 'Pout', '**' + member.display_name + '**' + ' is pouting, alone')
	
	# slap
	if (args[0].lower() == 'slap'):
		if (len(message.mentions) > 0):
			if (len(message.mentions) == 1 and message.mentions[0] == member):
				await get_image(client, channel, 'slap', 'Slap', 'Why am I doing this? *Slaps you*')
			else:
				list = await list_mentions(message.mentions)
				await get_image(client, channel, 'slap', 'Slap', '**' + member.display_name + '**' + ' is slapping ' + list)
		else:
			await channel.send('You need to mention someone to slap!')
	
	# stare
	if (args[0].lower() == 'stare'):
		if (len(message.mentions) > 0):
			if (len(message.mentions) == 1 and message.mentions[0] == member):
				await get_image(client, channel, 'stare', 'Stare', '*Stares at you*')
			else:
				list = await list_mentions(message.mentions)
				await get_image(client, channel, 'stare', 'Stare', '**' + member.display_name + '**' + ' is staring at ' + list)
		else:
			await channel.send('You need to mention someone to stare at!')
	
	# nom
	if (args[0].lower() == 'nom'):
		if (len(message.mentions) > 0):
			if (len(message.mentions) == 1 and message.mentions[0] == member):
				await get_image(client, channel, 'nom', 'Nom', '*Nibbles on you*')
			else:
				list = await list_mentions(message.mentions)
				await get_image(client, channel, 'nom', 'Nom', '**' + member.display_name + '**' + ' is eating ' + list)
		else:
			await get_image(client, channel, 'nom', 'Nom', '**' + member.display_name + '**' + ' is eating by themselves')
	
	# shrug
	if (args[0].lower() == 'shrug'):
		embed = discord.Embed(title = 'Shrug', type = 'rich')
		embed.set_image(url = 'http://i.imgur.com/dka933e.gif')
		await channel.send(content = None, embed = embed)
	
	# sugoi
	if (args[0].lower() == 'sugoi'):
		embed = discord.Embed(title = 'SUGOI!', type = 'rich')
		embed.set_image(url = 'http://i.imgur.com/ELdj5Nn.gif')
		await channel.send(content = None, embed = embed)
