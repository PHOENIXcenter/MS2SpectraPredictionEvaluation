import re
import collections

file_infos = []
csv_infos = {}
DataNCE = '35.0'
title2infos = collections.OrderedDict()
MS2PIPinputFile = 'ToMS2PIP/PXD003881_ms2pip.PEPREC'
MS2PIPpredictFile = 'PXD003881/MS2PIP-result/MS2PIP_msp.msp'
MS2PIPmspFile = 'PXD003881/MS2PIP-result/MS2PIP_new.msp'

with open(MS2PIPinputFile, 'r') as f:
	for line in f:
		if 'spec_id	modifications' in line:continue
		vaules = []
		title = line.split('\t')[0]
		mods = line.split('\t')[1]
		seq = line.split('\t')[2]
		vaules.append(mods)
		vaules.append(seq)
		title2infos[title] = vaules

with open(MS2PIPpredictFile, 'r') as f:
	while True:
		line = f.readline()
		if line == '':break
		if 'MS2PIP_ID=' in line:
			restitle = re.split('MS2PIP_ID=|\n',line)[1][1:-1]
			charge = restitle.split('.')[-3]
			line = f.readline()
			line = f.readline()
			temp_inten = []
			mz_intens = []
			resvaules = {}
			while line != '\n':
				mz_inten = []
				ion_pos = re.split('\t|\n',line)[2][1:-1]
				mz = re.split('\t|\n',line)[0]
				inten = re.split('\t|\n',line)[1]
				temp_inten.append(float(inten))
				mz_inten.append(ion_pos)
				mz_inten.append(mz)
				mz_inten.append(float(inten))
				mz_intens.append(mz_inten)
				line = f.readline()
				if line == '':break
			resvaules = {}
			resvaules['charge'] = charge
			max_inten = max(temp_inten)
			for info in mz_intens:
				resvaules[info[0]] = [info[1], str(info[2]/max_inten)]
			csv_infos[restitle] = resvaules

print(len(csv_infos))

for file in title2infos.keys():
	if file in csv_infos.keys():
		file_seq = title2infos[file][1]
		file_mods = title2infos[file][0]
		file_charge = csv_infos[file]['charge']
		if len(file_seq) >= 7 and len(file_seq) <= 30:
			if int(file_charge) >=1 and int(file_charge) <= 6:
				if file_mods == '-':
					modinfo = 0
					ModString = ''
				else:
					modlist = file_mods.split('|')
					modinfo = str(len(modlist)//2)
					ModString = ''
					for i in range(0, len(modlist), 2):
						pos = int(modlist[i])
						mod = modlist[1 + i]
						if mod == 'Oxidation[M]':
								modinfo = modinfo + '/' + str(pos - 1) + ',M,Oxidation'
								ModString = ModString + 'Oxidation@M' + str(pos) + '; '
						else:
							modinfo = modinfo + '/' + str(pos - 1) + ',C,Carbamidomethyl'
							ModString = ModString + 'Carbamidomethyl@C' + str(pos) + '; '
					ModString = ModString[:-2]
				file_infos.append('Name: ' + file_seq + '/' + file_charge + '\n')
				file_infos.append('MW: -\n')
				file_infos.append('Comment: Parent=- Collision_energy=%s Mods=%s ModString=%s//%s/%s\n'
					%(DataNCE, modinfo, file_seq, ModString, file_charge))
				file_infos.append('Num peaks: ' + str(len(csv_infos[file]) - 1) + '\n')
				for i in range(len(file_seq)):
					if ('Y' + str(i + 1)) in csv_infos[file].keys():
						file_infos.append(csv_infos[file]['Y' + str(i + 1)][0] + '\t' + csv_infos[file]['Y' + str(i + 1)][1] + '\t' + '"y' + str(i + 1) + '/0.0ppm"\n')
					if ('B' + str(i + 1)) in csv_infos[file].keys():
						file_infos.append(csv_infos[file]['B' + str(i + 1)][0] + '\t' + csv_infos[file]['B' + str(i + 1)][1] + '\t' + '"b' + str(i + 1) + '/0.0ppm"\n')

with open(MS2PIPmspFile, 'w') as f:
	for line in file_infos:
		f.write(line)