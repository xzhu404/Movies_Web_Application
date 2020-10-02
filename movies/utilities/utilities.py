from better_profanity import profanity
from flask import Blueprint, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError

import movies.adapters.repository as repo
import movies.utilities.services as services

# Configure Blueprint.
from movies.authentication.authentication import PasswordValid


def get_genres_and_urls():
    genre_names = services.get_genre_names(repo.repo_instance)
    genre_urls = dict()
    for genre_name in genre_names:
        genre_urls[genre_name] = url_for('news_bp.movies_by_genre', genre=genre_name)

    return genre_urls


def get_selected_movies(quantity=3):
    movies = services.get_random_movies(quantity, repo.repo_instance)

    return movies


class FilterForm(FlaskForm):
    genre = StringField('genre', render_kw={"placeholder": "Genre"})
    actor = StringField('actor', render_kw={"placeholder": "Actor"})
    director = StringField('director', render_kw={"placeholder": "Director"})

    submit = SubmitField('Search')


class RegistrationForm(FlaskForm):
    username = StringField('Username', [
        DataRequired(message='Your username is required'),
        Length(min=3, message='Your username is too short')], id="register-username")
    password = PasswordField('Password', [
        DataRequired(message='Your password is required'),
        PasswordValid()], id='register-password')
    submit = SubmitField('REGISTER NOW!', id="signup")


class LoginForm(FlaskForm):
    username = StringField('Username', [
        DataRequired()], id='login-username')
    password = PasswordField('Password', [
        DataRequired()], id='login-password')
    submit = SubmitField('Login', id='login')


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', [
        DataRequired(),
        Length(min=4, message='Your comment is too short'),
        ProfanityFree(message='Your comment must not contain profanity')], id='comment-text')
    movie_id = HiddenField("Movie id")
    submit = SubmitField('Submit')
