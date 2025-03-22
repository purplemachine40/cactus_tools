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

    if in_img_list.__len__() > 0:
        processed_img_list = template_cactus(in_img_list, template_img)

    if processed_img_list.__len__() > 0:
        for i in range(0, processed_img_list.__len__()):
            print("Writing image: "  + img_names[i])
            full_out_path = os.path.join(out_path, img_names[i])
            cv2.imwrite(full_out_path, processed_img_list[i])

    print("Done!")

def template_cactus(images, template):
    output_images = []

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
        #This commented out code draws a rectangle around the masked area so you can check placement of the mask.
        # overlay_img = img.copy()
        # cv2.rectangle(overlay_img, (mask_start_x, mask_start_y), (mask_start_x + mask_wt, mask_start_y + mask_ht), (0, 255, 0), 2)
        # output_images.append(overlay_img)

        result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        normalized_result = cv2.normalize(result, None, 0, 255, cv2.NORM_MINMAX)
        result_as_uint8 = np.uint8(normalized_result)
        output_images.append(result_as_uint8)

    return output_images

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
