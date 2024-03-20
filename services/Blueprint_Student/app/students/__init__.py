from apiflask import APIBlueprint

bp = APIBlueprint('Studis', __name__)

from app.students import routes