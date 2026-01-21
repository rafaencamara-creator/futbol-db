import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

ligas = [
    "LaLiga",
    "LaLiga 2",
    "Premier League",
    "Serie A",
    "Bundesliga",
    "Ligue 1"
]

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

for liga in ligas:
    c.execute(
        "INSERT OR IGNORE INTO ligas (nombre) VALUES (?)",
        (liga,)
    )

conn.commit()
conn.close()

print("Ligas cargadas correctamente")
