import discord
from discord import app_commands
from discord.ext import commands
import ollama
import asyncio

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

async def setup(bot):
    await bot.add_cog(IA(bot))