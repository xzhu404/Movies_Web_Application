import pytest

from movies.authentication.services import AuthenticationException
from movies.movies import services as news_services
from movies.authentication import services as auth_services
from movies.movies.services import NonExistentMovieException


def test_can_add_user(in_memory_repo):
    new_username = 'jz'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    user_as_dict = auth_services.get_user(new_username, in_memory_repo)
    assert user_as_dict['username'] == new_username

    # Check that password has been encrypted.
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')


def test_cannot_add_user_with_existing_name(in_memory_repo):
    username = 'thorke'
    password = 'abcd1A23'

    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(username, password, in_memory_repo)


def test_authentication_with_valid_credentials(in_memory_repo):
    new_username = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    try:
        auth_services.authenticate_user(new_username, new_password, in_memory_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repo):
    new_username = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_username, '0987654321', in_memory_repo)


def test_can_add_comment(in_memory_repo):
    movie_id = 13
    comment_text = 'The loonies are stripping the supermarkets bare!'
    username = 'fmercury'

    # Call the service layer to add the comment.
    news_services.add_comment(movie_id, comment_text, username, in_memory_repo)

    # Retrieve the comments for the article from the repository.
    comments_as_dict = news_services.get_comments_for_movie(movie_id, in_memory_repo)

    # Check that the comments include a comment with the new comment text.
    assert next(
        (dictionary['comment_text'] for dictionary in comments_as_dict if dictionary['comment_text'] == comment_text),
        None) is not None


def test_cannot_add_comment_for_non_existent_movie(in_memory_repo):
    movie_id = 7
    comment_text = "COVID-19 - what's that?"
    username = 'fmercury'

    # Call the service layer to attempt to add the comment.
    with pytest.raises(news_services.NonExistentMovieException):
        news_services.add_comment(movie_id, comment_text, username, in_memory_repo)


def test_cannot_add_comment_by_unknown_user(in_memory_repo):
    movie_id = 13
    comment_text = 'The loonies are stripping the supermarkets bare!'
    username = 'gmichael'

    # Call the service layer to attempt to add the comment.
    with pytest.raises(news_services.UnknownUserException):
        news_services.add_comment(movie_id, comment_text, username, in_memory_repo)


def test_can_get_movie(in_memory_repo):
    movie_id = 14

    movie_as_dict = news_services.get_movie(movie_id, in_memory_repo)

    assert movie_as_dict['id'] == movie_id
    assert movie_as_dict['title'] == 'Moana'
    assert movie_as_dict[
               'description'] == "In Ancient Polynesia, when a terrible curse incurred by the Demigod Maui reaches an impetuous Chieftain's daughter's island, she answers the Ocean's call to seek out the Demigod to set things right."
    assert movie_as_dict['year'] == 2016
    assert movie_as_dict['runtime'] == 107
    assert movie_as_dict['rating'] == 7.7
    assert movie_as_dict['votes'] == 118151
    assert movie_as_dict['revenue'] == 248.75
    assert movie_as_dict['metascore'] == 81
    assert len(movie_as_dict['comments']) == 0
    assert len(movie_as_dict['actors']) == 4

    genre_names = [dictionary['name'] for dictionary in movie_as_dict['genres']]
    assert 'Adventure' in genre_names
    assert 'Animation' in genre_names
    assert 'Comedy' in genre_names

    actor_names = [i["name"] for i in movie_as_dict["actors"]]
    assert "Auli'i Cravalho" in actor_names
    assert "Dwayne Johnson" in actor_names
    assert "Rachel House" in actor_names
    assert "Temuera Morrison" in actor_names


def test_cannot_get_movie_with_non_existent_id(in_memory_repo):
    movie_id = 7

    # Call the service layer to attempt to retrieve the Article.
    with pytest.raises(news_services.NonExistentMovieException):
        news_services.get_movie(movie_id, in_memory_repo)


def test_get_first_movie(in_memory_repo):
    movie_as_dict = news_services.get_first_movie(in_memory_repo)

    assert movie_as_dict['id'] == 1


def test_get_last_movie(in_memory_repo):
    movie_as_dict = news_services.get_last_movie(in_memory_repo)

    assert movie_as_dict['id'] == 16


def test_get_movies_by_id(in_memory_repo):
    target_movie_ids = [1, 13, 15, 18, 20]
    movies_as_dict = news_services.get_movies_by_id(target_movie_ids, in_memory_repo)

    # Check that 2 articles were returned from the query.
    assert len(movies_as_dict) == 3

    # Check that the article ids returned were 5 and 6.
    movie_ids = [movie['id'] for movie in movies_as_dict]
    assert {1, 13, 15}.issubset(movie_ids)


def test_get_comments_for_blog(in_memory_repo):
    comments_as_dict = news_services.get_comments_for_movie(1, in_memory_repo)

    # Check that 2 comments were returned for article with id 1.
    assert len(comments_as_dict) == 2

    # Check that the comments relate to the article whose id is 1.
    movie_ids = [comment['movie_id'] for comment in comments_as_dict]
    movie_ids = set(movie_ids)
    assert 1 in movie_ids and len(movie_ids) == 1


def test_get_comments_for_non_existent_article(in_memory_repo):
    with pytest.raises(NonExistentMovieException):
        comments_as_dict = news_services.get_comments_for_movie(7, in_memory_repo)


def test_get_comments_for_movie_without_comments(in_memory_repo):
    comments_as_dict = news_services.get_comments_for_movie(16, in_memory_repo)
    assert len(comments_as_dict) == 0
