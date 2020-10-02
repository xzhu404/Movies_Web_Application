import os

from flask import Flask
from flask_wtf import CSRFProtect

import movies.adapters.repository as repo
from movies.adapters.memory_repository import MemoryRepository, populate

csrf = CSRFProtect()


def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_object('config.Config')
    data_path = os.path.join("movies", 'adapters', 'data')

    csrf.init_app(app)

    if test_config:
        app.config.from_mapping(test_config)
        data_path = app.config["TEST_DATA_PATH"]

    repo.repo_instance = MemoryRepository()
    populate(data_path, repo.repo_instance)

    with app.app_context():
        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .movies import movies
        app.register_blueprint(movies.movies_blueprint)

        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

    return app
