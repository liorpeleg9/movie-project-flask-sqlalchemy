from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    movies = db.relationship(
        "Movie",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )


class Movie(db.Model):
    __tablename__ = "movie"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    year = db.Column(db.String(10))
    director = db.Column(db.String(120))
    poster_url = db.Column(db.String(300))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)