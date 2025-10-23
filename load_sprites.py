import base64
import os
import psycopg2
from dotenv import load_dotenv


load_dotenv()
conn = psycopg2.connect(
    dbname=os.getenv("PG_DBNAME"),
    user=os.getenv("PG_USER"),
    password=os.getenv("PG_PASSWORD"),
    host=os.getenv("PG_HOST"),
    port=os.getenv("PG_PORT")
)

cur = conn.cursor()
with open("schema.sql", "r", encoding="utf-8") as f:
    cur.execute(f.read())


folder = "./pokesprites"

for filename in os.listdir(folder):
    if filename.endswith(".png"):
        path = os.path.join(folder, filename)
        with open(path, "rb") as image_file:
            base64_string = base64.b64encode(image_file.read()).decode("utf-8")
        cur.execute(
            "INSERT INTO sprites (sprite_name, sprite_data) VALUES (%s, %s)",
            (filename, base64_string)
        )
conn.commit()
