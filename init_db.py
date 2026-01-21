import sqlite3

# Conecta a la base de datos (se crea automáticamente)
conn = sqlite3.connect("database.db")
c = conn.cursor()

# Tabla de jugadores
c.execute("""
CREATE TABLE jugadores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE,
    nacionalidad TEXT
)
""")

# Tabla de clubes
c.execute("""
CREATE TABLE clubes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE,
    liga TEXT
)
""")

# Tabla de entrenadores
c.execute("""
CREATE TABLE entrenadores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE,
    nacionalidad TEXT
)
""")

# Historial de jugadores en clubes
c.execute("""
CREATE TABLE historial_jugador (
    jugador_id INTEGER,
    club_id INTEGER,
    inicio INTEGER,
    fin INTEGER
)
""")

# Historial de entrenadores en clubes
c.execute("""
CREATE TABLE historial_entrenador (
    entrenador_id INTEGER,
    club_id INTEGER,
    inicio INTEGER,
    fin INTEGER
)
""")

# Títulos (colectivos o individuales)
c.execute("""
CREATE TABLE titulos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    tipo TEXT
)
""")

# Relación jugador-título
c.execute("""
CREATE TABLE titulos_jugador (
    jugador_id INTEGER,
    titulo_id INTEGER
)
""")

# Guardar cambios y cerrar conexión
conn.commit()
conn.close()

print("Base de datos creada")
