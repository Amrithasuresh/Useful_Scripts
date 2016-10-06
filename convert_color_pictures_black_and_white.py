
# -------------------------------------------------------------------------------
# Purpose:     Convert color pictures to black and white using
# Author:      Suresh Panneerselvam
#
# Created:     2016-07-11
# OS:          Ubuntu 16.04
# Licence:     MIT
# -------------------------------------------------------------------------------

from PIL import Image
import subprocess
import os

#change the directory accordingly
files = os.listdir('/home/suresh/Pictures/Wallpapers')

for file in files:
    filename,file_extension = os.path.splitext(file)

    if file_extension == ".jpg":
        f = filename+file_extension

        col = Image.open(f)
        gray = col.convert('L')
        gray.save(filename+"_bw"+file_extension)
        print filename +"  is converted"








