import discord
import random
from datetime import timedelta
from discord import Member

GUN_GIFS = [
    'https://tenor.com/view/bochhi-bocchi-the-rock-gun-gif-27545220',
    'https://tenor.com/view/bocchi-bocchi-the-rock-bocchi-the-hk416-bocchi-the-glock-hk416-gif-10280229870835712451',
    'https://tenor.com/view/bocchi-glock-gun-gif-15465161889683183569',
    'https://i.redd.it/1hgte4ivt1kb1.gif',
    'https://tenor.com/view/bocchi-the-rock-hitori-gotoh-bocchi-yamcha-birds-gif-27233195'
]

def register_duel_command(tree, client):
    @tree.command(
        name="duel",
        description="One of you gets timed out",
        guild=discord.Object(id=1080458538087890965)
    )
    async def duel(interaction, member: Member):
        
        # Prohibit user from duelling themselves
        if member == interaction.user:
            await interaction.response.send_message("S-sorry.. you can't duel yourself")
            return
        
        # Prohibit user from duelling bot
        if member == client.user:
            await interaction.response.send_message("I d-don't want to duel you...")
            return
        
        # Randomly determine the outcome of the duel
        loser = random.choice([interaction.user, member])
        winner = interaction.user if loser == member else member

        try:
            # Attempt to timeout the member
            await member.timeout(timedelta(minutes=1), reason="You lost a duel!")
            await interaction.response.send_message(f'{winner.mention} beat {loser.mention} in the duel!... I\'m gonna head home')
            await interaction.followup.send(random.choice(GUN_GIFS))
        except discord.Forbidden:
            await interaction.response.send_message(f"{member.mention} lost the duel, but can't be timed out... sorry")
