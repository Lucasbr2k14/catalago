from flask import Blueprint

front = Blueprint("front", __name__)

from . import index
from . import register
from . import login
from . import dashboard
from . import logout