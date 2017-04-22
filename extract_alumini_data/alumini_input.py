#Had a text file (sample alumini.txt) and need to extract the information name,image, and email. 
#Use form to replace name,image and email

import re
from string import Template

file = open('alumini.txt').read()
split_file = file.split('}')

print(split_file)
#remove white spaces
def remove_whitespace(string):
    string = string.strip()
    return string

# convert list to strings
def convert_list_string(list_value):
    string_value = ''.join(list_value)
    return string_value

form ='''
         <div class="media">
           <div class="media-left">
            <a href="#">
            <img class="media-object" src="../images/$image" alt="Simon" width="200px">
            </a>
            </div>
           <div class="media-body">
           <h4 class="media-heading">$name</h4>
           <a href="mailto:Email">$mail</a>
           </div>
           </div>
           <br/
         '''


for value in split_file:
    list_info = []

    email = re.findall(r'Email:|\s:(.*)\<br>', value)
    image = re.findall(r'Image:(.*)\|', value)
    name = re.findall(r'\'\'\'\*(.*)\<br>', value)

    email = convert_list_string(email)
    image = convert_list_string(image)
    name = convert_list_string(name)

    email = remove_whitespace(email)
    image = remove_whitespace(image)
    name = remove_whitespace(name)

    info = Template(form)
    info = info.substitute(image=image,name=name,mail=email)
    print(info)
