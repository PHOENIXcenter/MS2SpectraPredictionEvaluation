import re
import heapq
from numpy import *
from numpy import linalg as la

alldata = {
'LCMSMS':'PXD003881/LCMSMS-result/LCMSMS_all_inten_pears.txt',
# 'MassAnalyzer':'PXD005590/MassAnalyzer-result/MassAnalyzer_all_inten_pears.txt',
'MS2PIP':'PXD003881/MS2PIP-result/MS2PIP_new_all_inten_pears.txt',
'Prosit':'PXD003881/Prosit-result/Prosit_all_inten_pears.txt',
'pDeep2':'PXD003881/pDeep2-result/pDeep2_all_inten_pears.txt',
}

topK = 15

def pearSim(inA,inB):
	return 0.5+0.5*corrcoef(inA,inB,rowvar=0)[0][1]

def as_num(x):
	x = float(x)
	y='{:.8f}'.format(x) # 8f表示保留8位小数点的float型
	return(y)

for file in alldata.keys():
	all_pears = []
	peptide_num = 0
	with open(alldata[file], 'r') as f:
		for line in f:
			if 'peptide' in line:continue
			if line == '':break
			pred_topK, mgf_topK = [], []
			pred_b_inten = list(map(as_num, line.split('\t')[4][1:-1].split(', ')))
			mgf_b_inten = list(map(as_num, line.split('\t')[5][1:-1].split(', ')))
			pred_y_inten = list(map(as_num, line.split('\t')[7][1:-1].split(', ')))
			mgf_y_inten = list(map(as_num, line.split('\t')[8][1:-1].split(', ')))
			pred_inten = pred_b_inten + pred_y_inten
			mgf_inten = mgf_b_inten + mgf_y_inten
			max_num_index_list = map(pred_inten.index, heapq.nlargest(topK, pred_inten))
			for i in max_num_index_list:
				pred_topK.append(float(pred_inten[i]))
				mgf_topK.append(float(mgf_inten[i]))
			pcc = pearSim(pred_topK, mgf_topK)
			if 'nan' not in str(pcc):
				all_pears.append(pcc)
			peptide_num += 1

	all_pears = sorted(all_pears)
	lenall = len(all_pears)
	if lenall % 2 == 0:
		median_pears = (all_pears[int(lenall/2) - 1] + all_pears[int(lenall/2)])/2
	else:
		median_pears = all_pears[lenall//2]

	print('='*30)
	print(file + 'result :')
	print('valid peptide number: %s'%(lenall))
	print('total peptide number: %s'%(peptide_num))
	print('Median PCCs of Top %s ions: %s'%(topK, median_pears))