from flask import render_template, request, redirect, url_for, abort, Blueprint, flash

from app.controllers.task_controller import get_task, check_flag, get_all_tasks
from app.controllers.team_controller import create_team, get_team_scores
from app.login_tools import login_required, get_base_data, login_user, logout_user
from app.views import task_map
view = Blueprint('view', __name__, static_folder='static', template_folder='templates')

task_map = task_map


@view.route('/')
def index():
    context = get_base_data()
    return render_template('index.html', **context)


@view.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        tname = request.form['name']
        flash(create_team(tname))
        login_user(tname)
        return redirect(url_for('view.index'))


@view.route('/tasks')
@login_required
def get_tasks():
    context = get_base_data()
    context.update(task_map=task_map)
    return render_template('tasks.html', **context)


@view.route('/task/<_id>', methods=['POST', 'GET'])
@login_required
def get_task_page(_id):
    context = get_base_data()
    task = get_task(_id)
    if task is False:
        abort(404)
    if request.method == 'GET':
        context.update(task)
        return render_template('task_page.html', **context)
    else:
        usr_flag = request.form['flag']
        message = check_flag(_id, context['t_id'], usr_flag)
        context = get_base_data()
        context.update(message=message)
        return render_template('message.html', **context)


@view.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('view.index'))


@view.route('/score')
def scoreboard():
    context = get_base_data()
    context.update(teams=get_team_scores())
    return render_template('scores.html', **context)


@view.route('/test')
@login_required
def test():
    get_team_scores()
    return "OK"
