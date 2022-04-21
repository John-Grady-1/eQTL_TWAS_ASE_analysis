#!/usr/bin/env python3

# This script takes in raw paired-end fastq.gz files, and an index file from specified directories
# The script then aligns the reads from the input files to the index file using STAR as the read mapper
# The script returns the ouput of the STAR run; log.out, SJ.progress.out, log.final.out, log.progress.out and a .bam file which is required for downstream analysis


#########################
## Acquiring the files###
#########################

# Load the required modules
import os
import re
import subprocess

# Getting all the files in order
# First get the first mates of the sequencing run
# cycle through files in the directory, append files with correct ending to our empty list which we initialised
files = os.listdir()
mate1 = list()
for file in files:
  if file.find('_1.fq.gz') > -1 :
    mate1.append(file)


## Generate the second mate file and output prefix from star aligning
# Use regular expression to change the ending to the second mate of the paired end fastq.gz files
# change the ending again so we can specify the output in the STAR run
for file1 in sorted(mate1) :
  file2 = re.sub(r'_1.fq.gz', '_2.fq.gz', file1)
  ann  = re.sub(r'_1.fq.gz', '_', file1)
  # print(counter,file1, file2, ann) # check to make sure that everything is in order
  
  
  ###################################
  ##Compile the job within the loop##
  ###################################
  
  # basic options
  # Specify the index file and thread number
  job = 'STAR --genomeLoad LoadAndKeep --genomeDir /home/workspace/genomes/bostaurus/ARS_UCD1.2_NCBI/STAR-2.7.3a_index/ --runThreadN 4'
  
  # Input options
  # Specify the inputs which we would have generated above and unzip them on the fly
  job += f' --readFilesIn {file1} {file2} --readFilesCommand gunzip -c'
  
  # output options
  # Specify the output file name, the type of file (binary SAM; bam) and limit the RAM usage
  job += f' --outFileNamePrefix {ann} --outSAMtype BAM SortedByCoordinate --limitBAMsortRAM 10000000000'
  
  # limit to first 1000 reads for testing
  #job += ' --readMapNumber 1000'
  
  
  # Print the job to make sure it is ok
  print(job)
  
  # Perform the process
  proc = subprocess.run(job, shell=True, stdout=subprocess.PIPE, encoding='utf8')
  
  # Print the standard output to make sure everything is ok during the run
  print(proc.stdout)


