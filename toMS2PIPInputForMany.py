peptide_num = 0
file_num = 1
#每个列表存放10W数据
infos = []
#需要转化格式的输入文件
DataInputFile = '../PXD003881/PXD003881.txt'
#转化后的输出文件
DataOutputFile = 'PXD003881'

#将文件转化为MS2PIP预测所需的输入文件格式
with open(DataInputFile ,'r') as f:
	for line in f:
		seq = line.split('\t')[0]
		if seq == 'peptide':continue
		peptide_num += 1
		mods = line.split('\t')[1]
		charge = line.split('\t')[2]
		title = line.split('\t')[3].split('\n')[0]
		pepinfo = title
		if mods != '':
			mods = mods.replace(',','|')
			mods = mods.replace(';','|')
			mods = mods.replace('[M]','')
			mods = mods.replace('[C]','')
			mods = mods[:-1]
		else:
			mods = '-'
		if peptide_num <= 99999:
			info = []
			info.append(pepinfo)
			info.append(mods)
			info.append(seq)
			info.append(charge)
			infos.append(info)
		else:
			#输出到对应文件
			with open(DataOutputFile + '_ms2pip' + str(file_num) + '.PEPREC', 'w') as f:
				f.write('spec_id\tmodifications\tpeptide\tcharge\n')
				for info in infos:
					f.write(info[0] + '\t' + info[1] + '\t' + info[2] + '\t' + info[3] + '\n')
			infos = []
			info = []
			info.append(pepinfo)
			info.append(mods)
			info.append(seq)
			info.append(charge)
			infos.append(info)
			peptide_num = 1
			file_num += 1
			
with open(DataOutputFile + '_ms2pip' + str(file_num) + '.PEPREC', 'w') as f:
				f.write('spec_id\tmodifications\tpeptide\tcharge\n')
				for info in infos:
					f.write(info[0] + '\t' + info[1] + '\t' + info[2] + '\t' + info[3] + '\n')