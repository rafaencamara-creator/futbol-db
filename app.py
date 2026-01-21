from flask import Flask, render_template, request, jsonify, redirect, session
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

app = Flask(__name__)

app.secret_key = "#Mickybite18Ngolonigger47pickcotton"

# ===========================
# UTILIDAD DB
# ===========================
def query_db(query, params=()):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()
    return rows


# ===========================
# AUTOCOMPLETADO
# ===========================
@app.route("/autocomplete/<tipo>")
def autocomplete(tipo):
    q = request.args.get("q", "").strip().lower()
    if not q:
        return jsonify([])

    tablas = {
        "jugadores": "jugadores",
        "clubes": "clubes",
        "entrenadores": "entrenadores",
        "titulos": "titulos"
    }

    if tipo not in tablas:
        return jsonify([])

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute(
        f"""
        SELECT nombre
        FROM {tablas[tipo]}
        WHERE
            LOWER(nombre) LIKE ?
            OR LOWER(nombre) LIKE ?
        ORDER BY nombre
        LIMIT 10
        """,
        (
            q + "%",
            "% " + q + "%"
        )
    )

    resultados = [r[0] for r in c.fetchall()]
    conn.close()
    return jsonify(resultados)




# ===========================
# BUSQUEDA
# ===========================
@app.route("/", methods=["GET", "POST"])
def index():
    resultados = []

    if request.method == "POST":
        f_nacionalidad = request.form.get("f_nacionalidad")
        f_club = request.form.get("f_club")
        f_liga = request.form.get("f_liga")
        f_companero = request.form.get("f_companero")
        f_entrenador = request.form.get("f_entrenador")
        f_titulo = request.form.get("f_titulo")

        nacionalidad = request.form.get("nacionalidad")
        club = request.form.get("club")
        liga = request.form.get("liga")
        companero = request.form.get("companero")
        entrenador = request.form.get("entrenador")
        titulo = request.form.get("titulo")

        params = []
        necesita_historial = f_club or f_liga or f_companero or f_entrenador

        if not necesita_historial:
            query = "SELECT DISTINCT j.id, j.nombre FROM jugadores j WHERE 1=1"

            if f_nacionalidad and nacionalidad:
                query += " AND j.nacionalidad = ?"
                params.append(nacionalidad)

            if f_titulo and titulo:
                query += """
                AND EXISTS (
                    SELECT 1 FROM titulos_jugador tj
                    JOIN titulos t ON tj.titulo_id = t.id
                    WHERE tj.jugador_id = j.id AND t.nombre = ?
                )
                """
                params.append(titulo)
        else:
            query = """
            SELECT DISTINCT j.id, j.nombre
            FROM jugadores j
            JOIN historial_jugador hj ON j.id = hj.jugador_id
            JOIN clubes c ON hj.club_id = c.id
            WHERE 1=1
            """

            if f_club and club:
                query += " AND c.nombre = ?"
                params.append(club)

            if f_liga and liga:
                query += " AND c.liga = ?"
                params.append(liga)

            if f_companero and companero:
                query += """
                AND EXISTS (
                    SELECT 1 FROM historial_jugador hj2
                    JOIN jugadores j2 ON hj2.jugador_id = j2.id
                    WHERE j2.nombre = ?
                      AND hj2.club_id = hj.club_id
                      AND hj2.inicio <= hj.fin
                      AND hj2.fin >= hj.inicio
                )
                """
                params.append(companero)

            if f_entrenador and entrenador:
                query += """
                AND EXISTS (
                    SELECT 1 FROM historial_entrenador he
                    JOIN entrenadores e ON he.entrenador_id = e.id
                    WHERE he.club_id = hj.club_id
                      AND e.nombre = ?
                      AND he.inicio <= hj.fin
                      AND he.fin >= hj.inicio
                )
                """
                params.append(entrenador)

            if f_nacionalidad and nacionalidad:
                query += " AND j.nacionalidad = ?"
                params.append(nacionalidad)

            if f_titulo and titulo:
                query += """
                AND EXISTS (
                    SELECT 1 FROM titulos_jugador tj
                    JOIN titulos t ON tj.titulo_id = t.id
                    WHERE tj.jugador_id = j.id AND t.nombre = ?
                )
                """
                params.append(titulo)

        resultados = query_db(query, params)

    entrenadores = query_db("SELECT nombre FROM entrenadores ORDER BY nombre")
    ligas = query_db("SELECT DISTINCT liga FROM clubes ORDER BY liga")
    titulos = query_db("SELECT nombre FROM titulos ORDER BY nombre")


    return render_template(
        "index.html",
        resultados=resultados,
        entrenadores=entrenadores,
        ligas=ligas,
        titulos=titulos
    )




