import csv
import os
from datetime import datetime
from typing import List

from bisect import bisect_left, insort_left

from werkzeug.security import generate_password_hash

from movies.adapters.repository import AbstractRepository
from movies.domain.model import Movie, Genre, User, Comment, make_comment, Director, Actor, make_genre_association, \
    make_actor_association, make_director_association


class MemoryRepository(AbstractRepository):

    def __init__(self):
        self._movies: List[Movie] = list()
        self._movies_index = dict()
        self._genres: List[Genre] = list()
        self._actors: List[Genre] = list()
        self._directors: List[Genre] = list()
        self._users: List[User] = list()
        self._comments: List[Comment] = list()

    def add_user(self, user: User):
        self._users.append(user)

    def get_user(self, username) -> User:
        return next((user for user in self._users if user.username == username), None)

    def add_movie(self, movie: Movie):
        insort_left(self._movies, movie)
        self._movies_index[movie.id] = movie

    def get_movie(self, id: int) -> Movie:
        movie = None

        try:
            movie = self._movies_index[id]
        except KeyError:
            pass  # Ignore exception and return None.

        return movie

    def filter_movies(self, actor_name: str = "", director_name: str = "", genre_name: str = ""):
        movie_ids = list()
        for movie in self._movies:
            actor_names = [actor.actor_name.lower() for actor in movie.actors]
            genre_names = [genre.genre_name.lower() for genre in movie.genres]
            if (not actor_name or actor_name.lower() in actor_names) and (
                    not genre_name or genre_name.lower() in genre_names) and (
                    not director_name or director_name.lower() == movie.director.director_name.lower()):
                movie_ids.append(movie.id)
        return movie_ids

    def get_number_of_movies(self):
        return len(self._movies)

    def get_first_movie(self):
        movie = None

        if len(self._movies) > 0:
            movie = self._movies[-1]
        return movie

    def get_last_movie(self):
        movie = None

        if len(self._movies) > 0:
            movie = self._movies[0]
        return movie

    def get_movies_by_id(self, id_list):
        existing_ids = [id for id in id_list if id in self._movies_index]

        movies = [self._movies_index[id] for id in existing_ids]
        return movies

    def get_all_movie_ids(self):
        return [movie.id for movie in reversed(self._movies)]

    def get_movie_ids_for_genre(self, genre_name: str):
        genre = next((genre for genre in self._genres if genre.genre_name == genre_name), None)

        if genre is not None:
            movie_ids = [movie.id for movie in genre.genre_movies]
        else:
            movie_ids = list()

        return movie_ids

    def add_genre(self, genre: Genre):
        self._genres.append(genre)

    def add_actor(self, actor: Actor):
        self._actors.append(actor)

    def add_director(self, director: Director):
        self._directors.append(director)

    def get_genres(self) -> List[Genre]:
        return self._genres

    def add_comment(self, comment: Comment):
        super().add_comment(comment)
        self._comments.append(comment)

    def get_comments(self):
        return self._comments

    # Helper method to return movies index.
    def movie_index(self, movie: Movie):
        index = bisect_left(self._movies, movie)
        if index != len(self._movies) and self._movies[index].title == movie.title and self._movies[
            index].director == movie.director:
            return index
        raise ValueError


def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row


def load_movies_and_genres_and_actors_and_directors(data_path: str, repo: MemoryRepository):
    genres = dict()
    actors = dict()
    directors = dict()

    for data_row in read_csv_file(os.path.join(data_path, 'movies.csv')):

        movie_id = int(data_row[0])
        movie_genres = data_row[2].split(",")
        movie_director = data_row[4]
        movie_actors = data_row[5].replace(", ", ",").split(",")

        for genre in movie_genres:
            if genre not in genres.keys():
                genres[genre] = list()
            genres[genre].append(movie_id)

        for actor in movie_actors:
            if actor not in actors.keys():
                actors[actor] = list()
            actors[actor].append(movie_id)

        if movie_director not in directors.keys():
            directors[movie_director] = list()
        directors[movie_director].append(movie_id)

        if data_row[10] == "N/A":
            revenue = None
        else:
            revenue = float(data_row[10])

        if data_row[11] == "N/A":
            metascore = None
        else:
            metascore = int(data_row[11])

        movie = Movie(
            id=movie_id,
            title=data_row[1],
            description=data_row[3],
            year=int(data_row[6]),
            runtime=int(data_row[7]),
            rating=float(data_row[8]),
            votes=int(data_row[9]),
            revenue=revenue,
            metascore=metascore
        )

        repo.add_movie(movie)

    for genre_name in genres.keys():
        genre = Genre(genre_name)
        for movie_id in genres[genre_name]:
            movie = repo.get_movie(movie_id)
            make_genre_association(movie, genre)
        repo.add_genre(genre)

    for actor_name in actors.keys():
        actor = Actor(actor_name)
        for movie_id in actors[actor_name]:
            movie = repo.get_movie(movie_id)
            make_actor_association(movie, actor)
        repo.add_actor(actor)

    for director_name in directors.keys():
        director = Director(director_name)
        for movie_id in directors[director_name]:
            movie = repo.get_movie(movie_id)
            make_director_association(movie, director)
        repo.add_director(director)


def load_users(data_path: str, repo: MemoryRepository):
    users = dict()

    for data_row in read_csv_file(os.path.join(data_path, 'users.csv')):
        user = User(
            username=data_row[1],
            password=generate_password_hash(data_row[2])
        )
        repo.add_user(user)
        users[data_row[0]] = user
    return users


def load_comments(data_path: str, repo: MemoryRepository, users):
    for data_row in read_csv_file(os.path.join(data_path, 'comments.csv')):
        comment = make_comment(
            comment_text=data_row[3],
            user=users[data_row[1]],
            movie=repo.get_movie(int(data_row[2])),
            timestamp=datetime.fromisoformat(data_row[4])
        )
        repo.add_comment(comment)


def populate(data_path: str, repo: MemoryRepository):
    # Load articles and tags into the repository.
    load_movies_and_genres_and_actors_and_directors(data_path, repo)

    # Load users into the repository.
    users = load_users(data_path, repo)

    # Load comments into the repository.
    load_comments(data_path, repo, users)
