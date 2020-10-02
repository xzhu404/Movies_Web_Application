from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

import movies.adapters.repository as repo
import movies.utilities.utilities as utilities
import movies.movies.services as services

from movies.utilities.services import get_genre_names

movies_blueprint = Blueprint(
    'movies_bp', __name__)


@movies_blueprint.route('/details/<int:id>/', methods=['GET'])
def get_movie_by_id(id):
    username = session.get('username')

    filter_form = utilities.FilterForm()
    sign_up_form = utilities.RegistrationForm()
    login_form = utilities.LoginForm()

    movie = services.get_movie(id, repo.repo_instance)
    genres = get_genre_names(repo.repo_instance)
    selected_movies = utilities.get_selected_movies()
    return render_template(
        "details.html",
        movie=movie,
        genres=genres,
        selected_movies=selected_movies,
        filter_form=filter_form,
        sign_up_form=sign_up_form,
        login_form=login_form,
        username=username,
    )


@movies_blueprint.route('/filter_movies', methods=['GET', 'POST'])
def filter_movies():
    username = session.get('username')

    filter_form = utilities.FilterForm()
    sign_up_form = utilities.RegistrationForm()
    login_form = utilities.LoginForm()

    if filter_form.validate_on_submit():
        return redirect(url_for("movies_bp.filter_movies", genre=filter_form.genre.data, actor=filter_form.actor.data,
                                director=filter_form.director.data))

    movies_per_page = 4
    cursor = request.args.get("cursor", 0)
    cursor = int(cursor)

    selected_movies = utilities.get_selected_movies()

    genre_name = request.args.get("genre", '')
    actor_name = request.args.get("actor", '')
    director_name = request.args.get("director", '')

    movie_ids = services.filter_movies(actor_name, director_name, genre_name, repo.repo_instance)
    movies = services.get_movies_by_id(movie_ids[cursor: cursor + movies_per_page], repo.repo_instance)
    genres = get_genre_names(repo.repo_instance)

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if cursor > 0:
        prev_movie_url = url_for("movies_bp.filter_movies", cursor=cursor - movies_per_page, genre=genre_name.lower(),
                                 actor=actor_name.lower(), director=director_name.lower())
        first_movie_url = url_for("movies_bp.filter_movies")
    if cursor + movies_per_page < len(movie_ids):
        next_movie_url = url_for("movies_bp.filter_movies", cursor=cursor + movies_per_page, genre=genre_name.lower(),
                                 actor=actor_name.lower(), director=director_name.lower())
        last_cursor = movies_per_page * int(len(movie_ids) / movies_per_page)
        if len(movie_ids) % movies_per_page == 0:
            last_cursor -= movies_per_page
        last_movie_url = url_for("movies_bp.filter_movies", cursor=last_cursor, genre=genre_name.lower(),
                                 actor=actor_name.lower(), director=director_name.lower())

    return render_template(
        'home.html',
        movies=movies,
        genres=genres,
        selected_movies=selected_movies,
        first_movie_url=first_movie_url,
        last_movie_url=last_movie_url,
        next_movie_url=next_movie_url,
        prev_movie_url=prev_movie_url,
        filter_form=filter_form,
        sign_up_form=sign_up_form,
        login_form=login_form,
        username=username,
    )
