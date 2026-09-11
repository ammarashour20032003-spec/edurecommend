from google import genai
import json
import uuid
from app import db
from app.models.content import Content
from app.config import Config

client = genai.Client(Config.API_KEY)

def fetch_and_save_content(specialization, level):
    try:
        prompt = f"""
Find 10 real educational resources about {specialization} for {level} level learners.
Return ONLY a JSON array with no extra text, no markdown, no code blocks.
Each item must have exactly these fields:
- title: the resource title
- type: one of "course", "video", or "article"
- url: the real URL
- field: "{specialization}"
- level: "{level}"

Example format:
[{{"title":"Example","type":"course","url":"https://example.com","field":"{specialization}","level":"{level}"}}]
"""

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        text = response.text.strip()

        if text.startswith('```'):
            text = text.split('```')[1]
            if text.startswith('json'):
                text = text[4:]
        text = text.strip()

        resources = json.loads(text)

        saved = 0
        for r in resources:
            existing = Content.query.filter_by(url=r.get('url', '')).first()
            if existing:
                continue

            content = Content(
                id    = str(uuid.uuid4()),
                title = r.get('title', 'Untitled'),
                type  = r.get('type', 'article') if r.get('type') in ['course', 'video', 'article'] else 'article',
                url   = r.get('url', ''),
                field = r.get('field', specialization),
                level = r.get('level', level) if r.get('level') in ['beginner', 'intermediate', 'advanced'] else level,
                avg_rating = 0
            )
            db.session.add(content)
            saved += 1

        db.session.commit()
        print(f"Fetched and saved {saved} new content items for {specialization} ({level})")
        return saved

    except Exception as e:
        print(f"Gemini fetch error: {e}")
        db.session.rollback()
        return 0