# KEGG Application for BSF

## How to generate the KEGG data files

### BSF_Kegg.jar
This is a simple program created to generate the KEGG data files. Using [Kegg REST api](http://www.kegg.jp/kegg/rest/keggapi.html) the program gathers a list of each(ko numbers, organisms, pathways) using (http://rest.kegg.jp/list/ko, http://rest.kegg.jp/list/organism, http://rest.kegg.jp/list/pathway) respectivly. Then it creates three files for each set(Ko/Pathway, Organism/Pathway). The first two files are a row and column index, with the row or column identifier and the line they are located on being the zero based index in the matrix file. The third file is the matrix of zeros and ones, each character is a column and each line is a row. Zero means the ko or organism is not found in the pathway, one means it was found.
#### Running BSF_Kegg.jar
To run, download the file and in the command prompt
```
java -jar BSF_Kegg.jar
```
## Kegg data files
<!--### Kegg_ko_path_matrix.txt
The matrix of found KOs in pathways represented by zero(not found) or one(found).
Example
```
100000000
100100000
000000000
000000000
000000000
000110000
```
### Kegg_ko_path_matrix_rows_index.txt
A file that lists the KOs in the matrix, line number is the index found in the matrix.
### Kegg_ko_path_matrix_columns_index.txt
A file that lists the pathways in the matrix, line number is the index found in the matrix.-->
### Kegg_ko_org_matrix.txt
The matrix of found KOs in organisms represented by zero(not found) or one(found).

Example
```
100000000
100100000
000000000
000000000
000000000
000110000
```
### Kegg_ko_org_matrix_rows_index.txt
A file that lists the KOs in the matrix, line number is the index found in the matrix.
### Kegg_ko_org_matrix_columns_index.txt
A file that lists the organisms in the matrix, line number is the index found in the matrix.
