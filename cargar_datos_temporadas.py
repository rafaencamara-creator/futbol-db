import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# 1️⃣ Crear temporada
c.execute(
    "INSERT OR IGNORE INTO temporadas (nombre) VALUES (?)",
    ("2003-2004",)
)

# 2️⃣ Asociar club a liga en esa temporada
c.execute("""
INSERT INTO club_liga_temporada (club_id, liga_id, temporada_id)
VALUES (
    (SELECT id FROM clubes WHERE nombre = ?),
    (SELECT id FROM ligas WHERE nombre = ?),
    (SELECT id FROM temporadas WHERE nombre = ?)
)
""", (
    "Deportivo de La Coruña",
    "LaLiga",
    "2003-2004"
))

conn.commit()
conn.close()

print("Datos de temporada cargados correctamente")
