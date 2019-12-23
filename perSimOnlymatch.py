# -*- coding: utf-8 -*-
import re
import AminoAcidMass as config
import time

start = time.time()

SamePeptideFile = 'PXD003881/PXD003881.txt'
ToolpredictFile = 'PXD003881/pDeep2-result/pDeep2.msp'
TargetMGF = 'PXD003881/TargetMGF.mgf'
OutputPCCfile = 'PXD003881/pDeep2-result/pDeep2_onlymatch_inten_pears.txt'
all_pears = []
peplen = []
titleList = []
pepcharge = []

with open(SamePeptideFile, 'r') as f:
	for line in f:
		if line == '':break
		if 'peptide	modification' in line:continue
		title = re.split('\t|\n',line)[3]
		res_seq = re.split('\t|\n',line)[0]
		res_charge = re.split('\t|\n',line)[2]
		if len(res_seq) <= 30 and len(res_seq) >= 7:
			if int(res_charge) >= 1 and int(res_charge) <= 6:
				titleList.append(title)
print(len(titleList))

num = 0
title2inten = {}

with open(ToolpredictFile, 'r') as f:
	while True:
		line = f.readline()
		if line == '':break
		if 'ModString=' in line:
			pepinfos = re.split('ModString=|\n',line)[1]
			seq = pepinfos.split('//')[0]
			line = f.readline()
			line = f.readline()
			temp_dict = {}
			ion_mz = []
			ion_inten = []
			while 'Name:' not in line:
				ion = re.split('\t|\n',line)[2]
				mz = float(re.split('\t|\n',line)[0])
				inten = float(re.split('\t|\n',line)[1])
				if inten != 0.0:
					ion_mz.append(mz)
					ion_inten.append(inten)
				line = f.readline()
				if line == '':break
			title2inten[titleList[num]] = [pepinfos, ion_mz, ion_inten]
			num += 1
print(len(title2inten))

with open(TargetMGF, 'r') as f:
	while True:
		line = f.readline()
		if line == '':break
		if 'TITLE=' in line:
			mgf_title = re.split('=|\n',line)[1]
			mgf_pepinfo = title2inten[mgf_title][0]
			mgf_seq = mgf_pepinfo.split('/')[0]
			mgf_mods = mgf_pepinfo.split('/')[2]
			mgf_charge = mgf_pepinfo[-1]
			line = f.readline()
			line = f.readline()
			mgf_mz2inten = {}
			intenList = []
			while 'END IONS' not in line:
				mz = float(re.split(' |\n', line)[0])
				inten = float(re.split(' |\n', line)[1])
				intenList.append(inten)
				mgf_mz2inten[mz] = inten
				line = f.readline()
			max_inten = max(intenList)
			mgf_inten = []
			for pred_mz in title2inten[mgf_title][1]:
				isvalue = False
				for mz in mgf_mz2inten.keys():
					if abs((pred_mz - mz))/mz*(10**6) <= 20:
						mgf_inten.append(mgf_mz2inten[mz]/max_inten)
						isvalue = True
						break
				if not isvalue:
					mgf_inten.append(0.0)

			per = config.pearSim(title2inten[mgf_title][2], mgf_inten)
			all_pears.append(per)
			peplen.append(len(mgf_pepinfo.split('/')[0]))
			pepcharge.append(mgf_charge)

with open(OutputPCCfile, 'w') as f:
	f.write('all_pears\tpeplen\tcharge\n')
	for i in range(len(all_pears)):
		f.write(str(all_pears[i]) + '\t' + str(peplen[i]) + '\t' + str(pepcharge[i]) + '\n')

endtime = time.time() - start
print(endtime)
