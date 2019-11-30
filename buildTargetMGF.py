import re 
import os 

#质谱title作为键，值是一个列表[peptide, mods, charge]
title2pepinfos = {}
#mgf中需要保存的谱图信息
file_infos = []
#数据集的mgf文件路径
mgf_path = 'F:/1030Data/pfind_mgf/PXD003881/mgf/'
#pFind3和MQ鉴定后结果一致的肽段信息文件
SamePeptideFile = 'PXD003881/PXD003881.txt'
#生成的目标MGF文件
TargetMGF = 'PXD003881/TargetMGF.mgf'

#将SamePeptideFile中所有的信息保存在title2pepinfos，方便后面在mgf中提取信息
with open(SamePeptideFile, 'r') as f:
	for line in f:
		if 'peptide	modification' in line:continue
		if line == '':break
		seq = re.split('\t|\n',line)[0]
		mods = re.split('\t|\n',line)[1]
		charge = re.split('\t|\n',line)[2]
		title = re.split('\t|\n',line)[3]
		#Prosit预测要求：肽段长度[7,30],电荷值[1,6]
		if len(seq) >= 7 and len(seq) <= 30:
			if int(charge) >=1 and int(charge) <= 6:
				values = [] 
				values.append(seq)
				values.append(mods)
				values.append(charge)
				title2pepinfos[title] = values
print(len(title2pepinfos))


#循环mgf文件，将title在title2pepinfos的谱图信息（mz-intensity）提取出来
for filename in os.listdir(mgf_path):
	if os.path.splitext(filename)[1] == '.mgf':
		print('Begin dealing : %s'%filename)
		with open(mgf_path + filename, 'r') as f:
			while True:
				line = f.readline()
				if line == '':break
				if 'TITLE=' in line:
					mgf_title = re.split('=|\n',line)[1]
					if mgf_title in title2pepinfos.keys():
						file_infos.append('BEGIN IONS\n')
						file_infos.append(line)
						line = f.readline()
						line = f.readline()
						line = f.readline()
						while 'END IONS' not in line:
							file_infos.append(line)
							line = f.readline()
						file_infos.append('END IONS\n')
						
with open(TargetMGF, 'w') as f:
	for line in file_infos:
		f.write(line)

