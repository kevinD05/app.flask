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
        'select t.id, t.descripcion, u.username, t.completed, t.created_at'
        ' from todo t JOIN user u on t.created_by = u.id where t.created_by = %s order by created_at desc'
        (g,user['id'],)
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
                'values (%s, %s, %s)'
                (description, false, g.user['id'])  
            )    
            db.commit()
            return redirect(url_for('todo.index'))

    return render_template('todo/create.html')

def get_todo(id):
    db, c = get_db()
    c.execute(
        'select t.id, t.description, t.completed, t.created_by, t.created_at, u.username'
        'from todo t join user u on t.created_by = u.id where t.id = %s',
        (id,)
    )

    todo = c.fetchone()

    if todo is None:
        abort(404, 'el todo id {0} no existe'.format(id))

    return todo

@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_requierd 
def update(id):
    todo = get_todo(id)

    if request.method == 'post':
        description = request.form['descrition']
        completed = True is request.form.get('completed')
        error = None

        if not description:
            error = 'La descripcion es requerida.'

        if error is not None:
            flash(error)
        else:
            db, c = get_db()
            c.execute(
                'update todo set description = %s, completed = %s'
                ' where id  = %s and created_by =%s',
                (description, completed, id, g.user['id'])
            )
            db.commit()
            return redirect(url_for('todo.index'))

    return render_template('todo/update.html',todo=todo)

@bp.route('/<int:id>/delete', methods=['POST'])
@login_requierd 
def delete(id):
    db, c = get_db()
    c.execute('delete from todo where id = %s and created_by = %s', (id, g.user['id']))
    db.commit()
    return redirect(url_for('todo.index'))