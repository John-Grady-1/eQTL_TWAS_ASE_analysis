#!/usr/lib/python3
# This script normalises for TPM and filters genes for a specific threshold based on GTEX consortium

# Specify the modules used
import os
import subprocess
import re
import csv
import numpy as np
import pandas as pd

# Specify input file
# Annotation file for Gene length
# Temp file to change the geneID field in original file and filter for TPM
# Out file to write final selected genes.
fin = "count_matrix_clean.txt"
annotation = "Bovine_annotation_MF2.csv"
temp = "Temp1_matrix_unnormalised_filter.txt"
temp2 = "Temp2_matrix_gene_length_normalised"
fout= "count_matrix_TPM_normalised.txt"

# Open all the files in read and write mode
f = open(fin, "r")
fan = open(annotation)
tmp = open(temp, "w")
tmp2 = open(temp2, "w")
fout = open(fout, "w")

# Use CSV reader to read the annotation file
# Need to use this as there is a lot of ","s in the file and need to deliniate proper fields
csvreader = csv.reader(fan)

# Set up a dictionary, this will match gene ids to the ID length
ID_length = dict()

################################################################################################################################
################################ Calculating Gene length #######################################################################
################################################################################################################################

## Gene length will be ascertained from annotaiton file

# Extract the first line from the annotation file and print it
header = []
header = next(fan)


# Set up an empty list to capture all the fields in the annotation file
# Append these fields to the list
rows = []
for row in csvreader:
  rows.append(row)


# Cycle through the list of lists
# The GENE ID (ENTREZ) ID is row 0 (0 based)
# Gene start base and end base are fields 6 + 7
for row in rows:
  ID = int(row[0])
    
  
  # Skip the genes which we do not know the location of
  if (row[6] or row[7] == int()) and (row[6] and row[7] != "NA"):
    
    # Calculate the length of the feature
    start_base = int(row[6])
    end_base = int(row[7])
    length = (end_base - start_base)
    
    
    # If the value is negative, turn it positive 
    # Note, this occurs if the feature is on the negative strand
    # Match the ID and the length of the ID in the dictionary
    if length < 0:
      length = length * -1
      ID_length[ID] = round(float(length / float(1000)), 3) # Divide by 1000 to get the reads per kilobase
      
    else:
      ID_length[ID] = round(float(length / float(1000)), 3) # Divide by 1000 to get the reads per kilobase
      


fan.close()

###############################################################################################################################
################################ Filtering out lowly expressed genes based on Gtex recommendations ############################
################################        This is done on the raw counts (unnormalised)              ############################
###############################################################################################################################


# Filter out lowly expressed genes based on criteria in GTEX of unnormalised data

# Take out the header first and writ to the new file
header_in = f.readline()
tmp.write(header_in)

# Specify the cut off
# This is for unnormalised counts in 20* of the samples
cut_off_unnormalised = 6  

# Cycle through original input file
for line in f:
  fields = line.strip().split("\t")

  # Initiailse a counter
  # This counter keeps track of the number of cells with counts greater than the cut off
  counter = 0
  for i in range(1, len(fields)):
    # Set the read = to the value in the field
    read = int(fields[i])
    if read >= cut_off_unnormalised:
      counter += 1
  # If > 20% of samples have counts greater than 6, keep them
  # Write the gene and subsequent expression profiles to the file
  if counter >= (len(fields) - 1) * 0.2:
    final_line = "\t".join(fields)
    tmp.write(final_line + "\n")

# Close the file to avoid corruption
tmp.close()


##################################################################################################################################
################################## Scaling reads based on gene length ############################################################
##################################################################################################################################

# Open the file
# This file has features with low read counts removed (as above)
tmp = open(temp, "r")

# Read the header and write to a new file
header = tmp.readline()
tmp2.write(header)


# Cycle through all lines in the file
for line in tmp:
  fields = line.strip().split("\t")
  
  # Need to replace "GeneID" as in the annotation file, It is just the number
  ID = fields[0]
  ID = ID.replace("GeneID:", "")
  ID = ID.replace("'", "")
  ID = int(ID)
  
  # Match the ID to the key and set the length as the value
  for k, v in ID_length.items():
    if ID == k:
      length = v
  # Next, cycle through all values in a row and divide by the length calculated above
  for i in range (1, len(fields)):
    fields[i] = round((int(fields[i]) / length), 2)
    fields[i] = str(fields[i])
  # Write the line to the new file
  final_line = "\t".join(fields)
  tmp2.write(final_line + "\n")
    
  

###################################################################################################################################
################################### Calculating library dept scaling factor #######################################################
###################################################################################################################################

## Reopen the temp file
# Calculate the scaling factor based on the counts normalised for gene length
tmp = open(temp2, "r")




# Open up the file using pandas
df = pd.read_csv(tmp, sep="\t", header=0)