# ===========================
# AÑADIR DATOS BASE
# ===========================
@app.route("/add", methods=["GET", "POST"])
def add_data():
    if not session.get("admin"):
        return redirect("/login")

    ...

    if request.method == "POST":
        tipo = request.form["tipo"]
        nombre = request.form["nombre"]
        extra = request.form.get("extra")

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        if tipo == "jugador":
            c.execute(
                "INSERT OR IGNORE INTO jugadores (nombre, nacionalidad) VALUES (?, ?)",
                (nombre, extra)
            )
        elif tipo == "entrenador":
            c.execute(
                "INSERT OR IGNORE INTO entrenadores (nombre, nacionalidad) VALUES (?, ?)",
                (nombre, extra)
            )
        elif tipo == "club":
            c.execute(
                "INSERT OR IGNORE INTO clubes (nombre, liga) VALUES (?, ?)",
                (nombre, extra)
            )
        elif tipo == "titulo":
            c.execute(
                "INSERT OR IGNORE INTO titulos (nombre, tipo) VALUES (?, '')",
                (nombre,)
            )

        conn.commit()
        conn.close()

    return render_template("add_data.html")


# ===========================
# HISTORIAL JUGADOR
# ===========================
@app.route("/historial_jugador", methods=["GET", "POST"])
def historial_jugador():
    if not session.get("admin"):
        return redirect("/login")

    if request.method == "POST":
        jugador = request.form["jugador"]
        club = request.form["club"]
        inicio = request.form["inicio"]
        fin = request.form["fin"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        c.execute("SELECT id FROM jugadores WHERE nombre = ?", (jugador,))
        j = c.fetchone()
        c.execute("SELECT id FROM clubes WHERE nombre = ?", (club,))
        cl = c.fetchone()

        if j and cl:
            c.execute(
                "INSERT INTO historial_jugador (jugador_id, club_id, inicio, fin) VALUES (?, ?, ?, ?)",
                (j[0], cl[0], inicio, fin)
            )

        conn.commit()
        conn.close()

    return render_template("add_historial_jugador.html")


# ===========================
# HISTORIAL ENTRENADOR
# ===========================
@app.route("/historial_entrenador", methods=["GET", "POST"])
def historial_entrenador():
    if not session.get("admin"):
        return redirect("/login")

    if request.method == "POST":
        entrenador = request.form["entrenador"]
        club = request.form["club"]
        inicio = request.form["inicio"]
        fin = request.form["fin"]

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        c.execute("SELECT id FROM entrenadores WHERE nombre = ?", (entrenador,))
        e = c.fetchone()
        c.execute("SELECT id FROM clubes WHERE nombre = ?", (club,))
        cl = c.fetchone()

        if e and cl:
            c.execute(
                "INSERT INTO historial_entrenador (entrenador_id, club_id, inicio, fin) VALUES (?, ?, ?, ?)",
                (e[0], cl[0], inicio, fin)
            )

        conn.commit()
        conn.close()

    return render_template("add_historial_entrenador.html")


# ===========================
# TITULOS JUGADOR
# ===========================
@app.route("/titulo_jugador", methods=["GET", "POST"])
def titulo_jugador():
    if not session.get("admin"):
        return redirect("/login")

    if request.method == "POST":
        jugador = request.form["jugador"]
        titulo = request.form["titulo"]

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        c.execute("SELECT id FROM jugadores WHERE nombre = ?", (jugador,))
        j = c.fetchone()
        c.execute("SELECT id FROM titulos WHERE nombre = ?", (titulo,))
        t = c.fetchone()

        if j and t:
            c.execute(
                "INSERT INTO titulos_jugador (jugador_id, titulo_id) VALUES (?, ?)",
                (j[0], t[0])
            )

        conn.commit()
        conn.close()

    return render_template("add_titulo_jugador.html")


# ===========================
# ADMIN JUGADORES
# ===========================
@app.route("/admin/jugadores")
def admin_jugadores():
    if not session.get("admin"):
        return redirect("/login")

    jugadores = query_db("SELECT * FROM jugadores ORDER BY nombre")
    return render_template("admin_jugadores.html", jugadores=jugadores)


@app.route("/admin/jugadores/<int:jugador_id>")
def admin_jugador_detalle(jugador_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("SELECT * FROM jugadores WHERE id = ?", (jugador_id,))
    jugador = c.fetchone()

    c.execute("""
        SELECT c.nombre AS club, hj.inicio, hj.fin
        FROM historial_jugador hj
        JOIN clubes c ON hj.club_id = c.id
        WHERE hj.jugador_id = ?
        ORDER BY hj.inicio
    """, (jugador_id,))
    historial = c.fetchall()

    conn.close()

    return render_template(
        "admin_jugador_detalle.html",
        jugador=jugador,
        historial=historial
    )

# ===========================
# ADMIN CLUBES
# ===========================
@app.route("/admin/clubes")
def admin_clubes():
    if not session.get("admin"):
        return redirect("/login")

    clubes = query_db("SELECT * FROM clubes ORDER BY nombre")
    return render_template("admin_clubes.html", clubes=clubes)

@app.route("/admin/clubes/editar/<int:club_id>", methods=["GET", "POST"])
def editar_club(club_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    if request.method == "POST":
        nombre = request.form["nombre"]
        liga = request.form["liga"]

        c.execute(
            "UPDATE clubes SET nombre = ?, liga = ? WHERE id = ?",
            (nombre, liga, club_id)
        )
        conn.commit()
        conn.close()
        return redirect("/admin/clubes")

    c.execute("SELECT * FROM clubes WHERE id = ?", (club_id,))
    club = c.fetchone()
    conn.close()

    return render_template("edit_club.html", club=club)

@app.route("/admin/clubes/borrar/<int:club_id>")
def borrar_club(club_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # borrar relaciones primero
    c.execute("DELETE FROM historial_jugador WHERE club_id = ?", (club_id,))
    c.execute("DELETE FROM historial_entrenador WHERE club_id = ?", (club_id,))

    # borrar club
    c.execute("DELETE FROM clubes WHERE id = ?", (club_id,))

    conn.commit()
    conn.close()

    return redirect("/admin/clubes")

@app.route("/autocomplete/selecciones")
def autocomplete_selecciones():
    q = request.args.get("q", "")
    if not q:
        return jsonify([])

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT DISTINCT nacionalidad
        FROM jugadores
        WHERE nacionalidad LIKE ?
        ORDER BY nacionalidad
        LIMIT 10
    """, (q + "%",))
    resultados = [r[0] for r in c.fetchall()]
    conn.close()
    return jsonify(resultados)


# ===========================
# ARRANQUE
# ===========================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password")

        if password == "#Mickybite18Ngolonigger47pickcotton":
            session["admin"] = True
            return redirect("/")

        else:
            return "Clave incorrecta"

    return """
        <h2>Acceso administrador</h2>
        <form method="POST">
            <input type="password" name="password" placeholder="Clave">
            <button type="submit">Entrar</button>
        </form>
    """


if __name__ == "__main__":
    app.run(debug=True)


