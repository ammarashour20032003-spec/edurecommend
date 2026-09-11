from flask import Blueprint, request, jsonify
from app.models.content import Content
from app.models.content_tag import ContentTag
from app.models.tag import Tag
from app.utils.decorators import token_required

content_bp = Blueprint('content', __name__)

@content_bp.route('/', methods=['GET'])
@token_required
def get_all_content(user_id):
    field  = request.args.get('field')
    level  = request.args.get('level')
    type_  = request.args.get('type')

    query = Content.query

    if field:
        query = query.filter_by(field=field)
    if level:
        query = query.filter_by(level=level)
    if type_:
        query = query.filter_by(type=type_)

    contents = query.all()
    return jsonify({'content': [c.to_dict() for c in contents]}), 200


@content_bp.route('/<content_id>', methods=['GET'])
@token_required
def get_content(user_id, content_id):
    content = Content.query.get(content_id)

    if not content:
        return jsonify({'error': 'Content not found'}), 404

    return jsonify({'content': content.to_dict()}), 200


@content_bp.route('/search', methods=['GET'])
@token_required
def search_content(user_id):
    query_str = request.args.get('q', '')

    if not query_str:
        return jsonify({'error': 'Search query is required'}), 400

    results = Content.query.filter(
        Content.title.ilike(f'%{query_str}%')
    ).all()

    return jsonify({'results': [c.to_dict() for c in results]}), 200