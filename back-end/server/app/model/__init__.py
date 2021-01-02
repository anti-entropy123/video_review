from .. import db

Meeting = None
User = None
Message = None
Project = None
Video = None

from .Meeting import Meeting as db_Meeting 
Meeting = db_Meeting

from .Message import Message as db_Message
Message = db_Message

from .User import User as db_User
User = db_User

from .Project import ProjectMember
from .Project import Project as db_Project
Project = db_Project

from .Video import Comment
from .Video import Video as db_Video
Video = db_Video

