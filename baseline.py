# -*- coding: utf-8 -*-
import re
import AminoAcidMass as config
import time
import numpy as np

start = time.time()

#存放MQ和pFind3共同肽段信息的文件
SamePeptideFile = 'D:/SoftwareEvaluationNew/2016Eric_NC_Try_Mouse/2016Eric_NC_Try_Mouse.txt'
#比对的目标MGF文件
TargetMGF = 'D:/SoftwareEvaluationNew/2016Eric_NC_Try_Mouse/TargetMGF.mgf'
#b,y离子单独比对的PCC结果和b,y离子一起比对的PCC结果
b_ion_PCC, y_ion_PCC, by_ion_PCC = {}, {}, {}
resultbPCC, resultyPCC, resultbyPCC = [], [], []
#按SamePeptideFile中肽段顺序生成的title列表
titleList = {}
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
				mods = re.split('\t|\n',line)[1]
				if mods:
					res_seq = [i for i in res_seq]
					mods = mods.split(';')[:-1]
					for m in mods:
						pos = int(m.split(',')[0])
						if m.split(',')[1] == 'Oxidation[M]':
							res_seq[pos - 1] = 'Mmod'
						else:
							res_seq[pos - 1] = 'Cmod'
					# res_seq = ''.join(res_seq)
				titleList[title] = res_seq
print(len(titleList))

#获取mgf文件中的谱图title，以及对应的mz-intensity
with open(TargetMGF, 'r') as f:
	while True:
		line = f.readline()
		if line == '':break
		if 'TITLE=' in line:
			mgf_title = re.split('=|\n',line)[1]
			if mgf_title in titleList.keys():
				mgf_seq = titleList[mgf_title]
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
				mgf_seq_mass = mgf_seq_mass + config.mass_H2O
				pro_mass = 0
				mgf_b_inten,mgf_y_inten = [], []
				for index, AA in enumerate(mgf_seq[:-1]):
					pro_mass = pro_mass + config.mass_AA[AA]
					isb, isy, isb2, isy2 = False, False, False, False
					for mz in mgf_mz2inten.keys():
						if abs(pro_mass + config.mass_H - mz)/mz*(10**6) <= 20 and isb == False:
							mgf_b_inten.append(mgf_mz2inten[mz]/max_inten)
							isb = True
						if abs(pro_mass/2 + config.mass_H - mz)/mz*(10**6) <= 20 and isb2 == False:
							mgf_b_inten.append(mgf_mz2inten[mz]/max_inten)
							isb2 = True
						if abs(mgf_seq_mass - pro_mass + config.mass_H - mz)/mz*(10**6) <= 20 and isy == False:
							mgf_y_inten.append(mgf_mz2inten[mz]/max_inten)
							isy = True
						if abs((mgf_seq_mass - pro_mass)/2 + config.mass_H - mz)/mz*(10**6) <= 20 and isy2 == False:
							mgf_y_inten.append(mgf_mz2inten[mz]/max_inten)
							isy2 = True
					if not isb:
						mgf_b_inten.append(0.0)
					if not isb2:
						mgf_b_inten.append(0.0)
					if not isy:
						mgf_y_inten.append(0.0)
					if not isy2:
						mgf_y_inten.append(0.0)
				mgf_by_inten = mgf_b_inten + mgf_y_inten[::-1]
				if ''.join(mgf_seq) in b_ion_PCC.keys():
					b_ion_PCC[''.join(mgf_seq)].append(mgf_b_inten)
					y_ion_PCC[''.join(mgf_seq)].append(mgf_y_inten)
					by_ion_PCC[''.join(mgf_seq)].append(mgf_by_inten)
				else:
					b_ion_PCC[''.join(mgf_seq)] = [mgf_b_inten]
					y_ion_PCC[''.join(mgf_seq)] = [mgf_y_inten]
					by_ion_PCC[''.join(mgf_seq)] = [mgf_by_inten]

