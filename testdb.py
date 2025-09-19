import sqlite3
import pandas as pd

conn = sqlite3.connect("silph-scope.db")
df = pd.read_sql_query("select p.pokemon_id, p.name AS pokemon_name, a.ability_id, a.name AS ability_name FROM pokemon_abilities pa JOIN pokemon p ON pa.pokemon_id = p.pokemon_id JOIN abilities a ON pa.ability_id = a.ability_id where p.name = 'tympole' ORDER BY p.pokemon_id;", conn)
df2 = pd.read_sql_query("select * from evolution_chains", conn)
print(df2)
conn.close()
