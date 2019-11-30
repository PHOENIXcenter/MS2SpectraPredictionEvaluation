import re

alldata = {
'LCMSMS':'PXD003881/LCMSMS-result/LCMSMS_onlymatch_inten_pears.txt',
# 'MassAnalyzer':'PXD005590/MassAnalyzer-result/MassAnalyzer_onlymatch_inten_pears.txt',
'MS2PIP':'PXD003881/MS2PIP-result/MS2PIP_new_onlymatch_inten_pears.txt',
'Prosit':'PXD003881/Prosit-result/Prosit_onlymatch_inten_pears.txt',
'pDeep2':'PXD003881/pDeep2-result/pDeep2_onlymatch_inten_pears.txt',
}

for file in alldata.keys():
	all_pears = 0
	total_num = 0
	with open(alldata[file], 'r') as f:
		for line in f:
			if 'all_pears' in line:continue
			if line == '':break
			if 'nan' not in line:
				by_p = re.split('\t|\n',line)[0]
				if float(by_p) >= 0.8:all_pears += 1
				total_num += 1

	print('='*30)
	print(file + 'result :')
	# print('valid number: %s'%all_pears)
	# print('total number: %s'%total_num)
	print('>=0.8 PCCs of BY ions: %s'%(all_pears/total_num))

