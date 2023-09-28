from flask import Flask, render_template, request, redirect, url_for, session
from psycopg2.extras import RealDictCursor
import psycopg2
import os
import re
from app import app, conn, cur


@app.route('/')
def homepage():
    if session.get('loggedin'):
        return render_template('homepage.html')
    else:
        return redirect(url_for('login'))

@app.route('/catalog')
def catalog():
    if session.get('loggedin'):
        cur.execute('SELECT * FROM books;')
        books = cur.fetchall()
        return render_template('catalog.html', books=books)
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = request.args.get('msg') 
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
            account = cursor.fetchone()
            if account:
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['username']
                session['roles'] = account['roles'] 
                msg = 'Logged in successfully!'
                return redirect(url_for('homepage'))
            else:
                msg = 'Incorrect username / password!'
    return render_template('login.html', msg=msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'roles' in request.form:
        username = request.form['username']
        password = request.form['password']
        roles = int(request.form['roles'])
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
            account = cursor.fetchone()
            # This part must be corrected ! Some works, some don't
            if account:
                msg = 'Account already exists!'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Username must contain only characters and numbers!'
            elif not username or not password or not roles:
                msg = 'Please fill out the form!'
            else:
                cursor.execute('INSERT INTO users (username, password, roles) VALUES (%s, %s, %s)', (username, password, roles))
                conn.commit()
                return redirect(url_for('login', msg="You've been successfully registered!"))
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)