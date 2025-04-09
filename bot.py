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
ROLE_AUTORISÉ = 1359104466682646642

# ID du rôle à retirer à l'utilisateur
ROLE_A_RETIRER = 1359104466682646642

# ID du rôle à ajouter au membre mentionné
ROLE_A_AJOUTER = 1359104403587600464  # Remplace par le vrai ID

# ID du salon où envoyer un message supplémentaire
SALON_LOG_ID = 1359274996211646514  # Remplace par l’ID du salon de logs/RP

# ID du rôle à pinger dans le salon de logs
ROLE_LOG_PING = 1087764830531883019  # Remplace par l'ID du rôle à mentionner

@bot.command()
@commands.has_role(ROLE_AUTORISÉ)
async def atomic(ctx, membre: discord.Member):
    await ctx.message.delete()  # Supprimer la commande

    # Création de l'embed
    embed = discord.Embed(
        title="Un mage vient d'utiliser une magie de niveau CHAOS !",
        description=f"**{ctx.author.mention}** a utilisé la magie interdite **Atomic** sur {membre.mention} !",
        color=discord.Color.purple()
    )
    embed.set_thumbnail(url="https://cdn.discordapp.com/icons/946034497219100723/65e3c9c08a1386ef3c4709a72bc56c5b.webp?size=1024&format=webp")
    embed.set_image(url="https://staticg.sportskeeda.com/editor/2023/02/6b9be-16772457791665-1920.jpg")
    embed.set_footer(
        text="Shadow Garden",
        icon_url="https://cdn.discordapp.com/icons/946034497219100723/65e3c9c08a1386ef3c4709a72bc56c5b.webp?size=1024&format=webp"
    )

      # Envoie de l'embed dans le salon actuel
    await ctx.send(embed=embed)

    # Envoi d’un message dans un autre salon
    salon_logs = ctx.guild.get_channel(SALON_LOG_ID)
    role_ping = ctx.guild.get_role(ROLE_LOG_PING)

    if salon_logs and role_ping:
        await salon_logs.send(
            f"""{role_ping.mention} 📜 **{ctx.author.display_name}** a invoqué la magie **Atomic de Niveau Chaos** sur {membre.mention}.""")

    # Retirer le rôle de l’auteur
    role_to_remove = ctx.guild.get_role(ROLE_A_RETIRER)
    if role_to_remove and role_to_remove in ctx.author.roles:
        await ctx.author.remove_roles(role_to_remove)

    # Ajouter un rôle au membre ciblé
    role_to_add = ctx.guild.get_role(ROLE_A_AJOUTER)
    if role_to_add:
        await membre.add_roles(role_to_add)
    else:
        await ctx.send("⚠️ Le rôle à ajouter est introuvable.")

ROLE_AUTORISÉ_INVERSION = 1359441308237828189  # Rôle autorisé à lancer la commande
ROLE_A_RETIRER_INVERSION = 1359441308237828189  # Rôle à retirer à l’auteur
ROLE_A_AJOUTER_INVERSION = 1359469141320536074  # Rôle à donner à la cible
ROLE_LOG_PING_INVERSION = 1087764830531883019  # Rôle à mentionner dans le salon de logs
SALON_LOG_ID_INVERSION = 1359274996211646514  # ID du salon de logs

@bot.command()
@commands.has_role(ROLE_AUTORISÉ_INVERSION)
async def inversion(ctx, membre: discord.Member):
    await ctx.message.delete()

    embed = discord.Embed(
        title="Une magie niveau inversion viens d'etre utilisé !",
        description=f"**{ctx.author.mention}** a déclenché la magie **Atomic niveau Inversion** sur {membre.mention}.\nLe flux du mana vient de s'inverser...",
        color=discord.Color.dark_red()
    )

    embed.set_thumbnail(url="https://cdn.discordapp.com/icons/946034497219100723/65e3c9c08a1386ef3c4709a72bc56c5b.webp?size=1024&format=webp")  # Image stylisée haut droite
    embed.set_image(url="https://i.ytimg.com/vi/WY5glA1U-pk/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLAl2g29pAjNHDwRLpalMu4y_WFJHw")  # Image du sort "Inversion"
    embed.set_footer(
        text="Shadow Garden",
        icon_url="https://cdn.discordapp.com/icons/946034497219100723/65e3c9c08a1386ef3c4709a72bc56c5b.webp?size=1024&format=webp"
    )

    await ctx.send(embed=embed)

    # 🔁 Log RP dans un autre salon
    salon_logs = ctx.guild.get_channel(SALON_LOG_ID_INVERSION)
    role_ping = ctx.guild.get_role(ROLE_LOG_PING_INVERSION)

    if salon_logs and role_ping:
        await salon_logs.send(
            f"""{role_ping.mention} ⚠️ **{ctx.author.display_name}** a utilisé **La magie Atomic Niveau Inversion** sur {membre.mention}.
Veuillez éffectuer l'inversion"""
        )

    # ❌ Retirer un rôle à l'auteur
    role_to_remove = ctx.guild.get_role(ROLE_A_RETIRER_INVERSION)
    if role_to_remove and role_to_remove in ctx.author.roles:
        await ctx.author.remove_roles(role_to_remove)

    # ✅ Ajouter un rôle au membre ciblé
    role_to_add = ctx.guild.get_role(ROLE_A_AJOUTER_INVERSION)
    if role_to_add:
        await membre.add_roles(role_to_add)

ROLE_FUTUR_TEMPORAIRE = 1359547493687234641  # Rôle temporaire à donner
SALON_LOGS_FUTUR = 1359274996211646514      # Salon de logs

@bot.command(name="futur")
async def futur(ctx):
    await ctx.message.delete()

    # Création de l'embed
    embed = discord.Embed(
        title="🌌 Vision du Futur",
        description=f"**{ctx.author.mention}** a entrevu le futur pendant un court instant...",
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url="https://cdn.discordapp.com/icons/946034497219100723/65e3c9c08a1386ef3c4709a72bc56c5b.webp?size=1024&format=webp")  # Icône stylisée
    embed.set_image(url="https://png.pngtree.com/thumb_back/fw800/back_our/20190625/ourmid/pngtree-financial-future-city-banner-background-image_260946.jpg")  # Visuel immersif
    embed.set_footer(text="Durée de la vision : 10 secondes")

    await ctx.send(embed=embed)

    # Rôle temporaire
    role_temp = ctx.guild.get_role(ROLE_FUTUR_TEMPORAIRE)
    if role_temp:
        await ctx.author.add_roles(role_temp)
        await asyncio.sleep(10)
        await ctx.author.remove_roles(role_temp)

    # Log dans le salon
    salon_logs = ctx.guild.get_channel(SALON_LOGS_FUTUR)
    if salon_logs:
        await salon_logs.send(
            f"🌀 **{ctx.author.display_name}** a activé `la magie temporelle` et a vu le futur restock."
        )
    else:
        print("⚠️ Salon de logs introuvable.")

# Token pour démarrer le bot (à partir des secrets)
# Lancer le bot avec ton token depuis l'environnement  
keep_alive()
bot.run(token)
