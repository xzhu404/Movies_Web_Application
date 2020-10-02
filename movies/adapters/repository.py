import abc
from typing import List
from datetime import date

from movies.domain.model import User, Movie, Genre, Actor, Director, Comment

repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_user(self, user: User):
        """" Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username) -> User:
        """ Returns the User named username from the repository.

        If there is no User with the given username, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_movie(self, movie: Movie):
        """ Adds a Movie to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie(self, id: int) -> Movie:
        """ Returns Movie with id from the repository.

        If there is no Movie with the given id, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def filter_movies(self, actor_name: str = "", director_name: str = "", genre_name: str = "") -> List[int]:
        """Returns a list of ids representing Movies filter by actor name or director name or genre.

        If there are no matches, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_movies(self) -> int:
        """ Returns the number of Movies in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_first_movie(self) -> Movie:
        """ Returns the first Movie, ordered by id, from the repository.

        Returns None if the repository is empty.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_last_movie(self) -> Movie:
        """ Returns the last Movie, ordered by id, from the repository.

        Returns None if the repository is empty.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_id(self, id_list) -> List[Movie]:
        """ Returns a list of Movies, whose ids match those in id_list, from the repository.

        If there are no matches, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_movie_ids(self) -> List[int]:
        """
        Returns a list of all ids representing Movies.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_ids_for_genre(self, genre_name: str) -> List[int]:
        """ Returns a list of ids representing Movies that are applied to genre_name.

        If there are Movies that are applied to genre_name, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, genre: Genre):
        """ Adds a Genre to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_director(self, director: Director):
        """ Adds a Director to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_actor(self, actor: Actor):
        """ Adds an Actor to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_genres(self) -> List[Genre]:
        """ Returns the Genres stored in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_comment(self, comment: Comment):
        """ Adds a Comment to the repository.

        If the Comment doesn't have bidirectional links with an Movie and a User, this method raises a
        RepositoryException and doesn't update the repository.
        """
        if comment.user is None or comment not in comment.user.comments:
            raise RepositoryException('Comment not correctly attached to a User')
        if comment.movie is None or comment not in comment.movie.comments:
            raise RepositoryException('Comment not correctly attached to an Movie')

    @abc.abstractmethod
    def get_comments(self):
        """ Returns the Comments stored in the repository. """
        raise NotImplementedError
