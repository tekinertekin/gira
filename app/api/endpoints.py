from flask import jsonify, request, url_for
from app import db
from app.api.errors import bad_request
from app.models import User, Project 
from app.api import bp
from app.api.auth import token_auth

@bp.route('/project/<string:title>', methods=['GET'])
@token_auth.login_required
def get_project(title):
    project = Project.query.filter_by(title=title)
    if project.count() > 0:
        return jsonify(Project.query.filter_by(title=title).first().to_dict())
    else:
        return bad_request(f'Project {title} does not exists at database')

@bp.route('/projects', methods=['GET'])
@token_auth.login_required
def get_projects():
    page = request.args.get('page', 1,type=int)
    per_page = min(request.args.get('per_page',10,type=int),100)
    data = Project.to_collection_dict(Project.query,page,per_page,'api.get_projects')
    return jsonify(data)
