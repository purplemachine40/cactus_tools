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
        sys.exit(1)

    path = movie_settings["input_path"]
    out_path = movie_settings["output_path"]
    out_video_name = movie_settings["movie_name"]
    out_video_full_path = out_path + out_video_name

    pre_imgs = os.listdir(path)
    img_list = []

    for img in pre_imgs:
        if img.lower().endswith('.jpg'):
            full_img_path = os.path.join(path, img)
            img_list.append(full_img_path)

    if len(img_list) > 0:
        print("Number of input images: ", len(img_list))
        #Read first image to get size
        frame = cv2.imread(img_list[0])
    else:
        print("No images!")
        sys.exit(1)

    width = frame.shape[1]
    height = frame.shape[0]
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    video = cv2.VideoWriter(out_video_full_path, fourcc, 10, (width, height))

    for img_path in img_list:
        print("Processing image " + img_path + "\n")
        frame = cv2.imread(img_path)

        # Ensure the image is read correctly

        if frame is not None:
            video.write(frame)
        else:
            print("Frame is blank!")

    video.release()

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