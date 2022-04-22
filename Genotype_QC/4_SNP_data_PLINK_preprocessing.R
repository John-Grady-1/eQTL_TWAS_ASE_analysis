##############################################################################
############# R script for Analysing SNP genotype data #######################
##############################################################################

library(dplyr)
library(stringr)
library(ggplot2)

## Set the directory for the location of the files and the Plink
# Run a simple command to make sure that everything works
setwd("C:/Users/crtuser/OneDrive/OneDrive - University College Dublin/Data_Analysis_no_Rodeo/PLINK_files")
system(paste("plink --help <flagname>"))
system(paste("plink --help --update-map"))

# Specify input and output data
input_data_raw <- "SNP_data"
input_data_remapped_CHR <- "SNP_in_remapped_CHR"
input_data_remapped_POS <- "SNP_in_remapped_POS"
input_data_final <- "SNP_in_FINAL"
input_data_final_no_Kerry <- "SNP_in_FINAL_no_Kerry"
out_missing_1 <- "out_SNP_missing_sample"
out_missing_2 <- "out_SNP_missing_snp"
out_maf <- "out_SNP_MAF"
out_maf_10 <- "out_SNP_MAF_10"
out_HWE <- "out_SNP_HWE"
out_HWE_10 <- "out_SNP_HWE_10"
out_pruned <- "out_SNP_pruned"
out_final <- "SNP_data_clean_final"
out_final_10 <- "SNP_data_clean_final_MAF_10"
update_pos <- "ARS_1.2_Build_AX_pos_final.txt"
update_chromosome <- "ARS_1.2_Build_AX_CHR_final.txt"

#####################################################################
############ Updating chromosomes and positions #####################
############ Required for remapping to ARSUCD1.2#####################
#####################################################################

## Run these scripts prior
# python Affyx_2_AX_IDs_remapping.py - This generates a file with updated positions for variants
# python Update_Chromosome.py - This generates a file with updated Chromosmes for variants
# These were required for 2 reasons:
# 1. The master map file had Affyx Ids instead of AX IDs for variants
# 2. Separate processes are required in Plink to update Chr and position

# Following this, run the following R script
# R RM_DUplicates_remapping.r
# Reason is master remapping file had duplicates and plink requires these removed

######################################
### Update/remap the chromosomes #####
######################################


# This is because some sex chromosome SNPs have been moved to autosomes
system(paste("plink --cow --bfile", input_data_raw,"--update-chr", update_chromosome, "2 1 --make-bed --allow-extra-chr --out", input_data_remapped_CHR))  

#######################################
### Update variant positions ##########
#######################################

system(paste("plink --cow --bfile", input_data_remapped_CHR,"--update-map", update_pos, "2 1 --make-bed --allow-extra-chr --out", input_data_remapped_POS))  



#######################################
### Restrict analysis to autosomes ####
#######################################

# specify allow extra chromosomes as some are coordinated differently and not picked up by Plink


system(paste("plink --cow --bfile", input_data_remapped_POS, "--chr 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 --allow-extra-chr --make-bed  --out", input_data_final))


################################################
### Extract just control and infected animals ##
################################################

system(paste("plink --cow --bfile", input_data_final, "--remove Exclude_Kerry.txt --make-bed --allow-extra-chr --out", input_data_final_no_Kerry))

########################################
### QC and Filtering ###################
########################################


# 1. Assess missing rates, first per individual/sample

system(paste("plink --cow --bfile", input_data_final_no_Kerry, "--mind 0.05 --make-bed  --out", out_missing_1))



# 2. Assess missing rates, next for per SNP locus

system(paste("plink --cow --bfile", out_missing_1, "--geno 0.05 --make-bed --out", out_missing_2))

# 3. Check remove SNPs with a low minor allele frequency
# Note 0.1 cut off in Higgins eqtl study 2018
# 0.1 cut off in eQTL study of DCs
# 0.1 cut off in horse eQTL study.
system(paste("plink --cow --bfile", out_missing_2, "--maf 0.01 --make-bed --out", out_maf))

# 4. Check for SNPs which deviate significantly from Hardy Weinberg Equilibrium
system(paste("plink --cow --bfile", out_maf, "--hwe 0.000001 --make-bed --out", out_HWE))


# Convert to VCF, this will aid in changing our Affy IDs to RS IDs
system(paste("plink --cow --bfile",out_HWE,"--recode vcf --out",out_final))



## MAF 10
# https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6294523/ --> Requirement for eQTL and our power
system(paste("plink --cow --bfile", out_missing_2, "--maf 0.1 --make-bed --out", out_maf_10))

system(paste("plink --cow --bfile", out_maf_10, "--hwe 0.000001 --make-bed --out", out_HWE_10))




system(paste("plink --cow --bfile",out_HWE_10,"--recode vcf --out", out_final_10))

