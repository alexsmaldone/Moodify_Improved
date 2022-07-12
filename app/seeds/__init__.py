from flask.cli import AppGroup
from .users import seed_users, undo_users
from .library import seed_library, undo_library
from .moods import seed_moods, undo_moods
from .playlists import seed_playlists, undo_playlists

# Creates a seed group to hold our commands
# So we can type `flask seed --help`
seed_commands = AppGroup('seed')


# Creates the `flask seed all` command
@seed_commands.command('all')
def seed():
    seed_users()
    seed_moods()
    seed_library()


    # Add other seed functions here


# Creates the `flask seed undo` command
@seed_commands.command('undo')
def undo():
    undo_users()
    undo_moods()
    undo_library()
    undo_playlists()
    # Add other undo functions here
