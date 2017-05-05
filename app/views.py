from flask import Blueprint, request
from flask import render_template
from app import state

blueprint = Blueprint('views', __name__)


def filter_ok_projects(projects):
    filtered = dict()
    for name, project in projects.items():
        if project['status-code'] != 'ok':
            filtered[name] = project
    return filtered


@blueprint.route('/')
def repos():
    filter_switch = request.args.get('filter', 'false') == 'true'
    if filter_switch:
        print(filter_switch)
        content = filter_ok_projects(state.projects)
    else:
        content = state.projects
    return render_template("overview.html",
                           title="Repos",
                           parameter=request.args,
                           projects=content)
