from PIL import Image


def change_logo_color():
    logoname = input("Logo name: ")
    logo = Image.open(logoname).convert("RGBA")
    new_color = (255, 0, 0, 255)  # Red (R, G, B, A)
    colored_logo = Image.new("RGBA", logo.size, new_color)
    logo_with_new_color = Image.composite(colored_logo, logo, logo)
    logo_with_new_color.save("finished_logos/colored_logo.png")
    print("Logo color changed and saved as 'colored_logo.png'")
