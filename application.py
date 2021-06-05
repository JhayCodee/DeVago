from cs50 import SQL
from flask import Flask, redirect, render_template, request, session, flash
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from tempfile import mkdtemp
from flask_session import Session
from helpers import apology, login_required

# Configure application
app = Flask(__name__)
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///devago.db")

global_opc = []

@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/map")
@login_required
def map():
    return render_template("map.html")


@app.route("/lugares", methods=["GET", "POST"])
@login_required
def Lugares():

    rows = db.execute('SELECT * FROM lugares')
    return render_template("lugares.html", rows=rows)


@app.route("/hoteles", methods=["GET", "POST"])
@login_required
def Hoteles():

    rows = db.execute('SELECT * FROM hoteles')
    return render_template("hoteles.html", rows=rows)


@app.route("/ofertas", methods=["GET", "POST"])
@login_required
def Buscar():

    rows = db.execute('SELECT * FROM ofertas')
    return render_template("ofertas.html", rows=rows)


@app.route("/editar", methods=["GET", "POST"])
@login_required
def Editar():

    if request.method == "POST":

        ruta = request.form.get("ruta")

        if not ruta:
            return apology("seleccione una opcion")

        if ruta == "Hoteles":

            opc = "hoteles"
            rows = db.execute("SELECT * FROM hoteles")
            return render_template("editar2.html", rows=rows, opc1=opc)

        if ruta == "Lugares":
            opc = "lugares"
            rows = db.execute("SELECT * FROM lugares")
            return render_template("editar2.html", rows=rows, opc1=opc)

        if ruta == "Ofertas":
            opc = "ofertas"
            rows = db.execute("SELECT * FROM ofertas")
            return render_template("editar2.html", rows=rows, opc1=opc)


    else:
        return render_template("editar.html")


@app.route("/editar2/<opc1>", methods=["GET", "POST"])
@login_required
def Editar2(opc1):

    if request.method == "POST":

        nombre = request.form.get("nombre")
        departamento = request.form.get("departamento")
        descripcion= request.form.get("descripcion")
        precio = request.form.get("precio")
        url= request.form.get("url")
        opc = request.form.get("opc")


        if not nombre:
            return apology("Espacio en blanco")
        if not departamento:
            return apology("Espacio en blanco")
        if not descripcion:
            return apology("Espacio en blanco")
        if not precio:
            return apology("Espacio en blanco")
        if not url:
            return apology("Espacio en blanco")
        if not opc:
            return apology("Espacio en blanco")

        #aactualizar hoteles
        if opc1 == "hoteles":

            idd = db.execute("SELECT * FROM hoteles WHERE nombre = :name", name=opc)
            hid= idd[0]["idhotel"]

            act = db.execute("""
                            UPDATE hoteles SET nombre=:nombre, departamento=:departamento,
                            descripcion=:descripcion, precio=:precio, urlimage=:url
                            WHERE idhotel=:idd
                            """,
                            nombre=nombre, departamento=departamento, descripcion=descripcion,
                            precio=precio, url=url, idd=hid)

            rows = db.execute("select * from hoteles")
            return render_template("hoteles.html", rows=rows)


        #aactualizar lugares
        if opc1 == "lugares":

            idd = db.execute("SELECT * FROM lugares WHERE nombre = :name", name=opc)
            hid= idd[0]["idlugar"]

            act = db.execute("""
                            UPDATE lugares SET nombre=:nombre, departamento=:departamento,
                            descripcion=:descripcion, precio=:precio, urlimage=:url
                            WHERE idlugar=:idd
                            """,
                            nombre=nombre, departamento=departamento, descripcion=descripcion,
                            precio=precio, url=url, idd=hid)

            rows = db.execute("select * from lugares")
            return render_template("lugares.html", rows=rows)


        #aactualizar lugares
        if opc1 == "ofertas":

            idd = db.execute("SELECT * FROM ofertas WHERE nombre = :name", name=opc)
            hid= idd[0]["id"]

            act = db.execute("""
                            UPDATE lugares SET nombre=:nombre, departamento=:departamento,
                            descripcion=:descripcion, precio=:precio, urlimage=:url
                            WHERE id=:idd
                            """,
                            nombre=nombre, departamento=departamento, descripcion=descripcion,
                            precio=precio, url=url, idd=hid)

            rows = db.execute("select * from ofertas")
            return render_template("ofertas.html", rows=rows)





        return render_template("editar2.html")

    else:
        return render_template("editar2.html")



