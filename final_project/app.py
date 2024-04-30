from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from helper import login_required
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/')
@login_required
def index():
    id = session['user_id']
    conn = sqlite3.connect('track.db')
    db = conn.cursor()
    db.execute('SELECT username FROM users WHERE id = ?',(id,))
    username = db.fetchall()

    exercises = ['squat','bench','deadlift']
    dates = []
    start_weight = []
    for i in exercises:
        db.execute('SELECT date FROM "{}" WHERE user_id = ?ORDER BY date DESC'.format(i.replace('"','""')), (id,) )
        dates.append(db.fetchone())
        db.execute('SELECT weight FROM "{}" WHERE user_id = ? ORDER BY date'.format(i.replace('"','""')), (id,) )
        start_weight.append(db.fetchone())
    db.execute('SELECT weight,date FROM squat WHERE user_id = ? AND weight = (SELECT MAX(weight) FROM squat WHERE user_id = ?)',(id,id))
    max_squat = db.fetchall()
    print(max_squat)
    db.execute('SELECT weight,date FROM bench WHERE user_id = ? AND weight = (SELECT MAX(weight) FROM bench WHERE user_id = ?)',(id,id))
    max_bench = db.fetchall()
    db.execute('SELECT weight,date FROM deadlift WHERE user_id = ? AND weight = (SELECT MAX(weight) FROM deadlift WHERE user_id = ?)',(id,id))
    max_deadlift = db.fetchall()
    return render_template('index.html', username = username[0][0], max_squat = max_squat, max_deadlift = max_deadlift, max_bench = max_bench, dates = dates, start_weight = start_weight)

@app.route("/login", methods = ["GET", "POST"])
def login():
    session.clear()
    if request.method == "GET":
        return render_template("login.html")
    else:
        conn = sqlite3.connect('track.db')
        db = conn.cursor()
        username = request.form.get('username')
        password = request.form.get('password')
        if not username:
            text = "Enter Valid Username"
            return render_template('apology.html', text = text)
        elif not password:
            text = "Enter Valid Password"
            return render_template('apology.html', text = text)
        else:
            db.execute("SELECT * FROM users WHERE username = ?",(username,))
            id = db.fetchall()

            if not id:
                return render_template('apology.html', text = 'Incorrect username / password')
            if not check_password_hash(id[0][2], password):
                return render_template('apology.html', text = 'Incorrect username / password')


            conn.commit()
            session["user_id"] = id[0][0]

            return redirect("/")



@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        conn = sqlite3.connect('track.db')
        db = conn.cursor()
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm_password')
        body_weight = request.form.get('body_weight')
        if (password != confirm):
            text = "Passwords do not match."
            return render_template('apology.html', text = text)

        elif not username:
            text = 'Enter valid username'
            return render_template('apology.html', text = text)

        elif not password:
            text = 'Enter valid password'
            return render_template('apology.html', text = text)

        elif not body_weight:
            text = 'Enter valid body weight'
            return render_template('apology.html', text = text)

        else:
            db.execute("SELECT * FROM users WHERE username = ?",(username,))
            id = db.fetchall()
            if len(id) != 0:
                text = "Username already in use"
                return render_template("apology.html", text = text)
            hash = generate_password_hash(password)
            db.execute('INSERT INTO users (username,hash,body_weight) VALUES (?,?,?)',(username,hash,body_weight))
            db.execute('SELECT id FROM users WHERE username = ?',(username,))
            id = db.fetchall()
            conn.commit()
            return redirect('/login')


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route('/pr', methods = ["GET","POST"])
def pr():
    conn = sqlite3.connect('track.db')
    db = conn.cursor()
    id = session['user_id']
    if request.method == "GET":
        db.execute('SELECT * FROM squat WHERE user_id = ? ORDER BY date DESC', (id,))
        squat = db.fetchall()
        db.execute('SELECT * FROM bench WHERE user_id = ? ORDER BY date DESC', (id,))
        bench = db.fetchall()
        db.execute('SELECT * FROM deadlift WHERE user_id = ? ORDER BY date DESC', (id,))
        deadlift = db.fetchall()
        db.execute('SELECT weight,date FROM squat WHERE user_id = ? AND weight = (SELECT MAX(weight) FROM squat WHERE user_id = ?)',(id,id))
        max_squat = db.fetchall()
        db.execute('SELECT weight,date FROM bench WHERE user_id = ? AND weight = (SELECT MAX(weight) FROM bench WHERE user_id = ?)',(id,id))
        max_bench = db.fetchall()
        db.execute('SELECT weight,date FROM deadlift WHERE user_id = ? AND weight = (SELECT MAX(weight) FROM deadlift WHERE user_id = ?)',(id,id))
        max_deadlift = db.fetchall()
        return render_template('pr.html', squat = squat, max_squat = max_squat, bench = bench, deadlift=deadlift, max_bench = max_bench, max_deadlift = max_deadlift)

    if request.method == "POST":
        exercise = request.form.get('select_pr')
        weight = request.form.get('weight')
        date = request.form.get('date')
        try:
            weight = int(weight)
        except ValueError:
            return render_template('apology.html', text = 'Enter Valid Weight')
        if weight < 1:
            return render_template('apology.html', text = 'Enter Valid Weight')
        try:
            db.execute('INSERT INTO "{}" (user_id,weight,date) VALUES (?,?,?)'.format(exercise.replace('"', '""')), (id,weight,date))
        except AttributeError:
            return render_template("apology.html", text = "Choose an exercise")
        conn.commit()
        return redirect('/pr')


@app.route("/delete", methods = ["GET","POST"])
def delete():
    conn = sqlite3.connect('track.db')
    db = conn.cursor()
    if request.method == "POST":
        squat = request.form.get('squat_button')
        db.execute('DELETE FROM squat WHERE date = ?',(squat,))
        bench = request.form.get('bench_button')
        db.execute('DELETE FROM bench WHERE date = ?',(bench,))
        deadlift = request.form.get('deadlift_button')
        db.execute('DELETE FROM deadlift WHERE date = ?',(deadlift,))
        conn.commit()
        return redirect("/pr")
    else:
        return redirect("/pr")

