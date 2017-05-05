import logging
import os.path
from pprint import pprint

import yaml
from flask import Flask

from app import views, update, view_util
from app import state

logger = logging.getLogger(__name__)


def create_app(port, environment, working_dir, greedy):
    app = Flask(__name__)
    app.config.from_pyfile('state.py')
    app.register_blueprint(views.blueprint)
    app.jinja_env.filters['linebreaks'] = view_util.linebreaks
    config = load_config()

    projects = []
    for directory in config['project_dirs']:
        projects.extend(get_project_directories(directory))

    start_update_threads(projects, config['update_interval'], greedy)
    pprint(state.projects)
    return app


def load_config():
    with open('./resources/config.yaml', 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def get_project_directories(directory):
    paths = [(d, os.path.join(directory, d)) for d in os.listdir(directory)]
    project_paths = [path for path in paths if os.path.isdir(path[1]) and os.path.isdir(path[1] + '/.git')]
    return project_paths


def start_update_threads(projects, interval, greedy):
    cwd = os.getcwd()
    for project in projects:
        update.start_update(project[0], project[1], interval, greedy)
