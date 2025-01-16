from PIL import Image, ImageDraw, ImageFont, ImageFilter
from data import logo_handler
import math
import threading
import time

class imageQue:

    maxThread = 8

    def __init__(self):
        self.active_threads: list[tuple[str | threading.Thread]] = []
        self.queue: list[tuple[str | threading.Thread]] = []
        thread_Checker = threading.Thread(target=self.check_active_threads)

    def check_active_threads(self):
        while True:
            for element in self.active_threads:
                if not element[1].is_alive():
                    self.active_threads.remove(element)
            self.que_handler()
            time.sleep(5)

    def que_handler(self):
        if not len(self.active_threads) <= self.maxThread:
            return
        if self.queue is None:
            return
        for element in self.queue:
            element[1].start()
            self.active_threads.append(element)
            self.queue.remove(element)
            if len(self.active_threads) >= self.maxThread:
                return

    def thread_handler(self, preview_path, logo_path, distance, angle, prio: False):
        if preview_path in self.active_threads:
            self.active_threads.index(preview_path)
            # todo: regenerating pictures
        else:
            self.start_thread(prio, preview_path, logo_path, distance, angle)

    def start_thread(self, *args):
        thread = threading.Thread(target=logo_handler.preview, args=args[1:])
        data: tuple[str | threading.Thread] = args[1], thread
        if args[0] or len(self.active_threads) < self.maxThread:
            thread.start()
            self.active_threads.append(data)
        else:
            self.queue.append(data)


def preview(preview_path, logo_path, distance: int, angle: int):
    # todo: logo text outsourcing in other func
    # todo: add multithreading
    logo = Image.open(logo_path).convert("RGBA")
    shadow_layer, text_overlay = shadow(logo, distance, angle)
    logo_save(logo, shadow_layer, text_overlay, f"{preview_path}/{logo_path.split('\\')[-1]}")


def logo_gen(logo_list: list[str], distance: int, angle: int, names: list[str]):
    # todo: logo text outsourcing in other func
    # todo: add multithreading
    Image_list: list[Image] = []

    for logo_name in logo_list:
        Image_list.append(Image.open(logo_name).convert("RGBA"))

    for name in names:
        for logo in Image_list:
            shadow_layer, text_overlay = shadow(logo, distance, angle, name)
            filename = logo_handler.file_checker(f"finished_logos/{logo.filename().split('\\')[-1]}_{name}")
            logo_save(logo, shadow_layer, text_overlay, filename)


def shadow(logo: Image, distance: int, angle: int, text="FruchtLabor"):
    text_y = logo_handler.logo_handler.t_high  # position y, position x will be calculated automatically
    font_size = 200

    logo_width, logo_height = logo.size
    font = ImageFont.truetype(logo_handler.logo_handler.font_path , font_size)

    shadow_layer = Image.new("RGBA", logo.size, (0, 0, 0, 0))

    # Calculate shadow offset based on angle and distance
    shadow_offset_x = int(distance * math.cos(math.radians(angle)))
    shadow_offset_y = int(distance * math.sin(math.radians(angle)))

    text_overlay = Image.new("RGBA", logo.size, (255, 255, 255, 0))
    text_draw = ImageDraw.Draw(text_overlay)

    # Measure the text size
    text_bbox = text_draw.textbbox((0, 0), text, font=font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]

    # Check if the text fits; adjust font size if necessary
    while text_width > logo_width or text_height > logo_height:
        font_size -= 1  # Decrease font size
        font = ImageFont.truetype(logo_handler.logo_handler.font_path, font_size)
        text_bbox = text_draw.textbbox((0, 0), text, font=font)
        text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]

    text_x = (logo_width - text_width) // 2
    text_draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255, 255))

    draw = ImageDraw.Draw(shadow_layer)
    # Draw the shadow text at the offset position
    shadow_color = (0, 0, 0, 128)  # Semi-transparent black
    draw.text((text_x + shadow_offset_x, text_y + shadow_offset_y), text, font=font, fill=shadow_color)

    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(10))

    return shadow_layer, text_overlay


def logo_save(logo, shadow_layer, text_overlay, filename: str):
    # Combine the layers with the logo
    combined = Image.alpha_composite(logo, shadow_layer)
    combined = Image.alpha_composite(combined, text_overlay)

    # combined = Image.alpha_composite(logo, overlay)
    # todo: error if there are special chars in the name --> check for name_string
    combined.save(filename, format="PNG")
