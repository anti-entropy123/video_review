from flask_socketio import SocketIO

ws = SocketIO(cors_allowed_origins="*")

from . import view