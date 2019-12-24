## Evaluation process and the corresponding documents

1. Take the commonly identified PSMs of pFind3 and MaxQuant for evaluation (getsamepeptideinfo.py).
2. The identified peptide sequences were matched to the corresponding spectra in each MGF file and the corresponding mz-intensity key value pairs were extracted, which was used as the ground truth of the evaluation (buildtargetmgf.py).
3. The results from step 2 are converted to the corresponding input format of each tool separately (toXXinput.py). Note that pDeep2 and Guan's work do not need to be converted.
4. pDeep2 and Guan's work run in the local GPU environment. Prosit and MS2PIP run on its corresponding Web server.
5. After the prediction of each tool, the output files will be converted to the MSP format (XX2msp.py file). Note that Prosit does not need MSP conversion and the results of Guan's work were output to the MSP format by ourselves.
6. The prediction results of each tool are compared with the ground truth, respectively. The peptide sequence, peptide length, charge state, PCC, intensity value and other information are written into the output file (persim.py and perSimOnlymatch.py are used when 0 value is considered and 0 value is not considered).
7. After analyzing the results of these tools, the Median PCCs of B ions, Y ions, and BY ions were calculated (ComputeMEDpersim.py and ComputeMEDpersimOnlymatch.py are used when 0 value is considered and 0 value is not considere).
8. Calculate the proportion of peptides with PCC > 0.8 and PCC > 0.9 (filterMEDpersim.py and filterMEDpersimOnlymatch.py are used when 0 value is considered and 0 value is not considered).
9. Calculate the PCC for the predicted intensities of the top 6, 8, 11 and 15 peaks (ComputeTopKpeaks.py).

## Other codes related with the evaluation process
1. Spellms2pipresult.py: Since MS2PIP's Web server only can predict MS/MS spectra up to 100,000 peptides at a time. This file is used to merge all the MS2PIP's results from a dataset into a single file.
2. Dealdataforplot.py: This file is used to calculate information about b, y, and by ions.

##  Contact

  If you have any question, please contact [Dr. Cheng Chang](https://orcid.org/0000-0002-0361-2438)![](https://orcid.org/sites/default/files/images/orcid_16x16.png)
(Email: [changchengbio@gmail.com](mailto:changchengbio@gmail.com)).

