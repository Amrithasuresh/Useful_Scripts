# -------------------------------------------------------------------------------
# Purpose:     # This script converts small molecule 2D to 3D structures using corina software
# Author:      Suresh Panneerselvam
#
# Created:     2016-07-11
# OS:          Ubuntu 16.04
# Licence:     MIT
# -------------------------------------------------------------------------------
import subprocess
import glob

#requirement corina software


list_files = glob.glob("/home/suresh/python/project-pattern/files")

for file in list_files:
    filename, file_extension = os.path.splitext(file)
    filename = os.path.basename(filename)
    newfile = filename + '.mol2'
    cmd='corina  -o ' + file + '  ' + newfile
    print 'processing %s' % cmd
    subprocess.call(cmd,shell=True)

print '*************'
print 'Job finished'
print '*************'
    
