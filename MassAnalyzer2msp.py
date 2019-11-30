import re 

#存放所有的修饰信息
allmods = []
#存放需要写入文件的内容
file_infos = []
#设置该数据集对应的nce值
DataNCE = '35.0'
#存放MQ和pFind3共同肽段信息的文件
SamePeptideFile = 'PXD005590/PXD005590.txt'
#MS2PIP预测结果文件
MassAnalyzerpredictFile = 'PXD005590/MassAnalyzer-result/MSMSPredict.txt'
#转化为msp格式的MS2PIP预测结果文件
MassAnalyzermspFile = 'PXD005590/MassAnalyzer-result/MassAnalyzer.msp'


#按SamePeptideFile文件的顺序获取所有肽段对应的修饰信息
with open(SamePeptideFile, 'r') as f:
	for line in f:
		if 'peptide	modification' in line:continue
		rawmod = line.split('\t')[1]
		allmods.append(rawmod)
print(len(allmods))

# n负责记录当前是第几条肽段，对应获取allmods中的肽段修饰信息
n = 0
#获取MassAnalyzer预测结果中的离子信息，按msp文件格式存入file_infos中
with open(MassAnalyzerpredictFile, 'r') as f:
	line = '123'
	while True:
		line = line.split('\n')[0].replace('\t','')
		line = line.replace('.','')
		if line.isdigit():
			line = f.readline()
		if line == '':break
		line = line.split('\n')[0]
		if line.isalpha():
			seq = line
			line = f.readline()
			line = f.readline()
			charge = line.split('\n')[0]
			if len(seq) <= 30 and len(seq) >= 7:
				if int(charge) >= 1 and int(charge) <= 6:
					mods = allmods[n]
					n += 1
					if mods == '':
						modinfo = 0
						ModString = ''
					else:
						seq = list(seq)
						mods = mods.split(';')[:-1]
						modinfo = str(len(mods))
						ModString = ''
						for mod in mods:
							pos = int(mod.split(',')[0])
							modclass = mod.split(',')[1]
							if modclass == 'Oxidation[M]':
								# print(pos)
								seq[pos - 1] = 'M'
								modinfo = modinfo + '/' + str(pos - 1) + ',M,Oxidation'
								ModString = ModString + 'Oxidation@M' + str(pos) + '; '
							else:
								seq[pos - 1] = 'C'
								modinfo = modinfo + '/' + str(pos - 1) + ',C,Carbamidomethyl'
								ModString = ModString + 'Carbamidomethyl@C' + str(pos) + '; '
						ModString = ModString[:-2]
						seq = ''.join(seq)
					file_infos.append('Name: ' + seq + '/' + charge + '\n')
					file_infos.append('MW: -\n')
					file_infos.append('Comment: Parnet=- Collision_energy=%s Mods=%s ModString=%s//%s/%s\n'
						%(DataNCE, modinfo, seq, ModString, charge))
					r = 0
					while r < 8:
						line = f.readline()
						r += 1
					numpeaks = line.split('\n')[0]
					file_infos.append('Num peaks: ' + numpeaks + '\n')
					line = f.readline()
					while not line.split('\n')[0].isalpha():
						file_infos.append(line)
						line = f.readline()
						if line == '':break

with open(MassAnalyzermspFile, 'w') as f:
	for line in file_infos:
		f.write(line)
