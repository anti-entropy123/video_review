from flask import Blueprint

api = Blueprint('api', __name__)
admin = Blueprint('admin', __name__)

from . import user_view
from . import project_view
from . import video_view
from . import message_view
from . import meeting_view
from . import _webhook
from . import errors
from . import admin_view
