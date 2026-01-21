import sqlite3
import os

# Ruta correcta a la base de datos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# 1️⃣ Tabla de temporadas
c.execute("""
CREATE TABLE IF NOT EXISTS temporadas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL
)
""")

# 2️⃣ Tabla club + liga + temporada
c.execute("""
CREATE TABLE IF NOT EXISTS club_liga_temporada (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    club_id INTEGER NOT NULL,
    liga_id INTEGER NOT NULL,
    temporada_id INTEGER NOT NULL,
    FOREIGN KEY (club_id) REFERENCES clubes(id),
    FOREIGN KEY (liga_id) REFERENCES ligas(id),
    FOREIGN KEY (temporada_id) REFERENCES temporadas(id)
)
""")

# 3️⃣ Añadir temporada_id al historial del jugador
try:
    c.execute("""
    ALTER TABLE historial_jugador
    ADD COLUMN temporada_id INTEGER
    """)
except sqlite3.OperationalError:
    pass  # ya existe

conn.commit()
conn.close()

print("✅ Migración completada")
