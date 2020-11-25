from flask_socketio import SocketIO

ws = SocketIO(cors_allowed_origins="*", logger=False)

from . import view