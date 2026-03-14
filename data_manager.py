from models import db, User, Movie


class DataManager:
    def create_user(self, name):
        user = User(name=name)
        db.session.add(user)
        db.session.commit()
        return user

    def get_users(self):
        return User.query.order_by(User.id).all()

    def get_movies(self, user_id):
        return Movie.query.filter_by(user_id=user_id).order_by(Movie.id).all()

    def add_movie(self, movie):
        db.session.add(movie)
        db.session.commit()
        return movie

    def update_movie(self, movie_id, new_title):
        movie = db.session.get(Movie, movie_id)
        if movie:
            movie.title = new_title
            db.session.commit()
        return movie

    def delete_movie(self, movie_id):
        movie = db.session.get(Movie, movie_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()
        return movie