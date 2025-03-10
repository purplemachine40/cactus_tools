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

    in_path = movie_settings["raw_in_path"]
    out_path = movie_settings["align_in_path"]

    dir_list = os.listdir(in_path)
    img_names = []
    img_paths = []
    in_img_list = []

    for file_name in dir_list:
        if file_name.lower().endswith('.jpg'):
            print("Loading file: " + file_name)
            img_names.append(file_name)
            full_img_path = os.path.join(in_path, file_name)
            img_paths.append(full_img_path)
            in_img_list.append(cv2.imread(full_img_path))

    if in_img_list.__len__() > 0:
        processed_img_list = scale_images(in_img_list)

    if processed_img_list.__len__() > 0:
        for i in range(0, processed_img_list.__len__()):
            print("Writing image: "  + img_names[i])
            full_out_path = os.path.join(out_path, img_names[i])
            cv2.imwrite(full_out_path, processed_img_list[i])

    print("Done!")

def scale_images(images):
    resized_images = []
    scale_percent = 0.25
    width = int(images[0].shape[1] * scale_percent)
    height = int(images[0].shape[0] * scale_percent)
    dsize = (width, height)
    for img in images:
        print("Resizing image.")
        resized_img = cv2.resize(img, dsize)
        if resized_img is not None:
            resized_images.append(resized_img)

    return resized_images

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
