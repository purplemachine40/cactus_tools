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

    #Read first image to get size
    frame = cv2.imread(img_list[0])

    #Percent by which the image is resized
    scale_percent = movie_settings["image_scale_percent"]

    #Calculate the 50 percent of original dimensions
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)

    dsize = (width, height)
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    video = cv2.VideoWriter(out_video_full_path, fourcc, 10, (width, height))

    for img_path in img_list:
        print("Processing image " + img_path + "\n")
        frame = cv2.imread(img_path)    
        resized_frame = cv2.resize(frame, dsize)
        if resized_frame is not None:  # Ensure the image is read correctly
            video.write(resized_frame)

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