col_list = ['C001', 'C002', 'C003',  'C004', 'C005', 'C006', 'C007', 'C008', 'C009',
 'C010', 'C011', 'C012', 'C013', 'C014', 'C015', 'C016', 'C017', 'C018', 'C019',
 'C020', 'C021', 'C022', 'C023', 'C024', 'C025', 'C026', 'C027', 'C028', 'C029',
 'C030', 'C031', 'C032', 'C033', 'C034', 'C035', 'C036', 'C037', 'C038', 'C039',
 'C040', 'C041', 'C042', 'C043', 'C044', 'C045', 'C046', 'C047', 'C048', 'C049',
 'C050', 'C051', 'C052', 'C053', 'C054', 'C055', 'C056', 'C057', 'C058', 'C059',
 'C060', 'C061', 'C062', 'C063', 'C064', 'T001', 'T002', 'T003', 'T004', 'T005',
 'T006', 'T007', 'T008', 'T009', 'T010', 'T011', 'T013', 'T014', 'T015', 'T016',
 'T017', 'T018', 'T019', 'T020', 'T022', 'T023', 'T024', 'T026', 'T027', 'T028',
 'T029', 'T030', 'T031', 'T032', 'T033', 'T034', 'T035', 'T036', 'T037', 'T038',
 'T039', 'T040', 'T041', 'T042', 'T043', 'T044', 'T045', 'T046', 'T047', 'T048',
 'T049', 'T050', 'T051', 'T052', 'T053', 'T054', 'T055', 'T056', 'T057', 'T058',
 'T059', 'T060', 'T061', 'T062', 'T063', 'T064', 'T065']
 
# Calculate the total number of coutns normalised for gene length in each column (sample)
total_sum = df[col_list].sum(axis = 0)

# Convert to a dictionary  
total_sum = total_sum.to_dict()
total_sum_scaled = dict()

# Scale each value by 1 million (this is the TPM part)
for key, value in total_sum.items():
  total_sum_scaled[key] = round(float(value / float(1000000)), 4)

# Print original and scaled for a sanity check
print(total_sum["T029"])
print(total_sum_scaled["T029"])

# Close the above file to avoid corruption
tmp.close()

# Print length of the col list so we know how many cycles are there
print(len(col_list))

##############################################################################################################################
######################################### Filter for genes with low TPM value ################################################
##############################################################################################################################

# We have our gene length normalisation and we have each sample's dept normalisation
# Need to filter first on gene length, then on sample normalisation
# Calculate the TPM value 
# Remove those genes which have a low TPM

# Open the file again which was normalised for gene length
tmp = open(temp2, "r")

# Read the first line and write it to a new file
header = tmp.readline()
fout.write(header)

# Cycle through all lines in the file
for line in tmp:
  fields = line.strip().split("\t")
  
  # Cycle through each value in the file
  # Note, in the temp file we do not want to include the Gene ID column but we have one less field in the col_list list above
  # To circumvent this, when using the i for indexing, use i-1 in the col_list variable (i.e. we start at 0 in that list)
  for i in range(1, len(fields)):
    
    # Identify the sample and located the scaled value (TPM)
    # Divide the counts normalised for gene length by this count
    # Round to 4 decimal places
    # Convert to a string to facilitate writing to the file
    sample = col_list[i-1] 
    scale_factor = total_sum_scaled[sample]
    scaled_value = float((float(fields[i]) / float(scale_factor)))
    fields[i] = round(scaled_value, 4)
    fields[i] = str(fields[i])
  final_line = "\t".join(fields)
  fout.write(final_line + "\n")

# Close the file to avoid corruption    
fout.close()

# Open up the final file in read mode
f = open("count_matrix_TPM_normalised.txt", "r")

# Read in the header from our unnormalised counts file
header_in = f.readline()


# Initialise a list to capture our list of genes which pass the threshold
selected_genes = []

# Set the cut off
TPM_cutoff = 0.1

# Cycle through all the lines in the file (normalised for gene length and library size)
for line in f:
  counter = 0
  fields = line.strip().split("\t")
  
  # Cycle through each cell in the row
  for n in range(1, len(fields)):
    # Specify TPM as the value
    TPM_value = float(fields[n])
    # If TPM is bigger than our cut off
    if TPM_value > TPM_cutoff:
      # Add one to the counter
      counter += 1
  # If, in that row, the number of samples (counter) with a TPM bigger than the cut off is >= 20% of the samples
  # Append the gene id (fields 0) to the list initialised above
  if counter > (len(fields) - 1) * 0.2:
    selected_genes.append([fields[0]])

# Close the file to avoid corruption
f.close() 


# Open up the final file
# Write geneid and "\n"
selected_genes_file = "Gtex_criteria_filtered_genes"
final_out = open("Gtex_criteria_filtered_genes", "w")
final_out.write("Geneid" + "\n")

# Cycle throught the list of genes and modify the string to write them to the final file of selected genes
for element in selected_genes:
  gene = str(element)
  gene = gene.replace("[", "")
  gene = gene.replace("]", "")
  gene = gene.replace("'", "")
  final_out.write(gene + "\n")

# Close the file to avoid corruption  
final_out.close()

    
  





