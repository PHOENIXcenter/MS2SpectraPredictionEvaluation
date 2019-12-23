import re 

pdeep2file = 'PXD003881/pDeep2-result/pDeep2_all_inten_pears.txt'
prositfile = 'PXD003881/Prosit-result/Prosit_all_inten_pears.txt'
LCMSMSfile = 'PXD003881/LCMSMS-result/LCMSMS_all_inten_pears.txt'
ms2pipfile = 'PXD003881/MS2PIP-result/MS2PIP_new_all_inten_pears.txt'
# massanalyzerfile = 'PXD005590/MassAnalyzer-result/MassAnalyzer_all_inten_pears.txt'
AllToolsAllion = 'PXD003881/AllToolsAllionIntensity.txt'
AllToolsSingleion = 'PXD003881/AllToolsBionIntensity.txt'
peptides = []
peplen = []
charges = []
ionpos = []
pDeep2intensity = []
Prositintensity = []
LCMSMSintensity = []
MS2PIPintensity = []
# MassAnalyzerintensity = []
MGFintensity = []

with open(pdeep2file, 'r') as f:
	for line in f:
		if 'peptide	length' in line:continue
		if line == '':break
		peptide = re.split('\t|\n',line)[0]
		length = re.split('\t|\n',line)[1]
		charge = re.split('\t|\n',line)[2][:1]
		# pcc = re.split('\t|\n')[3]
		pred_b_ion = re.split('\t|\n',line)[4][1:-1].split(', ')
		mgf_b_ion = re.split('\t|\n',line)[5][1:-1].split(', ')
		pred_y_ion = re.split('\t|\n',line)[7][1:-1].split(', ')
		mgf_y_ion = re.split('\t|\n',line)[8][1:-1].split(', ')
		for pos in range(len(pred_b_ion)):
			peptides.append(peptide)
			peplen.append(length)
			charges.append(charge)
			ionpos.append('B' + str(pos + 1))
			pDeep2intensity.append(pred_b_ion[pos])
			MGFintensity.append(mgf_b_ion[pos])
		# for pos in range(len(pred_y_ion)):
		# 	peptides.append(peptide)
		# 	peplen.append(length)
		# 	charges.append(charge)
		# 	ionpos.append('Y' + str(pos + 1))
		# 	pDeep2intensity.append(pred_y_ion[pos])
		# 	MGFintensity.append(mgf_y_ion[pos])

with open(prositfile, 'r') as f:
	for line in f:
		if 'peptide	length' in line:continue
		if line == '':break
		# pcc = re.split('\t|\n')[3]
		pred_b_ion = re.split('\t|\n',line)[4][1:-1].split(', ')
		pred_y_ion = re.split('\t|\n',line)[7][1:-1].split(', ')
		for pos in range(len(pred_b_ion)):
			Prositintensity.append(pred_b_ion[pos])
		# for pos in range(len(pred_y_ion)):
		# 	Prositintensity.append(pred_y_ion[pos])

with open(LCMSMSfile, 'r') as f:
	for line in f:
		if 'peptide	length' in line:continue
		if line == '':break
		# pcc = re.split('\t|\n')[3]
		pred_b_ion = re.split('\t|\n',line)[4][1:-1].split(', ')
		pred_y_ion = re.split('\t|\n',line)[7][1:-1].split(', ')
		for pos in range(len(pred_b_ion)):
			LCMSMSintensity.append(pred_b_ion[pos])
		# for pos in range(len(pred_y_ion)):
		# 	LCMSMSintensity.append(pred_y_ion[pos])

with open(ms2pipfile, 'r') as f:
	for line in f:
		if 'peptide	length' in line:continue
		if line == '':break
		# pcc = re.split('\t|\n')[3]
		pred_b_ion = re.split('\t|\n',line)[4][1:-1].split(', ')
		pred_y_ion = re.split('\t|\n',line)[7][1:-1].split(', ')
		for pos in range(len(pred_b_ion)):
			MS2PIPintensity.append(pred_b_ion[pos])
		# for pos in range(len(pred_y_ion)):
		# 	MS2PIPintensity.append(pred_y_ion[pos])

# with open(massanalyzerfile, 'r') as f:
# 	for line in f:
# 		if 'peptide	length' in line:continue
# 		if line == '':break
# 		# pcc = re.split('\t|\n')[3]
# 		pred_b_ion = re.split('\t|\n',line)[4][1:-1].split(', ')
# 		pred_y_ion = re.split('\t|\n',line)[7][1:-1].split(', ')
# 		for pos in range(len(pred_b_ion)):
# 			MassAnalyzerintensity.append(pred_b_ion[pos])
# 		# for pos in range(len(pred_y_ion)):
# 		# 	MassAnalyzerintensity.append(pred_y_ion[pos])

print(len(peptides))
print(len(ionpos))
print(len(pDeep2intensity))
print(len(Prositintensity))
print(len(LCMSMSintensity))
print(len(MS2PIPintensity))
print(len(MGFintensity))
# print(len(MassAnalyzerintensity))

with open(AllToolsSingleion, 'w') as f:
	f.write('peptide\tlength\tcharge\tionnumber\tpDeep2predictInten\tPrositpredictInten\tLCMSMSpredictInten\tMS2PIPpredictInten\tMGFInten\n')
	for i in range(len(peptides)):
		f.write(peptides[i] + '\t' + peplen[i] + '\t' + charges[i] + '\t' + ionpos[i] + '\t' + pDeep2intensity[i] + '\t' + Prositintensity[i] + '\t' + LCMSMSintensity[i] + '\t' + MS2PIPintensity[i] + '\t' + MGFintensity[i] + '\n')	

# with open(AllToolsAllion, 'w') as f:
# 	f.write('peptide\tlength\tcharge\tionnumber\tpDeep2predictInten\tPrositpredictInten\tLCMSMSpredictInten\tMS2PIPpredictInten\tMGFInten\n')
# 	for i in range(len(peptides)):
# 		f.write(peptides[i] + '\t' + peplen[i] + '\t' + charges[i] + '\t' + ionpos[i] + '\t' + pDeep2intensity[i] + '\t' + Prositintensity[i] + '\t' + LCMSMSintensity[i] + '\t' + MS2PIPintensity[i] + '\t' + MGFintensity[i] + '\n')