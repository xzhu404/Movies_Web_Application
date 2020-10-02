from flask import Blueprint, render_template, redirect, url_for, session, request, flash

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

from password_validator import PasswordValidator

from functools import wraps

import movies.utilities.utilities as utilities
import movies.authentication.services as services
import movies.adapters.repository as repo

# Configure Blueprint.
authentication_blueprint = Blueprint(
    'authentication_bp', __name__, url_prefix='/authentication')


@authentication_blueprint.route('/register', methods=['POST'])
def register():
    form = utilities.RegistrationForm()

    if form.validate_on_submit():

        # Successful POST, i.e. the username and password have passed validation checking.
        # Use the service layer to attempt to add the new user.
        try:
            services.add_user(form.username.data, form.password.data, repo.repo_instance)

        except services.NameNotUniqueException:
            flash('Your username is already taken - please supply another')

    for error in form.username.errors:
        flash(error)
    for error in form.password.errors:
        flash(error)

    return redirect(url_for('home_bp.home'))


@authentication_blueprint.route('/login', methods=['POST'])
def login():
    form = utilities.LoginForm()
    username_not_recognised = None
    password_does_not_match_username = None

    if form.validate_on_submit():
        print(form.username.data, form.password.data)
        # Successful POST, i.e. the username and password have passed validation checking.
        # Use the service layer to lookup the user.
        try:
            user = services.get_user(form.username.data, repo.repo_instance)

            # Authenticate user.
            services.authenticate_user(user['username'], form.password.data, repo.repo_instance)

            # Initialise session and redirect the user to the home page.
            session.clear()
            session['username'] = user['username']
            return redirect(url_for('home_bp.home'))

        except services.UnknownUserException:
            # Username not known to the system, set a suitable error message.
            username_not_recognised = 'Username not recognised - please supply another'

        except services.AuthenticationException:
            # Authentication failed, set a suitable error message.
            password_does_not_match_username = 'Password does not match supplied username - please check and try again'

    # For a GET or a failed POST, return the Login Web page.
    return redirect(url_for("home_bp.home"))


@authentication_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home_bp.home'))


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'username' not in session:
            return redirect(url_for('authentication_bp.login'))
        return view(**kwargs)

    return wrapped_view


class PasswordValid:
    def __init__(self, message=None):
        if not message:
            message = u'Your password must be at least 8 characters, and contain an upper case letter, a lower case letter and a digit'
        self.message = message

    def __call__(self, form, field):
        schema = PasswordValidator()
        schema.min(8).has().uppercase().has().lowercase().has().digits()
        print('--------密码限制条件', schema)
        print('--------验证密码有效性：', schema.validate(field.data))
        if not schema.validate(field.data):
            print('----------密码无效')
            raise ValidationError(self.message)
