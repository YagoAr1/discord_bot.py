import discord
from discord import app_commands
from discord.ext import commands

class Comandos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # /ping
    @app_commands.command(name="ping", description="Mostra o ping do bot")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f'O ping do bot é {round(self.bot.latency * 1000)}ms'
        )

    # /clear
    @app_commands.command(name="clear", description="Apaga mensagens do canal atual")
    @app_commands.describe(quantidade="Quantidade de mensagens para apagar")
    async def clear(self, interaction: discord.Interaction, quantidade: int):

        # precisa defer para evitar timeout
        await interaction.response.defer(ephemeral=True)

        await interaction.channel.purge(limit=quantidade)

        await interaction.followup.send(
            f'{quantidade} mensagens foram apagadas com sucesso!',
            ephemeral=True
        )
    
    @app_commands.command(name='clearc', description='Apaga mensagens de um canal específico')
    @app_commands.describe(canal='Canal onde as mensagens serão apagadas', quantidade='quantidade de mensagens para apagar')
    async def clearc(self, interaction: discord.Interaction, canal: discord.TextChannel, quantidade: int):
        await canal.purge(limit=quantidade)
        msg = await interaction.response.send_message(f'{quantidade} de mensagens foram apagadas com sucesso no canal {canal.mention}! {interaction.user.mention}', ephemeral=True)
        await msg.delete(delay=5) #deleta a mensagem de confirmação após 5 segundos



    

async def setup(bot):
    await bot.add_cog(Comandos(bot))
