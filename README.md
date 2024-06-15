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
"output_path": "C:\\cactus_movie\\",
"movie_name": "cactus.mp4"
}

Update: I happened upon an error trying to process more cactus: "Failed to load OpenH264 library: openh264-1.8.0-win64.dll".
In the immortal words of Alan Turing, "Someth'n done broke". So I had to go here: https://github.com/cisco/openh264/releases
and download http://ciscobinary.openh264.org/openh264-1.8.0-win64.dll.bz2. Then I had to Google what a .bz2 is. Then, extract
it using 7-zip to the same folder that contained make_movie.py. And PRESTO! Works again.
