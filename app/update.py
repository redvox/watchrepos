from threading import Timer

import logging

from app import git
from app import state

logger = logging.getLogger(__name__)


def start_update(name, path, interval, greedy):
    if greedy:
        update(name, path)
    else:
        Timer(interval=0, function=handle_update,
              args=(name, path, interval)).start()


def handle_update(name, path, interval):
    update(name, path)
    Timer(interval=interval, function=handle_update,
          args=(name, path, interval)).start()


def update(name, path):
    git_info = dict()

    git_info['action'] = remove_tailing_linebreak(git.run_command_line(path, 'action'))
    commits_remote_local = remove_tailing_linebreak(git.run_command_line(path, 'commits_remote_local'))
    commits_remote_local = commits_remote_local.split('|')
    git_info['commits_behind'], git_info['commits_ahead'] = commits_remote_local[0], commits_remote_local[1]
    git_info['local_changes'] = remove_tailing_linebreak(git.run_command_line(path, 'local_changes'))
    git_info['status'] = git.run_command_line(path, 'status').split('\n')
    git_info['untracked'] = remove_tailing_linebreak(git.run_command_line(path, 'untracked'))
    git_info['status-code'] = status_code(git_info)
    state.projects[name] = git_info


def remove_tailing_linebreak(string):
    return string.replace('\n', '')


def status_code(git_info):
    status_level = 0
    if git_info['action'] != 'up-to-date':
        status_level = 1
    if git_info['commits_behind'] != '0':
        status_level = 1
    if git_info['untracked'] != '0':
        status_level = 1
    if git_info['local_changes'] != '0':
        status_level = 2
    if git_info['status'] == 'diverged':
        status_level = 2
    status_class = ['ok', 'warning', 'danger']
    return status_class[status_level]
