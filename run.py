"""run.py the main file to run the app"""

from app import polApp
from instance.config import configs

polApp.config.from_object(configs['development'])


if __name__ == "__main__":
    polApp.run()
    