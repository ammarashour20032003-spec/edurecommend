from flask import Blueprint, request, jsonify
from app import db
from app.models.interaction import Interaction
from app.models.content import Content
from app.utils.decorators import token_required

interactions_bp = Blueprint('interactions', __name__)

@interactions_bp.route('/', methods=['POST'])
@token_required
def log_interaction(user_id):
    data = request.get_json()

    if not data or not data.get('content_id') or not data.get('action'):
        return jsonify({'error': 'content_id and action are required'}), 400

    content = Content.query.get(data['content_id'])
    if not content:
        return jsonify({'error': 'Content not found'}), 404

    valid_actions = ['viewed', 'liked', 'rated', 'bookmarked']
    if data['action'] not in valid_actions:
        return jsonify({'error': f'action must be one of {valid_actions}'}), 400

    if data['action'] == 'rated' and not data.get('rating'):
        return jsonify({'error': 'rating is required for rated action'}), 400

    interaction = Interaction(
        user_id          = user_id,
        content_id       = data['content_id'],
        action           = data['action'],
        rating           = data.get('rating'),
        duration_seconds = data.get('duration_seconds', 0)
    )

    db.session.add(interaction)
    db.session.commit()

    return jsonify({'message': 'Interaction logged', 'interaction': interaction.to_dict()}), 201


@interactions_bp.route('/', methods=['GET'])
@token_required
def get_user_interactions(user_id):
    interactions = Interaction.query.filter_by(user_id=user_id).all()
    return jsonify({'interactions': [i.to_dict() for i in interactions]}), 200