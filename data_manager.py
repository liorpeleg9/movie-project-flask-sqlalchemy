"""Data access layer for working with users and movies."""

from models import db, User, Movie


class DataManager:
    """Handles database operations for users and movies."""

    def create_user(self, name):
        """Create a new user and save it to the database."""
        user = User(name=name)
        db.session.add(user)
        db.session.commit()
        return user

    def get_users(self):
        """Return all users ordered by their ID."""
        return User.query.order_by(User.id).all()

    def get_movies(self, user_id):
        """Return all movies for a given user ordered by their ID."""
        return Movie.query.filter_by(user_id=user_id).order_by(Movie.id).all()

    def add_movie(self, movie):
        """Add a movie object to the database."""
        db.session.add(movie)
        db.session.commit()
        return movie

    def update_movie(self, movie_id, new_title):
        """Update the title of a movie if it exists."""
        movie = db.session.get(Movie, movie_id)
        if movie:
            movie.title = new_title
            db.session.commit()
        return movie

    def delete_movie(self, movie_id):
        """Delete a movie from the database if it exists."""
        movie = db.session.get(Movie, movie_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()
        return movie