import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta

class Moderacao(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    # COMANDOS DE MODERAÇÂO
    @app_commands.command(name='unban', description='Revoga o banimento de um usuário usando o ID do usuário')
    @app_commands.describe(user_id='ID do usuário para revogar o banimento')
    async def unban(self, interaction: discord.Interaction, *, user_id: int):
        user = await self.bot.fetch_user(user_id)
        await interaction.guild.unban(user)
        await interaction.response.send_message(f'O banimento de {user.mention} foi revogado! Ele pode voltar ao servidor!')

    
    @app_commands.command(name='ban', description='Banir um usuário do servidor')
    @app_commands.describe(membro='Usuário a ser banido', motivo='Motivo do banimento')
    async def ban(self, interaction: discord.Interaction, membro: discord.Member, *, motivo=None):
        await membro.ban(reason=motivo)
        await interaction.response.send_message(f'{membro.mention} foi banido do servidor! Motivo: {motivo}')

    @app_commands.command(name='kick', description='Expulsar um usuário do servidor')
    @app_commands.describe(membro='Usuário a ser expulso', motivo='Motivo da expulsão')
    async def kick(self, interaction: discord.Interaction, membro: discord.Member, *, motivo=None):
        await membro.kick(reason=motivo)
        await interaction.response.send_message(f'{membro.mention} foi expulso do servidor! Motivo: {motivo}')


    # MUTE E UNMUTE 
    @app_commands.command(name='mute', description='Silenciar um usuário do servidor')
    @app_commands.describe(membro='Usuário a ser silenciado', motivo='Motivo do silenciamento')
    async def mute(self, interaction: discord.Interaction, membro: discord.Member, *, motivo=None):
        tempo = timedelta(minutes=10)
        await membro.timeout(tempo, reason=motivo)
        mute_role = discord.utils.get(interaction.guild.roles, name='mute')

        if mute_role:
            await membro.add_roles(mute_role)

        await interaction.response.send_message(f'{membro.mention} foi silenciado por 10 minutos! Motivo: {motivo}')
    @app_commands.command(name='unmute', description='Remover o silenciamento de um usuário do servidor')
    @app_commands.describe(membro='Usuário a ser desmutado')
    async def unmute(self, interaction: discord.Interaction, membro: discord.Member):
        # o comando unmute vai remover o cargo de mute do membro e também vai tirar o timeout do membro.
        # o comando discord.utils.get é um comando para pegar o cargo de mute do servidor, caso ele exista.
        unmute_role = discord.utils.get(interaction.guild.roles, name='mute')
        # se o cargo de mute existir, ele vai remover o cargo do membro.
        if unmute_role:
            await membro.remove_roles(unmute_role)
        # o comando timeout é um comando para tirar o timeout do membro, ou seja, ele vai poder falar novamente no servidor.
        await membro.timeout(None)
        await interaction.response.send_message(f'{membro.mention} foi desmutado! Ele pode falar novamente no servidor!')

    def __init__(self, bot):
        self.bot = bot
        self.lista_warns = {}
    # AVISOS
    @app_commands.command(name='warn', description='Dar um aviso para um usuário do servidor')
    @app_commands.describe(membro='Usuário a ser avisado', motivo='Motivo do aviso')
    async def warn(self, interaction: discord.Interaction, membro: discord.Member, *, motivo=None):

        if membro.id not in self.lista_warns:
            self.lista_warns[membro.id] = []

        self.lista_warns[membro.id].append(motivo)

        await interaction.response.send_message(f'{membro.mention} recebeu um aviso! Motivo: {motivo}')
        if membro.id in self.lista_warns and len(self.lista_warns[membro.id]) >= 3:
            await membro.ban(reason=None)
            await interaction.response.send_message(f'{membro.mention} foi banido do servidor por acumular 3 avisos!')

    @app_commands.command(name='warns', description='Ver os avisos de um usuário do servidor')
    @app_commands.describe(membro='Usuário a ser verificado')
    async def warns(self, interaction: discord.Interaction, membro: discord.Member):
        
        if membro.id not in self.lista_warns:
            await interaction.response.send_message(f'{membro.mention} não tem nenhum aviso!')
            return

        warns = self.lista_warns[membro.id]

        lista = "\n".join([f"{i+1}. {w}" for i, w in enumerate(warns)])

        await interaction.response.send_message(
        f'{membro.mention} tem {len(warns)} aviso(s):\n{lista}'
        )
    
    @app_commands.command(name='unwarn', description='Remover um aviso de um usuário do servidor')
    @app_commands.describe(membro='Usuário a ser desavisado')
    async def unwarn(self, interaction: discord.Interaction, membro: discord.Member):
        if membro.id not in self.lista_warns:
            await interaction.response.send_message(f'{membro.mention} não tem nenhum aviso para remover!')
        else:
            self.lista_warns.pop(membro.id)
            await interaction.response.send_message(f'O aviso de {membro.mention} foi removido!')


async def setup(bot):
    await bot.add_cog(Moderacao(bot))