import os
from flask import Flask, render_template
import data.website.routes


def create_app():
    app = Flask(__name__)
    # Set the directory to store uploaded files
    app.config['blueprint_logos'] = 'blueprint_logos/'

    app.register_blueprint(routes.bp)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    return app


def check_folder_structure():
    if not os.path.exists("blueprint_logos/"):
        os.makedirs("blueprint_logos/")
    if not os.path.exists("finished_logos/"):
        os.makedirs("finished_logos/")
