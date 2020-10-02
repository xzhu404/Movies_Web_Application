from datetime import datetime
from typing import List, Iterable


class User:
    def __init__(
            self, username: str, password: str
    ):
        self._username: str = username
        self._password: str = password
        self._comments: List[Comment] = list()

    @property
    def username(self) -> str:
        return self._username

    @property
    def password(self) -> str:
        return self._password

    @property
    def comments(self) -> Iterable['Comment']:
        return iter(self._comments)

    def add_comment(self, comment: 'Comment'):
        self._comments.append(comment)

    def __repr__(self) -> str:
        return f'<User {self._username} {self._password}>'

    def __eq__(self, other) -> bool:
        if not isinstance(other, User):
            return False
        return other._username == self._username


class Comment:
    def __init__(
            self, user: User, movie: 'Movie', comment: str, timestamp: datetime
    ):
        self._user: User = user
        self._movie: Movie = movie
        self._comment: str = comment
        self._timestamp: str = timestamp.strftime('%Y-%m-%d %H:%M:%S')

    @property
    def user(self) -> User:
        return self._user

    @property
    def movie(self) -> 'Movie':
        return self._movie

    @property
    def comment(self) -> str:
        return self._comment

    @property
    def timestamp(self) -> str:
        return self._timestamp

    def __eq__(self, other):
        if not isinstance(other, Comment):
            return False
        return other._user == self._user and other._movie == self._movie and other._comment == self._comment and other._timestamp == self._timestamp


# Genres Model
class Genre:
    def __init__(
            self, genre_name: str
    ):
        self._genre_name: str = genre_name
        self._genre_movies: List[Movie] = list()

    @property
    def genre_name(self) -> str:
        return self._genre_name

    @property
    def genre_movies(self) -> Iterable['Movie']:
        return iter(self._genre_movies)

    @property
    def number_of_genre_movies(self) -> int:
        return len(self._genre_movies)

    def is_applied_to(self, movie: 'Movie') -> bool:
        return movie in self._genre_movies

    def add_movie(self, movie: 'Movie'):
        self._genre_movies.append(movie)

    def __eq__(self, other):
        if not isinstance(other, Genre):
            return False
        return other._genre_name == self._genre_name


# actor
class Actor:
    def __init__(
            self, name: str
    ):
        self._name: str = name
        self._movies_starring_actor: List[Movie] = list()

    @property
    def actor_name(self) -> str:
        return self._name

    @property
    def movies_starring_actor(self) -> Iterable['Movie']:
        return iter(self._movies_starring_actor)

    @property
    def number_of_movies_starring_actor(self) -> int:
        return len(self._movies_starring_actor)

    def is_applied_to(self, movie: 'Movie') -> bool:
        return movie in self._movies_starring_actor

    def add_movie(self, movie: 'Movie'):
        self._movies_starring_actor.append(movie)

    def __eq__(self, other):
        if not isinstance(other, Actor):
            return False
        return other._name == self._name


# director
class Director:
    def __init__(
            self, name: str
    ):
        self._name: str = name
        self._movies_directed_by_director: List[Movie] = list()

    @property
    def director_name(self) -> str:
        return self._name

    @property
    def movies_directed_by_director(self) -> Iterable['Movie']:
        return iter(self._movies_directed_by_director)

    @property
    def number_of_movies_directed_by_director(self) -> int:
        return len(self._movies_directed_by_director)

    def is_applied_to(self, movie: 'Movie') -> bool:
        return movie in self._movies_directed_by_director

    def add_movie(self, movie: 'Movie'):
        self._movies_directed_by_director.append(movie)

    def __eq__(self, other):
        if not isinstance(other, Director):
            return False
        return other._name == self._name


class Movie:
    def __init__(self, id: int, title: str, description: str, year: int,
                 runtime: int, rating: float, votes: int, revenue: float = None, metascore: int = None):
        self._id: int = id
        self._title: str = title
        self._description: str = description
        self._year: int = year
        self._runtime: int = runtime
        self._rating: float = rating
        self._votes: int = votes
        self._revenue: float = revenue
        self._director: Director = None
        self._metascore: int = metascore
        self._actors: List[Actor] = list()
        self._comments: List[Comment] = list()
        self._genres: List[Genre] = list()

    @property
    def id(self) -> int:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @property
    def description(self) -> str:
        return self._description

    @property
    def year(self) -> int:
        return self._year

    @property
    def runtime(self) -> int:
        return self._runtime

    @property
    def rating(self) -> float:
        return self._rating

    @property
    def votes(self) -> int:
        return self._votes

    @property
    def revenue(self) -> float:
        return self._revenue

    @property
    def metascore(self) -> int:
        return self._metascore

    @property
    def director(self) -> Director:
        return self._director

    @director.setter
    def director(self, director_name: str):
        self._director = Director(director_name)

    @property
    def actors(self) -> Iterable[Actor]:
        return iter(self._actors)

    @property
    def genres(self) -> Iterable[Genre]:
        return iter(self._genres)

    @property
    def comments(self) -> Iterable[Comment]:
        return iter(self._comments)

    @property
    def number_of_actors(self) -> int:
        return len(self._actors)

    @property
    def number_of_genres(self) -> int:
        return len(self._genres)

    @property
    def number_of_comments(self) -> int:
        return len(self._comments)

    def add_genre(self, genre: Genre):
        self._genres.append(genre)

    def add_actor(self, actor: Actor):
        self._actors.append(actor)

    def belongs_to_director(self, director: Director):
        self._director = director

    def is_belong_to_genre(self, genre):
        return genre in self._genres

    def add_comment(self, comment: Comment):
        self._comments.append(comment)

    def __repr__(self):
        return f'<Movie {self._year} {self._title}>'

    def __eq__(self, other):
        if not isinstance(other, Movie):
            return False
        return (
                other._year == self._year and
                other._title == self._title and
                other._votes == self._votes and
                other._description == self._description and
                other._metascore == self._metascore and
                other._rating == self._rating and
                other._runtime == self._runtime and
                other._revenue == self._revenue
        )

    def __lt__(self, other):
        return self._id > other.id


class ModelException(Exception):
    pass


def make_comment(comment_text: str, user: User, movie: Movie, timestamp: datetime = datetime.today()):
    comment = Comment(user, movie, comment_text, timestamp)
    user.add_comment(comment)
    movie.add_comment(comment)

    return comment


def make_genre_association(movie: Movie, genre: Genre):
    if genre.is_applied_to(movie):
        raise ModelException(f'Genre {genre.genre_name} already applied to Move "{movie.title}"')

    movie.add_genre(genre)
    genre.add_movie(movie)


def make_actor_association(movie: Movie, actor: Actor):
    if actor.is_applied_to(movie):
        raise ModelException(f'Actor {actor.actor_name} already applied to Movie "{movie.title}"')

    movie.add_actor(actor)
    actor.add_movie(movie)


def make_director_association(movie: Movie, director: Director):
    if director.is_applied_to(movie):
        raise ModelException(f'Director {director.director_name} already applied to Movie "{movie.title}"')

    movie.belongs_to_director(director)
    director.add_movie(movie)
