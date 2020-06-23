import discord
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
print('The token is {}'.format(config['DEFAULT']['token']))
token = config['DEFAULT']['token']

client = discord.Client()


@client.event
async def on_ready():
    print('we are ready mother fucker {0.user}'.format(client))

@client.event
async def on_message(message):
    print(message)
    if message.content.startswith('!'):
        await message.channel.send('Hello')


client.run(token)