## LD pruning

# Pruning Algorithm: it uses the first SNP (in genome order) and computes the correlation with the following ones (e.g. 50). 
# When it finds a large correlation, it removes one SNP from the correlated pair, keeping the one with the largest minor allele frequency (MAF), 
# thus possibly removing the first SNP. Then it goes on with the next SNP (not yet removed). 
# So, in some worst case scenario, this algorithm may in fact remove all SNPs of the genome (expect one).

# Remove SNPs with greater than 80% correlation
system(paste("plink --cow --bfile", out_HWE_10, "--indep-pairwise 50 5 0.6 --out SNPs_pruned_60 "))


####################################################################################################
############################### PCA Analysis + animal extraction ###################################
####################################################################################################

## Control Only

system(paste("plink --cow --bfile", out_HWE_10, "--remove Exclude_TB_animals.txt --pca --out plinkPCA_Control_only"))
system(paste("plink --cow --bfile",out_HWE_10,"--remove Exclude_TB_animals.txt --extract SNPs_pruned_70.prune.in  --recode vcf --out Control_genotype_only"))

# TB only
system(paste("plink --cow --bfile", out_HWE_10, "--remove Exclude_Control_animals.txt --pca --out plinkPCA_TB_only"))
system(paste("plink --cow --bfile",out_HWE_10,"--remove Exclude_Control_animals.txt --extract SNPs_pruned_60.prune.in --recode vcf --out TB_genotype_only_LD_60"))

################################
## All cattle (including Kerry)#
################################


# Including out bred population
system(paste("plink --cow --bfile", input_data_final, "--pca --out plinkPCA_all"))

eigenValues_all <- read.csv("plinkPCA_Control_only.eigenval", sep =  " ", header = F)
eigenVectors_all <- read.csv("plinkPCA_Control_only.eigenvec", sep =  " ", header = F)
colnames(eigenVectors_all) <- c("Batch", "Sample", paste("PC",1:20, sep =""))
eigenVectors_all <- eigenVectors_all %>% select(-1)
eigenVectors_all$Sample <- str_replace_all(eigenVectors_all$Sample, "_.*", "")
eigenVectors_all$Sample
#eigenVectors_all$Group <- c(rep("Control", 63), rep("Outbread",7), rep("Infected", 64))
head(eigenVectors_all)
eigen_percent_all <- round((eigenValues_all / (sum(eigenValues_all))*100), 2)

# All the animals including the Kerry cattle
# Note here, we use all the data provided
ggplot(data = eigenVectors_all, aes(x = PC1, y = PC2)) +
  geom_point(size = 2.5) +
  stat_ellipse(size = 1.5) +
  geom_hline(yintercept = 0, linetype = "dotted") +
  geom_vline(xintercept = 0, linetype = "dotted") +
  #scale_color_manual(breaks = c("Control", "Infected", "Outbread"),
                     #values=c("steelblue", "indianred", "gray5")) +
  theme(
    plot.title = element_text(face = "bold", size = (25))
  ) +
  labs(title = "PCA of cattle populations",
       x = paste0("Principle component 1 (",eigen_percent_all[1,1],"%)"),
       y = paste0("Principle component 2 (",eigen_percent_all[2,1],"%)")) +
  theme_classic()





# Just the control and infected animals

system(paste("plink --cow --bfile", input_data_final_no_Kerry, "--pca --out plinkPCA_C_TB"))

eigenValues <- read.csv("plinkPCA_C_TB.eigenval", sep =  " ", header = F)
eigenVectors <- read.csv("plinkPCA_C_TB.eigenvec", sep =  " ", header = F)
colnames(eigenVectors) <- c("Batch", "Sample", paste("PC",1:20, sep =""))
eigenVectors <- eigenVectors %>% select(-1)
eigenVectors$Sample <- str_replace_all(eigenVectors$Sample, "_.*", "")
eigenVectors$Sample
eigenVectors$Group <- c(rep("Control", 63), rep("Infected", 64))
head(eigenVectors)
eigen_percent <- round((eigenValues / (sum(eigenValues))*100), 2)



ggplot(data = eigenVectors, aes(x = PC1, y = PC2, color = Group, shape = Group)) +
  geom_point(size = 2.5) +
  geom_hline(yintercept = 0, linetype = "dotted") +
  geom_vline(xintercept = 0, linetype = "dotted") +
  scale_color_manual(breaks = c("Control", "Infected", "Outbread"),
                     values=c("steelblue", "indianred", "gray5")) +
  theme(
    plot.title = element_text(face = "bold", size = (25))
  ) +
  labs(title = "PCA of cattle populations",
       x = paste0("Principle component 1 (",eigen_percent[1,1],"%)"),
       y = paste0("Principle component 2 (",eigen_percent[2,1],"%)")) +
  theme_classic()



  