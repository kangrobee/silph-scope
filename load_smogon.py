import os
import json
import sqlite3
import pandas as pd
import gzip
import requests
from bs4 import BeautifulSoup

variants = {
    "indeedee": "indeedee-male",
    "indeedee-f": "indeedee-female",
    "meowstic": "meowstic-male",
    "meowstic-f" : "meowstic-female",
    "basculegion": "basculegion-male",
    "basculegion-f": "basculegion-female",
    "oinkologne": "oinkologne-male",
    "oinkologne-f": "oinkologne-female",
    "ogerpon-hearthflame": "ogerpon-hearthflame-mask",
    "ogerpon-wellspring": "ogerpon-wellspring-mask",
    "ogerpon-cornerstone": "ogerpon-cornerstone-mask",
    "tornadus": "tornadus-incarnate",
    "landorus": "landorus-incarnate",
    "thundurus": "thundurus-incarnate",
    "enamorus": "enamorus-incarnate",
    "tatsugiri": "tatsugiri-curly",
    "urshifu": "urshifu-rapid-strike",
    "maushold": "maushold-family-of-four",
    "meloetta" : "meloetta-aria",
    "necrozma-dawn-wings" : "necrozma-dawn",
    "necrozma-dusk-mane" : "necrozma-dusk",
    "giratina": "giratina-altered",
    "palafin": "palafin-hero",
    "tauros-paldea-blaze": "tauros-paldea-blaze-breed",
    "tauros-paldea-combat": "tauros-paldea-combat-breed",
    "tauros-paldea-aqua": "tauros-paldea-aqua-breed",
    "dudunsparce" : "dudunsparce-three-segment",
    "keldeo": "keldeo-ordinary",
    "mimikyu": "mimikyu-disguised",
    "mimikyu-totem": "mimikyu-totem-disguised",
    "arceus-bug": "arceus",
    "arceus-dark": "arceus",
    "arceus-dragon": "arceus",
    "arceus-electric": "arceus",
    "arceus-fairy": "arceus",
    "arceus-fighting": "arceus",
    "arceus-fire": "arceus",
    "arceus-flying": "arceus",
    "arceus-ghost": "arceus",
    "arceus-grass": "arceus",
    "arceus-ground": "arceus",
    "arceus-ice": "arceus",
    "arceus-poison": "arceus",
    "arceus-psychic": "arceus",
    "arceus-rock": "arceus",
    "arceus-steel": "arceus",
    "arceus-water": "arceus",
    "toxtricity": "toxtricity-amped",
    "minior" : "minior-red",
    "lycanroc" : "lycanroc-midday",
    "morpeko" : "morpeko-full-belly",
    "shaymin" : "shaymin-land",
    "eiscue" : "eiscue-noice",
    "deoxys" : "deoxys-normal",
    "squawkabilly" : "squawkabilly-green-plumage",
    "basculin" : "basculin-red-striped",
    "oricorio" : 'oricorio-baile',
    "darmanitan" : 'darmanitan-standard',
    "gourgeist" : "gourgeist-average",
    "zygarde" : 'zygarde-50',
    "silvally-bug": "silvally",
    "silvally-dark": "silvally",
    "silvally-dragon": "silvally",
    "silvally-electric": "silvally",
    "silvally-fairy": "silvally",
    "silvally-fighting": "silvally",
    "silvally-fire": "silvally",
    "silvally-flying": "silvally",
    "silvally-ghost": "silvally",
    "silvally-grass": "silvally",
    "silvally-ground": "silvally",
    "silvally-ice": "silvally",
    "silvally-poison": "silvally",
    "silvally-psychic": "silvally",
    "silvally-rock": "silvally",
    "silvally-steel": "silvally",
    "silvally-water": "silvally",
    "aegislash" : "aegislash-shield",
    "wishiwashi" : "wishiwashi-school",
    "nidoranf" : "nidoran-f",
    "nidoranm" : "nidoran-m",
    "pumpkaboo" : "pumpkaboo-average",
    "wormadam" : "wormadam-plant"
}


conn = sqlite3.connect("silph-scope.db")
cur = conn.cursor()

with open("schema.sql", "r", encoding="utf-8") as f:
    cur.executescript(f.read())



# Load in all of the months
url = "https://www.smogon.com/stats/"
r = requests.get(url)
months = []
if r.status_code == 200:
    soup = BeautifulSoup(r.text, "html.parser")
    months = [a['href'].rstrip('/') for a in soup.find_all('a') if a.get('href', '').endswith('/')]
    months = months[1:]
    print(months)
else:
    print("Failed")

# Loading all formats possible to battle_formats
for month in months:
    url = f"https://www.smogon.com/stats/{month}/chaos"
    files = []
    r = requests.get(url)

    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "html.parser")
        files = [
            a['href'].removesuffix('.json')
            for a in soup.find_all('a')
            if a.get('href', '').endswith('.json') and "cap" not in a['href'].lower()
        ]
        #print(files)
    else:
        print("Failed")
    for file in files:
        cur.execute("INSERT OR IGNORE INTO battle_formats (battle_format_name) VALUES (?)", (file,))

conn.commit()


url = f"https://www.smogon.com/stats/2014-11/chaos"
files = []
r = requests.get(url)

if r.status_code == 200:
    soup = BeautifulSoup(r.text, "html.parser")

    files = [
        a['href'].removesuffix('.json')
        for a in soup.find_all('a')
        if a.get('href', '').endswith('.json') and "cap" not in a['href'].lower()
    ]
    print(files)
else:
    print("Failed")



def normalize_name(name):
    # lowercase, replace spaces with hyphens, strip punctuation issues
    name = name.lower()
    name = name.replace(" ", "-")
    name = name.replace("'", "")
    name = name.replace(".", "")
    name = name.replace("%", "")
    name = name.replace(":", "")
    return name


for file in files:
    url = f"https://www.smogon.com/stats/2014-11/chaos/{file}.json"
    r = requests.get(url)
    data = r.json()

    battle_format_name = file
    cur.execute("SELECT battle_format_id FROM battle_formats WHERE battle_format_name = ?", (battle_format_name,))
    bf_result = cur.fetchone()
    if not bf_result:
        print("could not find battle format", battle_format_name)
        continue
    battle_format_id = bf_result[0]

    for name in data['data']:

        normalized = normalize_name(name)
        if normalized in variants:
            normalized = variants[normalized]
        cur.execute("SELECT pokemon_id FROM pokemon WHERE name = ?", (normalized,))
        result = cur.fetchone()
        if not result:
            print("could not find ", normalized)
        pokemon_id = result[0]


        raw_count = data['data'][name].get('Raw count')

        usage_percent = data['data'][name].get('usage')
        if not usage_percent


        cur.execute("""
            INSERT INTO pokemon_usage (pokemon_id, battle_format_id, raw_count, usage_percent, month)
            VALUES (?, ?, ?, ?, ?)
        """, (pokemon_id, battle_format_id, raw_count, usage_percent, month))


conn.commit()
cur.close()
conn.close()




