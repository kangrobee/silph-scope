import os
import json
import sqlite3
import pandas as pd
import gzip
from pathlib import Path


conn = sqlite3.connect("silph-scope.db")
cur = conn.cursor()

with open("schema.sql", "r", encoding="utf-8") as f:
    cur.executescript(f.read())

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
    "wormadam" : "wormadam-plant",
    "marowak-alola-totem" : "marowak-totem",
    "darmanitan-galar" : "darmanitan-galar-standard",
    "rockruff-dusk" : "rockruff-own-tempo",
    "xerneas-neutral" : "xerneas"
}

item_variants = {
    "leek" : "stick",
    "miracleberry" : "lumberry",
    "mintberry" : "chestoberry",
    "goldberry" : "sitrusberry",
    "pinkbow" : "silkscarf",
    "polkadotbow" : "silkscarf",
    "przcureberry" : "cheriberry",
    "mysteryberry" : "leppaberry",
    "psncureberry" : "pechaberry",
    "bitterberry" : "persimberry",
    "iceberry" : "rawstberry",
    "burntberry" : "aspearberry",
    "berry" : "oranberry",
    "mail" : "likemail"
}

def normalize_name(name):
    # lowercase, replace spaces with hyphens, strip punctuation issues
    name = name.lower()
    name = name.replace(" ", "-")
    name = name.replace("'", "")
    name = name.replace(".", "")
    name = name.replace("%", "")
    name = name.replace(":", "")
    if "--" in name:
        name = name.split("--")[0]

    return name





# for file in os.listdir("./SmogonData/2025-09/chaos/gen9ou-0.json"):
#     json_path = os.path.join("./SmogonData/2025-09/chaos", file)
#     with open(json_path, "r", encoding="utf-8") as f:
#         data = json.load(f)
#     print(data["info"]["metagame"])

def build_cache(cur, table_name, id_col, name_col="name"):
    cur.execute(f"SELECT {id_col}, {name_col} FROM {table_name}")
    return {name: _id for _id, name in cur.fetchall()}

pokemon_cache = build_cache(cur, "pokemon", "pokemon_id")
item_cache = build_cache(cur, "items", "item_id", "normalized_name")
move_cache = build_cache(cur, "moves", "move_id", "normalized_name")

month = "2025-09"
data_dir = Path(f"./SmogonData/{month}/chaos/")  # folder with JSONs

missed_pokemon = []
missed_moves = []
missed_items = []


cur.execute("BEGIN TRANSACTION")

