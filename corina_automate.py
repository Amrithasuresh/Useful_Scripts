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
    
