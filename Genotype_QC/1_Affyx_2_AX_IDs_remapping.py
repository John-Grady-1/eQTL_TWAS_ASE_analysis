########## Affyx to AX Ids###################################################
########## This is required for variant remapping in updating map files######
#############################################################################

# Import relevant modules
import re

# Specify files.
# File 1 is the affymetrix SNP positions 
file = "ARS_1.2_Build_affyx_pos.txt"

# File 2 is a meta data file which contains Affymetrix and AX IDs
file2 = "Axiom_GW_Bos_SNP_1.na35.annot.csv"

# File 3 is the output file with new posiitons and AX ids
file3 = "ARS_1.2_Build_AX_pos.txt"

# Open all the files
f = open(file, "r")
f2 = open(file2, "r")
f3 = open(file3, "w")


counter = 0
# Initialise an empty dictionary
# This will collect the Affyx IDs as keys
id_dict= dict()

# Cycle through the input file
# Collect the first value in each line and input it as a key in dicitonary
for line in f:
  fields = line.strip().split("\t")
  ID = fields[0]
  id_dict[ID] = ""


# Sanity check to see how many lines there are
print(f'Initial dictionary created of size {len(id_dict)}')

# Close the file to avoid corruption
f.close()

# Initialise a tracker to keep track
tracker = 0
counter = 0

# Cycle through our metadata file which has AX IDs
for line2 in f2:
  if line2.find("AX") > -1 :
    # Split at comma when we find the AX id
    fields2 = line2.strip().split(",")
    
    # Do some data wrandling to remove quotes (how file was generated)
    affyx = fields2[1]
    affyx = affyx.replace('"',"")
    AX_id = fields2[0]
    AX_id = AX_id.replace('"', "")
    counter += 1
    
    # Once we have the AX id and Affyx id for the same SNP
    # Cycle throught the ID dictionary
    # Find the line which matches the Affyx ID
    for key, value in id_dict.items():
      if key == affyx:
        # Print both as a sanity check
        print(affyx, AX_id)
        # Set the affyx ID key value as the AX ID
        id_dict[affyx] = AX_id
        
        
# Santiy check, should be same size as the dictionary above
print(f'Dictionary created with IDs matching. The size of the dictionary is {len(id_dict)} elements')

# Open the origional file again
f = open(file, "r")

# Cycle thorugh the file again
# Split at tab, obtain the old ID
for line in f:
  fields3 = line.strip().split("\t")
  old_id = fields3[0]
  old_id = old_id.replace('"', "")
  
  # Cycle through the key value pairs in dictionary with Affyx and AX ids matching
  for key, value in id_dict.items():
    
    # If the Affyx in the file matches the affyx id in the dictioanry
    # The new id is the AX value of the affyx id key
    # Select the posiiton of the variants in the old file
    # These positions are the updated ARS1.2 build
    # Write the AX ID and the position to the final file.
    if key == old_id:
      new_id = value
      pos = fields3[1]
      print(new_id + "\t" + pos + "\n")
      f3.write(new_id + "\t" + pos + "\n")
      

      
  
        
  
