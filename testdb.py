import sqlite3
import pandas as pd

conn = sqlite3.connect("silph-scope.db")
df = pd.read_sql_query("select p.pokemon_id, p.name AS pokemon_name, s.species_id, s.name AS species_name FROM pokemon_species ps JOIN pokemon p ON ps.pokemon_id = p.pokemon_id JOIN species s ON ps.species_id = s.species_id where p.name = 'arcanine-hisui' ORDER BY p.pokemon_id;", conn)
df2 = pd.read_sql_query("select p.name AS pokemon_name, m.name AS move_name, pm.move_learn_method_id, pm.version_group_id, pm.level_learned_at from pokemon_moves pm JOIN moves m ON pm.move_id = m.move_id JOIN pokemon p ON pm.pokemon_id = p.pokemon_id WHERE pokemon_name = 'arcanine-hisui' limit 50;", conn)
df3 = pd.read_sql_query("select p.name, eg.name AS egg_group FROM pokemon p JOIN pokemon_species ps ON p.pokemon_id = ps.pokemon_id JOIN species_egg_groups seg ON ps.species_id = seg.species_id JOIN egg_groups eg ON seg.egg_group_id = eg.egg_group_id where p.name = 'crawdaunt' order by ps.species_id", conn)
df4 = pd.read_sql_query("select * from pokemon_stats ps join pokemon p on ps.pokemon_id = p.pokemon_id where name = 'typhlosion'", conn)
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
print(df4)
conn.close()
