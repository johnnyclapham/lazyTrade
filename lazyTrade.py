import discord
import config


'''
Simple bare-bones discord bot for further development.
Created for Python 3.7+
@author johnnyclapham 2021
'''

client = discord.Client()

@client.event
async def on_ready():
    print('Bot with userid: {0.user} connected'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('hello'):
        await message.channel.send('Hello! how are you?')
    if message.content.startswith('good'):
        await message.channel.send('Really? That is excellent news.')
    if message.content.startswith('bye'):
        await message.channel.send('until next time!')
    if message.content.startswith('bring me news'):
        await message.channel.send('until next time!')


client.run(config.KEY)
