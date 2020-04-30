import re
import os

#记录mascot和MQ&pFind相同的数量
sameNum = 0
#存放MQ和pFind交集中的title和对应序列
targetTitle2Seq = {}
#mascot结果路径
path = 'D:/SoftwareEvaluationNew/ninanjie/ninanjie-comet.txt'
tmppath = 'D:/SoftwareEvaluationNew/ninanjie/percolator/'
outpath = 'D:/SoftwareEvaluationNew/ninanjie/ninanjie.txt'
tendempath = 'D:/SoftwareEvaluationNew/ninanjie/target_searchgui_out/'
with open(path,'r') as f:
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

print('MQ、pFind、 Comet and Mascot total number:' + str(len(targetTitle2Seq)))
print('=============================================')

tandemTitle2allTitle = {}
for filename in os.listdir(tendempath):
	if os.path.splitext(filename)[1] == '.xml':
		print('Begin dealing ' + filename)
		title = os.path.splitext(filename)[0].split('.')[0]
		with open(tendempath+filename,'r') as f:
			line = True
			while line:
				line = f.readline()
				if '<group id="' in line:
					tandemScan = line.split('" mh="')[0].split('id="')[1]
					tandemTitle = title + '_' + tandemScan
					duiyingTitle = ''
					while '</group></group>' not in line:
						line = f.readline()
						if not line:break
						if '<note label="Description">' in line:
							duiyingTitle = line.split('label="Description">')[1].split(' RTINSECONDS=')[0]
					tandemTitle2allTitle[tandemTitle] = duiyingTitle
print('tendem total number:' + str(len(tandemTitle2allTitle)))
print('========================================')

outputDict = {}
for filename in os.listdir(tmppath):
	if os.path.splitext(filename)[1] == '.psms':
		print('Begin dealing ' + filename)
		with open(tmppath+filename,'r') as f:
			for line in f:
				if 'PSMId' in line: continue
				testTitle = line.split('\t')[0][:-4]
				qvalue = float(line.split('\t')[2])
				if qvalue < 0.01 and tandemTitle2allTitle[testTitle] in targetTitle2Seq.keys():
					testSeq = line.split('\t')[4][2:-2]
					testSeq = re.sub(r'\[.+\]','mod',testSeq)
					if testSeq == targetTitle2Seq[tandemTitle2allTitle[testTitle]]:
						sameNum += 1
						outputDict[tandemTitle2allTitle[testTitle]] = tandemTitle2allTitle[testTitle]
print('=============================================')
print('percolator results & MQ-pFind-Comet-Mascot results same:' + str(sameNum))

with open(outpath,'w') as fout:
	fout.write('peptide	modification	charge	RawFile+SCAN\n')
	with open(path,'r') as f:
		for line in f:
			outTitle = re.split('\t|\n', line)[3]
			if outTitle in outputDict.keys():
				fout.write(line)