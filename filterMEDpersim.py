import re

alldata = {
'LCMSMS':'PXD003881/LCMSMS-result/LCMSMS_all_inten_pears.txt',
# 'MassAnalyzer':'PXD005590/MassAnalyzer-result/MassAnalyzer_all_inten_pears.txt',
'MS2PIP':'PXD003881/MS2PIP-result/MS2PIP_new_all_inten_pears.txt',
'Prosit':'PXD003881/Prosit-result/Prosit_all_inten_pears.txt',
'pDeep2':'PXD003881/pDeep2-result/pDeep2_all_inten_pears.txt',
}

for file in alldata.keys():
	all_b_pears = 0
	all_y_pears = 0
	all_pears = 0
	total_num = 0
	with open(alldata[file], 'r') as f:
		for line in f:
			if 'peptide' in line:continue
			if line == '':break
			if '\tnan\t' not in line:
				b_p = re.split('\t|\n',line)[3]
				y_p = re.split('\t|\n',line)[6]
				by_p = re.split('\t|\n',line)[9]
				if float(b_p) >= 0.8:all_b_pears += 1
				if float(y_p) >= 0.8:all_y_pears += 1
				if float(by_p) >= 0.8:all_pears += 1
				total_num += 1

	print('='*30)
	print(file + 'result :')
	print('>=0.8 PCCs of BY ions: %s'%(all_pears/total_num))
	print('>=0.8 PCCs of B ions: %s'%(all_b_pears/total_num))
	print('>=0.8 PCCs of Y ions: %s'%(all_y_pears/total_num))

