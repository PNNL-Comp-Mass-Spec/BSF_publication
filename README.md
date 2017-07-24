# BSF_publication
All the data and materials for the publication about the Blazing Signature Filter. We have deposited here both the data and the code for various figures in the manuscript.

- Figure 2 - the benchmarking time trial for BSF versus
- Figure 3 - subnetwork for HDAC inhibitors
- Figure 4, 5, 6 - whole genome similarity comparisons.
- Figure S1 - LINCS pairwise similarity plot
- Figure S2 - subnetwork for Niclosamide


## Benchmarking the BSF - Figure 2
To demonstrate the speed of the Blazing Signature Filter, we performed a benchmark test of BSF, cosine similarity and Euclidean distance using a synthetic dataset mimicking gene expression measurements. 
- ~/benchmark/timetrials.txt - the console output of the time trial
- ~/benchmark/GraphTimeTrial.ipynb - the ipython notebook used to make figure 2
- ~/benchmark/ParseTimeTrials.py - auxiliary python code used by the notebook


## LINCS L1000 Dataset - Figure 3, S1, S2
In the manuscript, we compare the gene expression patterns of data from the LINCS L1000 project, to demonstrate the ability of BSF to scale to billions of pairwise comparisions and extract insight. Data and code for these figures are found in the following
- ~/lincs_data/bsf_allscore_heatmap.csv - the similarity of all 6.9 billion gene expression pairs
- ~/lincs_data/fig_s1_lincs_results.ipynb - the iPython notebook for figure S1
- ~/lincs_data/file_3a_HDAC_lincs_signatures.txt	- data for figure 3
- ~/lincs_data/file_3b_HDAC_lincs_top_edges.txt - data for figure 3
- ~/lincs_data/file_S1a_lincs_dn.bin.gz	- data for figure S1
- ~/lincs_data/file_S1b_lincs_up.bin.gz	- data for figure S1
- ~/lincs_data/file_S2a_nonhuman_lincs_signatures.txt	- data for figure S2
- ~/lincs_data/file_S2b_nonhuman_lincs_top_edges.txt - data for figure S2

## KEGG Genome similarity - Figure 4, 5, 6
In the manuscript, we perform a whole genome similarity for all pairs of genomes annotated by KEGG, which is Figure 4-6, showing the average number of shared genes between a genome and other genomes within its taxonomic group. Data and code to create the figures is found in the following:
- ~/kegg_data/Kegg_ko_org_matrix.txt - auxiliary data file for the iPython notebook
- ~/kegg_data/Kegg_ko_org_matrix_cols_index.txt - auxiliary data file for the iPython notebook
- ~/kegg_data/Kegg_ko_org_matrix_rows_index.txt - auxiliary data file for the iPython notebook
- ~/kegg_data/figure_4_5_bsf-kegg.ipynb - iPython notebook used to create figures 4 and 5
- ~/kegg_data/figure_6_bsf-kegg.ipynb - iPython notebook used to create figure 6
