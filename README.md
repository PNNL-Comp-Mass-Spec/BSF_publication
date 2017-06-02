# BSF_publication
All the data and materials for the publication about the Blazing Signature Filter. We have deposited here both the data and the code for various figures in the manuscript.

* Figure 2 - the benchmarking time trial for BSF versus
* Figure 3 - subnetwork for HDAC inhibitors
* Figure 4 - whole genome similarity comparisons.
* Figure S1 - LINCS pairwise similarity plot
* Figure S2 - subnetwork for Niclosamide


## Binarized LINCS L1000 Dataset.
We extract the information of differentially expressed genes identified by characteristic direction method. We download the mongo DB and fetch this information. Please refer to <http://amp.pharm.mssm.edu/public/L1000CDS_download/>.
Both of these files are gzipped and consist of a matrix with 64-bit unsigned integers. It has 22,268 genes by 117,373 signatures. It is used to generate Supplementary Figure 1 of the BSF paper.
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

## L1000 signatures associated to HDAC inhibitors.
It is used to generate Figure 3 of the BSF paper.
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

## L1000 signatures associated to niclosamide.
These files contain the raw data of the Supplementary Figure 2. Niclosamide is one of the non-human medications.
- file_S4a_nonhuman_lincs_signatures.txt (tab-delimited): It contains a list of signatures perturbed by the non-human medications.
- file_S4b_nonhuman_lincs_top_edges.txt (tab-delimited): It contains top 20,000 similar pairs linked to signatures of (a).

## KEGG Genome similarity.
This excel file contains the raw data of the Figure 4, which shows the average number of shared genes between a genome and other genomes within its taxonomic group.
- file_S3_kegg_taxa_group.xlsx: 
