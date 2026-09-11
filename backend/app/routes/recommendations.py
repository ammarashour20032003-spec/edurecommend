from flask import Blueprint, request, jsonify
from app import db
from app.models.recommendation import Recommendation
from app.models.content import Content
from app.models.interaction import Interaction
from app.models.user import User
from app.recommender.engine import generate_recommendations
from app.utils.decorators import token_required

recommendations_bp = Blueprint('recommendations', __name__)

@recommendations_bp.route('/', methods=['GET'])
@token_required
def get_recommendations(user_id):
    recommendations = Recommendation.query.filter_by(
        user_id=user_id
    ).order_by(
        Recommendation.score.desc()
    ).all()

    result = []
    for r in recommendations:
        content = Content.query.get(r.content_id)
        result.append({
            'recommendation_id': r.id,
            'score':             r.score,
            'algorithm':         r.algorithm,
            'clicked':           r.clicked,
            'saved':             r.saved,
            'content':           content.to_dict() if content else None
        })

    return jsonify({'recommendations': result}), 200


@recommendations_bp.route('/generate', methods=['POST'])
@token_required
def generate(user_id):
    interactions = Interaction.query.filter_by(user_id=user_id).all()

    if not interactions:
        user = User.query.get(user_id)
        specialization = user.specialization if user else None
        level = user.level if user else None

        query = Content.query
        if specialization:
            query = query.filter(Content.field.ilike(f'%{specialization}%'))
        if level:
            query = query.filter_by(level=level)

        content_list = query.limit(10).all()

        if not content_list and specialization:
            content_list = Content.query.filter(
                Content.field.ilike(f'%{specialization}%')
            ).limit(10).all()

        if not content_list:
            content_list = Content.query.limit(10).all()

        Recommendation.query.filter_by(user_id=user_id).delete()
        db.session.commit()

        saved = []
        for i, content in enumerate(content_list):
            score = round(1.0 - (i * 0.05), 4)
            rec = Recommendation(
                user_id    = user_id,
                content_id = content.id,
                score      = score,
                algorithm  = 'onboarding',
                clicked    = False,
                saved      = False
            )
            db.session.add(rec)
            saved.append({
                'content_id': content.id,
                'score':      score,
                'algorithm':  'onboarding'
            })

        db.session.commit()
        return jsonify({
            'message': f'{len(saved)} recommendations generated based on your profile',
            'recommendations': saved
        }), 200

    recs = generate_recommendations(user_id)

    if not recs:
        return jsonify({'message': 'Not enough data to generate recommendations'}), 200

    return jsonify({
        'message': f'{len(recs)} recommendations generated',
        'recommendations': recs
    }), 200


@recommendations_bp.route('/click/<recommendation_id>', methods=['POST'])
@token_required
def mark_clicked(user_id, recommendation_id):
    recommendation = Recommendation.query.filter_by(
        id=recommendation_id,
        user_id=user_id
    ).first()

    if not recommendation:
        return jsonify({'error': 'Recommendation not found'}), 404

    recommendation.clicked = True
    db.session.commit()

    return jsonify({'message': 'Marked as clicked', 'recommendation': recommendation.to_dict()}), 200


@recommendations_bp.route('/save/<recommendation_id>', methods=['POST'])
@token_required
def save_recommendation(user_id, recommendation_id):
    recommendation = Recommendation.query.filter_by(
        id=recommendation_id,
        user_id=user_id
    ).first()

    if not recommendation:
        return jsonify({'error': 'Recommendation not found'}), 404

    recommendation.saved = not recommendation.saved
    db.session.commit()

    return jsonify({
        'message': 'Saved' if recommendation.saved else 'Unsaved',
        'saved': recommendation.saved
    }), 200


@recommendations_bp.route('/save-content/<content_id>', methods=['POST'])
@token_required
def save_content(user_id, content_id):
    content = Content.query.get(content_id)
    if not content:
        return jsonify({'error': 'Content not found'}), 404

    existing = Recommendation.query.filter_by(
        user_id=user_id,
        content_id=content_id
    ).first()

    if existing:
        existing.saved = not existing.saved
        db.session.commit()
        return jsonify({
            'message': 'Saved' if existing.saved else 'Unsaved',
            'saved': existing.saved
        }), 200

    rec = Recommendation(
        user_id    = user_id,
        content_id = content_id,
        score      = 0,
        algorithm  = 'manual',
        clicked    = False,
        saved      = True
    )
    db.session.add(rec)
    db.session.commit()

    return jsonify({'message': 'Saved', 'saved': True}), 200


@recommendations_bp.route('/saved', methods=['GET'])
@token_required
def get_saved(user_id):
    saved = Recommendation.query.filter_by(
        user_id=user_id,
        saved=True
    ).all()

    result = []
    for r in saved:
        content = Content.query.get(r.content_id)
        result.append({
            'recommendation_id': r.id,
            'score':             r.score,
            'algorithm':         r.algorithm,
            'content':           content.to_dict() if content else None
        })

    return jsonify({'saved': result}), 200