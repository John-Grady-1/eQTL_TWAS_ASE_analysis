#!/usr/bin/env python3

## This script carries out an expression quantification analysis by using bam files as input and featureCounts as the software tool
## The script takes in Control and infected bam files which were previosuly alligned using STAR
## The script returns a matrix file (gene_counts) with number of reads associated with each feature 

# Import relevant modules
import os
import re
import subprocess


##########################
## Acquiring the files ###
##########################


# Need to get both Control and infected datasets for Feature Counts
# These directories will need to be changed for e.g. human datasets
# Note, these are the directories which the bam files from alignment are located.
Control_direc = "/home/workspace/jogrady/eqtl_study/data/Control_data"
TB_direc = "/home/workspace/jogrady/eqtl_study/data/Tuberculosis_data"

# List all the files in both these directories
Control_files = os.listdir(Control_direc)
TB_files = os.listdir(TB_direc)

# Initialise an empty list which we will append to below
featurecount_input_control = []
featurecount_input_tb = []

# Cycle through both directories and append desired files to our list
# Again the desired files are the bam files 
for con_file in Control_files:
  if con_file.find(".bam") > -1:
    featurecount_input_control.append(con_file)

for tb_file in TB_files:
  if tb_file.find(".bam") > -1:
    featurecount_input_tb.append(tb_file)

# We now have a list of bam files which we need to perform expression quanitfication on
# Sort this list so both Control (C0*) and infected (T0*) are in alphabetical order
# This will make analysis much easier down the line

featurecount_input_control = sorted(featurecount_input_control)
featurecount_input_tb = sorted(featurecount_input_tb)
print(len(featurecount_input_control))# check length to make sure everything picked up ##64 control
print(len(featurecount_input_tb)) ## check length to make sure everything picked up ##62 TB


######################
## Compile the job ###
######################

# Call featureCounts and specify directory of annotation file
# This file will need to be changed for human: different annotation file. 
# Can bring it into current directory or can call it from directory on server
job = "featureCounts -a GCF_002263795.1_ARS-UCD1.2_genomic.gff" 

# Specify the output file name, -
job += f' -o gene_counts.txt '

# Cycle through each file in the list and append that to the job path to the file
# Initialise the counter to keep track
# Essentially what we are doing is just continually adding to the above command by specifying files in the order that we want (sorted due to analysis above)
# Problem is that these input file paths will be included as sample name so will need to clean up later.
counter1 = 0
for i in range(0, len(featurecount_input_control)):
  job += f'/home/workspace/jogrady/eqtl_study/data/Control_data/{featurecount_input_control[i]} ' 
  counter1 += 1

# Repeat for the TB file path and input data types
counter2 = 0
for i in range(0,len(featurecount_input_tb)):
  job += f' /home/workspace/jogrady/eqtl_study/data/Tuberculosis_data/{featurecount_input_tb[i]}' 
  counter2 +=1

#### Paramaters:

# -B: Only fragments that have both ends successfully aligned will be considered for summarization.
# -p: If specified, fragments (or templates) will be counted instead of reads. This option is only applicable for paired-end reads.
# -C: If specified, the chimeric fragments (those fragments that have their two ends aligned to different chromosomes) will NOT be counted. 
# -T: Threads used
# -t: Specify the feature type. Only rows which have the matched feature type in the provided GTF annotation file will be included for read counting.
#     Specify the attribute type used to group features (eg. exons) into meta-features (eg. genes) when GTF annotation is provided.
#Note Had some trouble with GFF file and -g paramater, was fixed by specifiying gene with -t paramater
#Note Reason was that not all rows had the Dbxref annotation feature causing featureCounts to stop
#Note: All rows with gene in annotation file have Dbxref annotation

### Note: the paramaters will differ depending on RNA-seq data (stranded or not), annotation file format etc. Important to look at
job += " -B -p -C -R BAM -T 4 -s 0 -t gene -g Dbxref"


print(job) # Check to make sure the job is compiled -- will be extremely long
print(counter1, counter2, counter1 + counter2) # sanity check

################
##Run the job###
################


proc = subprocess.run(job, shell=True, stdout=subprocess.PIPE, encoding='utf8')

# Print the standard output to make sure everything is ok during the run
print(proc.stdout)

