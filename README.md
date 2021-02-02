## EdgePainting
A simple program that takes an folder of images and tracks the edges then maps it to a coloured spiral

This project contains 1 main program, and 2 scripts that may prove usful in fixing issues from editing the program.  The main program simply takes all images from a file and maps a another image to the edges that were detected, you can see the pre in Backgrounds and the afters in BackgroundOut.  Despite trying to make the input dynamic the program really struggles when a image lacks well defined edges.  It also has a long runtime for a 1920 x 1080 image it takes ~16.5 seconds and for a 2560 x1080 image it takes ~20 seconds.  The main time sink is mapping the image with the colour.

Key features that the main program has:
- Taking the histogram of an image, and dynamically generate the sobel low and high thresholds.
- Multiply the intesity of the edge by the the colour on the colour map.
- Skips files that it thinks it has already done.
- If the output and input file are seperate it will update the name of the files in the output. (This was mostly because a prior version didn't tag the new image with filename + 'Outline' + '.jpg')
- Easy to change key variables, located right at the top as constants.

The first script, fixin.py, is a simple script that will go through a file of images and remove extra junk after the .jpg / .png.  This was made simply because my original renaming section renamed all my input files not my output files.

The second script, deletingCopies.py, is a simple script that removes all files that lack outline in the file name.  This was made a prior version did specify Outline, and the files were a mix for '.jpg' and '.png'.  The main program itself takes care of any '.jpg' files so this was made to take care of the ".png"'s.

## Requirements

- Python3
  - Opencv2

# Author

Callum Coy

# Extras

Use any of the code as you want, I have commented it pretty well so it should be relatively understandable.
