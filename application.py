from cs50 import SQL
from flask import Flask, redirect, render_template, request, session, flash
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///devago.db")

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/lugares", methods=["GET", "POST"])
@login_required
def Lugares():
    return render_template("lugares.html")


@app.route("/hoteles", methods=["GET", "POST"])
@login_required
def Hoteles():
    return render_template("hoteles.html")


@app.route("/buscar")
@login_required
def Buscar():
    return render_template("search.html")


@app.route("/about")
@login_required
def About():
    return render_template("about.html")

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():

    if request.method == "POST":

        nombre = request.form.get("nombre")
        departamento = request.form.get("departamento")
        descripcion= request.form.get("descripcion")
        precio = request.form.get("precio")
        url= request.form.get("url")

        # Inserta el usario en la tabla.
        insertar = db.execute('''
                            INSERT INTO hoteles
                            (nombre, departamento, descripcion, precio, urlimage)
                            VALUES(:nombre, :departamento, :descripcion, :precio, :urlimage)
                            ''',
                            nombre=nombre, departamento=departamento, descripcion=descripcion,
                            precio=precio, urlimage=url)

        row = db.execute('SELECT * FROM hoteles'
        render_template("hoteles.html", rows=row)

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

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM user WHERE nombre = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["contraseña"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["idusuario"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")