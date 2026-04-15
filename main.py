import discord
from discord.ext import commands
import json
import random

# Initializing the bot with necessary permissions
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Load or create the inventory file
def load_data():
    try:
        with open("inventory.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open("inventory.json", "w") as f:
        json.dump(data, f, indent=4)

@bot.command()
async def mine(ctx):
    user_id = str(ctx.author.id)
    data = load_data()

    # Ensure the user exists in our "database"
    if user_id not in data:
        data[user_id] = {"Cobblestone": 0, "Iron": 0, "Diamond": 0}

    # Logic for what they find
    ores = ["Cobblestone", "Iron", "Diamond"]
    found = random.choices(ores, weights=[80, 18, 2], k=1)[0]
    
    data[user_id][found] += 1
    save_data(data)

    await ctx.send(f"⛏️ **{ctx.author.name}** mined a piece of **{found}**!")

@bot.command()
async def inv(ctx):
    user_id = str(ctx.author.id)
    data = load_data()
    
    if user_id not in data:
        return await ctx.send("Your inventory is empty! Use `!mine` to start.")

    inv_text = ""
    for item, amount in data[user_id].items():
        inv_text += f"**{item}:** {amount}\n"

    embed = discord.Embed(title=f"{ctx.author.name}'s Inventory", color=0x2ecc71)
    embed.description = inv_text
    await ctx.send(embed=embed)

# Replace 'YOUR_TOKEN_HERE' with your actual bot token from the Developer Portal
bot.run('YOUR_TOKEN_HERE')