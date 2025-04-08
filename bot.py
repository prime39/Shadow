import discord
from discord.ext import commands, tasks
from discord import app_commands
import os
import random
import asyncio
import time
import datetime
import re
import subprocess
import sys
import traceback
from keep_alive import keep_alive
from discord.ui import Button, View
from discord.ui import View, Select
from discord.ext import tasks
from collections import defaultdict
from collections import deque
import psutil
import platform

token = os.environ['SHADOW']
intents = discord.Intents.all()
start_time = time.time()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="!!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    global start_time
    start_time = time.time()  # Défini l'heure de démarrage lorsque le bot est prêt
    print(f'{bot.user} est prêt et l\'uptime est maintenant calculable.')
    print(f"✅ Le bot {bot.user} est maintenant connecté ! (ID: {bot.user.id})")

    # Initialisation de l'uptime du bot
    bot.uptime = time.time()
    
    # Récupération du nombre de serveurs et d'utilisateurs
    guild_count = len(bot.guilds)
    member_count = sum(guild.member_count for guild in bot.guilds)
    
    # Affichage des statistiques du bot dans la console
    print(f"\n📊 **Statistiques du bot :**")
    print(f"➡️ **Serveurs** : {guild_count}")
    print(f"➡️ **Utilisateurs** : {member_count}")
    
    # Liste des activités dynamiques
    activity_types = [
        discord.Activity(type=discord.ActivityType.watching, name="La lune de sang 🌕!"),
        discord.Activity(type=discord.ActivityType.streaming, name="L'Autre Monde 🪐"),
        discord.Activity(type=discord.ActivityType.streaming, name="Shadow Garden"),
    ]
    
    # Sélection d'une activité au hasard
    activity = random.choice(activity_types)
    
    # Choix d'un statut aléatoire
    status_types = [discord.Status.online, discord.Status.idle, discord.Status.dnd]
    status = random.choice(status_types)
    
    # Mise à jour du statut et de l'activité
    await bot.change_presence(activity=activity, status=status)
    
    print(f"\n🎉 **{bot.user}** est maintenant connecté et affiche ses statistiques dynamiques avec succès !")

    # Afficher les commandes chargées
    print("📌 Commandes disponibles 😊")
    for command in bot.commands:
        print(f"- {command.name}")

    try:

    # Synchroniser les commandes avec Discord
        synced = await bot.tree.sync()  # Synchronisation des commandes slash
        print(f"✅ Commandes slash synchronisées : {[cmd.name for cmd in synced]}")
    except Exception as e:
        print(f"❌ Erreur de synchronisation des commandes slash : {e}")

    # Jongler entre différentes activités et statuts
    while True:
        for activity in activity_types:
            for status in status_types:
                await bot.change_presence(status=status, activity=activity)
                await asyncio.sleep(10)  # Attente de 10 secondes avant de changer l'activité et le statut
    for guild in bot.guilds:
        GUILD_SETTINGS[guild.id] = load_guild_settings(guild.id)


# Gestion des erreurs globales pour toutes les commandes
@bot.event
async def on_error(event, *args, **kwargs):
    print(f"Une erreur s'est produite : {event}")
    embed = discord.Embed(
        title="❗ Erreur inattendue",
        description="Une erreur s'est produite lors de l'exécution de la commande. Veuillez réessayer plus tard.",
        color=discord.Color.red()
    )
    await args[0].response.send_message(embed=embed)

# ID du rôle autorisé à utiliser la commande
ROLE_AUTORISÉ = 1359104466682646642  # Remplace par l'ID du rôle autorisé (ex: Staff)
# ID du rôle à retirer à l'utilisateur
ROLE_A_RETIRER = 1359104466682646642  # Remplace par l'ID du rôle à retirer

@bot.command()
@commands.has_role(ROLE_AUTORISÉ)
async def atomic(ctx):
    embed = discord.Embed(
        title="Un mage viens d'utiliser une magie de niveau CHAOS !",
        description="Il a utilisé la magie **Atomic** !",
        color=discord.Color.purple()
    )

    # Image en haut à droite
    embed.set_thumbnail(url="https://cdn.discordapp.com/icons/946034497219100723/65e3c9c08a1386ef3c4709a72bc56c5b.webp?size=1024&format=webp")  # Logo ou avatar stylé

    # Image principale
    embed.set_image(url="https://staticg.sportskeeda.com/editor/2023/02/6b9be-16772457791665-1920.jpg")  # Image du sort "Atomic"

    # Footer en bas
    embed.set_footer(
        text="Shadow Garden",
        icon_url="https://cdn.discordapp.com/icons/946034497219100723/65e3c9c08a1386ef3c4709a72bc56c5b.webp?size=1024&format=webp"
    )

    await ctx.send(embed=embed)

    # 2. Lock le salon (empêche @everyone d'écrire)
    overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

    # 3. Retirer un rôle à l'utilisateur
    role_to_remove = ctx.guild.get_role(ROLE_A_RETIRER)
    if role_to_remove in ctx.author.roles:
        await ctx.author.remove_roles(role_to_remove)

# Token pour démarrer le bot (à partir des secrets)
# Lancer le bot avec ton token depuis l'environnement  
keep_alive()
bot.run(token)
