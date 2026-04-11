import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta
from typing import Optional

class Moderacao(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.lista_warns = {}

   
    @app_commands.command(name='unban', description='Revoga o banimento de um usuário usando o ID do usuário')
    @app_commands.describe(user_id='ID do usuário para revogar o banimento', motivo='Motivo para revogar o banimento (opcional)')
    @app_commands.checks.has_permissions(administrator=True)

    async def unban(self, interaction: discord.Interaction, *, user_id: str, motivo: Optional[str] = None):
        user = await self.bot.fetch_user(int (user_id))
        await interaction.guild.unban(user)
        await interaction.response.send_message(f'O banimento de {user.mention} foi revogado! Motivo: {motivo}', ephemeral=True)

        try:
            await user.send(f"Seu banimento do servidor **{interaction.guild.name}** foi revogado! Motivo: {motivo}")
        except discord.Forbidden:
            print("Não consegui enviar DM para o usuário.")
        
    
    @app_commands.command(name='ban', description='Banir um usuário do servidor')
    @app_commands.describe(membro='Usuário a ser banido', motivo='Motivo do banimento')
    @app_commands.checks.has_permissions(administrator=True)
    async def ban(self, interaction: discord.Interaction, membro: discord.Member, *, motivo: Optional[str] = None):
        await membro.ban(reason=motivo)
        await interaction.response.send_message(f'{membro.mention} foi banido do servidor! Motivo: {motivo}', ephemeral=True)
        try:
            await membro.send(f"Você foi banido do servidor **{interaction.guild.name}**. Motivo: {motivo}")
        except discord.Forbidden:
            print("Não consegui enviar DM para o usuário.")
        
  
    @app_commands.command(name='kick', description='Expulsar um usuário do servidor')
    @app_commands.describe(membro='Usuário a ser expulso', motivo='Motivo da expulsão')
    @app_commands.checks.has_permissions(administrator=True)

    async def kick(self, interaction: discord.Interaction, membro: discord.Member, *, motivo: Optional[str] = None):
        await membro.kick(reason=motivo)
        await interaction.response.send_message(f'{membro.mention} foi expulso do servidor! Motivo: {motivo}')

  
    @app_commands.command(name='mute', description='Silenciar um usuário do servidor')
    @app_commands.describe(membro='Usuário a ser silenciado', minuto='Tempo em minutos para o silenciamento', motivo='Motivo do silenciamento')
    @app_commands.checks.has_permissions(administrator=True)
    async def mute(self, interaction: discord.Interaction, membro: discord.Member, minuto: int, *, motivo: Optional[str] = None):
        tempo = timedelta(minutes=minuto)
        await membro.timeout(tempo, reason=motivo)
        mute_role = discord.utils.get(interaction.guild.roles, name='mute')

        if mute_role:
            await membro.add_roles(mute_role)

        await interaction.response.send_message(f'{membro.mention} foi silenciado por 10 minutos! Motivo: {motivo}')


    @app_commands.command(name='unmute', description='Remover o silenciamento de um usuário do servidor')
    @app_commands.describe(membro='Usuário a ser desmutado')
    @app_commands.checks.has_permissions(administrator=True)
    async def unmute(self, interaction: discord.Interaction, membro: discord.Member):
        unmute_role = discord.utils.get(interaction.guild.roles, name='mute')
        if unmute_role:
            await membro.remove_roles(unmute_role)
        await membro.timeout(None)
        await interaction.response.send_message(f'{membro.mention} foi desmutado! Ele pode falar novamente no servidor!')

    
    @app_commands.command(name='warn', description='Dar um aviso para um usuário do servidor')
    @app_commands.describe(membro='Usuário a ser avisado', motivo='Motivo do aviso')
    @app_commands.checks.has_permissions(administrator=True)
    async def warn(self, interaction: discord.Interaction, membro: discord.Member, *, motivo: Optional[str] = None):
        if membro.id not in self.lista_warns:
            self.lista_warns[membro.id] = []

        self.lista_warns[membro.id].append(motivo)
        await interaction.response.send_message(f'{membro.mention} recebeu um aviso! Motivo: {motivo}')

        if len(self.lista_warns[membro.id]) >= 3:
            await membro.ban(reason=None)
            await interaction.response.send_message(f'{membro.mention} foi banido do servidor por acumular 3 avisos!')

    
    @app_commands.command(name='warns', description='Ver os avisos de um usuário do servidor')
    @app_commands.describe(membro='Usuário a ser verificado')
    @app_commands.checks.has_permissions(administrator=True)
    async def warns(self, interaction: discord.Interaction, membro: discord.Member):
        if membro.id not in self.lista_warns:
            await interaction.response.send_message(f'{membro.mention} não tem nenhum aviso!')
            return

        warns = self.lista_warns[membro.id]
        lista = "\n".join([f"{i+1}. {w}" for i, w in enumerate(warns)])
        await interaction.response.send_message(f'{membro.mention} tem {len(warns)} aviso(s):\n{lista}')
  
    @app_commands.command(name='unwarn', description='Remover um aviso de um usuário do servidor')
    @app_commands.describe(membro='Usuário a ser desavisado')
    @app_commands.checks.has_permissions(administrator=True)
    async def unwarn(self, interaction: discord.Interaction, membro: discord.Member):
        if membro.id not in self.lista_warns:
            await interaction.response.send_message(f'{membro.mention} não tem nenhum aviso para remover!')
        else:
            self.lista_warns.pop(membro.id)
            await interaction.response.send_message(f'O aviso de {membro.mention} foi removido!')
    
    @app_commands.command(name='dm', description='Enviar uma mensagem direta para um usuário do servidor')
    @app_commands.describe(membro='Usuário a receber a mensagem', mensagem='Conteúdo da mensagem')
    @app_commands.checks.has_permissions(administrator=True)
    async def dm(self, interaction: discord.Interaction, membro: discord.Member, mensagem: str):
        try:
            await membro.send(mensagem)
            await interaction.response.send_message(f'Mensagem enviada para {membro.mention}!', ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message(
                f'Não foi possível enviar a mensagem para {membro.mention}. '
                'Ele pode ter DMs desativadas ou bloqueado o bot.',
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(Moderacao(bot))