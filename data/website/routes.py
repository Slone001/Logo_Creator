from flask import Blueprint, render_template, request
import os
import re


bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/seasonLogos')
def Season_logo():
    folder_path = os.path.join(os.getcwd(), "blueprint_logos/")
    folders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]

    return render_template("season_logo.html", folders=folders)


@bp.route("/season/<folder_name>")
def season_folder_page(folder_name):
    folder_path = os.path.join(os.getcwd(), "blueprint_logos/", folder_name)
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        return "Ordner nicht gefunden", 404

    return render_template("season_logo_creator.html")


@bp.route('/seasonLogoup')
def Season_logo_upload():
    return render_template("season_logo_up.html")


@bp.route('/upload', methods=['POST'])
def upload_file():

    season_dir = request.form.get("season_name", "")

    season_dir = season_dir.replace(" ", "_").replace("-", "_").replace("/", "")

    try:
        if not os.path.exists(season_dir):
            os.mkdir(f"blueprint_logos/{season_dir}")
    except FileExistsError:
        return "Ordner kann icht erstellt werden", 403

    files = request.files.getlist("files[]")

    if not files:
        return "No file part in the request.", 400

    files = request.files.getlist('files[]')
    if not files:
        return "No files selected.", 400

    saved_files = []
    for file in files:
        if file and file.filename != '':
            filepath = os.path.join(f"blueprint_logos/{season_dir}/", file.filename)
            file.save(filepath)
            saved_files.append(filepath)

    return f"Files uploaded successfully: {', '.join(saved_files)}"