for json_file in data_dir.glob("*.json"):

    if "cap" in json_file.name.lower() or "metronome" in json_file.name.lower():  # skip cap/metronome
        print(f"Skipping file: {json_file.name}")
        continue
    if not any(tier in json_file.name.lower() for tier in ["ou", "uu", "ru", "nu", "pu", "zu", "vgc", "double", "ubers" ]):
        print(f"Skipping file: {json_file.name}")
        continue
    print(f"{json_file.name}")
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        metagame = data['info']['metagame'] + '-' + str(int(data['info']['cutoff']))
        for pokemon_name, pokemon_data in data["data"].items():
            normalized = normalize_name(pokemon_name)
            if normalized in variants:
                normalized = variants[normalized]

            pokemon_id = pokemon_cache.get(normalized)

            if pokemon_id is None and normalized not in missed_pokemon:
                missed_pokemon.append(normalized)

            # cur.execute("SELECT pokemon_id FROM pokemon WHERE name = ?", (normalized,))
            # result = cur.fetchone()
            # if not result:
            #     print("could not find ", normalized)
            # pokemon_id = result[0]

            if "Items" in pokemon_data:
                inserts = []
                for item_name, item_count in pokemon_data["Items"].items():
                    if item_name in item_variants:
                        item_name = item_variants[item_name]

                    if not item_name or item_name.lower() in ("nothing", "empty") or item_count == 0:
                        continue
                    # cur.execute("SELECT item_id FROM items WHERE normalized_name = ?", (item_name,))
                    # result = cur.fetchone()

                    # if result:
                    #     item_id = result[0]
                    # else:
                    #     item_id = 0
                    #     #print("Item not found in items table:", item_name)

                    item_id = item_cache.get(item_name)

                    if item_id is None and item_name not in missed_items:
                        missed_items.append(item_name)

                    inserts.append((pokemon_id, item_id, item_count, month, metagame))

                cur.executemany("""
                        INSERT INTO smogon_items (pokemon_id, item_id, item_count, month, metagame)
                        VALUES (?, ?, ?, ?, ?)
                    """, inserts)

                    # cur.execute(
                    # """
                    # INSERT OR IGNORE INTO smogon_items (pokemon_id, item_id, item_count, month, metagame)
                    # VALUES (?, ?, ?, ?, ?)
                    # """,
                    # (pokemon_id, item_id, item_count, month, metagame))


            if "Moves" in pokemon_data:
                inserts = []
                for move_name, move_count in pokemon_data["Moves"].items():
                    if not move_name or move_name.lower() == "" or move_count == 0:
                        continue
                    if move_name == 'visegrip':
                        move_name = 'vicegrip'
                    # cur.execute("SELECT move_id FROM moves WHERE normalized_name = ?", (move_name,))
                    # result = cur.fetchone()

                    # if result:
                    #     move_id = result[0]
                    # else:
                    #     move_id = 0
                    #     print("Item not found in items table:", move_name)
                    total_count = sum(pokemon_data["Moves"].values())
                    move_id = move_cache.get(move_name)

                    if move_id is None and move_name not in missed_moves:
                        missed_moves.append(move_name)

                    move_perc = move_count / (total_count / 4)
                    inserts.append((pokemon_id, move_id, move_count, move_perc, month, metagame))

                cur.executemany("""
                            INSERT INTO smogon_moves (pokemon_id, move_id, move_count, move_perc, month, metagame)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, inserts)

                    # cur.execute(
                    # """
                    # INSERT INTO smogon_moves (pokemon_id, move_id, move_count, move_perc, month, metagame)
                    # VALUES (?, ?, ?, ?, ?, ?)
                    # """,
                    # (pokemon_id, move_id, move_count, move_perc, month, metagame))

            if "Teammates" in pokemon_data:
                inserts = []
                for teammate_name, teammate_count in pokemon_data["Teammates"].items():
                    if not teammate_name or teammate_name.lower() == "empty" or teammate_count == 0:
                        continue
                    normalized_teammate = normalize_name(teammate_name)
                    if normalized_teammate in variants:
                        normalized_teammate = variants[normalized_teammate]
                    # cur.execute("SELECT pokemon_id FROM pokemon WHERE name = ?", (normalized_teammate,))
                    # result = cur.fetchone()
                    # if not result:
                    #     print("could not find ", normalized_teammate)

                    # if result:
                    #     teammate_id = result[0]
                    # else:
                    #     #print("Item not found in items table:", normalized_teammate)
                    #     continue

                    teammate_id = pokemon_cache.get(normalized_teammate)
                    inserts.append((pokemon_id, teammate_id, teammate_count, month, metagame))

                cur.executemany("""
                            INSERT INTO smogon_teammates (pokemon_id, teammate_id, teammate_count, month, metagame)
                            VALUES (?, ?, ?, ?, ?)
                        """, inserts)
                    # cur.execute(
                    # """
                    # INSERT INTO smogon_teammates (pokemon_id, teammate_id, teammate_count, month, metagame)
                    # VALUES (?, ?, ?, ?, ?)
                    # """,
                    # (pokemon_id, teammate_id, teammate_count, month, metagame))


            if "Checks and Counters" in pokemon_data:
                inserts = []
                for check_name, check_arr in pokemon_data["Checks and Counters"].items():
                    if not check_name or check_name.lower() == "empty":
                        continue
                    normalized_check = normalize_name(check_name)
                    if normalized_check in variants:
                        normalized_check = variants[normalized_check]
                    # cur.execute("SELECT pokemon_id FROM pokemon WHERE name = ?", (normalized_teammate,))
                    # result = cur.fetchone()
                    # if not result:
                    #     print("could not find ", normalized_teammate)

                    # if result:
                    #     teammate_id = result[0]
                    # else:
                    #     #print("Item not found in items table:", normalized_teammate)
                    #     continue

                    check_id = pokemon_cache.get(normalized_check)
                    check_count = check_arr[0]
                    check_perc = check_arr[1]
                    check_sd = check_arr[2]

                    inserts.append((pokemon_id, check_id, check_count, check_perc, check_sd, month, metagame))

                cur.executemany("""
                            INSERT INTO smogon_checks (pokemon_id, check_id, check_count, check_perc, check_sd, month, metagame)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, inserts)

                    # cur.execute(
                    # """
                    # INSERT INTO smogon_checks (pokemon_id, check_id, check_count, check_perc, check_sd, month, metagame)
                    # VALUES (?, ?, ?, ?, ?, ?, ?)
                    # """,
                    # (pokemon_id, check_id, check_count, check_perc, check_sd, month, metagame))

print(missed_items)
conn.commit()
conn.close()



