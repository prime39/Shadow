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
from discord.ui import Modal, TextInput
from discord.ext import tasks
from collections import defaultdict
from collections import deque
import psutil
import platform

token = os.environ['SHADOW']
intents = discord.Intents.all()
start_time = time.time()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="-", intents=intents, help_command=None)

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

from discord.ui import View, Button

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # 🔹 Si le bot est mentionné
    if bot.user.mentioned_in(message) and message.content.strip().startswith(f"<@{bot.user.id}>"):
        embed = discord.Embed(
            title="👋 Besoin d’aide ?",
            description=(
                f"Salut {message.author.mention} ! Moi, c’est **{bot.user.name}**, je suis l'assistant de <@945762223366746142>. 🤖\n\n"
                "Clique sur le bouton ci-dessous pour voir mes commandes disponibles !"
            ),
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=bot.user.avatar.url)
        embed.set_footer(text="Réponse automatique • Disponible 24/7", icon_url=bot.user.avatar.url)

        view = View()
        button = Button(label="📜 Voir les commandes", style=discord.ButtonStyle.primary, custom_id="help_button")

        async def button_callback(interaction: discord.Interaction):
            ctx = await bot.get_context(interaction.message)
            await ctx.invoke(bot.get_command("help"))
            await interaction.response.send_message("Voici la liste des commandes !", ephemeral=True)

        button.callback = button_callback
        view.add_item(button)

        await message.channel.send(embed=embed, view=view)
        return

    # Important : continue de traiter les autres commandes !
    await bot.process_commands(message)

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
SALON_LOGS_FUTUR = 1359274996211646514       # Salon de logs
ROLE_AUTORISÉ_FUTUR = 1359554146725789856    # Rôle autorisé à utiliser la commande

class LienFutur(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(
            label="Accéder au salon",
            url="https://discord.com/channels/946034497219100723/1359547424166908116"  # Remplace ce lien par ton lien réel
        ))

@bot.command(name="futur")
@commands.has_role(ROLE_AUTORISÉ_FUTUR)
async def futur(ctx):
    await ctx.message.delete()

    embed = discord.Embed(
        title="🌌 Vision du Futur",
        description=f"**{ctx.author.mention}** a entrevu le futur pendant un court instant...",
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url="https://cdn.discordapp.com/icons/946034497219100723/65e3c9c08a1386ef3c4709a72bc56c5b.webp?size=1024&format=webp")
    embed.set_image(url="https://png.pngtree.com/thumb_back/fw800/back_our/20190625/ourmid/pngtree-financial-future-city-banner-background-image_260946.jpg")
    embed.set_footer(text="Durée de la vision : 10 secondes")

    view = LienFutur()
    await ctx.send(embed=embed, view=view)

    member = ctx.author
    role_temp = ctx.guild.get_role(ROLE_FUTUR_TEMPORAIRE)
    role_authorized = ctx.guild.get_role(ROLE_AUTORISÉ_FUTUR)

    if role_temp:
        await member.add_roles(role_temp)
        await asyncio.sleep(10)
        await member.remove_roles(role_temp)

    # Retirer le rôle autorisé à utiliser la commande
    if role_authorized and role_authorized in member.roles:
        await member.remove_roles(role_authorized)

    # Log l'action
    salon_logs = ctx.guild.get_channel(SALON_LOGS_FUTUR)
    if salon_logs:
        await salon_logs.send(
            f"🌀 **{ctx.author.display_name}** a activé `la magie temporelle`, a vu le futur restock et a perdu le rôle d'accès."
        )

@bot.command()
async def uptime(ctx):
    uptime_seconds = round(time.time() - start_time)
    days = uptime_seconds // (24 * 3600)
    hours = (uptime_seconds % (24 * 3600)) // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = uptime_seconds % 60
    embed = discord.Embed(
        title="Uptime du bot",
        description=f"Le bot est en ligne depuis : {days} jours, {hours} heures, {minutes} minutes, {seconds} secondes",
        color=discord.Color.blue()
    )
    embed.set_footer(text=f"♥️ by Shadow", icon_url=ctx.author.avatar.url)
    await ctx.send(embed=embed)

# CONFIGURATION : Remplace les ID ci-dessous
GUILD_ID = 946034497219100723  # Ton ID de serveur
PANEL_CHANNEL_ID = 1359833657581244568
LOG_CHANNEL_ID = 1358747155971571742
STAFF_ROLE_ID = 1265027964643315804

TICKET_CATEGORIES = {
    "Support": 1358748641879130234,
    "Partenariat": 1358752255381082152,
    "Recrutement": 1358751861535936643,
    "Signalement": 1358749533470851194,
}

@bot.event
async def on_ready():
    print(f"Bot connecté en tant que {bot.user}")
    await clear_panel_channel()
    await send_ticket_panel()

async def clear_panel_channel():
    channel = bot.get_channel(PANEL_CHANNEL_ID)
    await channel.purge()

async def send_ticket_panel():
    embed = discord.Embed(title="🎫 Ouvrir un Ticket", description="Choisissez une catégorie", color=0x00ff00)
    view = TicketPanelView()
    await bot.get_channel(PANEL_CHANNEL_ID).send(embed=embed, view=view)

