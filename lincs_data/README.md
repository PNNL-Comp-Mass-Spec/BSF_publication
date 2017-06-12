# LINCS application for BSF

## LINCS L1000 Dataset - Figure S1
We extract the information of differentially expressed genes identified by characteristic direction method. We download the mongo DB (<http://amp.pharm.mssm.edu/public/L1000CDS_download/>). These raw files were converted prior to input in the BSF; the data are gzipped and consist of a matrix with 64-bit unsigned integers. It has 22,268 genes by 117,373 signatures. It is used to generate Supplementary Figure 1 of the BSF paper.
- ~/lincs_data/file_S1a_lincs_dn.bin.gz: It contains the down-regulated genes of LINCS L1000 CDS2. 
- ~/lincs_data/file_S1b_lincs_up.bin.gz: It contains the up-regulated genes of LINCS L1000 CDS2. 
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
- ~/lincs_data/file_S2a_HDAC_lincs_signatures.txt (tab-delimited): It contains a list of signatures perturbed by the well-known 9 HDAC inhibitors.

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
- ~/lincs_data/file_S2b_HDAC_lincs_top_edges.txt (tab-delimited): Among 6.3 million pairs, it provides top 20,000 similar pairs.

The actual image for figure 3 was created using a custom javascript based on vis.js using the above files.

## L1000 signatures associated to niclosamide - Figure S2
These files contain the raw data of the Supplementary Figure 2. Niclosamide is one of the non-human medications.
- ~/lincs_data/file_S4a_nonhuman_lincs_signatures.txt (tab-delimited): It contains a list of signatures perturbed by the non-human medications.
- ~/lincs_data/file_S4b_nonhuman_lincs_top_edges.txt (tab-delimited): It contains top 20,000 similar pairs linked to signatures of (a).

The actual image for figure S2 was created using a custom javascript based on vis.js using the above files.
