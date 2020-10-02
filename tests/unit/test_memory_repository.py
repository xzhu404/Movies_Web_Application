from datetime import datetime
from typing import List

import pytest

from movies.domain.model import User, Movie, Genre, Actor, Director, Comment, make_comment
from movies.adapters.repository import RepositoryException


def test_repository_can_add_a_user(in_memory_repo):
    user = User('Dave', '123456789')
    in_memory_repo.add_user(user)

    assert in_memory_repo.get_user('Dave') is user


def test_repository_can_retrieve_a_user(in_memory_repo):
    user = in_memory_repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')


def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('prince')
    assert user is None


def test_repository_can_retrieve_movie_count(in_memory_repo):
    number_of_movies = in_memory_repo.get_number_of_movies()

    # Check that the query returned 6 Articles.
    assert number_of_movies == 5


def test_repository_can_add_movie(in_memory_repo):
    movie = Movie(
        100000000,
        'Movie 1',
        'It is Movie 1',
        2010,
        110,
        33.3,
        3434,
        12.34,
        53
    )
    in_memory_repo.add_movie(movie)

    assert in_memory_repo.get_movie(100000000) is movie


def test_repository_can_retrieve_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(1)

    # Check that the Movie has the expected title.
    assert movie.title == 'Guardians of the Galaxy'

    # Check that the Article is commented as expected.
    comment_one = [comment for comment in movie.comments if comment.comment == 'Oh no, COVID-19 has hit New Zealand'][
        0]
    comment_two = [comment for comment in movie.comments if comment.comment == 'Yeah Freddie, bad movies'][0]

    assert comment_one.user.username == 'fmercury'
    assert comment_two.user.username == "thorke"

    assert movie.is_belong_to_genre(Genre('Action'))
    assert movie.director == Director('James Gunn')


def test_repository_does_not_retrieve_a_non_existent_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(101)
    assert movie is None


def test_repository_can_retrieve_movies_by_filter(in_memory_repo):
    movies_1 = in_memory_repo.filter_movies(genre_name="Action")
    assert len(movies_1) == 3

    movies_2 = in_memory_repo.filter_movies(actor_name="Eric Stonestreet")
    assert len(movies_2) == 3

    movies_3 = in_memory_repo.filter_movies(director_name="James Gunn")
    assert len(movies_3) == 3

    movies_4 = in_memory_repo.filter_movies(actor_name="Eric Stonestreet", director_name="James Gunn",
                                            genre_name="Action")
    assert len(movies_4) == 2


def test_repository_does_not_retrieve_an_movie_when_there_are_no_movies_by_filter(in_memory_repo):
    movies_1 = in_memory_repo.filter_movies(director_name="Mike")
    assert len(movies_1) == 0


def test_repository_can_retrieve_genres(in_memory_repo):
    genres: List[Genre] = in_memory_repo.get_genres()

    assert len(genres) == 6

    genre_one = [genre for genre in genres if genre.genre_name == 'Action'][0]
    genre_two = [genre for genre in genres if genre.genre_name == 'Adventure'][0]
    genre_three = [genre for genre in genres if genre.genre_name == 'Sci-Fi'][0]
    genre_four = [genre for genre in genres if genre.genre_name == 'Animation'][0]
    genre_five = [genre for genre in genres if genre.genre_name == 'Comedy'][0]
    genre_six = [genre for genre in genres if genre.genre_name == 'Drama'][0]

    assert genre_one.number_of_genre_movies == 3
    assert genre_two.number_of_genre_movies == 4
    assert genre_three.number_of_genre_movies == 2
    assert genre_four.number_of_genre_movies == 2
    assert genre_five.number_of_genre_movies == 3
    assert genre_six.number_of_genre_movies == 1


def test_repository_can_get_first_movie(in_memory_repo):
    article = in_memory_repo.get_first_movie()
    assert article.title == 'Guardians of the Galaxy'


def test_repository_can_get_last_movie(in_memory_repo):
    article = in_memory_repo.get_last_movie()
    assert article.title == 'The Secret Life of Pets'


