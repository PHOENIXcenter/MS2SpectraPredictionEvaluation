# -*- coding: utf-8 -*-
import re
import AminoAcidMass as config
import time

start = time.time()

#存放MQ和pFind3共同肽段信息的文件
SamePeptideFile = '2019Wang_MSBLysN_HCD/2019Wang_MSBLysN_HCD.txt'
#工具预测结果文件
ToolpredictFile = '2019Wang_MSBLysN_HCD/MassAnalyzer-result/MassAnalyzer.msp'
#比对的目标MGF文件
TargetMGF = '2019Wang_MSBLysN_HCD/TargetMGF.mgf'
#肽段信息及比对的PCC结果文件
OutputPCCfile = '2019Wang_MSBLysN_HCD/MassAnalyzer-result/MassAnalyzer_onlymatch_inten_pears.txt'
all_pears = []
peplen = []

titleList = []
#按结果顺序生成一个title列表
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
#将预测结果中的b,y离子强度按title列表顺序获取并保存在title2inten[pepinfo,b_ionlist,y_ionlist]中
with open(ToolpredictFile, 'r') as f:
	while True:
		line = f.readline()
		if line == '':break
		if 'ModString=' in line:
			pepinfos = re.split('ModString=|\n',line)[1]
			seq = pepinfos.split('//')[0]
			mods = pepinfos.split('/')[2]
			seq = list(seq)
			if mods:
				for mod in mods.split('; '):
					if 'C' in mod.split('@')[1]:
						seq[int(mod.split('@')[1][1:]) - 1] = 'Cmod'
					else:
						seq[int(mod.split('@')[1][1:]) - 1] = 'Mmod'
			line = f.readline()
			line = f.readline()
			mz2inten = {}
			predintenList = []
			while 'Name:' not in line:
				mz = float(re.split('\t|\n', line)[0])
				inten = float(re.split('\t|\n', line)[1])
				predintenList.append(inten)
				mz2inten[mz] = inten
				line = f.readline()
				if line == '':break
			max_predinten = max(predintenList)
			seq_mass = 0
			for AA in seq:
			 	seq_mass += config.mass_AA[AA]
			pro_mass = 0
			ion_mz = []
			ion_inten = []
			for index, AA in enumerate(seq[:-1]):
				pro_mass = pro_mass + config.mass_AA[AA]
				isb, isb2, isy,isy2 = False, False, False, False
				for mz in mz2inten.keys():
					if abs((pro_mass + config.mass_H - mz))/mz*(10**6) <= 20:
						if not isb:
							ion_mz.append(mz)
							ion_inten.append(mz2inten[mz]/max_predinten)
							isb = True
					if abs((pro_mass/2 + config.mass_H - mz))/mz*(10**6) <= 20:
						if not isb2:
							ion_mz.append(mz)
							ion_inten.append(mz2inten[mz]/max_predinten)
							isb2 = True
					if abs((seq_mass - pro_mass + config.mass_H2O + config.mass_H - mz))/mz*(10**6) <= 20:
						if not isy:
							ion_mz.append(mz)
							ion_inten.append(mz2inten[mz]/max_predinten)
							isy = True
					if abs(((seq_mass - pro_mass)/2 + config.mass_H2O + config.mass_H - mz))/mz*(10**6) <= 20:
						if not isy2:
							ion_mz.append(mz)
							ion_inten.append(mz2inten[mz]/max_predinten)
							isy2 = True

			title2inten[titleList[num]] = [pepinfos, ion_mz, ion_inten]
			num += 1
print(len(title2inten))

#获取mgf文件中的谱图title，以及对应的mz-intensity
with open(TargetMGF, 'r') as f:
	while True:
		line = f.readline()
		if line == '':break
		if 'TITLE=' in line:
			mgf_title = re.split('=|\n',line)[1]
			mgf_pepinfo = title2inten[mgf_title][0]
			mgf_seq = mgf_pepinfo.split('/')[0]
			mgf_mods = mgf_pepinfo.split('/')[2]
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

with open(OutputPCCfile, 'w') as f:
	f.write('all_pears\tpeplen\n')
	for i in range(len(all_pears)):
		f.write(str(all_pears[i]) + '\t' + str(peplen[i]) + '\n')
endtime = time.time() - start
print(endtime)
