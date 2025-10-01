import os
import json
import sqlite3
import pandas as pd
import gzip
import requests



conn = sqlite3.connect("silph-scope.db")
cur = conn.cursor()

url = f"https://www.smogon.com/stats/2025-08/chaos/gen9ou-0.json"

r = requests.get(url)


if r.status_code == 200:
    print(f"Downloaded")
else:
    print(f"Failed to download")

def normalize_name(name):
    # lowercase, replace spaces with hyphens, strip punctuation issues
    name = name.lower()
    name = name.replace(" ", "-")
    name = name.replace("'", "")
    name = name.replace(".", "")
    name = name.replace("%", "")
    name = name.replace(":", "")
    return name

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
    "wishiwashi" : "wishiwashi-school"
}

data = r.json()
print(data["info"])

for name in data['data']:
    normalized = normalize_name(name)
    if normalized in variants:
        normalized = variants[normalized]
    cur.execute("SELECT name FROM pokemon WHERE name = ?", (normalized,))
    result = cur.fetchone()
    if not result:
        print("could not find ", normalized)






