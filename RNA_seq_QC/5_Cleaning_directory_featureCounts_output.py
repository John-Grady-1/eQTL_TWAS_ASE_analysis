#!/usr/bin/env python3

# This script will clean up a featureCounts matrix ouput
# Specifically, it will remove the long headings in sample names aswell as the .bam extension
# It will also remove the geneid name by modifying a temporary file which we will delete

import subprocess
import re

file = "gene_counts2_Clean.txt"
tempfile = "gene_counts_temp.txt"
outfile = "count_matrix_clean.txt"

fin = open(file, 'r') # Open in read mode
ftemp = open(tempfile, 'w')

    

##########################
##Changing the headers####
##########################

# Extract the first line in input file
# Replace the file path with nothing in patterns
# Replace the .bam extension
# Write to the specified temp file

header = fin.readline()
header = header.replace('/home/workspace/jogrady/eqtl_study/data/Control_data/', '')
header = header.replace('/home/workspace/jogrady/eqtl_study/data/Tuberculosis_data/', '')
header= header.replace('.bam', '')
ftemp.write(header)



#####################################
##Filtering out non expressed reads##
#####################################

# Cycle through lines in the file
# If the sum of the reads is < 2x the sample size
# Do not write them to the new file

for line in fin :
    fields = line.strip().split("\t")
    reads = 0
    for i in range(1,len(fields)) :
        reads += int(fields[i])
  
    if reads >= 0 : # this is what is modified for filtration
        ftemp.write(line)

  
ftemp.close()
fin.close()

################################
##Formating the geneID column###
################################

ftemp = open(tempfile, 'r') # open in read mode so as to not to overwrite the file
fout = open(outfile, 'w') # Open in write mode to write to write to at the end

header = ftemp.readline()
fout.write(header)

# Cycle through lines in the new file
# Change the first field = field[0] to the desired format of just GeneID:xxxxxxx
# Join the fields back together
# write to the file

for line in ftemp:
    fields = line.strip().split("\t")
    ID = fields[0]
    match = re.search(r'GeneID:\d*|Geneid', ID, re.I) 
    if match:
      new_id = match.group(0)
      new_id = new_id.replace(",", "")
      fields[0] = new_id
      new_line = '\t'.join(fields)
      fout.write(new_line + "\n")

#remove the temporary files we do not need
job = "rm gene_counts_temp.txt"
proc = subprocess.run(job, shell=True, stdout=subprocess.PIPE, encoding='utf8')


# Fixing the heading of the summary file
sum_file = 'gene_counts.txt.summary'
sum_out_file = 'gene_counts_clean.summary.txt'

fsum = open(sum_file, 'r')
fsum_out = open(sum_out_file, 'w')

header = fsum.readline()
header = header.replace('/home/workspace/jogrady/eqtl_study/data/Control_data/', '')
header = header.replace('/home/workspace/jogrady/eqtl_study/data/Tuberculosis_data/', '')
header= header.replace('.bam', '')
fsum_out.write(header)

for line in fsum:
  fsum_out.write(line)

fin.close()
fout.close()
fsum.close()
fsum_out.close()


      
