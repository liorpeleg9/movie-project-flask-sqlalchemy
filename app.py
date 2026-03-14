import os
import requests

from flask import Flask, render_template, request, redirect, url_for, abort
from data_manager import DataManager
from models import db, User, Movie

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

data_manager = DataManager()


def fetch_movie_data(title):
    api_key = os.getenv("OMDB_API_KEY")

    if not api_key:
        return {
            "title": title,
            "year": "",
            "director": "",
            "poster_url": ""
        }

    try:
        response = requests.get(
            "http://www.omdbapi.com/",
            params={"apikey": api_key, "t": title},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        if data.get("Response") == "True":
            poster = data.get("Poster", "")
            if poster == "N/A":
                poster = ""

            return {
                "title": data.get("Title", title),
                "year": data.get("Year", ""),
                "director": data.get("Director", ""),
                "poster_url": poster
            }

    except requests.RequestException:
        pass

    return {
        "title": title,
        "year": "",
        "director": "",
        "poster_url": ""
    }


@app.route("/")
def home():
    users = data_manager.get_users()
    return render_template("index.html", users=users)


@app.route("/users", methods=["POST"])
def create_user():
    name = request.form.get("name", "").strip()
    if name:
        data_manager.create_user(name)
    return redirect(url_for("home"))


@app.route("/users/<int:user_id>/movies", methods=["GET"])
def user_movies(user_id):
    user = db.session.get(User, user_id)
    if not user:
        abort(404)

    movies = data_manager.get_movies(user_id)
    return render_template("movies.html", user=user, movies=movies)


@app.route("/users/<int:user_id>/movies", methods=["POST"])
def add_movie(user_id):
    user = db.session.get(User, user_id)
    if not user:
        abort(404)

    title = request.form.get("title", "").strip()
    if title:
        movie_data = fetch_movie_data(title)

        movie = Movie(
            title=movie_data["title"],
            year=movie_data["year"],
            director=movie_data["director"],
            poster_url=movie_data["poster_url"],
            user_id=user.id
        )
        data_manager.add_movie(movie)

    return redirect(url_for("user_movies", user_id=user_id))


@app.route("/users/<int:user_id>/movies/<int:movie_id>/update", methods=["POST"])
def update_movie(user_id, movie_id):
    user = db.session.get(User, user_id)
    movie = db.session.get(Movie, movie_id)

    if not user or not movie or movie.user_id != user_id:
        abort(404)

    new_title = request.form.get("new_title", "").strip()
    if new_title:
        data_manager.update_movie(movie_id, new_title)

    return redirect(url_for("user_movies", user_id=user_id))


@app.route("/users/<int:user_id>/movies/<int:movie_id>/delete", methods=["POST"])
def delete_movie(user_id, movie_id):
    user = db.session.get(User, user_id)
    movie = db.session.get(Movie, movie_id)

    if not user or not movie or movie.user_id != user_id:
        abort(404)

    data_manager.delete_movie(movie_id)
    return redirect(url_for("user_movies", user_id=user_id))


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
    

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)