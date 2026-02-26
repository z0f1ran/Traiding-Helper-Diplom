from flask import Flask
from .models import *
from .views import *
from .controllers import *

def create_app():
    app = Flask(__name__)
    # ...инициализация конфигурации, БД и роутов...
    return app
