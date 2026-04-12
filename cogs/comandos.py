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

    @app_commands.command(name='avatar', description='Mostrar o avatar do usuário desejado')
    @app_commands.describe(usuário='Usuário que deseja ver o avatar')
    async def avatar(self, interaction: discord.Interaction, usuário: discord.Member):
        await interaction.response.send_message(f'{usuário.avatar.url}')

    @app_commands.command(name='info', description='Mostrar informações do servidor')
    async def info(self, interaction: discord.Interaction):
        embed  = discord.Embed(
            title='Informações do servidor',
            description=f'Nome: {interaction.guild.name}\nOwner: {interaction.guild.owner}\nCriado em: {interaction.guild.created}',
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='comandos', description='Mostrar os comandos do servidor')
    async def comandos(self, interaction: discord.Interaction): 
        embed = discord.Embed(
            title='Comandos Disponíveis',
            description=f'Aqui estão os comandos disponíveis no servidor: {interaction.guild.name}',
            color=discord.Color.blue()
        )
        embed.add_field(name='Comandos Gerais', value='- /ping\n- /clear\n- /clearc\n- /avatar\n- /info\n- /comandos', inline=False)
        embed.add_field(name='Comandos de Música', value='- /join\n- /play\n- /pause\n- /resume\n- /skip\n- /stop', inline=False)
        embed.add_field(name='Comandos de Ia', value='- /ia')
        embed.add_field(name='Comandos de Moderação', value='- /unban\n- /ban\n- /kick\n- /mute\n- /unmute\n- /warn\n- /warns\n- /unwarn\n- /dm')
        await interaction.response.send_message(embed=embed)
        

async def setup(bot):
    await bot.add_cog(Comandos(bot))
