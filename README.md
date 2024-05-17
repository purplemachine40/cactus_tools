Cactus Tools!
Tools for making a movie out of a cactus.

## rename_pics.ps1

This is a script for renaming pictures with the date taken. ex. 20231231_cactus.JPG

## make_movie.py

This python script makes a movie out of the cactus pictures. I probably should call
rename_pics.ps1 from this script. Why didn't I? Also, the script resizes the pictures, and
that's hard-coded, assuming the pictures are taken with my phone. I don't let you customize that.
Probably an oversite. Anyway, the script needs a json in the same folder called movie_settings.json.
Here's an example:

{
"input_path": "C:\\cactus_pics",
"output_path": "C:\\cactus_movie",
"movie_name": "cactus.mp4"
}
