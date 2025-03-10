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
        if file_name.lower().endswith('.jpg'):
            print("Loading file: " + file_name)
            img_names.append(file_name)
            full_img_path = os.path.join(in_path, file_name)
            img_paths.append(full_img_path)
            in_img_list.append(cv2.imread(full_img_path))

    if in_img_list.__len__() > 0:
        processed_img_list = align_images(in_img_list)

    if processed_img_list.__len__() > 0:
        for i in range(0, processed_img_list.__len__()):
            print("Writing image: "  + img_names[i])
            full_out_path = os.path.join(out_path, img_names[i])
            cv2.imwrite(full_out_path, processed_img_list[i])

    print("Done!")

def align_images(images):
    # Convert images to grayscale
    gray_images = [cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) for img in images]

    # Select first image as reference
    reference = gray_images[0]

    # Initialize ORB detector
    orb = cv2.ORB_create()

    aligned_images = [images[0]]

    for i in range(1, len(images)):
        print("Aligning image.")

        # Re-reference every 5 images.

        if (i < len(images) - 1) and (i % 20 == 0):
            reference = gray_images[i]

        # Detect keypoints and descriptors
        kp1, des1 = orb.detectAndCompute(reference, None)
        kp2, des2 = orb.detectAndCompute(gray_images[i], None)

        # Match descriptors
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(des1, des2)

        # Sort matches by distance
        matches = sorted(matches, key=lambda x: x.distance)

        # Select top matches
        good_matches = matches[:50]

        # Visualize matches for the first pair of images

        # aligned_image = visualize_matches(images[0], images[i], kp1, kp2, good_matches)

        # Get matched keypoints
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

        # Estimate transformation matrix
        M, _ = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC, 5.0)

        # Apply transformation
        aligned_image = cv2.warpPerspective(images[i], M, (images[i].shape[1], images[i].shape[0]))
        aligned_images.append(aligned_image)

    return aligned_images

def create_video(images, output_path, fps=10):
    print("Making Video")
    height, width, layers = images[0].shape
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    for image in images:
        video.write(image)

    video.release()

def visualize_matches(img1, img2, kp1, kp2, good_matches):
    # Create a copy of img1 to draw on
    match_img = img2.copy()

    # Draw small crosses for good matches
    for match in good_matches:
        x, y = map(int, kp1[match.queryIdx].pt)
        cv2.drawMarker(match_img, (x, y), (0, 255, 0), cv2.MARKER_CROSS, 10, 2)

    return match_img

    # Save the image with matches
    # cv2.imwrite('matches_visualization.jpg', match_img)
    # print("Matches visualization saved as 'matches_visualization.jpg'")


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
