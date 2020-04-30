## Evaluation process and the corresponding descriptions

1. We took the commonly identified PSMs of pFind3, MaxQuant, Mascot, Comet and X!Tandem for evaluation using getsamepeptideinfo.py, mascot2MQ&pFind.py, comet2MQ&pFind.py and tandem2all.py. The code files percolator-result.py and percolator-result2.py were used to read the quality controlled PSMs of X!Tandem searching results. The code file choose_peplist.py was used to read the quality controlled PSMs of Mascot.
2. The identified peptide sequences were matched to the corresponding spectra in each MGF file and the corresponding mz-intensity key value pairs were extracted, which were used as the ground truth of the evaluation (buildtargetmgf.py).
3. The results from step 2 were converted to the corresponding input format of each tool separately (toXXinput.py). Note that pDeep2 and Guan's work do not need to be converted.
4. pDeep2 and Guan's work was run in the local GPU environment. Prosit and MS2PIP was run on its corresponding Web server.
5. After the prediction of each tool, the output files were converted to the MSP format (XX2msp.py file). Note that Prosit does not need MSP conversion and the results of Guan's work were output to the MSP format by ourselves.
6. The prediction results of each tool were compared with the ground truth, respectively. The peptide sequence, peptide length, charge state, PCC, intensity value and other information were written into the output file (persim.py and perSimOnlymatch.py).
7. After analyzing the results of these tools, the Median PCCs of b ions, y ions, and b&y ions were calculated (ComputeMEDpersim.py and ComputeMEDpersimOnlymatch.py).
8. The proportion of peptides with PCC > 0.8 and PCC > 0.9 was calculated (filterMEDpersim.py and filterMEDpersimOnlymatch.py).
9. The PCC for the predicted intensities of the top 6, 8, 11 and 15 peaks was calculated (ComputeTopKpeaks.py).
10. The data processing for SCC and SA calculations is similarly to PCC.In step 6, we can run spearman.py and Spectral.py to calculate SCC and SA. In step 7, we can run ComputeMEDspearman.py and ComputeMEDspectral.py to count the median SCC and SA.In step 8, we can run filterMEDspearman.py and filterMEDspectral.py to calculate the proportion of peptides with SCC,SA> 0.8 and SCC,SA> 0.9.


## Other codes related with the evaluation process
1. Spellms2pipresult.py: Since MS2PIP's Web server only can predict MS/MS spectra up to 100,000 peptides at a time. This file was used to merge all the MS2PIP's results from a dataset into a single file.
2. Dealdataforplot.py: This file was used to calculate information about b, y, and b&y ions.
3. baseline.py: This file was used to calculate the baseline of each dataset.


##  Contact

  If you have any question, please contact [Dr. Cheng Chang](https://orcid.org/0000-0002-0361-2438)![](https://orcid.org/sites/default/files/images/orcid_16x16.png)
(Email: [changchengbio@163.com](mailto:changchengbio@163.com)).
