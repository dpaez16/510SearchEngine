import os
import re
from tqdm import tqdm

f = open('files.txt', 'w+')
dat_file = open('formatteddataset.dat', 'w+')

directory = "./grobid_processed"
title_directory = "./paper_fields/papers_to_index"
xml_files = os.listdir(directory)

for xml_file in tqdm(xml_files):
    # read in raw xml file
    f_ = open(os.path.join(directory, xml_file))
    lines = f_.read()
    lines = lines.replace('\n', '')
    lines = re.sub(r'<.*>', '', lines)
    dat_file.write(lines + "\n")
    f_.close()

    # extract title from xml file
    f_ = open(os.path.join(title_directory, xml_file))
    lines = f_.read()
    lines = lines.replace("\n", "")
    lines = re.sub(r'.*<title>', "", lines)
    title = re.sub(r'</title>.*', "", lines)
    f.write("{}\t{}\n".format(xml_file, title))
    f_.close()

f.close()
dat_file.close()
