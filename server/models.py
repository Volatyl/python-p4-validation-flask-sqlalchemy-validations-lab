from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = 'authors'
    # Add validations and constraints

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError('Name is required')
        return name

    @validates('phone_number')
    def validate_phone_number(self, key, number):
        if len(str(number)) != 10:
            raise ValueError('Number digits must be 10')
        return number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'


class Post(db.Model):
    __tablename__ = 'posts'
    # Add validations and constraints

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('title')
    def is_clickbait(self, key, title):
        clickbait_phrases = [
            "Why I love",
            "Secrets of",
            "You won't believe",
            "The truth about",
            "Shocking revelations about"
        ]
        for phrase in clickbait_phrases:
            if phrase in title:
                raise ValueError("Clickbait found")
        return title

    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Content can't be less than 250 characters")
        return content

    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) >= 250:
            raise ValueError("Summary too long")
        return summary

    @validates('category')
    def validate_category(self, key, category):
        valid_categories = ['Fiction', 'Non-Fiction']
        if category not in valid_categories:
            raise ValueError("Invalid category")
        return category

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
