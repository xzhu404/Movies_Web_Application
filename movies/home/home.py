from flask import Blueprint, render_template, request, url_for, session
import movies.adapters.repository as repo
import movies.utilities.utilities as utilities
import movies.utilities.services as services
from movies.movies.services import get_movies_by_id, get_all_movie_ids

home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    username = session.get('username')

    movies_per_page = 4
    cursor = request.args.get("cursor", 0, type=int)

    filter_form = utilities.FilterForm()
    sign_up_form = utilities.RegistrationForm()
    login_form = utilities.LoginForm()

    selected_movies = utilities.get_selected_movies()

    movie_ids = get_all_movie_ids(repo.repo_instance)
    movies = get_movies_by_id(movie_ids[cursor: cursor + movies_per_page], repo.repo_instance)
    genres = services.get_genre_names(repo.repo_instance)

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if cursor > 0:
        prev_movie_url = url_for("home_bp.home", cursor=cursor - movies_per_page)
        first_movie_url = url_for("home_bp.home")
    if cursor + movies_per_page < len(movie_ids):
        next_movie_url = url_for("home_bp.home", cursor=cursor + movies_per_page)
        last_cursor = movies_per_page * int(len(movie_ids) / movies_per_page)
        if len(movie_ids) % movies_per_page == 0:
            last_cursor -= movies_per_page
        last_movie_url = url_for("home_bp.home", cursor=last_cursor)

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
