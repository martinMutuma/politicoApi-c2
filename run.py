"""run.py the main file to run the app"""

from app import create_app
from instance.config import configs

polApp = create_app('development')


if __name__ == "__main__":
    polApp.run()
