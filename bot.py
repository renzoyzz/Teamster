import discord

client = discord.Client()


@client.event
async def on_ready():
    print('we are ready mother fucker {0.user}'.format(client))

@client.event
async def on_message(message):
    print(message)
    if message.content.startswith('!'):
        await message.channel.send('Hello')


client.run('NzI0Nzc0NDExNTg4MjA2NjQz.XvFL1Q.WjdVAqdUg4BZDc_HLgil3o1Hrgs')
