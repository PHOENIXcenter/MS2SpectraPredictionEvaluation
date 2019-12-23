# -*- coding: utf-8 -*-
import re
import AminoAcidMass as config
import time

start = time.time()

SamePeptideFile = 'PXD003881/PXD003881.txt'
ToolpredictFile = 'PXD003881/pDeep2-result/pDeep2.msp'
TargetMGF = 'PXD003881/TargetMGF.mgf'
OutputPCCfile = 'PXD003881/pDeep2-result/pDeep2_all_inten_pears.txt'
pred_b_intens, pred_y_intens = [], []
mgf_b_intens, mgf_y_intens = [], []
SeqInfos, ChargeInfos = [], []
b_ion_PCC, y_ion_PCC, by_ion_PCC = [], [], []
titleList = []

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
			while 'Name:' not in line:
				if '^' not in line:
					ion = re.split('\t|\n',line)[2].split('/')[0][1:]
					inten = float(re.split('\t|\n',line)[1])
					temp_dict[ion] = inten
				line = f.readline()
				if line == '':break
			b_ion, y_ion = [], []
			for i in range(1, len(seq)):
				if 'y'+str(i) in temp_dict:
					y_ion.append(temp_dict['y'+str(i)])
				else:
					y_ion.append(0.0)
				if 'b'+str(i) in temp_dict:
					b_ion.append(temp_dict['b'+str(i)])
				else:
					b_ion.append(0.0)
			title2inten[titleList[num]] = [pepinfos, b_ion, y_ion]
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
			mgf_charge = re.split('/|\n',mgf_pepinfo)[3]
			mgf_seq = list(mgf_seq)
			if mgf_mods:
				for mod in mgf_mods.split('; '):
					if 'C' in mod.split('@')[1]:
						mgf_seq[int(mod.split('@')[1][1:]) - 1] = 'Cmod'
					else:
						mgf_seq[int(mod.split('@')[1][1:]) - 1] = 'Mmod'
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
			mgf_seq_mass = 0
			for AA in mgf_seq:
			 	mgf_seq_mass += config.mass_AA[AA]
			mgf_seq_mass = mgf_seq_mass + config.mass_H2O + config.mass_H
			pro_mass = 0
			mgf_b_inten,mgf_y_inten = [], []
			for index, AA in enumerate(mgf_seq[:-1]):
				pro_mass = pro_mass + config.mass_AA[AA]
				isb, isy = False, False
				for mz in mgf_mz2inten.keys():
					if abs((pro_mass + config.mass_H - mz))/mz*(10**6) <= 20:
						mgf_b_inten.append(mgf_mz2inten[mz]/max_inten)
						isb = True
						break
				for mz in mgf_mz2inten.keys():
					if abs((mgf_seq_mass - pro_mass - mz))/mz*(10**6) <= 20:
						mgf_y_inten.append(mgf_mz2inten[mz]/max_inten)
						isy = True
						break
				if not isb:
					mgf_b_inten.append(0.0)
				if not isy:
					mgf_y_inten.append(0.0)
			pred_by_inten = title2inten[mgf_title][1] + title2inten[mgf_title][2]
			mgf_by_inten = mgf_b_inten + mgf_y_inten[::-1]
			b_pcc = config.pearSim(title2inten[mgf_title][1], mgf_b_inten)
			y_pcc = config.pearSim(title2inten[mgf_title][2][::-1], mgf_y_inten)
			by_pcc = config.pearSim(pred_by_inten, mgf_by_inten)

			SeqInfos.append(mgf_pepinfo.split('/')[0])
			ChargeInfos.append(mgf_charge)
			pred_b_intens.append(title2inten[mgf_title][1])
			pred_y_intens.append(title2inten[mgf_title][2])
			mgf_b_intens.append(mgf_b_inten)
			mgf_y_intens.append(mgf_y_inten[::-1])
			b_ion_PCC.append(b_pcc)
			y_ion_PCC.append(y_pcc)
			by_ion_PCC.append(by_pcc)

with open(OutputPCCfile, 'w') as f:
	f.write('peptide\tlength\tcharge\tb_ion_PCC\tpredict_b_ion\tmgf_b_ion\ty_ion_PCC\tpredict_y_ion\tmgf_y_ion\tby_ion_PCC\n')
	for i in range(len(SeqInfos)):
		f.write(SeqInfos[i] + '\t' + str(len(SeqInfos[i])) + '\t' + ChargeInfos[i] + '\t' +  str(b_ion_PCC[i]) + '\t' + str(pred_b_intens[i]) + '\t' + str(mgf_b_intens[i]) + '\t' +  str(y_ion_PCC[i]) + '\t' + str(pred_y_intens[i]) + '\t' + str(mgf_y_intens[i]) + '\t' + str(by_ion_PCC[i]) + '\n')

endtime = time.time() - start
print(endtime)
