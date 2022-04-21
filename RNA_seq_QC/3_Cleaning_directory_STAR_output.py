#!/usr/bin/env python3

# This script will look for files generated from a STAR output and find particular motifs and move them into a specified directory
# The script also renames the main output of the STAR format to a much similar extension (file.bam)


# Load the required modules
import os
import re
import subprocess

# specify the directory we are working in
# This will need to be changed depending on what directory you are in
direc = "/home/workspace/jogrady/eqtl_study/data/Control_data"
new_direc = "/STAR_output"

# list files in the directory
# Store this list in the variable files
files = os.listdir(direc)

# Move file with particualr motif
for file in files:
  if file.find("_Log.out") > -1:
    job = f'mv {file} {direc}{new_direc}'
    proc = subprocess.run(job, shell=True, stdout=subprocess.PIPE, encoding='utf8')
    #print(job)

# Move file with particualr motif
for file2 in files:
  if file2.find("Log.progress.out") > -1:
    job2 = f'mv {file2} {direc}{new_direc}'
    proc = subprocess.run(job2, shell=True, stdout=subprocess.PIPE, encoding='utf8')
    #print(job2)
    
# Rename the file which we want
for file3 in files:
  if file3.find("_Aligned.sortedByCoord.out") > -1 :
    file4 = re.sub("_Aligned.sortedByCoord.out", "", file3) # Use regular expression to change the name of the file
    job3 = f'mv {file3} {file4}'
    proc = subprocess.run(job3, shell=True, stdout=subprocess.PIPE, encoding='utf8')
    #print(job3)
    
# Move file with particualr motif
for file5 in files:
  if file5.find("SJ.out.tab") > -1:
    job4 = f'mv {file5} {direc}/STAR_align'
    proc = subprocess.run(job4, shell=True, stdout=subprocess.PIPE, encoding='utf8')
    #print(job4)
