from apiflask import APIBlueprint

bp = APIBlueprint('Kürslii', __name__)

from app.courses import routes