import os
import sys
import os.path
import time

# def list_file(path):
path = 'D:/SoftwareEvaluationNew/ninanjie/ninanjie_masot/'
index = 1
for filename in os.listdir(path):
	if os.path.splitext(filename)[1] == '.PepList':
		print('Begin dealing: ' + filename)
		with open(path+filename,'r') as f:
			header = f.readline()
			with open(path+os.path.splitext(filename)[0].split('.')[0] + '.Pep','a') as fp:
				fp.write(header)
			while True:
				line = f.readline()
				if line == "":
					break
				label = line.split('\t')[2]
				length = len(line.split('\t')[3])
				ionscore = line.split('\t')[13]
				q_value = line.split('\t')[18]
				# print(label)
				# print(str(label) + '---' + str(length) + '---' + str(ionscore) + '---' + str(q_value))
				if not label or not length or not ionscore or not q_value:continue
				if int(label) == 1 and int(length) >= 7 and float(ionscore) > 10 and float(q_value) < 0.01:
					# print(line)
					with open(path+os.path.splitext(filename)[0].split('.')[0] + '.Pep','a') as fp:
						fp.write(line)
		index += 1
print('Done!')

