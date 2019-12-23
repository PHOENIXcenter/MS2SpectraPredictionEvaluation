import os

MS2PIPresultPath = 'PXD003881/MS2PIP-result/'
file_infos = []
OutputFile = 'PXD003881/MS2PIP-result/MS2PIP_Predictions.msp'

for filename in os.listdir(MS2PIPresultPath):
	if os.path.splitext(filename)[1] == '.msp':
		print(filename)
		with open(MS2PIPresultPath + filename, 'r') as f:
			for line in f:
				if line == '':break
				file_infos.append(line)

with open(OutputFile, 'w') as f:
	for line in file_infos:
		f.write(line)