class TicketPanelView(View):
    def __init__(self):
        super().__init__(timeout=None)
        for name in TICKET_CATEGORIES:
            self.add_item(TicketButton(name))

class TicketButton(Button):
    def __init__(self, category_name):
        super().__init__(label=category_name, style=discord.ButtonStyle.primary)
        self.category_name = category_name

    async def callback(self, interaction: discord.Interaction):
        category = bot.get_channel(TICKET_CATEGORIES[self.category_name])
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            interaction.guild.get_role(STAFF_ROLE_ID): discord.PermissionOverwrite(view_channel=True)
        }
        ticket_channel = await interaction.guild.create_text_channel(
            name=f"ticket-{interaction.user.name}",
            category=category,
            overwrites=overwrites
        )
        embed = discord.Embed(title="🎟️ Ticket Ouvert", description=f"{interaction.user.mention} a ouvert un ticket.", color=0x3498db)
        await ticket_channel.send(content=f"<@&{STAFF_ROLE_ID}>", embed=embed, view=TicketActionsView(interaction.user))
        await interaction.response.send_message(f"Votre ticket a été ouvert : {ticket_channel.mention}", ephemeral=True)
        await log_action(f"{interaction.user.mention} a ouvert un ticket dans {ticket_channel.mention}")

class TicketActionsView(View):
    def __init__(self, author):
        super().__init__()
        self.author = author
        self.claimed = False

    @discord.ui.button(label="Claim", style=discord.ButtonStyle.secondary)
    async def claim(self, interaction: discord.Interaction, button: Button):
        if self.claimed:
            return await interaction.response.send_message("Ce ticket est déjà pris.", ephemeral=True)
        self.claimed = True
        await interaction.channel.send(f"{interaction.user.mention} a claim le ticket.")
        await log_action(f"{interaction.user.mention} a claim un ticket dans {interaction.channel.mention}")

    @discord.ui.button(label="Fermer", style=discord.ButtonStyle.danger)
    async def close(self, interaction: discord.Interaction, button: Button):
        modal = CloseModal()
        await interaction.response.send_modal(modal)

class CloseModal(Modal):
    def __init__(self):
        super().__init__(title="Fermer le ticket")

    reason = TextInput(
        label="Raison de la fermeture",
        style=discord.TextStyle.paragraph,
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.channel.send(f"Ticket fermé par {interaction.user.mention}.\nRaison : {self.reason.value}")
        await log_action(f"{interaction.user.mention} a fermé le ticket {interaction.channel.name}. Raison : {self.reason.value}")
        await asyncio.sleep(2)
        await interaction.channel.delete()


# LOGS
async def log_action(message):
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    await log_channel.send(message)

# COMMANDES TEXTE

@bot.command()
async def claim(ctx):
    await ctx.send(f"{ctx.author.mention} a claim ce ticket.")
    await log_action(f"{ctx.author.mention} a claim le ticket {ctx.channel.mention}")

@bot.command()
async def close(ctx, *, reason: str = "Aucune raison donnée."):
    await ctx.send(f"Ticket fermé. Raison : {reason}")
    await log_action(f"{ctx.author.mention} a fermé le ticket {ctx.channel.name}. Raison : {reason}")
    await asyncio.sleep(2)
    await ctx.channel.delete()

@bot.command()
async def transfer(ctx, category_id: int):
    category = bot.get_channel(category_id)
    if isinstance(category, discord.CategoryChannel):
        await ctx.channel.edit(category=category)
        await ctx.send(f"Ticket transféré vers {category.name}")
        await log_action(f"{ctx.author.mention} a transféré le ticket vers {category.name}")
    else:
        await ctx.send("Catégorie invalide.")

# COMMANDES SLASH

@bot.tree.command(name="claim", description="Claim le ticket")
async def slash_claim(interaction: discord.Interaction):
    await interaction.response.send_message(f"{interaction.user.mention} a claim ce ticket.")
    await log_action(f"{interaction.user.mention} a claim le ticket {interaction.channel.mention}")

@bot.tree.command(name="close", description="Ferme le ticket avec une raison")
@app_commands.describe(reason="Raison de la fermeture")
async def slash_close(interaction: discord.Interaction, reason: str):
    await interaction.response.send_message(f"Ticket fermé. Raison : {reason}")
    await log_action(f"{interaction.user.mention} a fermé le ticket {interaction.channel.name}. Raison : {reason}")
    await asyncio.sleep(2)
    await interaction.channel.delete()

@bot.tree.command(name="transfer", description="Transfère un ticket vers une autre catégorie")
@app_commands.describe(category_id="Nouvelle catégorie ID")
async def slash_transfer(interaction: discord.Interaction, category_id: int):
    category = bot.get_channel(category_id)
    if isinstance(category, discord.CategoryChannel):
        await interaction.channel.edit(category=category)
        await interaction.response.send_message(f"Ticket transféré vers {category.name}")
        await log_action(f"{interaction.user.mention} a transféré le ticket vers {category.name}")
    else:
        await interaction.response.send_message("Catégorie invalide.", ephemeral=True)

# Token pour démarrer le bot (à partir des secrets)
# Lancer le bot avec ton token depuis l'environnement  
keep_alive()
bot.run(token)
