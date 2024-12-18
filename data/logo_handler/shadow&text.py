from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import sys
import math
from data.logo_handler import logo_handler as lh

def shadow_handler(size: tuple[int, int], shadow):
    shadow_layer = Image.new("RGBA", size, (0, 0, 0, 0))

    # Calculate shadow offset based on angle and distance
    shadow_offset_x = int(shadow[0] * math.cos(math.radians(shadow[1])))
    shadow_offset_y = int(shadow[0] * math.sin(math.radians(shadow[1])))



def logo_shadow_preview(img, shadow: tuple[int | int]):

    image = Image.open(img).convert("RGBA")

    font = ImageFont.truetype(lh.font_path, lh.size)


