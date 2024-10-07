from ultralytics import YOLO
import cv2
import json
import fit_metrics as metrics
import os
import numpy as np
from scipy.spatial import KDTree
import webcolors

def convert_bgr_to_name(bgr_tuple):
    min_colours = {}
    for name in webcolors.names("css3"):
        r_c, g_c, b_c = webcolors.name_to_rgb(name)
        rd = (r_c - bgr_tuple[0]) ** 2
        gd = (g_c - bgr_tuple[1]) ** 2
        bd = (b_c - bgr_tuple[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]
    # rgb_tuple = (bgr_tuple[2], bgr_tuple[1], bgr_tuple[0])
    # # a dictionary of all the hex and their respective names in css3
    # css3_db = webcolors.names("css3")
    # names = []
    # rgb_values = []
    # for color_hex, color_name in css3_db:
    #     names.append(color_name)
    #     rgb_values.append(webcolors.hex_to_rgb(color_hex))
    
    # kdt_db = KDTree(rgb_values)
    # distance, index = kdt_db.query(rgb_tuple)
    # return str(names[index])
    

def generateRating(img, outfit):
    """
    Returns a string describing the rating of a particular outfit
    """
    main_colors = []
    strong_colors = []
    complexities = []
    aesthetics = {"neutral":0, "gloomy":0, "vibrant":0}
    incompatibilities = []
    for category, bbox in outfit:
        cropped_article = metrics.cropToBbox(img, bbox)
        complexities.append(metrics.get_complexity(cropped_article))
        colors = metrics.get_colors(cropped_article)
        main_colors.append((category, colors[0]))
        for c in colors:
            if not metrics.isNeutral(c):
                add = True
                for strongC in strong_colors:
                    if metrics.areTheSame(strongC, c): add = False
                if add: strong_colors.append(c)
        aesthetics[metrics.getAesthetic(colors)] += 1

    out = "After careful analysis of your fit, I came to the following conclusions: You've got on "
    if len(main_colors) > 1:
        out += "a"
        for category, color in main_colors[:-1]:
            # print("\n            " + str(color) + "            \n")
            out += " " + convert_bgr_to_name(color) + " " + category + ", a"
        print("\n            " + str(main_colors[0][1]) + "            \n")
        print(colors)
        print("\n            " + str(main_colors[1][1]) + "            \n")
        out += "nd a " + convert_bgr_to_name(main_colors[-1][1]) + " " + main_colors[-1][0] + ". "
    elif len(main_colors) == 1:
        # print("\n            " + str(main_colors[0][1]) + "            \n")
        out += "a " + convert_bgr_to_name(main_colors[0][1]) + " " + main_colors[0][0] + ". "
    else: 
        out += "nothing discernible. Dress up and try again."
        return out
    out += " The overall complexity of the patterns in your outfit were scored at " + str(np.mean(complexities)*100) + " percent, "
    if np.mean(complexities) > 0.7: out += "a bit high for my liking... Maybe throw in some solid colors? "
    elif np.mean(complexities) < 0.3: out += "which is pretty low... Try spicing it up with some fun patterns next time. "
    else: "a very reasonable score. Keep up the good work. "

    out += "In terms of your color palette, "
    if len(strong_colors) > 3: out += "I noticed that you've opted for not one, not two, but " + str(len(strong_colors)) + " bold colors for your fit. While I commend your creativity, you should consider throwing in some muted tones as well...X"
    elif len(strong_colors) == 0: out += "I couldn't help but notice you've only chosen neutral colors today. A splash of color would do you wonders! "
    else: " you've got a good balance of bold colors in your fit. "

    errors = []
    for _, c1 in main_colors:
        for _, c2 in main_colors:
            if not metrics.areCompatible(c1, c2): 
                errors.append((convert_bgr_to_name(c1), convert_bgr_to_name(c2)))
    out += "When it comes to color theory, you made " + str(len(errors)) + " mistakes. "
    if len(errors) > 0:
        out += "Those were the following color pairs: " + str(errors) + "... Maybe take some notes for next time. "
    else:
        out += "Congrats! "


    if len(incompatibilities) > 1:
        for inc in incompatibilities[:-1]:
            out += "Maybe you should re-think wearing the " + str(inc) + ", "
        out += "and " + incompatibilities[-1] + "."
    elif len(incompatibilities) == 1:
        out += "Maybe you should re-think wearing the " + str(incompatibilities[0]) + "... "
    else:
        out += "I think your fit will do just fine. "
    
    gloomCount = 100*aesthetics["gloomy"]/len(outfit)
    vibCount = 100*aesthetics["vibrant"]/len(outfit)
    neutralCount = 100*aesthetics["neutral"]/len(outfit)

    out += "Anyway, I've scored your vibe as " + str(gloomCount) + " percent gloomy, " + str(vibCount) + " percent bubbly, and " + str(neutralCount) + " percent boring. Keep up the good work!"
    
    return out
    
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
        print('Error')
        exit()
    # return outfit
    text = generateRating(img, outfit)
    print(text)
    for class_name, bbox in outfit:
        img = metrics.visualize_bbox(img, bbox, class_name)
    #delete filepath
    # os.remove(filepath)
    return img
    # return img, text

pwd = os.path.realpath(os.path.dirname(__file__))
names = ["short-sleeve shirt", "long-sleeve shirt", "short-sleeveoutwear", "long-sleeveoutwear", "pair of shorts", "pair of pants", "skirt", "hat", "shoe"]
# Load a model
model = YOLO(pwd + "/best.pt")  # load a model
have_a_model = True

cv2.imwrite("my_image.jpg", rate_my_fit(pwd + "/pink.jpg"))
# print(imread(pwd + "/none.jpg"))


