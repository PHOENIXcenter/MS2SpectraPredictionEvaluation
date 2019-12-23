import os
import time

start_time = time.time()
MQ_file = 'F:/1030Data/pfind_mgf/PXD003881/MQ/evidence.txt'
pFind3_file = 'F:/1030Data/pfind_mgf/PXD003881/pFindTask2/result/pFind.spectra'
OutputFile = 'PXD003881/PXD003881.txt'
mq_title2seq = {}
same_scans = []

print('Begin getting MQ data...')
with open(MQ_file,'r',encoding='UTF-8') as f:
	for line in f:
		MQ_sequence = line.split('\t')[3]
		if MQ_sequence == 'Modified sequence':continue
		Reverse = line.split('\t')[51]
		PotentialContaminant = line.split('\t')[52]
		if Reverse != '+' and PotentialContaminant != '+':
			has_Acetyl = int(line.split('\t')[6])
			has_Oxi = int(line.split('\t')[7])
			if has_Acetyl == 1:
				MQ_sequence = MQ_sequence[5:-1]
			else:
				MQ_sequence = MQ_sequence[1:-1]
			RawFile = line.split('\t')[13]
			charge = line.split('\t')[16]
			scan = line.split('\t')[45]
			mq_title = RawFile + '.' + scan + '.' + scan + '.' + charge
			mq_title2seq[mq_title] = MQ_sequence
print(len(mq_title2seq))
mq_time = time.time()
print('use %s seconds'%(mq_time - start_time))
print('=============================')
print('Begin getting pFind data...')

with open(pFind3_file,'r') as f:
	for line in f:
		pFind_title = line.split('\t')[0]
		if pFind_title == 'File_Name':continue
		pFind_title = pFind_title.split('.')
		pFind_title = '.'.join(pFind_title[:-2])
		if pFind_title in mq_title2seq.keys():
			pFind_sequence = line.split('\t')[5]
			pFind_mods = line.split('\t')[10].split(';')
			seq_len = len(pFind_sequence)
			pFind_sequence = list(pFind_sequence)
			for mod in pFind_mods:
				if mod == '':break
				mod_pos = int(mod.split(',')[0])
				if mod_pos > seq_len:continue
				if pFind_sequence[mod_pos-1] == 'M':
					pFind_sequence[mod_pos-1] = 'M(ox)'
			pFind_sequence = ''.join(pFind_sequence)
			mq_sequence = mq_title2seq[pFind_title]
			if mq_sequence == pFind_sequence:
				onegroup = []
				onegroup.append(line.split('\t')[0])
				onegroup.append(line.split('\t')[5])
				onegroup.append(line.split('\t')[10])
				onegroup.append(line.split('\t')[3])
				same_scans.append(onegroup)
				if len(same_scans) % 1000 == 0:
					print("same spectrum number : %s"%len(same_scans))

pFind_time = time.time()
print('use %s seconds'%(pFind_time - mq_time))
print('=============================')
print('Begin writing files...')

with open(OutputFile,'w') as f:
	f.write('peptide' + '\t' + 'modification' + '\t' + 'charge' + '\t' + 'RawFile+SCAN' + '\n')
	for line in same_scans:
		seq, mods, charge= line[1], line[2], line[3]
		if len(seq) >= 7 and len(seq) <= 30:
			if int(charge) >= 1 and int(charge) <= 6:
				if mods:
					istrue = False
					for mod in mods.split(';'):
						if mod == '':break
						if mod.split(',')[1] != 'Carbamidomethyl[C]' and mod.split(',')[1] != 'Oxidation[M]':
							istrue = True
							break
					if not istrue:
						f.write(line[1] + '\t' + line[2] + '\t' + line[3] + '\t' + line[0] + '\n')
				else:
					f.write(line[1] + '\t' + line[2] + '\t' + line[3] + '\t' + line[0] + '\n')

end_time = time.time()
print('use %s seconds'%(end_time - pFind_time))

