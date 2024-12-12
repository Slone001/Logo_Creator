from flask import Blueprint, render_template, request
import os


bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/seasonLogos')
def Season_logo():
    return render_template("Season_logo.html")


@bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part in the request.", 400

    file = request.files['file']

    if file.filename == '':
        return "No file selected.", 400

    # Save the file if it's valid
    if file:
        filepath = os.path.join("blueprint_logos/", file.filename)
        file.save(filepath)
        return f"File uploaded successfully to {filepath}!"
