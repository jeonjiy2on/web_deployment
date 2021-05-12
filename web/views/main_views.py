
from flask import Blueprint, render_template, url_for
from werkzeug.utils import redirect

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/hello')
def hello_web():
    return 'Hello, WEB!'

@bp.route('/')
def intro():
    return render_template('intro.html')


@bp.route('/modellist')
def modellist():
    return redirect(url_for('model._list'))

