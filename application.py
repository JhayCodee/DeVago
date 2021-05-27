from cs50 import SQL
from Flask import flask
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///devago.db")


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
        confirmar = db.execute("SELECT FROM user WHERE nombre=:username",
                                username=request.form.get("username"))
        if confirmar:
            return apology("Usuario Existente")

        # Inserta el usario en la tabla.
        insertar = db.execute("INSERT INTO user (nombre, contraseña) VALUES(:username, :pass)",\
                                username=request.form.get("username"), hash=passhash)

        #peticion del nombre de usuario
        rows1 = db.execute("SELECT nombre FROM user WHERE nombre=:username",
                                username=request.form.get("username"))

        flash("Bienvenido!")
        return render_template("login.html")

    else:
        return render_template("register.html")

