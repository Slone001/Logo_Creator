from flask import Blueprint, render_template, request, send_from_directory, jsonify, url_for, Response
import os
import functions
from data import logo_handler as lh

bp = Blueprint('main', __name__)
ImageQue = lh.imageQue


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/season')
def Season_logo():
    folder_path = os.path.join(os.getcwd(), "blueprint_logos/")
    folders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]

    return render_template("season_folder.html", folders=folders)


@bp.route("/season/<folder_name>")
def season_folder_page(folder_name):
    folder_path = os.path.join(os.getcwd(), "blueprint_logos", folder_name)
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        return "Ordner nicht gefunden", 404

    images = os.listdir(folder_path)
    image_list = []
    print(images)
    for image in images:
        print(image)
        if image.rstrip().endswith(".png"):
            image_list.append(image)
    return render_template("season_folder_img.html", folder_name=folder_name, images=image_list)


# check if needed
@bp.route('/blueprint_logos/<folder_name>/<filename>')
def blueprint_logo(folder_name, filename: str):
    folder_path = os.path.join(os.getcwd(), "blueprint_logos", folder_name)
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        return 404

    IMAGE_DIR = os.path.join(os.getcwd(), "blueprint_logos/", folder_name)

    return send_from_directory(IMAGE_DIR, filename)


@bp.route('/seasonLogoup')
def Season_logo_upload():
    return render_template("upload_season_logo.html")


@bp.route('/upload', methods=['POST'])
def upload_file():
    season_dir = request.form.get("season_name", "")

    season_dir = season_dir.replace(" ", "_").replace("-", "_").replace("/", "")

    try:
        if not os.path.exists(season_dir):
            os.mkdir(f"blueprint_logos/{season_dir}")
    except FileExistsError:
        return "Ordner kann ich erstellt werden", 403

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


# route for html page image-configuration
@bp.route('/season/<folder>/<img>')
def season_logo_config(folder, img):
    # todo: fix bug, if img endswith .png new config will be created
    if not img.endswith(".png"):
        return render_template("404.html"), 404
    if not os.path.exists(f"blueprint_logos/{folder}"):
        return render_template("404.html"), 404
    if not os.path.exists(f"blueprint_logos/{folder}/preview/{img}"):
        functions.image_generation(folder, img)
    return render_template("img_config.html")


# route update the configuration
@bp.route('/season/<folder>/<img>', methods=['POST'])
def season_logo_config_reload(folder, img):
    try:
        angle = int(request.form["angle"])
        distance = int(request.form["distance"])
    except Exception as e:
        # todo: New Error page
        return render_template("404.html"), 404
    data = [distance, angle]
    if angle == 0 or distance == 0:
        return render_template("404.html"), 404
    functions.save_img_con(folder, img, data)
    functions.image_generation(folder, img)
    return season_logo_config(folder, img)


@bp.route('/image_status/<folder>/<image_name>', methods=["HEAD"])
def check_image_status(folder, image_name):
    folder_path = os.path.join(os.getcwd(), "blueprint_logos", folder, "preview", image_name)
    if os.path.exists(folder_path):
        return Response(status=200)
    else:
        return Response(status=404)


@bp.route('/generated_preview/<folder>/<image_name>', )
def serve_preview(folder, image_name):
    image_dir = os.path.join(os.getcwd(), "blueprint_logos", folder, "preview")
    if os.path.exists(os.path.join(image_dir, image_name)):
        return send_from_directory(image_dir, image_name)
    else:
        return "Image not found", 404


@bp.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
