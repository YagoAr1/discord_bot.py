import discord
from discord.ext import commands


"""
    O intentes = discord.Intents.all() é uma configuração que permite 
    ao bot acessar todas as permissões disponíveis no Discord. 
    Isso é necessário para que o bot possa funcionar corretamente e interagir 
    com os usuários de maneira eficaz. 
    Sem essa configuração, o bot pode não ser capaz de responder a comandos ou realizar certas ações, 
    dependendo das permissões que ele tem. 

"""

bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())

@bot.command()
#depois do def você pode nomear o nome do seu comando
async def ola(ctx:commands.Context):
    #O reply é um comando para o bot responder a mensagem do usuário
    nome_mencionado = ctx.author.mention
    await ctx.reply(f'Olá, {nome_mencionado}! Tudo bem?')

@bot.command()
async def ping(ctx):
    await ctx.reply(f'O ping do bot é {round(bot.latency * 1000)}ms')

@bot.command()
async def tarefa(ctx):
    #O comando send é um comando para o bot apenas enviar a mensagem sem mencionar o usuário
    await ctx.send('Olá tudo bem? O que teremos hoje?')

@bot.command()
async def somar(ctx:commands.Context, num1: int, num2: int):
    resultado = num1 + num2
    await ctx.reply(f'a soma entre {num1} e {num2} é {resultado}')

@bot.command()
async def limpar(ctx:commands.Context, quantidade: int):
    await ctx.channel.purge(limit=quantidade)
    await ctx.channel.purge(limit=1) #Limpa a mensagem do comando
    await ctx.send(f'{quantidade} de mensagens foram apagadas com sucesso!')



@bot.event
async def on_ready():
    print(f'bot {bot.user} está online!')


bot.run('MTQ4NTQ2Nzc4NjA4NzEwNDU5Mw.G9nEHR.u0CvykA0L0_wT6czf34c8afoUPxQToGt0I2fGs')