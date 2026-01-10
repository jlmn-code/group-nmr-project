---
title: "Untitled"
author: 'jlmn'
format: html
---


# group-nmr-project

Welcome everyone. I want to create a code to manipulate a nmr collection

The idea is:

1.  open a large collection of nmr of HSQC

I don't have NMR spectra but I have worked so much with them and know its structure and form and I can simulated. In the file `code` there is a script `nmr_simulator.py` where in *python* code create 15 *HSQC* with the same structure that a real HSQC save in **MNova** software in format `.txt` or .csv

<br>

The results are HSQC spectra of size 8 megas and spectrum with noise

![TABLE: RAW HSQC](images/tbl-raw-hsqc.jpeg) ![GRAPH: RAW HSQC](images/fig-hsqc-raw.jpeg)

2.  Autamatic load & filter

With a simple lines of code, we can open all spectra collection reduce the files and improve the tables to analysis of data and spectra to elucidation and integration

![TABLE: FILTER HSQC](images/tbl-filter-hsqc.jpeg)  ![GRAPH: FILTER HSQC](images/fig-hsqc-filter.jpeg)

3.  reduce the size the files

With the 2. point reduce the info. from more 100 to 0.1 megas

![TABLE: INFO. FILES](images/tbl-info-files.jpeg)

![Column graph reduction size of HSQC files](images/fig-save.jpeg)

4.  open in a simple dataframe

![All HSQC spectra](images/fig-all-dataset.jpeg) 

5.  elucidate the compound

6.  integrate and quantify 6.
