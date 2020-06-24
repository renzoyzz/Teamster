from enum import Enum
import discord
import configparser
import random
import math
import time

config = configparser.ConfigParser()
config.read('config.ini')
print('The token is {}'.format(config['DEFAULT']['token']))
token = config['DEFAULT']['token']
tside = config['DEFAULT']['tside']
ctside = config['DEFAULT']['ctside']

client = discord.Client()

class Stage(Enum):
    IDLE = 0
    REGISTER_PLAYERS = 1
    SPLIT = 2


class Lobby:
    def __init__(self):
        self.startingChannel = 0
        self.teamOne = []
        self.teamTwo = []
        self.stage = Stage.IDLE
    players = set()
    teamOneChannel = 0
    teamTwoChannel = 0

lobby = Lobby()

def configure_team_channel(message):
    global lobby
    global tside
    global ctside
    inputs = message.content.split()
    print(inputs)
    if(len(inputs) != 3):
        return("Invalid number of arguments, please supply only 2 channels")
    else:
        lobby1 = inputs[1]
        lobby2 = inputs[2]
        foundLobby1 = False
        foundLobby2 = False
        for c in message.channel.guild.voice_channels:
            if c.name == lobby1:
                foundLobby1 = True
            if c.name == lobby2:
                foundLobby2 = True
        if(foundLobby1 & foundLobby2):
            tside = lobby1
            ctside = lobby2
            return("T-Side is now {}, CT-Side is now {}".format(lobby1,lobby2))
        else:
            if(foundLobby1 & (not foundLobby2)):
                return("{} is not found on server's list of channels".format(lobby2))
            elif(foundLobby2 & (not foundLobby1)):
                return("{} is not found on server's list of channels".format(lobby1))
            else:
                return("Supplied channels do not exist, not updating")

async def move_countdown(message):
    countdown = "3\n2\n1"
    await message.channel.send(countdown, tts=True)
    time.sleep(3.8)

def randomly_assign_teams():
    global lobby
    i = 0
    playerCount = len(lobby.players)
    players = lobby.players.copy()
    while i < playerCount:
        player = random.choice(tuple(players))
        players.remove(player)
        if i % 2 == 0:
            lobby.teamOne.append(player)
        else:
            lobby.teamTwo.append(player)
        i += 1

async def move_teams_to_voice_channels(message):
    global lobby
    for c in message.channel.guild.voice_channels:
        if c.name == tside:
            for p in lobby.teamOne:
                await p.move_to(c)
        elif c.name == ctside:
            for p in lobby.teamTwo:
                await p.move_to(c)
    lobby.stage = Stage.SPLIT

@client.event
async def on_message(message):
    # global keyword allows you to modify the variable outside of the current scope. It is used to create a global variable and make changes to the variable in a local context.
    # https://www.programiz.com/python-programming/global-keyword
    global lobby
    if message.content.startswith('!Teamster'):
        lobby = Lobby()
        for c in message.channel.guild.voice_channels:
            for m in c.members:
                if m.id == message.author.id:
                    lobby.startingChannel = c
        await message.channel.send('Players register by typing !register')
        lobby.stage = Stage.REGISTER_PLAYERS
    elif lobby.stage == Stage.REGISTER_PLAYERS and message.content.startswith('!register'):
        lobby.players.add(message.author)
        await message.channel.send('{0} has been registered'.format(message.author.name))
        await message.author.move_to(lobby.startingChannel)
    elif lobby.stage == Stage.REGISTER_PLAYERS and message.content.startswith('!removeme'):
        lobby.players.remove(message.author)
        await message.channel.send('{0} has been removed'.format(message.author.name))
    elif lobby.stage == Stage.REGISTER_PLAYERS and message.content.startswith('!list'):
        listOfPlayers = 'Current registered players : '
        for p in lobby.players:
            listOfPlayers += '\n' + p.name
        await message.channel.send(listOfPlayers)
    elif message.content.startswith('!configure'):
        await message.channel.send(configure_team_channel(message))
    elif lobby.stage == Stage.REGISTER_PLAYERS and message.content.startswith('!split'):
        randomly_assign_teams()
        await message.channel.send("Moving players to random teams!")
        await move_countdown(message)
        await move_teams_to_voice_channels(message)
        lobby.stage = Stage.SPLIT
    elif lobby.stage == Stage.SPLIT and message.content.startswith('!split'):
        randomly_assign_teams()
        await message.channel.send("Reshuffling teams!")
        await move_countdown(message)
        await move_teams_to_voice_channels(message)

client.run(token)