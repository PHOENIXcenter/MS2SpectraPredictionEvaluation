import re

alldata = {
'LCMSMS':'PXD003881/LCMSMS-result/LCMSMS_onlymatch_inten_pears.txt',
# 'MassAnalyzer':'PXD005590/MassAnalyzer-result/MassAnalyzer_onlymatch_inten_pears.txt',
'MS2PIP':'PXD003881/MS2PIP-result/MS2PIP_new_onlymatch_inten_pears.txt',
'Prosit':'PXD003881/Prosit-result/Prosit_onlymatch_inten_pears.txt',
'pDeep2':'PXD003881/pDeep2-result/pDeep2_onlymatch_inten_pears.txt',
}

for file in alldata.keys():
	all_pears = []
	with open(alldata[file], 'r') as f:
		for line in f:
			if 'all_pears' in line:continue
			if line == '':break
			if 'nan' not in line:
				per = re.split('\t|\n',line)[0]
				all_pears.append(float(per))

	all_pears = sorted(all_pears)
	lenall = len(all_pears)
	if lenall % 2 == 0:
		median_pears = (all_pears[int(lenall/2) - 1] + all_pears[int(lenall/2)])/2
	else:
		median_pears = all_pears[lenall//2]

	print('='*30)
	print(file + 'result :')
	print('valid : %s'%str(lenall))
	print('Median PCCs of B,Y ions: %s'%median_pears)