import os
import requests
import json
from flask import Blueprint
from .parsers import survey_from_json

main = Blueprint('main', __name__) 

from . import views, question_views, answer_views, survey_views
