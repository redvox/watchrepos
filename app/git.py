import subprocess
from shlex import quote

git_commands = {
    'action': '/home/jens/projects/watchrepos/scripts/action.sh',
    'commits_remote_local': '/home/jens/projects/watchrepos/scripts/commits_remote_local.sh',
    'local_changes': '/home/jens/projects/watchrepos/scripts/local_changes.sh',
    'status': '/home/jens/projects/watchrepos/scripts/status.sh',
    'untracked': '/home/jens/projects/watchrepos/scripts/untracked.sh',
}


def run_command_line(path, command):
    change_dir = 'cd ' + quote(path)
    return subprocess.check_output([git_commands[command]], cwd=path).decode("utf-8")
