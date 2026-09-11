import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.models.interaction import Interaction
from app.models.content import Content

def get_content_based_recommendations(user_id, top_n=10):
    try:
        all_content = Content.query.all()

        if not all_content:
            return []

        content_data = [{
            'id':       c.id,
            'features': f"{c.field or ''} {c.level or ''} {c.type or ''} {c.title or ''}"
        } for c in all_content]

        df = pd.DataFrame(content_data)

        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(df['features'])

        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

        interactions = Interaction.query.filter_by(user_id=user_id).all()

        if not interactions:
            return []

        user_seen = set(i.content_id for i in interactions)

        liked_content = [
            i.content_id for i in interactions
            if i.action in ('liked', 'bookmarked', 'rated') and
               (i.rating is None or i.rating >= 3)
        ]

        if not liked_content:
            liked_content = list(user_seen)

        content_ids = df['id'].tolist()

        scored = {}
        for liked_id in liked_content:
            if liked_id not in content_ids:
                continue
            idx = content_ids.index(liked_id)
            sim_scores = list(enumerate(cosine_sim[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

            for i, score in sim_scores[1:]:
                cid = content_ids[i]
                if cid not in user_seen:
                    scored[cid] = max(scored.get(cid, 0), float(score))

        results = sorted(scored.items(), key=lambda x: x[1], reverse=True)[:top_n]

        recommendations = []
        for content_id, score in results:
            content = Content.query.get(content_id)
            if content:
                recommendations.append({
                    'content_id': content_id,
                    'score':      round(score, 4),
                    'algorithm':  'content_based'
                })

        return recommendations

    except Exception as e:
        print(f"Content-based filtering error: {e}")
        return []