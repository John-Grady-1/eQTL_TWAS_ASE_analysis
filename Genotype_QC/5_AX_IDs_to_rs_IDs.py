#!/usr/bin/python
# Conversion of AX  IDs to rs IDs in conventional format
# 2 inputs
# 1, clean genotype data file (vcf)
# 2, AX  axiom Bos 1 annotation file




#############################################
######## Import relevant modules ############
#############################################
import subprocess
import re
import os

#os.chdir("C:/Users/crtuser/OneDrive/OneDrive - University College Dublin/Data_Analysis_no_Rodeo/PLINK_files/")

#############################################
####### Specify input files #################
#############################################
input_file = open("SNP_data_clean_final.vcf", "r")
annotation_file = open("Axiom_GW_Bos_SNP_1.na35.annot.csv", "r")
temp_file = open("temp_file.vcf", "w")
out_file = open("SNP_data_clean_annotated_final.vcf", "w")


#############################################################
###### Getting VCF header and writing to new file ###########
###### Remaining output written to temp file ################
#############################################################

# Get/retain VCF header in new file
# Initialise a counter to keep track of header lines
counter = 0
# Cycle through the lines in the file
# Write all header lines to the new file
for line in input_file:
  counter += 1
  out_file.write(line)
  # If the line starts with chromosome (header of columns)  break the loop
  if line.startswith("#CHROM"):
    break

# Specifying in the output that this ahs been completed
print("VCF header Written to new outfile")

# Use the counter to transfer the remaining data to the temp file (no headers)
# Use the subprocess module for this
job = f'tail -n +{counter + 1} SNP_data_clean_final.vcf > temp_file.vcf'
proc = subprocess.run(job, shell = "TRUE", stdout=subprocess.PIPE, encoding='utf8')



# Print a status information in output
print("Transferred vcf information to temp file")

# Close the temp file
# Avoids file corruption
# Required when running python on command line
temp_file.close()

################################################
##### Getting dictionary with AX IDs ###
################################################

# Open the temp file again in read mode
# Again required when running on command line
temp_file = "temp_file.vcf"
t_file = open(temp_file, "r")

# Initialise an empty list for the fields and a dictionary for our k:v pairs
fields = list()
AX_dict = dict()

# Cycle through all the lines in the temp file (just genotype and variant coordinates)
# Split at the tab and select field number 2 (AX  ID)
# Set the key as that AX  ID and the value as nothing
for line in t_file:
  fields = line.strip().split("\t")
  AX_dict[fields[2]] = ""


# Close the file to avoid corruption
t_file.close()

# Print a status point in output
# Check the size of the dictionary, used as a reference point for later
print("Dictionary created with AX  IDs with a size of {len(AX_dict))}.\nNote: the next command will take a while to run")

###########################################################
#### Getting rsIDs as values for AX keys ##########
###########################################################


# Initialise a list for the fields and a dictionary for the k:value pairs
fields2 = list()
rs_dict = dict()

# Cycle through all lines in annotation file
for line2 in annotation_file:
  # If we find the identifier, split at COMMA (CSV file)
  if line2.find("AX") > -1 :
    fields2 = line2.strip().split(",")
    # Change around the strings
    # old id is the AX  id in the csv file
    old_id = str(fields2[0])
    old_id = old_id.replace('"', "")
    
    # New id is the rs id in the csv file
    new_id = str(fields2[2])
    new_id = new_id.replace('"', "")
    
    # Cycle through k:v items in our dictionary
    for key, value in AX_dict.items():
      # If there is a match of AX id from SNP data and id from csv file
      # Set the value of the AX id key as the rs snp from the annotaiton file
      if key == old_id :
        rs_dict[key] =  new_id



# This is a check to make sure that the length of the new dictionary is the same
print(f'The size of the RS dictionary is : {len(rs_dict)}')



########################################################################
##### Swapping AX  IDs for rs IDs and wiritng to new file #######
########################################################################

# reopen the file again in read mode
temp_file1 = "temp_file.vcf"
t_file1 = open(temp_file1, "r")

# initialis a list to separate the fields
fields3 = list()

# Cycle through all the lines in the temp file
# Split at tab and set AX_id as the third column in the file
for temp_line1 in t_file1 :
  fields3 = temp_line1.strip().split("\t")
  AX_id = fields3[2]
  
  # Once AX_id is obtained, cycle through all keys in the rs_dictionary
  for key, value in rs_dict.items():
    # if we find a match of a key and AX_id
    # set the Ax_id of that line as the value in the rs_dictionary (i.e., the rs ID)
    if key == AX_id :
      fields3[2] = rs_dict[key]
      
      # Once the column in the line has been changed
      # Join the columns at tab and write to a new file with \n for new line at end
      line4 = "\t".join(fields3)
      out_file.write(line4 + "\n")

# Print output statement to confirm
print("Outfile updated with new rs IDs ")   
    
  




