import re
import os

#记录mascot和MQ&pFind相同的数量
sameNum = 0
#存放MQ和pFind交集中的title和对应序列
targetTitle2Seq = {}
#mascot结果路径
path = 'D:/SoftwareEvaluationNew/ninanjie/ninanjie_comet/'
tmppath = 'D:/SoftwareEvaluationNew/ninanjie/tmp.txt'
outpath = 'D:/SoftwareEvaluationNew/ninanjie/ninanjie-comet.txt'
with open(tmppath,'r') as f:
	for line in f:
		if 'peptide' in line:continue
		tarSeq = list(re.split('\t|\n', line)[0])
		tarMods = re.split('\t|\n', line)[1].split(';')[:-1]
		tarTitle = re.split('\t|\n', line)[3].split('.')[0:4]
		tarTitle = ".".join(tarTitle)
		for mods in tarMods:
			pos = int(mods.split(',')[0])
			mod = mods.split(',')[1]
			if mod == 'Carbamidomethyl[C]':
				tarSeq[pos - 1] = 'Cmod'
			else:
				tarSeq[pos - 1] = 'Mmod'
		targetTitle2Seq[tarTitle] = "".join(tarSeq)

print('MQ and pFind total number:' + str(len(targetTitle2Seq)))
print('=============================================')

outputDict = {}

for filename in os.listdir(path):
	if os.path.splitext(filename)[1] == '.xml':
		print('Begin dealing ' + filename)
		with open(path+filename,'r') as f:
			line = True
			while line:
				line = f.readline()
				if '<error_point error="0.0100"' in line:
					min_prob = float(line.split(' ')[2].split('ob="')[1][:-1])
				if '<spectrum_query' in line:
					testTitle = line.split(' ')[1].split('um="')[1][:-1]
					if testTitle in targetTitle2Seq.keys():
						testSeq = ''
						while '</spectrum_query>' not in line:
							line = f.readline()
							if '<search_hit ' in line:
								testSeq = line.split(' ')[2].split('e="')[1][:-1]
							if '<modification_info' in line:
								testSeq = line.split('"')[1]
								testSeq = testSeq.replace('C','Cmod')
								testSeq = re.sub(r'\[.+\]','mod',testSeq)
							if '<peptideprophet_result' in line:
								probability = float(line.split(' ')[1].split('ity="')[1][:-1])
						if testSeq == targetTitle2Seq[testTitle] and probability >= min_prob:
							sameNum += 1
							outputDict[testTitle] = testTitle

print('Mascot results & MQ-pFind results same:' + str(sameNum))

with open(outpath,'w') as fout:
	fout.write('peptide	modification	charge	RawFile+SCAN\n')
	with open(tmppath,'r') as f:
		for line in f:
			outTitle = re.split('\t|\n', line)[3].split('.')[0:4]
			outTitle = ".".join(outTitle)
			if outTitle in outputDict.keys():
				fout.write(line)