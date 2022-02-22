# eQTL_TWAS_ASE_analysis
This repository contains scripts required to perform an expression quantitative trait loci (eQTL), transcriptome wide association study (TWAS) and allele specific expression (ASE) analysis

## List of software/computational tools used in this analysis
- _fastqc_
- _STAR_
- _featureCounts_
- _DESeq2_
- _PEER_
- _FastQTL_
- _PLINK_

## Required datasets
1. RNA-seq data
2. Genotype data
3. Genome wide assocation studies summary statistics / individual level data

## Preprocessing of RNA-seq reads
Note: All of the preprocessing steps in RNA-seq can be implemented using the python script
The first step invovled in this type of analysis involves an assessment of the transcriptomic data available for analysis using _fastqc_. 

## Differential expression analysis
DEA analysis will be carried out using _DESeq2_ in _R_

## Preprocessing of SNP/genotype data
