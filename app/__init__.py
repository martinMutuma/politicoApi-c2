from flask import Flask
from instance.config import configs


polApp = Flask(__name__)

polApp.config.from_object(configs['production'])


from app.routes import *


