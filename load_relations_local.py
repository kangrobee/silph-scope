import os
import json
import sqlite3
import pandas as pd

# Connect
conn = sqlite3.connect("silph-scope.db")
cur = conn.cursor()

# SCHEMA
cur.executescript("""


CREATE TABLE IF NOT EXISTS pokemon (
    pokemon_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    height INTEGER,
    weight INTEGER,
    base_experience INTEGER,
    hp INTEGER,
    attack INTEGER,
    defense INTEGER,
    special_attack INTEGER,
    special_defense INTEGER,
    speed INTEGER
);

CREATE TABLE IF NOT EXISTS abilities (
    ability_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    generation TEXT
);

CREATE TABLE IF NOT EXISTS moves (
    move_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    generation TEXT,
    power INTEGER,
    accuracy INTEGER,
    pp INTEGER,
    priority INTEGER
);

CREATE TABLE IF NOT EXISTS berries (
    berry_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS egg_groups (
    egg_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS encounter_conds (
    encounter_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS encounter_values (
    encounter_value_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS encounter_methods (
    encounter_method_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);


CREATE TABLE IF NOT EXISTS evolution_chains (
    evolution_chain_id INTEGER PRIMARY KEY,
    evolution_chain_id2 INTEGER
);

CREATE TABLE IF NOT EXISTS evolution_triggers (
    evolution_trigger_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS genders (
    gender_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS generations (
    generation_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);


CREATE TABLE IF NOT EXISTS growth_rates (
    growth_rate_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);


CREATE TABLE IF NOT EXISTS items (
    item_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    cost INTEGER,
    fling_power INTEGER
);

CREATE TABLE IF NOT EXISTS item_attributes (
    item_attribute_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS item_categories (
    item_category_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS item_fling_effects (
    item_fling_effect_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS item_pockets (
    item_pocket_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);


CREATE TABLE IF NOT EXISTS locations (
    location_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS location_areas (
    location_area_id INTEGER PRIMARY KEY,
    location_name TEXT NOT NULL,
    name TEXT
);


CREATE TABLE IF NOT EXISTS machines (
    machine_id INTEGER PRIMARY KEY,
    item_name TEXT NOT NULL,
    move_name TEXT
);

CREATE TABLE IF NOT EXISTS move_ailments (
    move_ailment_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS move_battle_styles (
    move_battle_style_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS move_categories(
    move_category_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS move_damage_classes (
    move_damage_class_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);


CREATE TABLE IF NOT EXISTS move_learn_methods (
    move_learn_method_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS move_targets (
    move_target_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS natures (
    nature_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    decreased_stat TEXT,
    increased_stat TEXT
);

CREATE TABLE IF NOT EXISTS pokedexes (
    pokedex_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS colors (
    color_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS shapes (
    shape_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS habitats (
    habitat_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS regions (
    region_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS stats (
    stat_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS types (
    type_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS versions (
    version_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS version_groups (
    version_group_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    order_num INTEGER
);


CREATE TABLE IF NOT EXISTS pokemon_abilities (
    pokemon_id INTEGER,
    ability_id INTEGER,
    PRIMARY KEY (pokemon_id, ability_id),
    FOREIGN KEY (pokemon_id) REFERENCES pokemon(pokemon_id),
    FOREIGN KEY (ability_id) REFERENCES abilities(ability_id)
);

CREATE TABLE IF NOT EXISTS pokemon_types (
    pokemon_id INTEGER,
    type_id INTEGER,
    PRIMARY KEY (pokemon_id, type_id),
    FOREIGN KEY (pokemon_id) REFERENCES pokemon(pokemon_id),
    FOREIGN KEY (type_id) REFERENCES types(type_id)
)


""")


# Extractors
def get_Pokemon(data): return (data["id"], data["name"], data["height"], data["weight"], data["base_experience"], data["stats"][0]["base_stat"], data["stats"][1]["base_stat"], data["stats"][2]["base_stat"], data["stats"][3]["base_stat"], data["stats"][4]["base_stat"], data["stats"][5]["base_stat"])
def get_Abilities(data): return (data["id"], data["name"], data["generation"]["name"])
def get_Moves(data): return (data["id"], data["name"], data["generation"]["name"], data["power"], data["accuracy"], data["pp"], data["priority"])
def get_Id_Name(data): return (data["id"], data["name"])
def get_Evolution_Chain(data): return (data["id"], data["id"])
def get_Machine(data): return (data["id"], data["item"]["name"], data["move"]["name"])
def get_Version_Group(data): return (data["id"], data["name"], data["order"])
def get_Location_Area(data): return (data["id"], data["location"]["name"], data["name"])
def get_Item(data): return (data["id"], data["name"], data["cost"], data["fling_power"])
def get_Natures(data): return (data["id"], data["name"], data["increased_stat"]["name"] if data["increased_stat"] else None, data["decreased_stat"]["name"] if data["decreased_stat"] else None)

