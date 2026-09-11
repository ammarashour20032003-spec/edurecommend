from app import db
from app.models.recommendation import Recommendation
from app.recommender.collaborative import get_collaborative_recommendations
from app.recommender.content_based import get_content_based_recommendations

COLLABORATIVE_WEIGHT = 0.6
CONTENT_BASED_WEIGHT = 0.4

def generate_recommendations(user_id, top_n=10):
    try:
        collaborative = get_collaborative_recommendations(user_id, top_n)
        content_based = get_content_based_recommendations(user_id, top_n)

        collab_scores = {r['content_id']: r['score'] for r in collaborative}
        content_scores = {r['content_id']: r['score'] for r in content_based}

        all_content_ids = set(collab_scores.keys()) | set(content_scores.keys())

        if not all_content_ids:
            return []

        hybrid_scores = {}
        for content_id in all_content_ids:
            c_score = collab_scores.get(content_id, 0)
            cb_score = content_scores.get(content_id, 0)
            hybrid_scores[content_id] = (
                COLLABORATIVE_WEIGHT * c_score +
                CONTENT_BASED_WEIGHT * cb_score
            )

        max_score = max(hybrid_scores.values()) if hybrid_scores else 1
        for cid in hybrid_scores:
            hybrid_scores[cid] = round(hybrid_scores[cid] / max_score, 4)

        sorted_recs = sorted(
            hybrid_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )[:top_n]

        Recommendation.query.filter_by(user_id=user_id).delete()
        db.session.commit()

        saved = []
        for content_id, score in sorted_recs:
            if content_id in collab_scores and content_id in content_scores:
                algorithm = 'hybrid'
            elif content_id in collab_scores:
                algorithm = 'collaborative'
            else:
                algorithm = 'content_based'

            rec = Recommendation(
                user_id    = user_id,
                content_id = content_id,
                score      = score,
                algorithm  = algorithm,
                clicked    = False
            )
            db.session.add(rec)
            saved.append({
                'content_id': content_id,
                'score':      score,
                'algorithm':  algorithm
            })

        db.session.commit()
        return saved

    except Exception as e:
        print(f"Engine error: {e}")
        db.session.rollback()
        return []