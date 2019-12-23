## Evaluation process and corresponding documents

1. Take the intersection of the pFind3 and Maxquant results as the data for the evaluation. (done by getsamepeptideinfo.py)
2. Combining the identified intersection of MGF file and pFind3 and Maxquant, the identified peptide sequence was matched with the mass spectrogram in MGF file to facilitate the acquisition of the corresponding mz-intensity key value pair, which was used as the ground truth of the evaluation. (done by buildtargetmgf.py)
3. The intersection results in the first step are processed and converted to the corresponding input format of each tool separately. (done by toxxxinput.py, pDeep2 and Guan's work do not need to be converted)
4. PDeep2 and Guan's work run in the local GPU environment;Prosit and MS2PIP run on its corresponding Web server.
5. After the prediction of each tool, the output format will be unified into the MSP file. (done by xxx2msp.py file, Prosit does not need conversion, and Guan's work output part shall be directly output to the MSP file by ourselves)
6. The prediction results of each tool are compared with the ground truth data respectively, and the peptide sequence, peptide length, charge value, PCC, intensity value and other information are written into the file. (persim.py and perSimOnlymatch.py are used when 0 value is considered and 0 value is not considered)
7. After analyzing the results of the comparison of the tools and ground truth data, the Median PCCs of B ions, Y ions, and BY ions were counted. (ComputeMEDpersim.py and ComputeMEDpersimOnlymatch.py are used when 0 value is considered and 0 value is not considere)
8. For the proportion of PCC > 0.8 and the proportion of PCC > 0.9 parts statistics. (filterMEDpersim.py and filterMEDpersimOnlymatch.py are used when 0 value is considered and 0 value is not considered)
9. Statistics are performed on the PCC for the predicted peak intensity of top6, 8, 11, and 15. (done by ComputeTopKpeaks.py)

## Code outside the evaluation process
1. Spellms2pipresult.py: since MS2PIP's Web server predicts up to 100,000 peptides at a time, this file is used to consolidate all peptide results from a dataset into a single file.
2. Dealdataforplot.py: this file is used to obtain information about B, Y, and BY ions required for plotting.
