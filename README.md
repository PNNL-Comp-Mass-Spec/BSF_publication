# BSF_publication
All the data and materials for the publication about the Blazing Signature Filter. We have deposited here both the data and the code for various figures in the manuscript.

- Figure 2 - the benchmarking time trial for BSF versus
- Figure 3 - subnetwork for HDAC inhibitors
- Figure 4 - whole genome similarity comparisons.
- Figure S1 - LINCS pairwise similarity plot
- Figure S2 - subnetwork for Niclosamide


## Benchmarking the BSF - Figure 2
To demonstrate the speed of the Blazing Signature Filter, we performed a benchmark test of BSF, cosine similarity and Euclidean distance using a synthetic dataset mimicking gene expression measurements. 
- timetrials.txt - the console output of the time trial
- Figure_2.ipynb - the ipython notebook used to make figure 2
- ParseTimeTrials.py - auxiliary python code used by the notebook

The synthetic data was created as a table (15K columns x 20K rows) of floating point numbers drawn randomly from the gaussian distribution of N(0, 0.5). Rows can be thought of as different gene measurements, and columns as distinct datasets. This continuous data was binarized into two tables to represent the extremes of the distribution, i.e. values < -0.6 were written as 1 in a binary table representing the ‘low’ values and values > 0.6 were written as 1 to a binary table representing high values.

We performed the full pairwise comparison of all 15k columns versus each other on a single CPU (Intel Core i7-3770, Ivy Bridge). To characterize the time-dependence of each algorithm on the length of the signature, we tested each algorithm with a different number of rows ranging from 2000 to 20,000. This is essential to understanding the utility of each algorithm, as different applications may contain highly variable signature lengths. The total number of comparisons done is about 225 million. Because for each pair (i,j) of columns, we perform the comparison of both the up and down matrix. Since these results are symmetric, that amounts to 15,000 * 15,000 /2 (for symmetric) * 2 (for up and down matrix).

## Binarized LINCS L1000 Dataset - Figure S1
We extract the information of differentially expressed genes identified by characteristic direction method. We download the mongo DB (<http://amp.pharm.mssm.edu/public/L1000CDS_download/>). These raw files were converted prior to input in the BSF; the data are gzipped and consist of a matrix with 64-bit unsigned integers. It has 22,268 genes by 117,373 signatures. It is used to generate Supplementary Figure 1 of the BSF paper.
- file_S1a_lincs_dn.bin.gz: It contains the down-regulated genes of LINCS L1000 CDS2. 
- file_S1b_lincs_up.bin.gz: It contains the up-regulated genes of LINCS L1000 CDS2. 
You can easily unzip it and get the numpy-formatted matrix as follows:
```python
### Please use python 3 for this example code.
import gzip

input_file = gzip.open(filename, 'rb')
nrows = int.from_bytes(input_file.read(4), byteorder='little')
ncols = int.from_bytes(input_file.read(4), byteorder='little')
dt = np.dtype(np.uint64)
dt = dt.newbyteorder('L')
print('uint64_mat size:', nrows, ncols)
t = np.frombuffer(input_file.read(), dtype=np.uint64).reshape((nrows, ncols))
```

## L1000 signatures associated to HDAC inhibitors - Figure 3
Data used to generate Figure 3.
- file_S2a_HDAC_lincs_signatures.txt (tab-delimited): It contains a list of signatures perturbed by the well-known 9 HDAC inhibitors.

| Header | Description |
| ------------ | ------------- |
| \_id | object id of mongodb document |
| cell_id | A shorthand CMap identifier number assigned to each cell line used in the L1000 assay. |
| pert_desc | A brief summary of the biological function (for genetic perturbagens) or mechanism of action (for compound perturbagens) |
| pert_dose | Precise amount of compound used to treat cells. |
| pert_dose_unit | Unit (generally micromolar) applied to the dose of compound used to treat cells. |
| pert_id | A unique identifier for a perturbagen that refers to the perturbagen in general, not to any particular batch or sample. |
| pert_time | The length of time, expressed as a number, that a perturbagen was applied to the cells; does not include the unit. |
| pert_time_unit | The unit that applies to the pert_time numerical value. |
| pert_type | Abbreviated designation for perturbagen type, referring to compound or genetic perturbagens that are used in cell treatments to assess gene expression effects. |
| sig_id | A CMap unique  identification number assigned to each signature generated from L1000 data. |
| dnGenesSize | The number of down-regulated genes in this signature. |
| upGenesSize| The number of up-regulated genes in this signature. |
* Note: Please refer to this [link](https://docs.google.com/document/d/1q2gciWRhVCAAnlvF2iRLuJ7whrGP6QjpsCMq1yWz7dU/edit) for more details.
- file_S2b_HDAC_lincs_top_edges.txt (tab-delimited): Among 6.3 million pairs, it provides top 20,000 similar pairs.

The actual image for figure 3 was created using a custom javascript based on vis.js using the above files.

## L1000 signatures associated to niclosamide - Figure S2
These files contain the raw data of the Supplementary Figure 2. Niclosamide is one of the non-human medications.
- file_S4a_nonhuman_lincs_signatures.txt (tab-delimited): It contains a list of signatures perturbed by the non-human medications.
- file_S4b_nonhuman_lincs_top_edges.txt (tab-delimited): It contains top 20,000 similar pairs linked to signatures of (a).

The actual image for figure 3 was created using a custom javascript based on vis.js using the above files.

## KEGG Genome similarity - Figure 4
This excel file contains the raw data of the Figure 4, which shows the average number of shared genes between a genome and other genomes within its taxonomic group.
- file_S3_kegg_taxa_group.xlsx: 
