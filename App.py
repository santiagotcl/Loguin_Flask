from flask import Flask, render_template, request, url_for, redirect, flash, session, escape
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app=Flask(__name__)

##MYSQL conexion
#app.config["MYSQL_HOST"] = "localhost"
#app.config["MYSQL_USER"] = "root"
#app.config["MYSQL_PASSWORD"] = "password"
#app.config["MYSQL_DB"] = "bbddlub" #le pido que se conecte a la base de datos prueba flask
##cuando pongo el puerto no anda


#get envia las peticiones a travez de la barra de direcciones, post no.
#iniciamos sesion(guarda datos en una memoria para luego usarlos)
app.secret_key="mysecretkey"

#en templates guardo todo lo que se ve

suma=[]#memoria interna de articulos seleccionados
total=0.0#total en pesos de la compra

#hashed_pw = generate_password_hash("1995",method="sha256")
#mysql.execute("INSERT INTO usuarios (username,password,permiso) VALUES (?,?,?)", 
#        ("scuozzo",hashed_pw,"1"))
#mysql.commit()

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/Ingreso", methods= ["POST"])
def Ingreso():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        mysql = sqlite3.connect("./Proyecto.db")
        cur=mysql.cursor()
        cur.execute("SELECT * FROM usuarios WHERE username =?",(username,))
        data = cur.fetchall()
        if len(data) == 0 :
            flash("Usuario inexistente, verifique y vuelva a intentar.")
            return render_template("index.html")
        else:
            data=list(data[0])
            print(data[1])
            if data[1] == username and check_password_hash(data[2], password):
                session["username"] = username #creo la cookie username y le agrego el valor del nombre de usuario, esto lo hago para verificar que el usuario este logueado y no entre a las paginas por url
                return render_template("buscar.html", session=session)
            else:
                flash("Contraseña INCORRECTA, verifique y vuelva a intentar.")
                return render_template("index.html")


##########################################################################
#######################REGISTRO DE NUEVO USUARIO##########################
##########################################################################

@app.route("/Registro", methods=["POST"])
def Registro():
    if request.method == "POST":
        return render_template("registro.html")



@app.route("/Registro_usuario", methods= ["POST"])
def Registro_usuario():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_pw = generate_password_hash(password,method="sha256")
        mysql = sqlite3.connect("./Proyecto.db")
        mysql.execute("INSERT INTO usuarios (username,password,permiso) VALUES (?,?,?)", 
                (username,hashed_pw,"5"))
        mysql.commit()
        flash("Usuario Registrado")
        return render_template("index.html")




    
if __name__ == "__main__":
    app.run(port = 3000, debug = True) #hacemos que se refresque solo
