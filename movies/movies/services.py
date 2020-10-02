from typing import List, Iterable

from movies.adapters.repository import AbstractRepository
from movies.domain.model import make_comment, Movie, Comment, Genre, Actor, Director


class NonExistentMovieException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def add_comment(movie_id: int, comment_text: str, username: str, repo: AbstractRepository):
    # Check that the movies exists.
    movie = repo.get_movie(movie_id)
    if movie is None:
        raise NonExistentMovieException

    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    # Create comment.
    comment = make_comment(comment_text, user, movie)

    # Update the repository.
    repo.add_comment(comment)


def get_movie(movie_id: int, repo: AbstractRepository):
    movie = repo.get_movie(movie_id)

    if movie is None:
        raise NonExistentMovieException

    return movie_to_dict(movie)


def get_first_movie(repo: AbstractRepository):
    movie = repo.get_first_movie()

    return movie_to_dict(movie)


def get_last_movie(repo: AbstractRepository):
    movie = repo.get_last_movie()
    return movie_to_dict(movie)


def get_all_movie_ids(repo: AbstractRepository):
    movie_ids = repo.get_all_movie_ids()
    return movie_ids


def get_movie_ids_for_genre(genre_name, repo: AbstractRepository):
    movie_ids = repo.get_movie_ids_for_genre(genre_name)

    return movie_ids


def get_movies_by_id(id_list, repo: AbstractRepository):
    movies = repo.get_movies_by_id(id_list)

    movies_as_dict = movies_to_dict(movies)

    return movies_as_dict


def get_comments_for_movie(movie_id, repo: AbstractRepository):
    movie = repo.get_movie(movie_id)

    if movie is None:
        raise NonExistentMovieException

    return comments_to_dict(movie.comments)


def filter_movies(actor_name: str, director_name: str, genre_name: str, repo: AbstractRepository):
    movie_ids = repo.filter_movies(actor_name, director_name, genre_name)
    return movie_ids


# ============================================
# Functions to convert model entities to dicts
# ============================================

def movie_to_dict(movie: Movie):
    movie_dict = {
        'id': movie.id,
        'title': movie.title,
        'description': movie.description,
        'year': movie.year,
        'runtime': movie.runtime,
        'rating': movie.rating,
        'votes': movie.votes,
        'revenue': movie.revenue,
        'metascore': movie.metascore,
        "genres": genres_to_dict(movie.genres),
        'comments': comments_to_dict(movie.comments),
        'actors': actors_to_dict(movie.actors),
        'director': director_to_dict(movie.director)
    }
    return movie_dict


def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]


def comment_to_dict(comment: Comment):
    comment_dict = {
        'username': comment.user.username,
        'movie_id': comment.movie.id,
        'comment_text': comment.comment,
        'timestamp': comment.timestamp
    }
    return comment_dict


def comments_to_dict(comments: Iterable[Comment]):
    return [comment_to_dict(comment) for comment in comments]


def genre_to_dict(genre: Genre):
    genre_dict = {
        'name': genre.genre_name,
        'genre_movies': [movie.id for movie in genre.genre_movies]
    }
    return genre_dict


def genres_to_dict(genres: Iterable[Genre]):
    return [genre_to_dict(genre) for genre in genres]


def actor_to_dict(actor: Actor):
    actor_dict = {
        'name': actor.actor_name,
        'actor_movies': [movie.id for movie in actor.movies_starring_actor]
    }
    return actor_dict


def actors_to_dict(actors: Iterable[Actor]):
    return [actor_to_dict(actor) for actor in actors]


def director_to_dict(director: Director):
    director_dict = {
        'name': director.director_name,
        'director_movies': [movie.id for movie in director.movies_directed_by_director]
    }
    return director_dict


# ============================================
# Functions to convert dicts to model entities
# ============================================

def dict_to_article(dict):
    article = Movie(dict.id, dict.date, dict.title, dict.first_para, dict.hyperlink)
    # Note there's no comments or tags.
    return article
