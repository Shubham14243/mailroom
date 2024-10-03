from flask import Blueprint, jsonify, request
from mailer.controllers.admin_controller import AdminController

bp = Blueprint('admin', __name__)

@bp.route('/user/create', methods=['POST'])
def create():
    data = request.get_json()
    return AdminController.create(data)

@bp.route('/user/updatedomain', methods=['POST'])
def update_domain():
    data = request.get_json()
    return AdminController.update_domain(data)