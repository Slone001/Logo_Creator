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

