import pandas as pd

seqs = []
allmods = []
modified_sequence = []
collision_energy = []
precursor_charge = []
DataInputFile = '../PXD003881/PXD003881.txt'
DataNCE = '35'
DataOutputFile = 'PXD003881_Prosit.csv'

with open(DataInputFile, 'r') as f:
	for line in f:
		seq = line.split('\t')[0]
		if seq == 'peptide':continue
		if len(seq) > 30 or len(seq) < 7:continue
		mods = line.split('\t')[1]
		charge = line.split('\t')[2]
		title = line.split('\t')[3].split('\n')[0]
		if int(charge) > 6 or int(charge) < 1:continue
		seqs.append(seq)
		allmods.append(mods)
		seq = list(seq)
		for mod in mods.split(';'):
			if mod == '':break
			pos = int(mod.split(',')[0])
			if seq[pos - 1] == 'M':
				seq[pos - 1] = 'M(ox)'
		seq = ''.join(seq)
		modified_sequence.append(seq)
		collision_energy.append(DataNCE)
		precursor_charge.append(charge)

print(len(modified_sequence))
with open(DataOutputFile, 'w') as f_out:
	f_out.write('modified_sequence,collision_energy,precursor_charge\n')
	for i in range(len(modified_sequence)):
		f_out.write(modified_sequence[i] + ',' + collision_energy[i] + ',' + precursor_charge[i] + '\n')