def test_repository_can_get_movies_by_ids(in_memory_repo):
    movies = in_memory_repo.get_movies_by_id([1, 13, 15])

    assert len(movies) == 3
    assert movies[
               0].title == 'Guardians of the Galaxy'
    assert movies[1].title == "Rogue One"
    assert movies[2].title == 'Colossal'


def test_repository_does_not_retrieve_movie_for_non_existent_id(in_memory_repo):
    movies = in_memory_repo.get_movies_by_id([14, 9])

    assert len(movies) == 1
    assert movies[
               0].title == 'Moana'


def test_repository_returns_an_empty_list_for_non_existent_ids(in_memory_repo):
    movies = in_memory_repo.get_movies_by_id([0, 9])

    assert len(movies) == 0


def test_repository_returns_movie_ids_for_existing_genre(in_memory_repo):
    movies_ids = in_memory_repo.get_movie_ids_for_genre('Action')

    assert movies_ids == [1, 13, 15]


def test_repository_returns_an_empty_list_for_non_existent_genre(in_memory_repo):
    movies_ids = in_memory_repo.get_movie_ids_for_genre('Love')

    assert len(movies_ids) == 0


def test_repository_can_add_a_genre(in_memory_repo):
    genre = Genre('Motoring')
    in_memory_repo.add_genre(genre)

    assert genre in in_memory_repo.get_genres()


def test_repository_can_add_a_comment(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    movie = in_memory_repo.get_movie(1)
    comment = make_comment("Trump's onto it!", user, movie)

    in_memory_repo.add_comment(comment)

    assert comment in in_memory_repo.get_comments()


def test_repository_does_not_add_a_comment_without_a_user(in_memory_repo):
    movie = in_memory_repo.get_movie(13)
    comment = Comment(None, movie, "Trump's onto it!", datetime.today())

    with pytest.raises(RepositoryException):
        in_memory_repo.add_comment(comment)


def test_repository_does_not_add_a_comment_without_an_movie_properly_attached(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    movie = in_memory_repo.get_movie(13)
    comment = Comment(None, movie, "Trump's onto it!", datetime.today())

    user.add_comment(comment)

    with pytest.raises(RepositoryException):
        # Exception expected because the Movie doesn't refer to the Comment.
        in_memory_repo.add_comment(comment)


def test_repository_can_retrieve_comments(in_memory_repo):
    assert len(in_memory_repo.get_comments()) == 2


def test_repository_filter_movies_by_genre_or_actor_name_or_director_name(in_memory_repo):
    movie_ids = in_memory_repo.filter_movies(genre_name="Action")
    assert set(movie_ids) == {1, 13, 15}

    movie_ids = in_memory_repo.filter_movies(genre_name="Love")
    assert len(movie_ids) == 0

    movie_ids = in_memory_repo.filter_movies(actor_name="Auli'i Cravalho")
    assert set(movie_ids) == {14}

    movie_ids = in_memory_repo.filter_movies(actor_name="Auli Cravalho")
    assert len(movie_ids) == 0

    movie_ids = in_memory_repo.filter_movies(actor_name="Auli'i Cravalho", genre_name="Comedy")
    assert set(movie_ids) == {14}

    movie_ids = in_memory_repo.filter_movies(actor_name="Auli Cravalho", genre_name="Action")
    assert len(movie_ids) == 0

    movie_ids = in_memory_repo.filter_movies(director_name='James Gunn')
    assert set(movie_ids) == {1, 13, 16}

    movie_ids = in_memory_repo.filter_movies(director_name="Auli")
    assert len(movie_ids) == 0

    movie_ids = in_memory_repo.filter_movies(director_name="James Gunn", genre_name="Action")
    assert set(movie_ids) == {1, 13}

    movie_ids = in_memory_repo.filter_movies(director_name="James Gunn", genre_name="Action", actor_name='Chris Pratt')
    assert movie_ids == [1]