@app.route("/add", methods=["GET", "POST"])
@login_required
def add():

    if request.method == "POST":

        nombre = request.form.get("nombre")
        departamento = request.form.get("departamento")
        descripcion= request.form.get("descripcion")
        precio = request.form.get("precio")
        url= request.form.get("url")
        ruta = request.form.get("ruta")

        if not nombre:
            return apology("Espacio en blanco")
        if not departamento:
            return apology("Espacio en blanco")
        if not descripcion:
            return apology("Espacio en blanco")
        if not precio:
            return apology("Espacio en blanco")
        if not url:
            return apology("Espacio en blanco")
        if not ruta:
            return apology("Espacio en blanco")


        if ruta == "Hoteles":

            insertar = db.execute('''
                            INSERT INTO hoteles
                            (nombre, departamento, descripcion, precio, urlimage)
                            VALUES(:nombre, :departamento, :descripcion, :precio, :urlimage)
                            ''',
                            nombre=nombre, departamento=departamento, descripcion=descripcion,
                            precio=precio, urlimage=url)


        rows = db.execute('SELECT * FROM hoteles')
        return render_template("hoteles.html", rows=rows)

    else:
        return render_template("add.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    """Register user"""
    if request.method == "POST":

        # Comprueba que se hayan llenado los campos
        username = request.form.get("username")
        if not username:
            return apology("username")

        password = request.form.get("password")
        if not password:
            return apology("password")

        confirmacion = request.form.get("confirmation")

        if password != confirmacion:
            return apology("No coinciden")

        # encripta la  contraseña
        passhash = generate_password_hash(password)

        #confirmamos que no se haya registrado un usuario con el mismo nombre
        confirmar = db.execute("SELECT nombre FROM user WHERE nombre=:username",
                                username=request.form.get("username"))
        if confirmar:
            return apology("Usuario Existente")

        # Inserta el usario en la tabla.
        insertar = db.execute("INSERT INTO user (nombre, contraseña) VALUES(:username, :hash)",\
                                username=request.form.get("username"), hash=passhash)

        #peticion del nombre de usuario
        rows1 = db.execute("SELECT nombre FROM user WHERE nombre=:username",
                                username=request.form.get("username"))
        flash("¡Bienvenido!")
        return redirect("/")

    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    #olvida sesion
    session.clear()

    if request.method == "POST":

        if not request.form.get("username"):
            return apology("must provide username", 403)

        elif not request.form.get("password"):
            return apology("must provide password", 403)

        elif not request.form.get("ruta"):
            return apology("debe escoger un tipo de usuario", 403)

        ruta = request.form.get("ruta")

        if ruta == "Admin":
            #Peticion de Usuario
            rows = db.execute("SELECT * FROM user WHERE nombre = :username",
                              username=request.form.get("username"))

            # verifica que sea correcta la info
            if len(rows) != 1 or not check_password_hash(rows[0]["contraseña"], request.form.get("password")):
                return apology("invalid username and/or password", 403)

            if rows[0]["categoria"] != "Admin":
                return apology("Usted no es admin")

            # Rcuerda la sesion
            session["admin"] = rows[0]["idusuario"]


        #Peticion de Usuario
        rows = db.execute("SELECT * FROM user WHERE nombre = :username",
                          username=request.form.get("username"))

        # verifica que sea correcta la info
        if len(rows) != 1 or not check_password_hash(rows[0]["contraseña"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Rcuerda la sesion
        session["user_id"] = rows[0]["idusuario"]

        # Redirect user to home page
        return render_template("index.html")

    
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")