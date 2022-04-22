# This script creates an updated chromosome location for remapped Ids
# This script should be activated after positions have been updated

# Import modules
import subprocess
import re
import os

# specify files
fin = "ARS12_BOS1_array_updated.map" # Contains chromosome locations
fin2 = "ARS_1.2_Build_AX_pos.txt" # Newly mapped Chr positions with AX IDs
fout = "ARS_1.2_Build_AX_CHR.txt" # out file

# Short hand notation
f = open(fin, "r")
f2 = open(fin2, "r")
f3 = open(fout, "w")

# Set a list of chromosmes
chromosome = list()

# Cycle through the file
# split at tab and select the chromosomes and append
for line in f:
  fields = line.strip().split("\t")
  chromosome.append(fields[0])

# Sanity check - should be length of map file
print(f'List generated of chromosomes. Length of which is {len(chromosome)}')

# Cycle through newly generated AX and posiiton file
# Do the same and pull out IDs and append to a list
IDs = list()  
for line2 in f2:
  fields2 = line2.strip().split("\t")
  ID = fields2[0]
  IDs.append(ID)

# Length of IDs should be the same as length of chr list
print(f'List generated of IDs. Length of which is {len(IDs)}')


# Initialise a counter for indexing
counter  = -1


# Cycle through IDs list
#Cycle through chr list
# write IDs with new updated chromsomes
for ID in IDs:
  counter +=1
  Id = IDs[counter]
  Chr = chromosome[counter]
  #print(counter)
  #print(Chr + "\t" + Id + "\n")
  f3.write(Id + "\t" + Chr + "\n")
