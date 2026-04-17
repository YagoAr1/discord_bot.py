import discord
from discord import app_commands
from discord.ext import commands
import ollama
import asyncio
import io

class IA(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='ia', description='Faça uma pergunta para a IA')
    @app_commands.describe(pergunta='O que você quer perguntar?')
    async def ia(self, interaction: discord.Interaction, pergunta: str):
        await interaction.response.defer()

        try:
            resposta = await asyncio.wait_for(
                asyncio.to_thread(
                    ollama.chat,
                    model='llama3',
                    messages=[
                        {"role": "system", "content": "Você é um assistente útil e simpático."},
                        {"role": "user", "content": pergunta}
                    ]
                ),
                timeout=60  # Ollama pode ser mais lento dependendo do PC
            )

            texto = resposta['message']['content']

            embed = discord.Embed(
                title="🤖 Resposta da IA",
                color=discord.Color.blurple()
            )
            embed.add_field(name="📩 Pergunta", value=pergunta, inline=False)
            embed.add_field(name="💬 Resposta", value=texto, inline=False)
            embed.set_footer(text=f"Perguntado por {interaction.user.display_name}")

            await interaction.followup.send(embed=embed)

        except asyncio.TimeoutError:
            await interaction.followup.send("⏱️ A IA demorou demais. Tente novamente.")
        except Exception as e:
            await interaction.followup.send(f"❌ Erro: `{e}`")

    @app_commands.command(name='criarcanal', description='cria um canal de texto dentro de uma categoria específica')
    @app_commands.describe(
        nome='Nome do canal',
        categoria='Categoria onde o canal será criado',
        topic='Assunto do canal (opcional)'
    )
    async def criarCanal(self, interaction: discord.Interaction, nome: str, categoria: discord.CategoryChannel = None, topic: str = None):
        await interaction.response.defer(ephemeral=False)

        try:
            canal = await interaction.guild.create_text_channel(
                name=nome, 
                category=categoria, 
                topic=topic or ""
            )
            
            embed = discord.Embed(
                title='✅ Canal criado com sucesso!',
                description=f"O canal <#{canal.id}> foi criado na categoria **{categoria.name if categoria else 'Sem categoria'}**.",
                color=discord.Color.green()
            )
            
            # 4. Envia a mensagem FINAL usando followup
            await interaction.followup.send(embed=embed)

        except discord.Forbidden:
            await interaction.followup.send("❌ Não tenho permissão para criar canais aqui.", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f'❌ Erro ao criar canal: `{e}`', ephemeral=True)


async def setup(bot):
    await bot.add_cog(IA(bot))
