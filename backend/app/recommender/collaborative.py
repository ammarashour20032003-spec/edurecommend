import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from app import db
from app.models.interaction import Interaction
from app.models.content import Content

def get_collaborative_recommendations(user_id, top_n=10):
    try:
        interactions = Interaction.query.all()

        if not interactions:
            return []

        data = [{
            'user_id':    i.user_id,
            'content_id': i.content_id,
            'score':      _action_score(i.action, i.rating, i.duration_seconds)
        } for i in interactions]

        df = pd.DataFrame(data)

        df = df.groupby(['user_id', 'content_id'])['score'].sum().reset_index()

        matrix = df.pivot(index='user_id', columns='content_id', values='score').fillna(0)

        if user_id not in matrix.index:
            return []

        similarity = cosine_similarity(matrix)
        sim_df = pd.DataFrame(similarity, index=matrix.index, columns=matrix.index)

        similar_users = sim_df[user_id].drop(user_id).sort_values(ascending=False)

        user_seen = set(df[df['user_id'] == user_id]['content_id'].tolist())

        scored = {}
        for other_user, sim_score in similar_users.items():
            if sim_score <= 0:
                continue
            other_interactions = df[df['user_id'] == other_user]
            for _, row in other_interactions.iterrows():
                cid = row['content_id']
                if cid not in user_seen:
                    scored[cid] = scored.get(cid, 0) + sim_score * row['score']

        results = sorted(scored.items(), key=lambda x: x[1], reverse=True)[:top_n]

        recommendations = []
        for content_id, score in results:
            content = Content.query.get(content_id)
            if content:
                recommendations.append({
                    'content_id': content_id,
                    'score':      round(float(score), 4),
                    'algorithm':  'collaborative'
                })

        return recommendations

    except Exception as e:
        print(f"Collaborative filtering error: {e}")
        return []


def _action_score(action, rating, duration_seconds):
    score = 0
    if action == 'viewed':
        score += min((duration_seconds or 0) / 300, 3)
    elif action == 'liked':
        score += 3
    elif action == 'bookmarked':
        score += 4
    elif action == 'rated' and rating:
        score += rating
    return score