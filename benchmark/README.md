# TimeTrialsForBSF
here's some code to make the figure for the paper


To demonstrate the speed of the Blazing Signature Filter, we performed a benchmark test of BSF, cosine similarity and Euclidean distance using a synthetic dataset mimicking gene expression measurements. This repository holds the console output from that time trials (bakeoff). and then some python code to parse that output and make a chart.

The synthetic data was created as a table (15K columns x 20K rows) of floating point numbers drawn randomly from the gaussian distribution of N(0, 0.5). Rows can be thought of as different gene measurements, and columns as distinct datasets. This continuous data was binarized into two tables to represent the extremes of the distribution, i.e. values < -0.6 were written as 1 in a binary table representing the ‘low’ values and values > 0.6 were written as 1 to a binary table representing high values. 


We performed the full pairwise comparison of all 15k columns versus each other on a single CPU (Intel Core i7-3770, Ivy Bridge). To characterize the time-dependence of each algorithm on the  length of the signature, we tested each algorithm with a different number of rows ranging from 2000 to 20,000. This is essential to understanding the utility of each algorithm, as different applications may contain highly variable signature lengths. As expected, the time taken by each algorithm grows with the length of the signature. However, we note that the time dependence of the BSF grows dramatically more slowly than other methods.  The total number of comparisons done is about 225 million. Because for each pair (i,j) of columns, we perform the comparison of both the up and down matrix. Since these results are symmetric, that amounts to 15,000 * 15,000 /2 (for symmetric) * 2 (for up and down matrix)
