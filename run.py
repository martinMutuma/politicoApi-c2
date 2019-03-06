"""run.py the main file to run the app"""

from app import create_app
from dotenv import load_dotenv
from flasgger import Swagger
from flask_cors import CORS


load_dotenv()
polApp = create_app('development')
CORS(polApp)

polApp.config['SWAGGER'] = {
    'specs_route': '/',
}
Swagger(polApp, template_file='../api_docs.yaml')

if __name__ == "__main__":
    polApp.run()
