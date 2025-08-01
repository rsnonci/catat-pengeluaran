import discord
import openai
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from datetime import datetime
import os
import re
from dotenv import load_dotenv
import asyncio

load_dotenv()

# === SETUP DISCORD BOT ===
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# === KEEP ALIVE TASK ===
# This task will run every 10 minutes to keep the bot alive
async def keep_alive():
    while True:
        print("Keep alive:", datetime.now())
        await asyncio.sleep(600)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.lower() == "ping":
        await message.channel.send("pong")

async def on_ready():
    print(f'Bot ready: {client.user}')

    # keep_alive
    client.loop.create_task(keep_alive())

    #=== HEARTBEAT TASK ===
    channel_id = int(os.getenv("DISCORD_CHANNEL_ID"))
    channel = client.get_channel(channel_id)

    async def heartbeat():
        while True:
            if channel:
                await channel.send(f"✅ Bot masih aktif {datetime.now().strftime('%H:%M:%S')}")
            await asyncio.sleep(3600)

    client.loop.create_task(heartbeat())

# === OPENAI SETUP ===
openai.api_key = os.getenv("OPEN_API_KEY")
openai.api_base = os.getenv("OPEN_API_BASE_URL")

# === GOOGLE SHEETS SETUP ===
SHEET_ID = os.getenv("SHEET_ID")
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
sheet = build('sheets', 'v4', credentials=creds).spreadsheets()

# === DISCORD EVENTS ===
@client.event
async def on_ready():
    print(f'Bot aktif sebagai {client.user}')

@client.event
async def on_message(message):
    print(f"[DEBUG] Pesan dari {message.author}: {message.content}")

    if message.author == client.user:
        return

    if message.content.startswith('!catat'):
        user_input = message.content.replace('!catat', '').strip()
        prompt = f"""
        Kamu adalah AI pencatat keuangan.

        Dari input ini: "{user_input}", keluarkan dalam format CSV **tanpa header**, satu baris:

        [Tanggal (YYYY-MM-DD), Kategori, Jumlah, Deskripsi]

        **Tanggal otomatis adalah hari ini.**  
        Jika ada kata 'makan', kategorinya = makanan.

        Contoh input dan output:

        Input: "5000 beli kopi"  
        Output: [2025-07-13, makanan, 5000, beli kopi]

        Input: "10000 makan siang"  
        Output: [2025-07-13, makanan, 10000, makan siang]

        Output kamu **harus** dalam format persis seperti ini (tanpa tambahan penjelasan):
        [2025-07-13, kebutuhan, 12500, beli sabun]

        Jangan jelaskan, langsung beri output satu baris dalam format CSV seperti di atas.

        Sekarang proses input ini: "{user_input}"
        Output hanya 1 baris CSV.
        """

        try:
            response = openai.ChatCompletion.create(
                model=os.getenv("OPEN_API_MODEL"),
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            output = response['choices'][0]['message']['content']
            print("[DEBUG] Response dari OpenRouter:\n", output)

            # Parsing output CSV
            cleaned = output.strip().replace('`', '').replace('[','').replace(']','')
            raw_line = re.split(r'[,\t]+', cleaned)
            parts = [p.strip().strip('"').strip("'") for p in raw_line if p.strip()]
            print(f"[DEBUG] Pesan dari {cleaned}: {parts}")

            if len(parts) == 3:
                parts.insert(0, datetime.today().strftime('%Y-%m-%d'))

            if len(parts) != 4:
                raise ValueError(f"Format output AI tidak sesuai: {parts}")

            tanggal = datetime.today().strftime('%Y-%m-%d')
            kategori, jumlah, deskripsi = parts[1], parts[2], parts[3]

            try:
                jumlah = int(jumlah)
            except ValueError:
                await message.channel.send(
                    "⚠️ Jumlah harus berupa angka. Format yang benar misalnya: `!catat 10000 beli sabun`"
                )
                return

            row = [[tanggal, kategori, jumlah, deskripsi]]

            # Simpan ke Google Sheets
            sheet.values().append(
                spreadsheetId=SHEET_ID,
                range='Sheet1!A:D',
                valueInputOption='USER_ENTERED',
                body={'values': row}
            ).execute()

            await message.channel.send(f"✅ Dicatat: {jumlah} untuk {deskripsi}")
        except Exception as e:
            print("[ERROR]", e)
            await message.channel.send(f"⚠️ Error: {e}")

client.run(os.getenv("DISCORD_TOKEN"))
