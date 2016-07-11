
# -------------------------------------------------------------------------------
# Purpose:     How to automate fuzznuc program (emboss fuzznuc) in linux?
# Author:      Suresh Panneerselvam
#
# Created:     2016-07-11
# OS:          Ubuntu 16.04
# Licence:     MIT
# -------------------------------------------------------------------------------
#import the docx module
#Documentation can be found here http://python-docx.readthedocs.io/en/latest/


import subprocess
import glob
import os

# fuzznuc -sequence fasta.txt -pattern CATTGTA -outfile output.txt
patterns = ['CTTTGTT','CATTGTG','CAGGACG','CAGGGTG','TTTTGTA','GATTGTA','CATTACG','ATTTGTA']

#fasta sequences saved as file_name.fasta in this folder
list_files = glob.glob("/home/suresh/python/project-pattern/files")

for file in list_files:
    for pattern in patterns:
        filename, file_extension = os.path.splitext(file)
        filename = os.path.basename(filename)
        out_name = str(pattern) + '-' + filename + '_fuzz_output' + '.txt'
        cmd = 'fuzznuc -sequence'+ ' ' + file +' ' + '-pattern' +' ' + pattern + ' ' + '-outfile' + ' ' + out_name

        subprocess.call(cmd, shell=True)
        print('Running file name is: %s' % cmd)
