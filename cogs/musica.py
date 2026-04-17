import discord
from discord.ext import commands
from discord import app_commands
import yt_dlp
import asyncio
 
YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,          # remove logs desnecessários no terminal
    'no_warnings': True,
}
 
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}
 
 
class Musica(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
 
    # ── Helpers ────────────────────────────────────────────────
 
    async def _conectar(self, interaction: discord.Interaction) -> bool:
        """Conecta ao canal de voz do usuário. Retorna False se não for possível."""
        if interaction.guild.voice_client:
            return True
        if not interaction.user.voice:
            await interaction.followup.send(
                '❌ Você precisa estar em um canal de voz para usar este comando.',
                ephemeral=True
            )
            return False
        await interaction.user.voice.channel.connect()
        return True
 
    def _buscar_audio(self, busca: str) -> dict:
        """Extrai informações do áudio via yt_dlp (roda em thread separada)."""
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            eh_url = 'youtube.com' in busca or 'youtu.be' in busca
            info = ydl.extract_info(busca if eh_url else f"ytsearch:{busca}", download=False)
            if 'entries' in info:
                info = info['entries'][0]
            return info
 
    def _tocar_proximo(self, interaction: discord.Interaction):
        """Toca a próxima música da fila automaticamente."""
        if self.queue and interaction.guild.voice_client:
            url, titulo = self.queue.pop(0)
            source = discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS)
            interaction.guild.voice_client.play(
                source,
                after=lambda e: self._tocar_proximo(interaction)
            )
 
    # ── Comandos ───────────────────────────────────────────────
 
    @app_commands.command(name='join', description='Entra no canal de voz')
    async def join(self, interaction: discord.Interaction):
        if not interaction.user.voice:
            return await interaction.response.send_message(
                '❌ Você precisa estar em um canal de voz para usar este comando.',
                ephemeral=True
            )
 
        canal = interaction.user.voice.channel
 
        # Se já estiver em outro canal, move para o do usuário
        if interaction.guild.voice_client:
            await interaction.guild.voice_client.move_to(canal)
            return await interaction.response.send_message(f'🔀 Movi para o canal **{canal.name}**!')
 
        await canal.connect()
        await interaction.response.send_message(f'✅ Entrei no canal **{canal.name}**!')
 
    @app_commands.command(name='play', description='Toca uma música a partir de um link ou nome')
    @app_commands.describe(busca='Link do YouTube ou nome da música para tocar')
    async def play(self, interaction: discord.Interaction, busca: str):
        await interaction.response.defer()
 
        if not await self._conectar(interaction):
            return
 
        try:
            info = await asyncio.to_thread(self._buscar_audio, busca)
        except Exception:
            return await interaction.followup.send('❌ Não consegui encontrar ou reproduzir essa música.', ephemeral=True)
 
        url = info['url']
        titulo = info['title']
        duracao = info.get('duration', 0)
        minutos, segundos = divmod(duracao, 60)
 
        vc = interaction.guild.voice_client
 
        # Se já estiver tocando, adiciona na fila
        if vc.is_playing() or vc.is_paused():
            self.queue.append((url, titulo))
            return await interaction.followup.send(f'📋 Adicionado à fila: **{titulo}**')
 
        source = discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS)
        vc.play(source, after=lambda e: self._tocar_proximo(interaction))
 
        await interaction.followup.send(
            f'🎵 Tocando agora: **{titulo}** `({minutos:02d}:{segundos:02d})`'
        )
 
    @app_commands.command(name='pause', description='Pausa a música atual')
    async def pause(self, interaction: discord.Interaction):
        vc = interaction.guild.voice_client
        if vc and vc.is_playing():
            vc.pause()
            await interaction.response.send_message('⏸️ Música pausada!')
        else:
            await interaction.response.send_message('❌ Não há nenhuma música tocando.', ephemeral=True)
 
    @app_commands.command(name='resume', description='Retoma a música pausada')
    async def resume(self, interaction: discord.Interaction):
        vc = interaction.guild.voice_client
        if vc and vc.is_paused():
            vc.resume()
            await interaction.response.send_message('▶️ Música retomada!')
        else:
            await interaction.response.send_message('❌ Não há nenhuma música pausada.', ephemeral=True)
 
    @app_commands.command(name='skip', description='Pula para a próxima música da fila')
    async def skip(self, interaction: discord.Interaction):
        vc = interaction.guild.voice_client
        if vc and (vc.is_playing() or vc.is_paused()):
            vc.stop()  # o callback after= cuida de tocar a próxima
            await interaction.response.send_message('⏭️ Música pulada!')
        else:
            await interaction.response.send_message('❌ Não há nenhuma música tocando.', ephemeral=True)
 
    @app_commands.command(name='stop', description='Para a música e limpa a fila')
    async def stop(self, interaction: discord.Interaction):
        vc = interaction.guild.voice_client
        if vc and (vc.is_playing() or vc.is_paused()):
            self.queue.clear()
            vc.stop()
            await interaction.response.send_message('⏹️ Música parada e fila limpa!')
        else:
            await interaction.response.send_message('❌ Não estou tocando nada no momento.', ephemeral=True)
 
    @app_commands.command(name='leave', description='Sai do canal de voz')
    async def leave(self, interaction: discord.Interaction):
        vc = interaction.guild.voice_client
        if vc:
            self.queue.clear()
            await vc.disconnect()
            await interaction.response.send_message('👋 Saí do canal de voz!')
        else:
            await interaction.response.send_message('❌ Não estou em nenhum canal de voz.', ephemeral=True)
 
 
async def setup(bot):
    await bot.add_cog(Musica(bot))
 