from crypt import methods
from pydoc import describe
from flask import(
    blueprints, flash, g, redirect, render_template, request,url_for, description, false
)
from werkzeug.exceptions import abort
import todo
from todo.auth import login_requierd
from todo.db import get_db

bp = blueprints('todo',__name__)

@bp.route('/')
@login_requierd
def index():
    db, c = get_db()
    c.execute(
        'select t.id, t.descripcion, u.username, t.completed, t.created_at    from todo t JOIN user u on t.created_by = u.id order by created_at desc'
    )
    todos = c.fetchall()

    return render_template('todo/index.html', todos=todos)

@bp.route('/create', methods=['GET', 'POST'])
@login_requierd 
def create():
    if request.method == 'POST':
        description == request.form['description']
        error =  None
        if not description: 
            error = 'Descripcion es requerida'

        if error is not None:
            flash(error)
        else:
            db, c = get_db()
            c.execute(
                'insert into todo (descripcion, completed, created_by)'
                'values (%$, %$, %$)'
                (description, false, g.user['id'])  
            )    
            db.commit()
    return render_template('todo/create.html')

@bp.route('/update', methods=['GET', 'POST'])
@login_requierd 
def update():
    return ''