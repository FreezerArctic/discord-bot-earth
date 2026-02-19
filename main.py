import discord
from discord.ext import commands
from discord import app_commands
import json
import os
import matplotlib.pyplot as plt
import io
from datetime import datetime
from dotenv import load_dotenv

load_dotenv() # Cette ligne lit ton fichier .env
token = os.getenv('DISCORD_TOKEN')

# Configuration de Matplotlib
plt.switch_backend('Agg')

# --- 1. CONFIGURATION DES ITEMS BILINGUES ---
ITEMS_DATA = [
    {"fr": "Diamant", "en": "Diamond"},
    {"fr": "Lingot d'or", "en": "Gold Ingot"},
    {"fr": "Epée en fer", "en": "Iron Sword"},
    {"fr": "Pioche en fer", "en": "Iron Pickaxe"},
    {"fr": "Obsidienne", "en": "Obsidian"},
    {"fr": "Netherite", "en": "Netherite ingot"},
    {"fr": "Elytra", "en": "Elytra"},
    {"fr": "Epée légendaire", "en": "Legendary Sword"},
    {"fr": "Pioche légendaire", "en": "Legendary Pickaxe"},
    {"fr": "Hache légendaire", "en": "Legendary Axe"},
    {"fr": "Pelle 3x3", "en": "3x3 Shovel"},
    {"fr": "Casque légendaire", "en": "Legendary Helmet"},
    {"fr": "Plastron légendaire", "en": "Legendary Chestplate"},
    {"fr": "Pantalon légendaire", "en": "Legendary Leggings"},
    {"fr": "Bottes légendaires", "en": "Legendary Boots"},
    {"fr": "Brise-Roche", "en": "Rock-Breaker"},
    {"fr": "Baton de vente légendaire", "en": "Legendary Sell Stick"},
    {"fr": "Multitool", "en": "Multitool"},
    {"fr": "Pioche spawner légendaire", "en": "Legendary Spawner Pickaxe"},
    {"fr": "Clé Légendaire", "en": "Legendary Key"},
    {"fr": "Casque Epique", "en": "Epic Helmet"},
    {"fr": "Platron Epique", "en": "Epic Chestplate"},
    {"fr": "Jambieres Epique", "en": "Epic Leggings"},
    {"fr": "Bottes Epique", "en": "Epic Boots"},
    {"fr": "Lame du Châtiment", "en": "Blade of Punishment"},
    {"fr": "Pioche 3x3", "en": "3x3 Pickaxe"},
    {"fr": "Pioche de Feu", "en": "Fire Pickaxe"},
    {"fr": "Pioche Spawner Epique", "en": "Epic Spawner Pickaxe"},
    {"fr": "Baton de vente Epique", "en": "Epic Sell Stick"},
    {"fr": "Foudroyeuse", "en": "Lightning Striker"},
    {"fr": "Houe 3x3 Epique", "en": "Epic 3x3 Hoe"},
    {"fr": "Houe 3x3 légendaire", "en": "Legendary 3x3 Hoe"},
    {"fr": "Générateur a Golem de Fer", "en": "Iron Golem Spawner"},
    {"fr": "Générateur a Wither Squelette", "en": "Wither Skeleton Spawner"},
    {"fr": "Générateur a Poulpe Lumineux", "en": "Glow Squid Spawner"},
    {"fr": "Générateur a Poules", "en": "Chicken Spawner"},
    {"fr": "Générateur a Cochons", "en": "Pig Spawner"},
    {"fr": "Générateur a Zombie", "en": "Zombie Spawner"},
    {"fr": "Générateur a Vaches", "en": "Cow Spawner"},
    {"fr": "Générateur a Lapins", "en": "Rabbit Spawner"},
    {"fr": "Générateur a Hoglins", "en": "Hoglin Spawner"},
    {"fr": "Générateur a Piglins", "en": "Piglin Spawner"},
    {"fr": "Générateur a Piglins-Zombifiés", "en": "Zombified Piglin Spawner"},
    {"fr": "Générateur a Magma Cube", "en": "Magma Cube Spawner"},
    {"fr": "Générateur a Guardians", "en": "Guardian Spawner"},
    {"fr": "Générateur a Slimes", "en": "Slime Spawner"},
    {"fr": "Générateur a Creepers", "en": "Creeper Spawner"},
    {"fr": "Générateur a Endermans", "en": "Enderman Spawner"},
    {"fr": "Générateur a Blaze", "en": "Blaze Spawner"},
    {"fr": "Générateur a Araignées", "en": "Spider Spawner"},
    {"fr": "Pomme d'Or Enchantée", "en": "Enchanted Golden Apple"},
    {"fr": "Ender Pearl", "en": "Ender Pearl"},
    {"fr": "Débris antiques", "en": "Ancient Debris"},
    {"fr": "Oeuf de dragon", "en": "Dragon Egg"},
    {"fr": "Tête de dragon", "en": "Dragon Head"},
    {"fr": "Lingot de Cuivre", "en": "Copper Ingot"},
    {"fr": "Balise", "en": "Beacon"},
    {"fr": "Boîte de Shulker", "en": "Shulker Box"},
    {"fr": "Verrue du Nether", "en": "Nether Wart"},
    {"fr": "Canne a Sucre", "en": "Sugar Cane"},
    {"fr": "Etoile du Nether", "en": "Nether Star"},
    {"fr": "Bloc de Slime", "en": "Slime Block"},
    {"fr": "Totem d'immortalité", "en": "Totem of Undying"},
    {"fr": "Filet de Capture", "en": "Catch Net"},
]

