import numpy as np
import cv2
import os
import json

def main():
    print("Running...")
    work_dir = os.getcwd()
    movie_settings = load_settings(work_dir)

    if movie_settings.__len__() == 0:
       print("No settings file!")
       exit(0)

    in_path = movie_settings["align_in_path"]
    out_path = movie_settings["align_out_path"]

    dir_list = os.listdir(in_path)
    img_names = []
    img_paths = []
    in_img_list = []

    for file_name in dir_list:
        if file_name.lower().endswith('cactus.jpg'):
            print("Loading file: " + file_name)
            img_names.append(file_name)
            full_img_path = os.path.join(in_path, file_name)
            img_paths.append(full_img_path)
            in_img_list.append(cv2.imread(full_img_path))

    if in_img_list.__len__() > 0:
        processed_img_list = crop_cactus(in_img_list)

    if processed_img_list.__len__() > 0:
        for i in range(0, processed_img_list.__len__()):
            print("Writing image: "  + img_names[i])
            full_out_path = os.path.join(out_path, img_names[i])
            cv2.imwrite(full_out_path, processed_img_list[i])

    print("Done!")

def crop_cactus(images):
    cropped_images = []

    print("Image shape: ", images[0].shape)
    hsv_images = [cv2.cvtColor(img, cv2.COLOR_BGR2HSV) for img in images]

    # These get the cactus on blue background; lime green not so much.
    lower_blue = np.array([45, 50, 50])  # Adjust as needed
    upper_blue = np.array([72, 255, 255])

    #These get the blue background.
    # lower_blue = np.array([90, 50, 50])  # Adjust as needed
    # upper_blue = np.array([130, 255, 255])

    for i in range(len(hsv_images)):  # Start loop at 0 to process all images
        # Create a mask based on the HSV bounds
        mask = cv2.inRange(hsv_images[i], lower_blue, upper_blue)
        # cv2.imshow("Mask", mask)

        # Apply the mask to the original BGR image (not HSV image)
        # cropped_img = cv2.bitwise_and(images[i], images[i], mask=mask)
        # cropped_images.append(cropped_img)
        cropped_images.append(mask)

    return cropped_images

def visualize_matches(img1, img2, kp1, kp2, good_matches):
    # Create a copy of img1 to draw on
    match_img = img2.copy()

    # Draw small crosses for good matches
    for match in good_matches:
        x, y = map(int, kp1[match.queryIdx].pt)
        cv2.drawMarker(match_img, (x, y), (0, 255, 0), cv2.MARKER_CROSS, 10, 2)

    return match_img

def load_settings(settings_dir):
    return get_json_file(os.path.join(settings_dir, "movie_settings.json"))

def get_json_file(json_path):
    js_dict = dict()

    try:
        with open(json_path, 'r') as json_file:
            file_contents = json_file.read()
            js_dict = json.loads(file_contents)
    except:
        print("Error opening file at location: " + json_path)

    return js_dict

if __name__ == '__main__':
    main()
