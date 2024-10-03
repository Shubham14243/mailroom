from flask import Blueprint, render_template

bp = Blueprint('ui', __name__)

@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
def index():
    return render_template('index.html')

@bp.route('/docs', methods=['GET'])
def docs():
    return render_template('docs.html')
