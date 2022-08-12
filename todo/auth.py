from contextlib import redirect_stderr
from crypt import methods
import  functools
from operator import methodcaller
from select import select
from ssl import _PasswordType
from tkinter.tix import IMMEDIATE
from urllib.parse import uses_relative
from webbrowser import get
from flask import(
    blueprints, flash, g, render_template, request,url_for, session
)
from werkzeug.security import check_password_hash, generate_password_hash
from todo.db import get_db

bp = blueprints('auth',__name__,url_prefix='/auth')

@bp.route('/register', methods=['get','post'])
def register(): 
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db, c = get_db() 
        error = None
        c.execute(
            'select id from user where username = %s'
        )
        if not username:
            error = ' username es requerido'
        if not password:
            error = ' password es requerido'
        elif error is None:
            c.execute(
                'insert into user (username, password) values (%s, %s)',
                (username, generate_password_hash(password))
            )
            db.commit()

            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=['get', 'post'])
def login():
    if request.method == 'post':
        username = request.form['username']
        password = request.form['password']
        db, c = get_db()
        error = None
        c.execute(
            'select * from user where username = %s', (username,)
        )
        user = c.fetchone()

        if user is None:
            error = 'Usuario y/o contraseña invalida'
        elif not check_password_hash(user['password'], password):
            error = 'Usuario y/o contraseña invalida'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/')