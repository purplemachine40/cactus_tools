import numpy as np
import cv2
import os
import json
import sys

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

    template_img = cv2.imread(os.path.join(in_path, "template.jpg"))
    if template_img is None:
        print("No template image.")
        sys.exit(1)

    processed_img_list = []
    if in_img_list.__len__() > 0:
        template_img_list, rect_img_list, final_img_list = template_cactus(in_img_list, template_img)
        processed_img_list = final_img_list.copy()

    if processed_img_list.__len__() > 0:
        for i in range(0, processed_img_list.__len__()):
            print("Writing image: "  + img_names[i])
            full_out_path = os.path.join(out_path, img_names[i])
            cv2.imwrite(full_out_path, processed_img_list[i])

    print("Done!")

def template_cactus(images, template):
    grayscale_match_images = []
    match_rect_images = []
    shifted_images = []
    output_images = []
    template_loc = []
    final_img_loc = []
    template_wt = template.shape[1]
    template_ht = template.shape[0]
    img_wt = images[0].shape[1]
    img_ht = images[0].shape[0]
    background_wt = img_wt + 300
    background_ht = img_ht + 300
    base_x = 150
    base_y = 150
    max_start_x = 0
    min_start_x = background_wt
    max_start_y = 0
    min_start_y = background_ht

    # This commented out code makes a mask that can be used to constrain the match area.
    # Note that in the OpenCV coordinate system, (0,0) is top left corner of the image.
    # img_ht, img_wt, img_channels = images[0].shape
    # print("Image width: %d, height: %d " % (img_wt, img_ht))
    # mask_wt, mask_ht = 260, 260
    # mask_start_x = ((img_wt - mask_wt) // 2) - 50
    # mask_start_y = img_ht - mask_ht - 140
    # mask = np.zeros((img_ht, img_wt), dtype=np.uint8)
    # mask[mask_start_y:mask_start_y + mask_ht, mask_start_x:mask_start_x + mask_wt] = 255

    for img in images:
        # This commented out code draws a rectangle around the masked area so you can check placement of the mask.
        # overlay_img = img.copy()
        # cv2.rectangle(overlay_img, (mask_start_x, mask_start_y), (mask_start_x + mask_wt, mask_start_y + mask_ht), (0, 255, 0), 2)
        # output_images.append(overlay_img)

        result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        min_val, maxval, min_loc, max_loc = cv2.minMaxLoc(result);
        template_loc.append(max_loc)
        top_left = max_loc
        print("max_loc: ", max_loc)
        bottom_right = (top_left[0] + template_wt, top_left[1] + template_ht)
        temp_img = img.copy()
        cv2.rectangle(temp_img, top_left, bottom_right, (0, 255, 0), 2)
        match_rect_images.append(temp_img)
        normalized_result = cv2.normalize(result, None, 0, 255, cv2.NORM_MINMAX)
        result_as_uint8 = np.uint8(normalized_result)
        grayscale_match_images.append(result_as_uint8)

    # template_loc has the location of the top right corner of the template on all images.
    # Using the first image as the base, shift all other images so their template locations align with the base location.

    for i in range(1, template_loc.__len__()):
        tl = template_loc[i]
        # print("Template Loc x: %d Template Loc y: %d" % (tl[0], tl[1]))
        x_dif = template_loc[i][0] - template_loc[0][0]
        y_dif = template_loc[i][1] - template_loc[0][1]
        print("x_dif: %d, y_dif: %d" % (x_dif, y_dif))

        # Might have a pic or two where the template did not work well, causing a larger than acceptable offset.
        # Don't include those pics in the output.

        if abs(x_dif) < base_x:
            placement_x = base_x - x_dif
        else:
            print("x_dif of picture index %d is out of range." % i)
            continue

        if abs(y_dif) < base_y:
            placement_y = base_y - y_dif
        else:
            print("y_dif of picture index %d is out of range." % i)
            continue

        print("placement_x: %d, placement_y: %d" % (placement_x, placement_y))
        max_start_x = max(max_start_x, placement_x)
        max_start_y = max(max_start_y, placement_y)
        min_start_x = min(min_start_x, placement_x)
        min_start_y = min(min_start_y, placement_y)
        final_img_loc.append((placement_y, placement_x))
        background = np.full((background_ht, background_wt, 3), (255, 255, 255), dtype=np.uint8)
        background[placement_y:placement_y + img_ht, placement_x:placement_x + img_wt] = images[i]
        shifted_images.append(background)

    # Now crop the shifted images so there is no whitespace

    crop_x = max_start_x
    crop_wt = img_wt - (max_start_x - min_start_x)
    crop_y = max_start_y
    crop_ht = img_ht - (max_start_y - min_start_y)

    for img in shifted_images:
        cropped_img = img[crop_y:crop_y + crop_ht, crop_x:crop_x + crop_wt]
        output_images.append(cropped_img)

    return grayscale_match_images, match_rect_images, output_images

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