for seq in b_ion_PCC:
	if len(b_ion_PCC[seq]) > 1:
		medintenb = []
		peplenb = len(b_ion_PCC[seq][0])
		pepnumb = len(b_ion_PCC[seq])
		for i in range(peplenb):
			temp = []
			for j in b_ion_PCC[seq]:
				temp.append(j[i])
			temp = sorted(temp)
			if pepnumb % 2 == 0:
				medintenb.append((temp[int(pepnumb/2) - 1] + temp[int(pepnumb/2)])/2)
			else:
				medintenb.append(temp[pepnumb//2])
		tempPCC = []
		for v in b_ion_PCC[seq]:
			pearb = config.pearSim(medintenb, v)
			tempPCC.append(pearb)
		tempPCC = sorted(tempPCC)
		if len(tempPCC) % 2 == 0:
			resultbPCC.append((tempPCC[int(len(tempPCC)/2) - 1] + tempPCC[int(len(tempPCC)/2)])/2)
		else:
			resultbPCC.append(tempPCC[len(tempPCC)//2])

	if len(y_ion_PCC[seq]) > 1:
		medinteny = []
		pepleny = len(y_ion_PCC[seq][0])
		pepnumy = len(y_ion_PCC[seq])
		for i in range(pepleny):
			temp = []
			for j in y_ion_PCC[seq]:
				temp.append(j[i])
			temp = sorted(temp)
			if pepnumy % 2 == 0:
				medinteny.append((temp[int(pepnumy/2) - 1] + temp[int(pepnumy/2)])/2)
			else:
				medinteny.append(temp[pepnumy//2])
		tempPCC = []
		for v in y_ion_PCC[seq]:
			peary = config.pearSim(medinteny, v)
			tempPCC.append(peary)
		tempPCC = sorted(tempPCC)
		if len(tempPCC) % 2 == 0:
			resultyPCC.append((tempPCC[int(len(tempPCC)/2) - 1] + tempPCC[int(len(tempPCC)/2)])/2)
		else:
			resultyPCC.append(tempPCC[len(tempPCC)//2])

	if len(by_ion_PCC[seq]) > 1:
			medintenby = []
			peplenby = len(by_ion_PCC[seq][0])
			pepnumby = len(by_ion_PCC[seq])
			for i in range(peplenby):
				temp = []
				for j in by_ion_PCC[seq]:
					temp.append(j[i])
				temp = sorted(temp)
				if pepnumby % 2 == 0:
					medintenby.append((temp[int(pepnumby/2) - 1] + temp[int(pepnumby/2)])/2)
				else:
					medintenby.append(temp[pepnumby//2])
			tempPCC = []
			for v in by_ion_PCC[seq]:
				pearby = config.pearSim(medintenby, v)
				tempPCC.append(pearby)
			tempPCC = sorted(tempPCC)
			if len(tempPCC) % 2 == 0:
				resultbyPCC.append((tempPCC[int(len(tempPCC)/2) - 1] + tempPCC[int(len(tempPCC)/2)])/2)
			else:
				resultbyPCC.append(tempPCC[len(tempPCC)//2])

all_b_pears = sorted(resultbPCC)
all_y_pears = sorted(resultyPCC)
all_pears = sorted(resultbyPCC)

lenB = len(all_b_pears)
lenY = len(all_y_pears)
lenall = len(all_pears)
# print(str(lenB) + '|' + str(lenY) + '|' + str(lenall))
if lenB % 2 == 0:
	median_b_pears = (all_b_pears[int(lenB/2) - 1] + all_b_pears[int(lenB/2)])/2
	median_y_pears = (all_y_pears[int(lenY/2) - 1] + all_y_pears[int(lenY/2)])/2
else:
	median_b_pears = all_b_pears[lenB//2]
	median_y_pears = all_y_pears[lenY//2]
if lenall % 2 == 0:
	median_pears = (all_pears[int(lenall/2) - 1] + all_pears[int(lenall/2)])/2
else:
	median_pears = all_pears[lenall//2]

print('='*30)
print('PXD005590' + '-result :')	#SamePeptideFile.split('.')[0]
print('by ions total number: %s'%(lenall))
print('Median PCCs of BY ions: %s'%median_pears)
print('Median PCCs of B ions: %s'%median_b_pears)
print('Median PCCs of Y ions: %s'%median_y_pears)

endtime = time.time() - start
print(endtime)
