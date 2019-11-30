import re

alldata = {
'LCMSMS':'PXD003881/LCMSMS-result/LCMSMS_all_inten_pears.txt',
# 'MassAnalyzer':'2019Wang_MSBLysN_HCD/MassAnalyzer-result/MassAnalyzer_all_inten_pears.txt',
'MS2PIP':'PXD003881/MS2PIP-result/MS2PIP_new_all_inten_pears.txt',
'Prosit':'PXD003881/Prosit-result/Prosit_all_inten_pears.txt',
'pDeep2':'PXD003881/pDeep2-result/pDeep2_all_inten_pears.txt',
}

for file in alldata.keys():
	all_b_pears = []
	all_y_pears = []
	all_pears = []
	with open(alldata[file], 'r') as f:
		for line in f:
			if 'peptide' in line:continue
			if line == '':break
			if '\tnan\t' not in line:
				b_p = re.split('\t|\n',line)[3]
				y_p = re.split('\t|\n',line)[6]
				by_p = re.split('\t|\n',line)[9]
				all_b_pears.append(float(b_p))
				all_y_pears.append(float(y_p))
				all_pears.append(float(by_p))

	all_b_pears = sorted(all_b_pears)
	all_y_pears = sorted(all_y_pears)
	all_pears = sorted(all_pears)
	lenB = len(all_b_pears)
	lenY = len(all_y_pears)
	lenall = len(all_pears)
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
	print(file + 'result :')
	print('by ions total number: %s'%(lenall))
	print('Median PCCs of BY ions: %s'%median_pears)
	print('Median PCCs of B ions: %s'%median_b_pears)
	print('Median PCCs of Y ions: %s'%median_y_pears)