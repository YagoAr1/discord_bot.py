import discord
from discord.ext import commands
import asyncio
import os
 
# ── Configurações ──────────────────────────────────────────────
TOKEN = "SEU_TOKEN_AQUI"  # Substitua pelo token do seu bot
PREFIX = "/"
# ──────────────────────────────────────────────────────────────
 
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents)
 
 
@bot.event
async def on_ready():
    
    print(f"✅ Bot online como {bot.user} (ID: {bot.user.id})")
    print(f"📡 Conectado em {len(bot.guilds)} servidor(es)")
    print("_" * 10)
 
@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Sincronizados {len(synced)} comandos")
    except Exception as e:
        print(e)
 
async def carregar_cogs():
    """Carrega automaticamente todos os arquivos dentro da pasta cogs/"""
    pasta_cogs = "./cogs"
    
    # Verifica se a pasta cogs/ existe, se não existir, cria a pasta
    if not os.path.exists(pasta_cogs):
        os.makedirs(pasta_cogs)
        print("📁 Pasta 'cogs/' criada automaticamente.")
    
    # Percorre todos os arquivos da pasta cogs/ e tenta carregar cada um como uma extensão do bot
    for arquivo in os.listdir(pasta_cogs):
        # Verifica se o arquivo eh um arquivo .py e nao eh um arquivo oculto
        if arquivo.endswith(".py") and not arquivo.startswith("_"):
            nome_cog = f"cogs.{arquivo[:-3]}"
            # Tenta carregar o arquivo como uma extensão do bot e imprime o resultado no console
            try:
                await bot.load_extension(nome_cog)
                print(f"✅ Cog carregado: {nome_cog}")
            # Se ocorrer um erro ao carregar o cog, imprime o erro no console
            except Exception as e:
                print(f"❌ Erro ao carregar {nome_cog}: {e}")
 
 
async def main():
    async with bot:
        await carregar_cogs()
        await bot.start(TOKEN)
 
 
asyncio.run(main())