import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# =========================
# JUGADORES
# =========================
c.execute("""
CREATE TABLE IF NOT EXISTS jugadores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL,
    nacionalidad TEXT
)
""")

# =========================
# CLUBES
# =========================
c.execute("""
CREATE TABLE IF NOT EXISTS clubes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL
)
""")

# =========================
# ENTRENADORES
# =========================
c.execute("""
CREATE TABLE IF NOT EXISTS entrenadores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL,
    nacionalidad TEXT
)
""")

# =========================
# TITULOS
# =========================
c.execute("""
CREATE TABLE IF NOT EXISTS titulos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL,
    tipo TEXT
)
""")

# =========================
# TEMPORADAS
# =========================
c.execute("""
CREATE TABLE IF NOT EXISTS temporadas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL
)
""")

# =========================
# HISTORIAL JUGADOR
# =========================
c.execute("""
CREATE TABLE IF NOT EXISTS historial_jugador (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    jugador_id INTEGER NOT NULL,
    club_id INTEGER NOT NULL,
    inicio TEXT,
    fin TEXT,
    FOREIGN KEY (jugador_id) REFERENCES jugadores(id),
    FOREIGN KEY (club_id) REFERENCES clubes(id)
)
""")

# =========================
# HISTORIAL ENTRENADOR
# =========================
c.execute("""
CREATE TABLE IF NOT EXISTS historial_entrenador (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entrenador_id INTEGER NOT NULL,
    club_id INTEGER NOT NULL,
    inicio TEXT,
    fin TEXT,
    FOREIGN KEY (entrenador_id) REFERENCES entrenadores(id),
    FOREIGN KEY (club_id) REFERENCES clubes(id)
)
""")

# =========================
# TITULOS JUGADOR
# =========================
c.execute("""
CREATE TABLE IF NOT EXISTS titulos_jugador (
    jugador_id INTEGER NOT NULL,
    titulo_id INTEGER NOT NULL,
    PRIMARY KEY (jugador_id, titulo_id),
    FOREIGN KEY (jugador_id) REFERENCES jugadores(id),
    FOREIGN KEY (titulo_id) REFERENCES titulos(id)
)
""")

# =========================
# CLUB - LIGA - TEMPORADA
# =========================
c.execute("""
CREATE TABLE IF NOT EXISTS club_liga_temporada (
    club_id INTEGER NOT NULL,
    temporada_id INTEGER NOT NULL,
    liga TEXT NOT NULL,
    PRIMARY KEY (club_id, temporada_id),
    FOREIGN KEY (club_id) REFERENCES clubes(id),
    FOREIGN KEY (temporada_id) REFERENCES temporadas(id)
)
""")

conn.commit()
conn.close()

print("Base de datos creada correctamente.")
