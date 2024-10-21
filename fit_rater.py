from ultralytics import YOLO
import cv2
import json
import fit_metrics as metrics
import os
import numpy as np
from scipy.spatial import KDTree
import webcolors
import matplotlib.pyplot as plt

# def get_colour_name(bgr_tuple):
#     min_colours = {}
#     for name in webcolors.names("css3"):
#         r_c, g_c, b_c = webcolors.name_to_rgb(name)
#         rd = (r_c - bgr_tuple[2]) ** 2
#         gd = (g_c - bgr_tuple[1]) ** 2
#         bd = (b_c - bgr_tuple[0]) ** 2
#         min_colours[(rd + gd + bd)] = name
#     return min_colours[min(min_colours.keys())]

def get_colour_name(bgr_tuple):
    # add colors: https://www.w3schools.com/tags/ref_colornames.asp
    myColors = {
        "red"     : "#ff0000", # R
        "orange"  : "#ffa500", # O
        "yellow"  : "#ffff00", # Y
        "green"   : "#008000", # G
        "blue"    : "#0000ff", # B
        "magenta" : "#ff00ff", # I
        "purple"  : "#800080", # V
        "black"   : "#000000", # B
        "white"   : "#FFFFFF", # W
        "pink"    : "#FFC0CB",
        "grey"    : "#808080" 
        # "light blue"    : "#ADD8E6", 
        
        # # "coral"   : "#ff7f50", # light red
        # "maroon"  : "#800000", # dark red
        # "navy"    : "#000080", # dark blue
        # "cyan"    : "#00ffff", # light blue
        # "gold"    : "#ffd700", # dark yellow
        # "lime"    : "#00ff00", # bright green
        # "jade"    : "#00a36c", # light green
        # "olive"   : "#808000", # dark green
        }
        
    min_colours = {}
    for name, hex_val in myColors.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(hex_val)
        rd = (r_c - bgr_tuple[2]) ** 2
        gd = (g_c - bgr_tuple[1]) ** 2
        bd = (b_c - bgr_tuple[0]) ** 2
        min_colours[(rd + gd + bd)] = name
    
    return min_colours[min(min_colours.keys())]

def generateRating(img, outfit):
    main_colors = []
    only_colors = []
    complexities = []
    aesthetics = {"neutral":0, "gloomy":0, "vibrant":0}
    incompatibilities = []
    for category, bbox in outfit:
        cropped_article = metrics.cropToBbox(img, bbox)
        complexities.append(metrics.get_complexity(cropped_article))
        colors = metrics.get_colors(cropped_article)
        print(colors)
        main_colors.append((category, colors[0]))
        only_colors.append((colors[0]))

    i = 0
    for category, color in main_colors: 
        print(str(category) + ": " + str(get_colour_name(color)) + ". Complexity = " + str(complexities[i]) + "\n")
        i += 1
    
    print("Aesthetic: " + str(metrics.getAesthetic(only_colors)) + "\n")
    
    for color in only_colors:
        print("Gloomy: " + str(metrics.isGloomy(color)))
        print("Neutral: " + str(metrics.isNeutral(color)))
        print("Bright: " + str(metrics.isBright(color)))
        print("Vibrant: " + str(metrics.isVibrant(color)))
        print("Grey: " + str(not metrics.is_not_grey(color)) + "\n")


    if len(main_colors) < 1:
        print("Nothing discernible. Dress up and try again.")
        exit()
   
    print("Overall Complexity: " + str(np.mean(complexities)*100) + " %")

    errors = []
    for _, c1 in main_colors:
        for _, c2 in main_colors:
            if not metrics.areCompatible(c1, c2): 
                errors.append((get_colour_name(c1), get_colour_name(c2)))
    print("When it comes to color theory, you made " + str(len(errors)) + " mistakes.")
    if len(errors) > 0:
        print("Those were the following color pairs: " + str(errors) + "... Maybe take some notes for next time. ")
    else:
        print("Congrats! ")

    return ''
    
def rate_my_fit(filepath):
    img = cv2.imread(filepath)
    if have_a_model:
        pred = model(img)
        outfit = []
        for results in pred:
            box = results.boxes.numpy()
            for b in box:
                bbox = list(b.xywh[0])
                h, w, channels = img.shape
                bbox[0] *= 1/w
                bbox[1] *= 1/h
                bbox[2] *= 1/w
                bbox[3] *= 1/h
                class_name = names[int(list(b.cls)[0])]
                if float(list(b.conf)[0]) > 0.65:
                    outfit.append((class_name, bbox))
    else:
        print('Error: No Model Detected.')
        exit()
        
    text = generateRating(img, outfit)
    
    for class_name, bbox in outfit:
        img = metrics.visualize_bbox(img, bbox, class_name)
    # os.remove(filepath)
    return img, text

pwd = os.path.realpath(os.path.dirname(__file__))
names = ["short-sleeve shirt", "long-sleeve shirt", "short-sleeveoutwear", "long-sleeveoutwear", "pair of shorts", "pair of pants", "skirt", "hat", "shoe"]

model = YOLO(pwd + "/best.pt")  # load a model
have_a_model = True

cv2.imwrite("my_image.jpg", rate_my_fit(pwd + "/pink.jpg"))

# DeepFashion
# https://www.kaggle.com/datasets/vishalbsadanand/deepfashion-1?resource=download
