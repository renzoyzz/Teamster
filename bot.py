from enum import Enum
import discord

client = discord.Client()

class Stage(Enum):
    IDLE = 0
    SETUP_CHANNELS = 1
    REGISTER_PLAYERS = 2
    SPLIT = 3


class Lobby:
    players = []
    stage = Stage.IDLE
    channelId = 0
    teamOneChannel = 0
    teamTwoChannel = 0

class Player:
    def __init__(self, username, id):
        self.username = username
        self.id = id
    
lobby = Lobby()


@client.event
async def on_ready():
    print('we are ready mother fucker {0.user}'.format(client))

@client.event
async def on_message(message):
    print(message)
    print(lobby.stage)
    if lobby.stage == Stage.IDLE and message.content.startswith('!Teamster'):
        await message.channel.send('Players register by typing !register')
        lobby.channelId = message.channel.id
        lobby.stage = Stage.REGISTER_PLAYERS
    if lobby.stage == Stage.REGISTER_PLAYERS and message.content.startswith('!register'):
        player = Player(message.author.name, message.author.id)
        lobby.players.append(player)
        await message.channel.send('{0} has been registered'.format(player.username))
    if lobby.stage == Stage.REGISTER_PLAYERS and message.content.startswith('!list'):
        for p in lobby.players:
            await message.channel.send(p.username)
    if lobby.stage == Stage.REGISTER_PLAYERS and message.content.startswith('!lockin'):
        for p in lobby.players:
            await message.channel.send(p.username)




client.run('')
