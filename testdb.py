import sqlite3
import pandas as pd

conn = sqlite3.connect("silph-scope.db")
df_check = pd.read_sql_query("""
    SELECT
        pe.pokemon_id,
        p.name AS pokemon_name,
        v.name AS version_name,
        la.name AS location_area_name,
        em.name AS encounter_method_name,
        pe.min_level,
        pe.max_level
    FROM pokemon_encounters pe
    JOIN pokemon p ON p.pokemon_id = pe.pokemon_id
    JOIN versions v ON v.version_id = pe.version_id
    JOIN location_areas la ON la.location_area_id = pe.location_area_id
    JOIN encounter_methods em ON em.encounter_method_id = pe.encounter_method_id
    WHERE p.name = "magikarp" AND version_name = "emerald"
    ORDER BY pe.pokemon_id, v.version_id
    LIMIT 50
""", conn)

df_check2 = pd.read_sql_query("""
    SELECT
        *
    FROM pokemon_abilities
    JOIN pokemon on pokemon.pokemon_id = pokemon_abilities.pokemon_id
    JOIN abilities on pokemon_abilities.ability_id = abilities.ability_id
    WHERE pokemon.name = 'braviary-hisui'
""", conn)

df_check3 = pd.read_sql_query("""
    SELECT
        *
    FROM species_egg_groups seg
    JOIN species s ON seg.species_id = s.species_id
    JOIN egg_groups eg ON eg.egg_group_id = seg.egg_group_id
    WHERE s.name = 'crawdaunt';
""", conn)


print(df_check3)
conn.close()
