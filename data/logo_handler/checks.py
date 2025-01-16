import os


def path_creation() -> bool:
    try:
        if not os.path.exists("logos/"):
            os.mkdir("logos/")
        if not os.path.exists("finished_logos/"):
            os.mkdir("finished_logos/")
        if not os.path.exists("backgrounds/"):
            os.mkdir("backgrounds/")
        return True
    except Exception as e:
        print(e)
        return False


def file_checker(filename):
    num = 0
    base, ext = os.path.splitext(filename)
    while True:
        if num == 1:
            base = f"{base} ({num})"
        if num >= 2:
            base = f"{base[:-4]} ({num})"
        if not os.path.exists(f"{base}.png"):
            return f"{base}.png"
        num += 1


def add_letters_until_number(elements):
    result = ""

    for element in elements:
        # Check if the string is purely numeric
        if element.isnumeric() or element.replace('.', '', 1).isnumeric():
            break  # Stop when encountering a purely numeric string

        # Add the element to the result
        result += f"{element} "

    return result


def idk():
    # Check if needed for future project
    shadow = Image.new("RGBA", logo.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)

    # Draw the shadow as solid black below the text
    shadow_y = text_y + text_height + 5  # Shadow starts below the text
    shadow_height = 20  # Height of the shadow gradient
    max_alpha = 192

    for i in range(shadow_height):
        alpha = int(max_alpha * (1 - i / shadow_height))  # Gradually reduce opacity
        shadow_draw.rectangle(
            [text_x, shadow_y + i, text_x + text_width, shadow_y + i + 1],
            fill=(0, 0, 0, alpha)
        )

    # Blur the shadow for a smoother effect
    shadow = shadow.filter(ImageFilter.GaussianBlur(5))




