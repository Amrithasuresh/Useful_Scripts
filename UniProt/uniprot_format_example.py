#!/usr/bin/python3
import glob
import os
import re
import csv

# The file path is given where all the uniprot text files are kept
#one example file given as uniprot_file
list_files = glob.glob("/home/suresh/uniprot/" + "*." + "txt")

# This is to create a file
writefile = open("required_file_new.txt", "w")

# These string is written as a first line of the file
writefile.write("Reviewed, UniProt_ID, Gene_Name, Gene_ID, Chromosome" + "\n")

#This function reads the file and return True or False if they have "GeneID" and "Reviewed" line in the file
#This is to skip reading files once returns false
def filename_with_geneid(filename):
    textfile = open(filename, 'r')
    lines = textfile.read()
    textfile.close()
    matches = re.findall("\GeneID", lines)
    matches1 = re.findall("\Reviewed", lines)

    if matches and matches1:
        return True
    else:
        return False


# for each file from the list of files
for file in list_files:
    # This command splits filename and saves it
    filename = os.path.splitext(file)[0]

    # opening the file one by one
    pattern = filename_with_geneid(filename+".txt")

    if pattern is True:
        with open(filename + '.txt') as lines:
            row = []
            count1=count2=count3=count4=0
            for line in lines:

                try:
                    if line.startswith('GN   Name='):
                        count1 += 1
                        if count1 > 1:
                            pass
                        elif count1 == 1:
                            match = re.search('\Name=[\w]+.', line)
                            match = re.findall(('=(\w+)'), match.group(0))
                            match = ', '.join(match)
                            row.append(match)
                        else:
                            row.append("None")

                    elif line.startswith('AC'):
                        count2 += 1
                        if count2 > 1:
                            pass
                        elif count2 == 1:
                            match = re.search('AC\s+\w+', line)
                            match = re.findall(('\s+\w+'), match.group(0))
                            match = ', '.join(match)
                            match = match.strip()
                            row.append(match)
                        else:
                            row.append("None")

                    elif line.startswith('DR   GeneID'):
                        count3 += 1
                        if count3 > 1:
                            pass
                        elif count3 == 1:
                            line = re.sub(r'[^\w]', ' ', line)
                            match = re.search('\GeneID\s+\d+\s', line)
                            match = re.search('\d+', match.group(0))
                            match = match.group(0).strip()
                            row.append(match)
                        else:
                            row.append("None")

                    elif line.startswith('DR   Proteomes'):
                        try:
                            count4 += 1
                            if count4 > 1:
                                pass
                            elif count4 == 1:
                                line = re.sub(r'[^\w]', ' ', line)
                                match = re.search('\Chromosome\s+\d+\s', line)
                                match = re.search('\d+', match.group(0))
                                match = match.group(0).strip()
                                row.append("Chromosome:"+match+ "\n")
                            else:
                                row.append("None"+ "\n")
                        except:
                            row.append("None" + "\n")

                    elif line.startswith('ID'):
                        try:
                            # if the line contains the pattern Reviewed then write to the file as "Yes"
                            match = re.search(r'\Reviewed', line)
                            row.append("Yes")
                        except:
                            # in case if it is absent write it as None
                            row.append("None")

                except:
                    row.append("None")
        print (row)
	format_list = ",".join(str(x) for x in row)
        writefile.write(format_list)
