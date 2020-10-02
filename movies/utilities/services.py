from typing import Iterable
import random

import movies.adapters.repository as repo
from movies.adapters.repository import AbstractRepository
from movies.domain.model import Movie
from movies.movies.services import genres_to_dict, actors_to_dict


def get_genre_names(repo: AbstractRepository):
    genres = repo.get_genres()
    genre_names = [genre.genre_name for genre in genres]

    return genre_names


def get_random_movies(quantity, repo: AbstractRepository):
    movie_count = repo.get_number_of_movies()

    if quantity >= movie_count:
        quantity = movie_count - 1

    random_ids = random.sample(range(1, movie_count), quantity)
    movies = repo.get_movies_by_id(random_ids)

    return movies_to_dict(movies)


# ============================================
# Functions to convert dicts to model entities
# ============================================

def movie_to_dict(movie: Movie):
    movie_dict = {
        "id": movie.id,
        "title": movie.title,
        "description": movie.description,
        "year": movie.year,
        "director": movie.director.director_name,
        "genres": genres_to_dict(movie.genres),
        "actors": actors_to_dict(movie.actors),
    }
    return movie_dict


def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]
