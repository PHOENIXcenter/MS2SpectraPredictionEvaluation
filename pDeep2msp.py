import re

#存放所有title以及对应的肽段信息
allinfos = {}
#设置该数据集对应的nce值
DataNCE = '35.0'
#pDeep2预测结果文件
pDeep2predictFile = 'PXD003881/pDeep2test/predict.txt'
#存放MQ和pFind3共同肽段信息的文件
SamePeptideFile = 'PXD003881/PXD003881.txt'
#转化为msp格式的pDeep2预测结果文件
pDee2mspFile = 'PXD003881/pDeep2test/pDeep2.msp'

#获取pDeep2预测结果中的离子信息，按msp文件格式存入allinfos字典中
with open(pDeep2predictFile, 'r') as f:
	while True:
		line = f.readline()
		if line == '':break
		if 'TITLE=' in line:
			file_infos = []
			title = re.split('=|\n',line)[1]
			line = f.readline()
			line = f.readline()
			seq = re.split('=|\||\n',line)[1]
			mods = re.split('=|\||\n',line)[2]
			charge = re.split('=|\||\n',line)[3]
			if len(seq) <= 30 and len(seq) >= 7:
				if int(charge) >= 1 and int(charge) <= 6:
					key2value = {}
					b1 = re.split('=|,|\n',f.readline())[1:-1]
					b2 = re.split('=|,|\n',f.readline())[1:-1]
					y1 = re.split('=|,|\n',f.readline())[1:-1]
					y2 = re.split('=|,|\n',f.readline())[1:-1]
					pepmass = re.split('=|\n',f.readline())[1]
					line = f.readline()
					while 'END IONS' not in line:
						values = []
						ion = re.split(' |\n',line)[2]
						values.append(re.split(' |\n',line)[0])
						values.append(re.split(' |\n',line)[1])
						key2value[ion] = values
						line = f.readline()
					if mods == '':
						modinfo = 0
						ModString = ''
					else:
						mods = mods.split(';')[:-1]
						modinfo = str(len(mods))
						ModString = ''
						for mod in mods:
							pos = int(mod.split(',')[0])
							modclass = mod.split(',')[1]
							if modclass == 'Oxidation[M]':
								modinfo = modinfo + '/' + str(pos - 1) + ',M,Oxidation'
								ModString = ModString + 'Oxidation@M' + str(pos) + '; '
							else:
								modinfo = modinfo + '/' + str(pos - 1) + ',C,Carbamidomethyl'
								ModString = ModString + 'Carbamidomethyl@C' + str(pos) + '; '
						ModString = ModString[:-2]
					file_infos.append('Name: ' + seq + '/' + charge + '\n')
					file_infos.append('MW: ' + pepmass + '\n')
					file_infos.append('Comment: Parnet=%s Collision_energy=%s Mods=%s ModString=%s//%s/%s\n'
						%(pepmass, DataNCE, modinfo, seq, ModString, charge))
					file_infos.append('Num peaks: ' + str(len(key2value)) + '\n')
					for i in range(len(b1)):
						if ('y' + str(i + 1) + '+1') in key2value.keys():
							file_infos.append(key2value['y' + str(i + 1) + '+1'][0] + '\t' + key2value['y' + str(i + 1) + '+1'][1] + '\t' + '"y' + str(i + 1) + '/0.0ppm"\n')
						if ('y' + str(i + 1) + '+2') in key2value.keys():
							file_infos.append(key2value['y' + str(i + 1) + '+2'][0] + '\t' + key2value['y' + str(i + 1) + '+2'][1] + '\t' + '"y' + str(i + 1) + '^2)/0.0ppm"\n')
						if ('b' + str(i + 1) + '+1') in key2value.keys():
							file_infos.append(key2value['b' + str(i + 1) + '+1'][0] + '\t' + key2value['b' + str(i + 1) + '+1'][1] + '\t' + '"b' + str(i + 1) + '/0.0ppm"\n')
						if ('b' + str(i + 1) + '+2') in key2value.keys():
							file_infos.append(key2value['b' + str(i + 1) + '+2'][0] + '\t' + key2value['b' + str(i + 1) + '+2'][1] + '\t' + '"b' + str(i + 1) + '^2)/0.0ppm"\n')
			allinfos[title] = file_infos

#按SamePeptideFile文件中肽段的顺序存放title
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

#按titleList中的顺序，将转化后的信息写入文件
with open(pDee2mspFile, 'w') as f:
	for title in titleList:
		infos = allinfos[title]
		for line in infos:
			f.write(line)