import os
from flask import Flask


def create_app():
    app = Flask(__name__)
    # Set the directory to store uploaded files
    app.config['blueprint_logos'] = 'blueprint_logos/'

    import routes
    app.register_blueprint(routes.bp)

    return app


def check_folder_structure():
    if not os.path.exists("blueprint_logos/"):
        os.makedirs("blueprint_logos/")
    if not os.path.exists("finished_logos/"):
        os.makedirs("finished_logos/")
