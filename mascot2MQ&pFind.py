import re
import os

#记录mascot和MQ&pFind相同的数量
sameNum = 0
#存放MQ和pFind交集中的title和对应序列
targetTitle2Seq = {}
#mascot结果路径
path = 'D:/SoftwareEvaluationNew/ninanjie/ninanjie_masot/'
tmpput = 'D:/SoftwareEvaluationNew/ninanjie/ninanjieMP.txt'
output = 'D:/SoftwareEvaluationNew/ninanjie/tmp.txt'
with open(tmpput,'r') as f:
	for line in f:
		if 'peptide' in line:continue
		tarSeq = list(re.split('\t|\n', line)[0])
		tarMods = re.split('\t|\n', line)[1].split(';')[:-1]
		tarTitle = re.split('\t|\n', line)[3]
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
	if os.path.splitext(filename)[1] == '.Pep':
		print('Begin dealing ' + filename)
		with open(path+filename,'r') as f:
			for line in f:
				if 'query' in line:continue
				testTitle = line.split('\t')[1]
				if testTitle not in targetTitle2Seq.keys():continue
				testSeq = line.split('\t')[3].replace('C','Cmod')
				testSeq = list(testSeq)
				testMods = line.split('\t')[4][1:-1]
				for index,v in enumerate(testMods):
					if v == '1':
						testSeq[index] = 'Mmod'
				if "".join(testSeq) == targetTitle2Seq[testTitle]:
					sameNum += 1
					outputDict[testTitle] = testTitle
print('Mascot results & MQ-pFind results same:' + str(sameNum))

with open(output,'w') as fout:
	fout.write('peptide	modification	charge	RawFile+SCAN\n')
	with open(tmpput,'r') as f:
		for line in f:
			outTitle = re.split('\t|\n', line)[3]
			if outTitle in outputDict.keys():
				fout.write(line)

