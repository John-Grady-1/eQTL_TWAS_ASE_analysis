# This script removes duplicates in updated remapped chr and position files
# Duplicates were acquired from the original Map file from ROB schnaeble
# Only a few duplicates so errors are minimal

# Load in library
library(dplyr)

###########################################################
# Variant position on Chromosome file######################
###########################################################

# Specify the CHR file generated from previous script
chr_file <- read.csv("ARS_1.2_Build_AX_CHR.txt", sep = "\t", header = FALSE)

# Santiy check 
dim(chr_file)
head(chr_file)
colnames(chr_file)

# Remove duplicates using unique command
chr_file <- unique(chr_file)

# Check dimensions
dim(chr_file)

# Double check ID row
length(unique(chr_file$V1)) == nrow(chr_file)

# Write to new file
write.table(chr_file, file = "ARS_1.2_Build_AX_CHR_final.txt", 
            row.names = FALSE, col.names = FALSE, quote = FALSE, 
            sep = "\t")

648874 - 648855

######################################################################
########### Variant Position File ####################################
######################################################################

# Read in the file and check the dimensions
pos_file <- read.csv("ARS_1.2_Build_AX_pos.txt", sep = "\t", header = FALSE)

#Sanity check
dim(pos_file)

# Get unique values
pos_file <- unique(pos_file)
head(pos_file)
dim(pos_file)

# Double check ID row length
length(unique(pos_file$V1)) == nrow(pos_file)

#Use a table to find the duplicate IDs
#n_occur <- data.frame(table(pos_file$V1))
#n_occur[n_occur$Freq > 1,]

#pos_file[pos_file$V1 %in% n_occur$Var1[n_occur$Freq > 1],]

# Check these IDs to make sure which is the right ID
# Take the first value, these will be removed anyway as they are Y chromosome
#             V1      V2
# 648855 AX-28607522 4992225
# 648856 AX-28607522 4984889
# 648872 AX-28607948 9362483
# 648873 AX-28607948 9641583
# Delete 648856 & 648873
pos_file <- pos_file %>% 
  filter(pos_file$V1 != c("AX-28607522", "AX-28607948") 
         & pos_file$V2 != c(4984889, 9641583)) %>%
  as.data.frame()

# Sanity check again
head(pos_file,2)
dim(pos_file)
length(unique(pos_file$V1)) == nrow(pos_file)

# Check that the length of position file is the same as variant file
length(unique(pos_file$V1)) == length(unique(chr_file$V1))

# Write the final variant position file
write.table(pos_file, file = "ARS_1.2_Build_AX_pos_final.txt", 
            row.names = FALSE, col.names = FALSE, quote = FALSE, 
            sep = "\t")


