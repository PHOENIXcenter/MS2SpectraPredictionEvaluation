import os

output = 'D:/SoftwareEvaluationNew/ninanjie/percolator'

for filename in os.listdir(output):
	if os.path.splitext(filename)[1] == '.tsv':
		print('Begin dealing ' + filename)
		print('================================')
		os.system('percolator.exe -r %s/%s.psms %s/%s'%(output, os.path.splitext(filename)[0], output, filename))
