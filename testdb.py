import sqlite3
import pandas as pd

conn = sqlite3.connect("silph-scope.db")
df_check = pd.read_sql_query("""
    SELECT
        *
    FROM pokemon WHERE name LIKE "%mimikyu%";
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
        t.name as type_name,
        COUNT(*) as move_count
    FROM move_types mt
    join moves m on mt.move_id = m.move_id
    join types t on mt.type_id = t.type_id
    group by t.name;
""", conn)

df_check4 = pd.read_sql_query("""
    SELECT
        p.pokemon_id, m.name, p.name, pm.version_group_id, pm.level_learned_at, vg.name, m.power
    FROM pokemon_moves pm
    join moves m on m.move_id = pm.move_id
    JOIN pokemon p on pm.pokemon_id = p.pokemon_id
    join version_groups vg on pm.version_group_id = vg.version_group_id
    where p.name = 'bulbasaur' and vg.name = 'crystal' order by pm.level_learned_at;
""", conn)


print(df_check)
conn.close()
