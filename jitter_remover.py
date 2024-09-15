import cv2
import numpy as np
import os

def remove_jitter(input_folder, output_folder):
    # Get list of image files
    image_files = [f for f in os.listdir(input_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    image_files.sort()  # Ensure images are processed in order

    # Read the first image as the reference
    reference = cv2.imread(os.path.join(input_folder, image_files[0]))
    gray_reference = cv2.cvtColor(reference, cv2.COLOR_BGR2GRAY)

    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Save the reference image
    cv2.imwrite(os.path.join(output_folder, image_files[0]), reference)

    # Process each subsequent image
    for image_file in image_files[1:]:
        # Read the image
        image = cv2.imread(os.path.join(input_folder, image_file))
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect ORB features and compute descriptors
        orb = cv2.ORB_create()
        kp1, des1 = orb.detectAndCompute(gray_reference, None)
        kp2, des2 = orb.detectAndCompute(gray_image, None)

        # Match features
        matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = matcher.match(des1, des2)

        # Sort matches by score
        matches.sort(key=lambda x: x.distance, reverse=False)

        # Remove not so good matches
        numGoodMatches = int(len(matches) * 0.15)
        matches = matches[:numGoodMatches]

        # Extract location of good matches
        points1 = np.zeros((len(matches), 2), dtype=np.float32)
        points2 = np.zeros((len(matches), 2), dtype=np.float32)

        for i, match in enumerate(matches):
            points1[i, :] = kp1[match.queryIdx].pt
            points2[i, :] = kp2[match.trainIdx].pt

        # Find homography
        h, mask = cv2.findHomography(points2, points1, cv2.RANSAC)

        # Use homography to warp image
        height, width = reference.shape[:2]
        aligned_image = cv2.warpPerspective(image, h, (width, height))

        # Save the aligned image
        cv2.imwrite(os.path.join(output_folder, image_file), aligned_image)

    print("Jitter removal complete.")

# Usage
input_folder = "path/to/input/folder"
output_folder = "path/to/output/folder"
remove_jitter(input_folder, output_folder)