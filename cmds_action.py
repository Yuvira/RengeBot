# import
import discord

# info cmds
async def cmds_action(message, umsg, client):
	
	# args/variables
	args = umsg.split(' ')
	channel = message.channel
	
	# shrug
	if (args[0] == 'shrug'):
		embed = discord.Embed(title='Shrug', type='rich')
		embed.set_image(url='http://i.imgur.com/dka933e.gif')
		await client.send_message(channel, content=None, embed=embed)
	
	# sugoi
	if (args[0] == 'sugoi'):
		embed = discord.Embed(title='SUGOI!', type='rich')
		embed.set_image(url='http://i.imgur.com/ELdj5Nn.gif')
		await client.send_message(channel, content=None, embed=embed)
