Cactus Tools!
Tools for making a movie out of a cactus.

## rename_pics.ps1
This is a script for renaming pictures with the date taken. ex. 20231231_cactus.JPG

## Python Settings
The following python scripts require a json in the same folder called movie_settings.json.

Here's an example:
```
{
    "raw_in_path": "C:\\raw_img_in", - This is where the raw un-scaled pictures go.
    "align_in_path": "C:\\align_img_in", - Directory where the scaled down images go; input directory for further processing.
    "align_out_path": "C:\\align_img_out", - Output directory for processed images and the input directory for make_movie.py.
    "output_path": "C:\\cactus_movie", - This is the output directory for make_movie.py.
    "movie_name": "cactus.mp4", - The movie name.
    "image_scale_percent": 50 - This is the percentage to scale the images in raw_in_path; if the pictures are too big, processing may fail.
}
```

## resize_pics.py
This python script resizes the pictures in the raw_in_path, scaling them down by image_scale_percent.

## stabilize_images.py
This python script runs a stabilization algorithm on the the images.

## make_movie.py
This python script makes a movie out of the stabilized cactus pictures.
