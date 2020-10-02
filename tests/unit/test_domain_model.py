from movies.domain.model import User, Movie, Genre, Director, Actor, make_comment, make_genre_association, \
    make_actor_association, make_director_association, ModelException

import pytest


@pytest.fixture()
def movie():
    m = Movie(
        1,
        "Guardians of the Galaxy",
        "It's a nice movies",
        2020,
        120,
        66.8,
        23424,
        122.7,
        76
    )
    m.director = 'Denis Villeneuve'
    return m


@pytest.fixture()
def user():
    return User('dbowie', '1234567890')


@pytest.fixture()
def actor():
    return Actor("Michelle Williams")


@pytest.fixture()
def director():
    return Director('Denis Villeneuve')


@pytest.fixture()
def genre():
    return Genre('Action')


def test_user_construction(user):
    assert user.username == 'dbowie'
    assert user.password == '1234567890'
    assert repr(user) == '<User dbowie 1234567890>'

    for comment in user.comments:
        # User should have an empty list of Comments after construction.
        assert False


def test_movie_construction(movie: Movie):
    assert movie.id == 1
    assert movie.title == "Guardians of the Galaxy"
    assert movie.description == "It's a nice movies"
    assert movie.year == 2020
    assert movie.runtime == 120
    assert movie.rating == 66.8
    assert movie.votes == 23424
    assert movie.revenue == 122.7
    assert movie.metascore == 76

    assert movie.number_of_comments == 0
    assert movie.number_of_genres == 0
    assert movie.number_of_actors == 0
    assert movie.director.director_name == 'Denis Villeneuve'

    assert repr(movie) == '<Movie 2020 Guardians of the Galaxy>'


def test_movie_less_than_operator():
    movie_1 = Movie(
        1, "", "", 0, 0, 0, 0, None, None
    )

    movie_2 = Movie(
        2, "", "", 0, 0, 0, 0, None, None
    )

    assert movie_1 > movie_2


def test_genre_construction(genre: Genre):
    assert genre.genre_name == 'Action'

    for movie in genre.genre_movies:
        assert False

    assert not genre.is_applied_to(Movie(0, "", "", 0, 0, 0, 0, None, None))


def test_make_comment_establishes_relationships(movie, user):
    comment_text = 'nice movies'
    comment = make_comment(comment_text, user, movie)

    # Check that the User object knows about the Comment.
    assert comment in user.comments

    # Check that the Comment knows about the User.
    assert comment.user is user

    # Check that Article knows about the Comment.
    assert comment in movie.comments

    # Check that the Comment knows about the Article.
    assert comment.movie is movie


def test_make_genre_associations(movie, genre):
    make_genre_association(movie, genre)

    assert movie.is_belong_to_genre(genre)

    # check that the Tag knows about the Article.
    assert genre.is_applied_to(movie)
    assert movie in genre.genre_movies


def test_make_genre_associations_with_movie_already_was_applied_to_genre(movie, genre):
    make_genre_association(movie, genre)

    with pytest.raises(ModelException):
        make_genre_association(movie, genre)


def test_make_actor_association(movie, actor):
    make_actor_association(movie, actor)

    assert actor.is_applied_to(movie)
    assert movie in actor.movies_starring_actor


def test_make_actor_association_with_movie_already_was_applied_to_actor(movie, actor):
    make_actor_association(movie, actor)

    with pytest.raises(ModelException):
        make_actor_association(movie, actor)


def test_make_director_association(movie, director):
    make_director_association(movie, director)

    assert director.is_applied_to(movie)
    assert movie in director.movies_directed_by_director


def test_make_director_association_with_movie_already_was_applied_to_director(movie, director):
    make_director_association(movie, director)

    with pytest.raises(ModelException):
        make_director_association(movie, director)
