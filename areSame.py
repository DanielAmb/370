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

# from PIL import Image
# from collections import Counter

# def get_main_color(image_path, num_colors=10):
#     # Open the image
#     img = Image.open(image_path)

#     # Resize the image to reduce the number of pixels
#     img = img.resize((150, 150))

#     # Convert image to RGB mode (in case it's in another mode)
#     img = img.convert("RGB")

#     # Get all pixels from the image
#     pixels = list(img.getdata())

#     # Count the frequency of each color in the image
#     color_count = Counter(pixels)

#     # Get the most common color
#     most_common_colors = color_count.most_common(num_colors)

#     # Return the most common color
#     return most_common_colors[0][0] if num_colors == 1 else most_common_colors

# # Usage example
# main_color = get_main_color('370/sweater2.jpg')
# print("Main color (R, G, B):", main_color)

# import numpy as np
# import cv2
# from PIL import Image
# import matplotlib.pyplot as plt
# from sklearn.cluster import KMeans


# new_image = plt.imread('370/sweater.jpg')
# flat_img = np.reshape(new_image,(-1,3))
# kmeans = KMeans(n_clusters=5,random_state=0)
# kmeans.fit(flat_img)
# print(kmeans)
# img = plt.imshow(kmeans)
# plt.show()
# flat_img = np.reshape(img,(-1,3))
# cv2.imwrite("my_image5.jpg", img)

######################################################################
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans

# Assuming you already have new_image and flat_img defined
new_image = plt.imread('370/sweater2.jpg')
flat_img = np.reshape(new_image, (-1, 3))

# KMeans clustering
kmeans = KMeans(n_clusters=5, random_state=0)
kmeans.fit(flat_img)

# Display the cluster centers (dominant colors)
cluster_centers = kmeans.cluster_centers_
print("Cluster Centers (Dominant Colors):")
print(cluster_centers)

percentages = (np.unique(kmeans.labels_,return_counts=True)[1])/flat_img.shape[0]
# p_and_c = zip(percentages,dominant_colors)
print(percentages)
# print(list(zip(percentages,cluster_centers)))
######################################################################

# import webcolors

# def get_colour_name(rgb_triplet):
#     # full list: https://www.w3schools.com/tags/ref_colornames.asp
#     myColors = {
#         "red"     : "#ff0000", # R
#         "orange"  : "#ffa500", # O
#         "yellow"  : "#ffff00", # Y
#         "green"   : "#008000", # G
#         "blue"    : "#0000ff", # B
#         "magenta" : "#ff00ff", # I
#         "purple"  : "#800080", # V
#         "black"   : "#000000", # B
#         "white"   : "#FFFFFF", # W
        
#         "coral"   : "#ff7f50", # light red
#         "maroon"  : "#800000", # dark red
#         "navy"    : "#000080", # dark blue
#         "cyan"    : "#00ffff", # light blue
#         "gold"    : "#ffd700", # dark yellow
#         "lime"    : "#00ff00", # bright green
#         "jade"    : "#00a36c", # light green
#         "olive"   : "#808000", # dark green
#         "grey"    : "#808080" }
        
#     min_colours = {}
#     for name, hex_val in myColors.items():
#         r_c, g_c, b_c = webcolors.hex_to_rgb(hex_val)
#         rd = (r_c - rgb_triplet[0]) ** 2
#         gd = (g_c - rgb_triplet[1]) ** 2
#         bd = (b_c - rgb_triplet[2]) ** 2
#         min_colours[(rd + gd + bd)] = name
    
#     return min_colours[min(min_colours.keys())]


# # # what is the name for this kml color???
# # kml_color='ff00eb00' # this is kml for green

# # # kml colors are non-standard: aabbggrr    (alpha, blue, green, red)
# # def kml_color_to_rgba(kml_color):
# #     # convert kml color to standard RGB's and alpha
# #     alpha=int( kml_color[0:2] , 16)
# #     blu  =int( kml_color[2:4] , 16) # convert 2-place hex into 16-bit int
# #     grn  =int( kml_color[4:6] , 16)
# #     red  =int( kml_color[6:]  , 16)
# #     print(f'kml_color={kml_color} --> RGB=({red},{grn},{blu}), alpha={alpha}')
# #     return red,grn,blu,alpha


# # rgba = kml_color_to_rgba(kml_color)
# rgb = tuple([36,34,38])

# closest_colorname = get_colour_name(rgb)
# print(f'the closest CSS color to , which is RGBA={rgb} is {closest_colorname}')