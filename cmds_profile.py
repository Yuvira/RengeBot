# import
import discord
from pathlib import Path
from ast import literal_eval
import codecs

# info cmds
async def cmds_profile(message, umsg, client):
	
	# args/variables
	args = umsg.split(' ')
	channel = message.channel
	member = message.author
	
	# check/create profile
	profile = Path('profiles/' + member.id + '.prof')
	if (profile.is_file()):
		pass
	else:
		data = ['Nothing to see here.']
		file = codecs.open('profiles/' + member.id + '.prof', 'w+', 'utf-8')
		for a in range(0, len(data)):
			file.write(str(data[a]) + '\n')
		file.close()
	
	# profile
	if (args[0] == 'profile'):
		
		# load data
		with open('profiles/' + member.id + '.prof') as f:
			data = f.readlines()
		data = [x.strip('\n') for x in data]
		try:
			data[0] = literal_eval(data[0])
		except:
			data[0] = literal_eval('"' + data[0] + '"')
				
		# profile commands
		if (len(args) > 1):
			
			# description set
			if (args[1] == 'desc'):
				if (len(args) > 2):
					data[0] = umsg[13:]
					await client.send_message(channel, 'Description set to `' + data[0] + '`!')
				else:
					await client.send_message(channel, 'You need to enter a description!')
		
		# show profile
		else:
			embed = discord.Embed(title=member.name + "'s profile", type='rich', description=str(data[0]))
			await client.send_message(channel, content=None, embed=embed)
		
		# save profile
		file = codecs.open('profiles/' + member.id + '.prof', 'w+', 'utf-8')
		file.write(repr(data[0]))
		for a in range(1, len(data)):
			file.write(str(data[a]) + '\n')
		file.close()
