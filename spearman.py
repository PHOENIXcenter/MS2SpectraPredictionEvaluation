# -*- coding: utf-8 -*-
import re
import AminoAcidMass as config
import time
import scipy.stats as stats

start = time.time()

#存放MQ和pFind3共同肽段信息的文件
SamePeptideFile = 'ninanjie/ninanjie.txt'
#工具预测结果文件
ToolpredictFile = 'ninanjie/pDeep-result/pDeep2.msp'
#比对的目标MGF文件
TargetMGF = 'D:/SoftwareEvaluationNew/ninanjie/TargetMGF.mgf'
#肽段信息及比对的PCC结果文件
OutputPCCfile = 'ninanjie/pDeep-result/pDeep2_all_inten_spearman.txt'
#工具预测结果中各位置b,y离子的强度
pred_b_intens, pred_y_intens = [], []
#mgf文件中各位置b,y离子的强度
mgf_b_intens, mgf_y_intens = [], []
#肽段序列以及电荷信息
SeqInfos, ChargeInfos = [], []
#b,y离子单独比对的PCC结果和b,y离子一起比对的PCC结果
b_ion_PCC, y_ion_PCC, by_ion_PCC = [], [], []
#按SamePeptideFile中肽段顺序生成的title列表
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

## n负责记录当前是第几条肽段，对应获取titleList中的title信息
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
			line = f.readline()
			line = f.readline()
			#记录msp文件中的mz-intensity
			temp_dict = {}
			while 'Name:' not in line:
				if '^' not in line:
					ion = re.split('\t|\n',line)[2].split('/')[0][1:]
					inten = float(re.split('\t|\n',line)[1])
					temp_dict[ion] = inten
				line = f.readline()
				if line == '':break
			#生成所有的b,y离子
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

#获取mgf文件中的谱图title，以及对应的mz-intensity
with open(TargetMGF, 'r') as f:
	while True:
		line = f.readline()
		if line == '':break
		if 'TITLE=' in line:
			mgf_title = re.split('=|\n',line)[1]
			if mgf_title in title2inten.keys():
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
				#分别对b离子，y离子计算PCC，再对b,y离子一起计算PCC
				b_pcc = stats.stats.spearmanr(title2inten[mgf_title][1], mgf_b_inten)[0]
				y_pcc = stats.stats.spearmanr(title2inten[mgf_title][2][::-1], mgf_y_inten)[0]
				by_pcc = stats.stats.spearmanr(pred_by_inten, mgf_by_inten)[0]
				# nb, ny, nby = len(mgf_b_inten), len(mgf_y_inten), len(mgf_by_inten)
				# totalb, totaly, totalby = 0,0,0
				# for i in range(nb):
				# 	totalb += (title2inten[mgf_title][1][i] - mgf_b_inten[i]) ** 2
				# for i in range(ny):
				# 	totaly += (title2inten[mgf_title][2][::-1][i] - mgf_y_inten[i]) ** 2
				# for i in range(nby):
				# 	totalby += (pred_by_inten[i] - mgf_by_inten[i]) ** 2
				# b_pcc = 1 - float(6 * totalb) / (nb * (nb ** 2 - 1))
				# y_pcc = 1 - float(6 * totaly) / (ny * (ny ** 2 - 1))
				# by_pcc = 1 - float(6 * totalby) / (nby * (nby ** 2 - 1))
				#将所需信息写入列表
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
	f.write('peptide\tlength\tcharge\tb_ion_SA\tpredict_b_ion\tmgf_b_ion\ty_ion_SA\tpredict_y_ion\tmgf_y_ion\tby_ion_SA\n')
	for i in range(len(SeqInfos)):
		f.write(SeqInfos[i] + '\t' + str(len(SeqInfos[i])) + '\t' + ChargeInfos[i] + '\t' +  str(b_ion_PCC[i]) + '\t' + str(pred_b_intens[i]) + '\t' + str(mgf_b_intens[i]) + '\t' +  str(y_ion_PCC[i]) + '\t' + str(pred_y_intens[i]) + '\t' + str(mgf_y_intens[i]) + '\t' + str(by_ion_PCC[i]) + '\n')

endtime = time.time() - start
print(endtime)