ITEMS_AFFICHAGE = [f"{i['fr']} / {i['en']}" for i in ITEMS_DATA]

# --- 2. GESTION DES DONNÉES ---
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
DATA_FILE = "marche_v2.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try: return json.load(f)
            except: return {}
    return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'✅ Bot prêt | Historique Global Activé')

async def item_autocomplete(interaction: discord.Interaction, current: str):
    return [
        app_commands.Choice(name=choice, value=choice)
        for choice in ITEMS_AFFICHAGE if current.lower() in choice.lower()
    ][:25]

# --- 3. COMMANDES ---

@bot.tree.command(name="transaction", description="Enregistrer un achat ou une vente")
@app_commands.describe(type="Achat ou Vente", item="L'objet", prix="Prix unité", quantite="Nombre")
@app_commands.choices(type=[
    app_commands.Choice(name="Achat 📥", value="achat"),
    app_commands.Choice(name="Vente 📤", value="vente")
])
async def transaction(interaction: discord.Interaction, type: str, item: str, prix: int, quantite: int = 1):
    if item not in ITEMS_AFFICHAGE:
        await interaction.response.send_message("❌ Utilise la liste !", ephemeral=True)
        return

    item_key = item.split(" / ")[0].lower()
    data = load_data()
    
    if item_key not in data:
        data[item_key] = {"achat": [], "vente": []}
    
    if "global_history" not in data:
        data["global_history"] = []

    # Moyennes
    for _ in range(quantite):
        data[item_key][type].append(prix)
    
    # Historique
    nouvelle_entree = {
        "joueur": interaction.user.display_name,
        "item": item,
        "type": "ACHAT" if type == "achat" else "VENTE",
        "emoji": "📥" if type == "achat" else "📤",
        "prix": prix,
        "quantite": quantite,
        "date": datetime.now().strftime("%d/%m %H:%M")
    }
    data["global_history"].insert(0, nouvelle_entree)
    data["global_history"] = data["global_history"][:10]

    save_data(data)
    
    prix_total = prix * quantite
    embed = discord.Embed(title="Transaction Enregistrée", color=discord.Color.green() if type == "achat" else discord.Color.gold())
    embed.add_field(name="Item", value=item, inline=False)
    embed.add_field(name="Quantité", value=f"x{quantite}", inline=True)
    embed.add_field(name="Total", value=f"**{prix_total}** 💰", inline=True)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="historique", description="Voir les 10 dernières activités du marché")
