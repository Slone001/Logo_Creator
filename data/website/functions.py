import os
import json
import logging
from data import logo_handler


def path_creator(folder: str, img: str) -> str:
    img = img.replace(" ", "_")
    path = os.path.join(os.getcwd(), "blueprint_logos", folder)
    base, ext = os.path.splitext(img)
    path = f"{path}/{base}.cfg"
    return path


def load_img_con(folder: str, img: str) -> list[tuple[str, int]]:
    path = path_creator(folder, img)

    if not os.path.exists(path):
        with open(path, "w") as file:
            data = {"distance": 20, "angle": 45}
            json.dump(data, file)

    with open(path, "r") as file:
        data = json.load(file)
    config: list[tuple[str, int]] = []
    for i in data:
        config.append((i, data[i]))
    return config


def save_img_con(folder: str, img: str, data: list[int]) -> bool:
    try:
        path = path_creator(folder, img)
        config = {"distance": data[0], "angle": data[1]}
        with open(path, "w") as file:
            json.dump(config, file)
        image_generation(folder, img, config)
        return True
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(e)
        return False


def season_config_gen(folder, img, ImageQue):
    load_img_con(folder, img)
    folder_path = os.path.join(os.getcwd(), "blueprint_logos", folder)
    ImageQue.thread_handler(folder_path, os.path.join(folder_path, "preview"))


def image_generation(folder: str, img: str) -> None:
    # start image creation
    img_path = os.path.join(os.getcwd(), "blueprint_logos", folder, img)
    preview_path = os.path.join(os.getcwd(), "blueprint_logos", folder, "preview")
    if not os.path.exists(preview_path):
        os.makedirs(preview_path)
    config = load_img_con(folder, img)
    logo_handler.preview(preview_path, img_path, config[0][1], config[1][1])


if __name__ == "__main__":
    image_generation("season1", "Slone001 Fruchtlabor.png", {"distance": 20, "angle": 45})

