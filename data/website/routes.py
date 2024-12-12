from flask import Blueprint, render_template, request
import os


bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/seasonLogos')
def Season_logo():
    return render_template("season_logo.html")


@bp.route('/seasonLogoup')
def Season_logo_upload():
    return render_template("season_logo_up.html")


@bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part in the request.", 400

    files = request.files.getlist('file')
    if not files:
        return "No files selected.", 400

    saved_files = []
    for file in files:
        if file and file.filename != '':
            filepath = os.path.join("static/uploads", file.filename)
            file.save(filepath)
            saved_files.append(filepath)

    return f"Files uploaded successfully: {', '.join(saved_files)}"
