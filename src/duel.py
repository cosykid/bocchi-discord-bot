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

DUEL_MESSAGES = [
    '{winner.mention} hit {loser.mention} with a a 6-string bass',
    '{loser.mention} was sent the squid games by {winner.mention}',
    '{loser.mention} was sent to the summoner\'s rift by {winner.mention}',
    '{winner.mention} threw {loser.mention} into orbit',
    '{loser.mention} was suplexed by {winner.mention}',
    '{loser.mention} got mogged by {winner.mention}',
    '{winner.mention} was too alpha for {loser.mention}',
    '{winner.mention} installed league of legends on {loser.mention}\'s computer',
    '{winner.mention} emoted on {loser.mention}'
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
        loser = None
        winner = None

        if (random.choice([interaction.user, member]) == member):
            winner = member
            loser = await interaction.guild.fetch_member(interaction.user.id)
        else:
            winner = interaction.user
            loser = member

        try:
            # Attempt to timeout the member
            await loser.timeout(timedelta(minutes=2), reason="You lost a duel!")
            message = random.choice(DUEL_MESSAGES).format(winner=winner, loser=loser)
            await interaction.response.send_message(message)
            await interaction.followup.send(random.choice(GUN_GIFS))
        except discord.Forbidden:
            await interaction.response.send_message(f"{loser.mention} lost the duel, but can't be timed out... sorry")