# Table config
TABLE_CONFIG = [
    {"name": "pokemon", "path": "./PokeData/api/v2/pokemon", "columns": ["pokemon_id","name","height","weight","base_experience", "hp", "attack", "defense", "special_attack", "special_defense", "speed"], "extract": get_Pokemon},
    {"name": "abilities", "path": "./PokeData/api/v2/ability", "columns": ["ability_id","name","generation"], "extract": get_Abilities},
    {"name": "moves", "path": "./PokeData/api/v2/move", "columns": ["move_id","name","generation","power","accuracy","pp","priority"], "extract": get_Moves},
    {"name": "berries", "path": "./PokeData/api/v2/berry", "columns": ["berry_id","name"], "extract": get_Id_Name},
    {"name": "egg_groups", "path": "./PokeData/api/v2/egg-group", "columns": ["egg_id","name"], "extract": get_Id_Name},
    {"name": "encounter_conds", "path": "./PokeData/api/v2/encounter-condition", "columns": ["encounter_id","name"], "extract": get_Id_Name},
    {"name": "encounter_values", "path": "./PokeData/api/v2/encounter-condition-value", "columns": ["encounter_value_id","name"], "extract": get_Id_Name},
    {"name": "encounter_methods", "path": "./PokeData/api/v2/encounter-method", "columns": ["encounter_method_id","name"], "extract": get_Id_Name},
    {"name": "evolution_chains", "path": "./PokeData/api/v2/evolution-chain", "columns": ["evolution_chain_id", "evolution_chain_id2"], "extract": get_Evolution_Chain},
    {"name": "evolution_triggers", "path": "./PokeData/api/v2/evolution-trigger", "columns": ["evolution_trigger_id","name"], "extract": get_Id_Name},
    {"name": "genders", "path": "./PokeData/api/v2/gender", "columns": ["gender_id","name"], "extract": get_Id_Name},
    {"name": "generations", "path": "./PokeData/api/v2/generation", "columns": ["generation_id","name"], "extract": get_Id_Name},
    {"name": "growth_rates", "path": "./PokeData/api/v2/growth-rate", "columns": ["growth_rate_id","name"], "extract": get_Id_Name},
    {"name": "items", "path": "./PokeData/api/v2/item", "columns": ["item_id","name", "cost", "fling_power"], "extract": get_Item},
    {"name": "item_attributes", "path": "./PokeData/api/v2/item-attribute", "columns": ["item_attribute_id","name"], "extract": get_Id_Name},
    {"name": "item_categories", "path": "./PokeData/api/v2/item-category", "columns": ["item_category_id","name"], "extract": get_Id_Name},
    {"name": "item_fling_effects", "path": "./PokeData/api/v2/item-fling-effect", "columns": ["item_fling_effect_id","name"], "extract": get_Id_Name},
    {"name": "item_pockets", "path": "./PokeData/api/v2/item-pocket", "columns": ["item_pocket_id","name"], "extract": get_Id_Name},
    {"name": "locations", "path": "./PokeData/api/v2/location", "columns": ["location_id","name"], "extract": get_Id_Name},
    {"name": "location_areas", "path": "./PokeData/api/v2/location-area", "columns": ["location_area_id","location_name", "name"], "extract": get_Location_Area},
    {"name": "machines", "path": "./PokeData/api/v2/machine", "columns": ["machine_id","item_name", "move_name"], "extract": get_Machine},
    {"name": "move_ailments", "path": "./PokeData/api/v2/move-ailment", "columns": ["move_ailment_id","name"], "extract": get_Id_Name},
    {"name": "move_battle_styles", "path": "./PokeData/api/v2/move-battle-style", "columns": ["move_battle_style_id","name"], "extract": get_Id_Name},
    {"name": "move_categories", "path": "./PokeData/api/v2/move-category", "columns": ["move_category_id","name"], "extract": get_Id_Name},
    {"name": "move_damage_classes", "path": "./PokeData/api/v2/move-damage-class", "columns": ["move_damage_class_id","name"], "extract": get_Id_Name},
    {"name": "move_learn_methods", "path": "./PokeData/api/v2/move-learn-method", "columns": ["move_learn_method_id","name"], "extract": get_Id_Name},
    {"name": "move_targets", "path": "./PokeData/api/v2/move-target", "columns": ["move_target_id","name"], "extract": get_Id_Name},
    {"name": "natures", "path": "./PokeData/api/v2/nature", "columns": ["nature_id","name", "increased_stat", "decreased_stat"], "extract": get_Natures},
    {"name": "pokedexes", "path": "./PokeData/api/v2/pokedex", "columns": ["pokedex_id","name"], "extract": get_Id_Name},
    {"name": "colors", "path": "./PokeData/api/v2/pokemon-color", "columns": ["color_id","name"], "extract": get_Id_Name},
    {"name": "habitats", "path": "./PokeData/api/v2/pokemon-habitat", "columns": ["habitat_id","name"], "extract": get_Id_Name},
    {"name": "shapes", "path": "./PokeData/api/v2/pokemon-shape", "columns": ["shape_id","name"], "extract": get_Id_Name},
    {"name": "regions", "path": "./PokeData/api/v2/region", "columns": ["region_id","name"], "extract": get_Id_Name},
    {"name": "stats", "path": "./PokeData/api/v2/stat", "columns": ["stat_id","name"], "extract": get_Id_Name},
    {"name": "types", "path": "./PokeData/api/v2/type", "columns": ["type_id","name"], "extract": get_Id_Name},
    {"name": "versions", "path": "./PokeData/api/v2/version", "columns": ["version_id","name"], "extract": get_Id_Name},
    {"name": "version_groups", "path": "./PokeData/api/v2/version-group", "columns": ["version_group_id","name", "order_num"], "extract": get_Version_Group}

]

