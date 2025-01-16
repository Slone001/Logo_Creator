from PIL import Image, ImageDraw, ImageFont, ImageFilter
from data import logo_handler
import sys
import math

font_path = "data/files/Hitmo2.0-Bold.ttf"


def logo_comb(logo_path: list | None = None):
    if logo_path is None:
        logo_path = []
    for logo_name in logo_path:
        logo = Image.open(logo_name).convert("RGBA")
        logo_name = logo_name.split("\\")[-1]
        size = logo.size
        canvas = quader(size[0], size[1])
        canvas = canvas.convert("RGBA")
        logo.paste(canvas, (0, 0), canvas)
        logo.save(f"finished_logos/{logo_name}_wm.png")


def quader(canvas_width, canvas_height, text: str = "Nimm mich!", font_size: int = 200) -> Image:
    canvas = Image.new("RGBA", (canvas_width, canvas_height), (255, 255, 255, 0))

    blue_rectangle = Image.new("RGBA", (canvas_width, canvas_height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(blue_rectangle)

    rect_x0, rect_y0 = (0, 0)  # Top-left corner
    rect_x1, rect_y1 = canvas_width, canvas_height  # Bottom-right corner
    blue_color = (20, 100, 255, 192)  # Blue with 75% transparency (R, G, B, Alpha)

    draw.rectangle([(rect_x0, rect_y0), (rect_x1, rect_y1)], fill=blue_color)

    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print("Font file not found. Make sure the font path is correct.")
        exit()

    # Measure the text size using getbbox()
    text_bbox = font.getbbox(text)  # Returns (left, top, right, bottom)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # Center the text in the rectangle
    text_x = (rect_x0 + rect_x1 - text_width) // 2  # Center horizontally
    text_y = (rect_y0 + rect_y1 - text_height) // 2  # Center vertically

    # Create a mask for the text
    mask = Image.new("L", (canvas_width, canvas_height), 0)  # Black and white mask
    mask_draw = ImageDraw.Draw(mask)

    # Draw the text onto the mask (white areas will be transparent in the final image)
    mask_draw.text((text_x, text_y), text, fill=255, font=font)

    # Apply the mask to "cut out" the text area from the rectangle
    blue_rectangle = Image.composite(canvas, blue_rectangle, mask)

    # Paste the result onto the main canvas
    canvas.paste(blue_rectangle, (0, 0))

    # Save the result
    # canvas.save("transparent_text_on_blue_quader.png")
    # print("Image saved as 'transparent_text_on_blue_quader.png'")

    return canvas


def named_logo(logo_list: list[str] | str):
    # todo: logo text outsourcing in other func
    # todo: add multithreading
    text_y = 200  # position y, position x will be calculated automatically
    count = 1
    distance = 20
    angle = 45
    Image_list: list[Image] = []
    logo: Image
    if type(logo_list) == str:
        print(f"{count} {logo_list.split("\\")[-1]}")
        Image_list.append(Image.open(logo_list).convert("RGBA"))
    else:
        for logo_name in logo_list:
            print(f"{count} {logo_name.split("\\")[-1]}")
            Image_list.append(Image.open(logo_name).convert("RGBA"))
            count += 1
        del count
    names = input("Name von Member und dahinter mit Doppelpunkt die Nummern von den Logos, bsp: Slone 1 3,:\n")
    names = names.rstrip().lstrip().split(',')
    for name in names:
        args = name.split(" ")
        print(args)
        text = logo_handler.add_letters_until_number(args).lstrip().rstrip()
        for arg in reversed(args):
            font_size = 200
            try:
                logo = Image_list[int(arg) - 1]
                print(arg)
                logo_width, logo_height = logo.size
            except ValueError:
                break
            font = ImageFont.truetype(font_path, font_size)

            shadow_layer = Image.new("RGBA", logo.size, (0, 0, 0, 0))

            # Calculate shadow offset based on angle and distance
            shadow_offset_x = int(distance * math.cos(math.radians(angle)))
            shadow_offset_y = int(distance * math.sin(math.radians(angle)))

            # Measure the text size and calculate position

            # Draw the main text on top of the shadow
            text_overlay = Image.new("RGBA", logo.size, (255, 255, 255, 0))
            text_draw = ImageDraw.Draw(text_overlay)

            # Measure the text size
            text_bbox = text_draw.textbbox((0, 0), text, font=font)
            text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]

            # Check if the text fits; adjust font size if necessary
            while text_width > logo_width or text_height > logo_height:
                font_size -= 1  # Decrease font size
                font = ImageFont.truetype(font_path, font_size)
                text_bbox = text_draw.textbbox((0, 0), text, font=font)
                text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]

            text_x = (logo_width - text_width) // 2
            text_draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255, 255))

            draw = ImageDraw.Draw(shadow_layer)
            # Draw the shadow text at the offset position
            shadow_color = (0, 0, 0, 128)  # Semi-transparent black
            draw.text((text_x + shadow_offset_x, text_y + shadow_offset_y), text, font=font, fill=shadow_color)

            # Apply blur to the shadow for a smoother fade
            shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(10))

            # Combine the layers with the logo
            combined = Image.alpha_composite(logo, shadow_layer)
            combined = Image.alpha_composite(combined, text_overlay)

            # combined = Image.alpha_composite(logo, overlay)
            # todo: error if there are special chars in the name --> check for name_string
            filename = logo_handler.file_checker(
                f"finished_logos/{logo_list[int(arg) - 1].split("\\")[-1][:-4]} {text}.png")
            combined.save(filename, format="PNG")


if __name__ == '__main__':
    canvas_wh = (2084, 300)  # (4167, 800)

    if not logo_handler.path_creation():
        print(f"error while path creating")
        exit()
    Auswahl = input(f"1=Watermark, 2=Namensgebung: ")
    if Auswahl == "1":
        if len(sys.argv) > 1:
            logos = sys.argv[1:]
            logo_comb(logos)
    if Auswahl == "2":
        if len(sys.argv) > 1:
            logos = sys.argv[1:]
            named_logo(logos)
    if Auswahl == "3":
        logo_handler.change_logo_color()
