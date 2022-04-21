
# This bash script downloads data (transcriptomic) from a specified data base
# #### This script is activated in /data directory #######
# This bash script carrys out fastqc analysis on raw transcriptomic files downloaded from NCBI/GEO/SRA
# It also outputs number of reads in each sample which is useful for supplementary information


# COMMAND 
# fastq-dump --split-files SRRXXX


# At this point it is necessary to change files to change files to 
# C001, C002..... C00N or C0001 ... if samples > 100
# T001, T002..... T00N or T0001 ... if samples > 100


# Make a separate script for this with loop etc...

# Make a directory ~/data/Control_data
# Move all control files into this
mkdir Control_data
mv C0* /Control_data

# Same for TB
mkdir TB_data
mv T0* TB_Data

# Check the number of reads in samples
# Reads in fq.gz samples are number of lines/4 which follows fq.gz file format
# This will be useful supplementary information.
# Specify directory also of the fq.gz files to ensure command works.
for i in C0*.fq.gz; do expr $(zcat $i | wc -l) / 4; done # Control dataset
for i in T0*.fq.gz; do expr $(zcat $i | wc -l) / 4; done # TB dataset
#for i in N*.fq.gz; do expr $(zcat $i | wc -l) / 4; done # Unannotated dataset



# Make a directory in the Control directory and output FastQC results to this directory
# Once the data has been downloaded and renamed using naming convention C0...
# Change directory depending on where your data is
cd ~/eqtl_study/data/Control_data
mkdir fastqc
# Command is fastqc on all samples, with 4 processers and output files to fastqc directory
fastqc CO* --threads 4 -o fastqc

# Make a directory in the Tuberculosis directory and output FastQC results to this directory
cd ~/eqtl_study/data/Tuberculosis_data
mkdir fastqc
fastqc TO* --threads 4 -o fastqc

# At this stage it is important to look at fastqc report and determine whether trimming needs to be applied
# Number of tools to do this: Trimgalore, trimmomatic, fastp etc. Read up on documentation and apply if required
# trimming was not required on bovine dataset, quality extremely good accross all bases