# Loader for generic data
def load_table(cur, cfg):
    for folder in os.listdir(cfg["path"]):
        folder_path = os.path.join(cfg["path"], folder)

        if not os.path.isdir(folder_path):
            continue

        json_path = os.path.join(folder_path, "index.json")

        if not os.path.exists(json_path):
            continue

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        values = cfg["extract"](data)
        placeholders = "?" if isinstance(values, int) else ", ".join(["?"] * len(values))
        columns_str = ", ".join(cfg["columns"])
        cur.execute(f"INSERT OR IGNORE INTO {cfg['name']} ({columns_str}) VALUES ({placeholders})", values)

# Load
for cfg in TABLE_CONFIG:
    load_table(cur, cfg)

# Loader for many2many tables. Need to make a general function later.
for folder in os.listdir("./PokeData/api/v2/pokemon"):
    folder_path = os.path.join("./PokeData/api/v2/pokemon", folder)
    if not os.path.isdir(folder_path): continue
    json_path = os.path.join(folder_path, "index.json")
    if not os.path.exists(json_path): continue
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    pokemon_id = data["id"]
    for ability in data.get("abilities", []):
        ability_name = ability["ability"]["name"]
        cur.execute("SELECT ability_id FROM abilities WHERE name = ?", (ability_name,))
        result = cur.fetchone()
        if result:
            ability_id = result[0]
            cur.execute("INSERT OR IGNORE INTO pokemon_abilities (pokemon_id, ability_id) VALUES (?, ?)", (pokemon_id, ability_id))


# Loader for pokemon_types

for folder in os.listdir("./PokeData/api/v2/pokemon"):
    folder_path = os.path.join("./PokeData/api/v2/pokemon", folder)
    if not os.path.isdir(folder_path): continue
    json_path = os.path.join(folder_path, "index.json")
    if not os.path.exists(json_path): continue
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    pokemon_id = data["id"]
    for type in data.get("types", []):
        type_name = type["type"]["name"]
        cur.execute("SELECT type_id FROM types WHERE name = ?", (type_name,))
        result = cur.fetchone()
        if result:
            type_id = result[0]
            cur.execute("INSERT OR IGNORE INTO pokemon_types (pokemon_id, type_id) VALUES (?, ?)", (pokemon_id, type_id))





conn.commit()
cur.close()
conn.close()
