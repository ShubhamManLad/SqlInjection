from flask import Flask, request, render_template
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

@app.route("/create")
def create():
    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    sql_command = """CREATE TABLE sqlinjectionUsers ( 
    username VARCHAR(20), 
    password VARCHAR(30));"""
    c.execute(sql_command)
    conn.commit()
    return "Database Created"

@app.route("/add")
def add():
    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    sql_command = """INSERT INTO sqlinjectionUsers VALUES( 
    'user2', 
    'password2');"""
    c.execute(sql_command)
    conn.commit()
    return "Data added"

@app.route("/get")
def get():
    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    c.execute("select * from sqlinjectionUsers")
    data = c.fetchall()
    return "<br>".join([i[0] for i in data])

@app.route("/delete")
def delete():
    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    c.execute("delete from sqlinjectionUsers WHERE username = 'user1'")
    # data = c.fetchall()
    # return "<br>".join([i[0] for i in data]).join("<br>").join([i[1] for i in data])
    return "Deleted"


@app.route("/register")
def register():
    code = request.args.get('code')
    password = request.args.get('password')
    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO sqlinjectionUsers VALUES ('"+ code + "','" + password + "')")
        conn.commit()
        return f"Successfully added {code}"
    except sqlite3.Error as e:
        return str(e)


@app.route("/search")
def search():
    code = request.args.get('code')
    password = request.args.get('password')
    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    try:
        statement = "select * from sqlinjectionUsers where username='" + code + "'" + "and password='" + password + "'"
        c.execute(statement)
        found = c.fetchall()
        data = ""
        for str in found:
            data = data + str[0] +":" +str[1]+ "<br>"
        if found == []:
            return f"Invalid Code<br>{statement}"
        else:
            print(found)
            return f"Login Successful---<br>{data}"
    except sqlite3.Error as e:
        return str(e) + f"<br>{statement}"


@app.route("/login")
def login():
    return open("login.html").read()


@app.route("/")
def main():
    return open("403.html").read()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
