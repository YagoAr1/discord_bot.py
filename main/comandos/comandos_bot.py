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