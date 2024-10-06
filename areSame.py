# import math
# import torch

# def areTheSame(c1, c2, tolerance=20):    
#     # Convert RGB to XYZ color space
#     def rgb_to_xyz(rgb):
#         r, g, b = [x / 255.0 for x in rgb]
#         r = r ** 2.2
#         g = g ** 2.2
#         b = b ** 2.2
        
#         x = r * 0.4124564 + g * 0.3575761 + b * 0.1804375
#         y = r * 0.2126729 + g * 0.7151522 + b * 0.0721750
#         z = r * 0.0193339 + g * 0.1191920 + b * 0.9503041
#         return (x, y, z)

#     # Calculate Delta E
#     def delta_e(c1, c2):
#         x1, y1, z1 = rgb_to_xyz(c1)
#         x2, y2, z2 = rgb_to_xyz(c2)
#         return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)
    
#     delta_e_value = delta_e(c1, c2)
#     print(delta_e_value * 100)
    
#     return (delta_e_value * 100) < tolerance

# # Example usage
# color1 = (0, 255, 0)  # Red
# color2 = (0, 230, 0)  # A slightly different red
# tolerance = 20

# print(areTheSame(color1, color2, tolerance))  # Output: True or False

# print(torch.load("370/best.pt"))

from PIL import Image
from collections import Counter

def get_main_color(image_path, num_colors=10):
    # Open the image
    img = Image.open(image_path)

    # Resize the image to reduce the number of pixels
    img = img.resize((150, 150))

    # Convert image to RGB mode (in case it's in another mode)
    img = img.convert("RGB")

    # Get all pixels from the image
    pixels = list(img.getdata())

    # Count the frequency of each color in the image
    color_count = Counter(pixels)

    # Get the most common color
    most_common_colors = color_count.most_common(num_colors)

    # Return the most common color
    return most_common_colors[0][0] if num_colors == 1 else most_common_colors

# Usage example
main_color = get_main_color('370/sweater2.jpg')
print("Main color (R, G, B):", main_color)