async def historique(interaction: discord.Interaction):
    data = load_data()
    history = data.get("global_history", [])

    if not history:
        await interaction.response.send_message("📜 L'historique est vide.", ephemeral=True)
        return

    embed = discord.Embed(title="📜 Historique Global", color=discord.Color.blue())

    for entry in history:
        e = entry.get("emoji", "💰")
        t = entry.get("type", "TRANS.")
        i = entry.get("item", "Inconnu")
        q = entry.get("quantite", 1)
        p = entry.get("prix", 0)
        j = entry.get("joueur", "Anonyme")
        d = entry.get("date", "??/??")

        embed.add_field(
            name=f"{e} {t} : {i}",
            value=f"**{q}x** pour **{p*q}** 💰 (u: {p})\n*Par {j} le {d}*",
            inline=False
        )

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="prix", description="Voir les moyennes du marché")
async def prix(interaction: discord.Interaction, item: str):
    if item not in ITEMS_AFFICHAGE:
        await interaction.response.send_message("❌ Item invalide.", ephemeral=True)
        return

    item_key = item.split(" / ")[0].lower()
    data = load_data()
    
    if item_key in data:
        stats = data[item_key]
        moy_achat = sum(stats["achat"]) / len(stats["achat"]) if stats["achat"] else 0
        moy_vente = sum(stats["vente"]) / len(stats["vente"]) if stats["vente"] else 0
        
        embed = discord.Embed(title=f"📊 Marché : {item}", color=discord.Color.blue())
        embed.add_field(name="📥 Achat Moyen", value=f"**{moy_achat:.2f}** 💰", inline=True)
        embed.add_field(name="📤 Vente Moyenne", value=f"**{moy_vente:.2f}** 💰", inline=True)
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message(f"Aucune donnée pour **{item}**.")

@bot.tree.command(name="graphique", description="Évolution des prix")
async def graphique(interaction: discord.Interaction, item: str):
    if item not in ITEMS_AFFICHAGE:
        await interaction.response.send_message("❌ Item invalide.", ephemeral=True)
        return

    item_key = item.split(" / ")[0].lower()
    data = load_data()
    
    ventes = data.get(item_key, {}).get("vente", [])
    achats = data.get(item_key, {}).get("achat", [])

    if len(ventes) < 2 and len(achats) < 2:
        await interaction.response.send_message("📈 Pas assez de transactions.", ephemeral=True)
        return

    plt.figure(figsize=(10, 6))
    if len(ventes) >= 1: plt.plot(ventes, marker='o', color='#F1C40F', label='Ventes')
    if len(achats) >= 1: plt.plot(achats, marker='s', color='#3498DB', label='Achats')

    plt.title(f"Analyse : {item}")
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close()

    file = discord.File(buf, filename="graph.png")
    await interaction.response.send_message(file=file)

@bot.tree.command(name="clear_item", description="Réinitialiser un item")
async def clear_item(interaction: discord.Interaction, item: str):
    if item not in ITEMS_AFFICHAGE: 
        await interaction.response.send_message("❌ Item invalide.", ephemeral=True)
        return
    
    item_key = item.split(" / ")[0].lower()
    data = load_data()
    if item_key in data:
        del data[item_key]
        save_data(data)
        await interaction.response.send_message(f"✅ Données de **{item}** effacées.")
    else:
        await interaction.response.send_message("⚠️ Aucune donnée à effacer.")

# Autocomplétion
@transaction.autocomplete('item')
@prix.autocomplete('item')
@graphique.autocomplete('item')
@clear_item.autocomplete('item')
async def auto_all(interaction, current):
    return await item_autocomplete(interaction, current)

token = os.getenv('DISCORD_TOKEN') # On crée la variable 'token' ici !
bot.run(token)