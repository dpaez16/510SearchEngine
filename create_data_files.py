import os
import re

f = open('files.txt', 'w+')
dat_file = open('lit_search.dat', 'w+')

directory = "./grobid_processed"
xml_files = os.listdir(directory)

for xml_file in xml_files:
    f_ = open(os.path.join(directory, xml_file))
    lines = f_.read()
    lines = lines.replace('\n', '')
    lines = re.sub(r'<.*>', '', lines)
    dat_file.write(lines + "\n")
    f.write(file_ + "\n")
    f_.close()

f.close()
dat_file.close()
