#存放带修饰的肽段序列
modified_sequence = []
#存放肽段对应的母离子电荷
precursor_charge = []
#需要转化格式的输入文件
DataInputFile = '../PXD005590/PXD005590.txt'
#转化后的输出文件
DataOutputFile = 'PXD005590_MassAnalyzer.txt'

#将文件转化为MassAnalyzer预测所需的输入文件格式
with open(DataInputFile, 'r') as f:
	for line in f:
		seq = line.split('\t')[0]
		if seq == 'peptide':continue
		mods = line.split('\t')[1]
		charge = line.split('\t')[2]
		title = line.split('\t')[3].split('\n')[0]
		seq = list(seq)
		if mods != '':
			for mod in mods.split(';'):
				if mod == '':break
				pos = int(mod.split(',')[0])
				if seq[pos - 1] == 'M':
					seq[pos - 1] = 'O'
				else:
					seq[pos - 1] = 'U'
		seq = ''.join(seq)
		modified_sequence.append(seq)
		precursor_charge.append(charge)

with open(DataOutputFile, 'w') as f:
	for i in range(len(modified_sequence)):
		f.write(modified_sequence[i] + '\t' + precursor_charge[i] + '\n')
