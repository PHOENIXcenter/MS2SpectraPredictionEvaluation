import os

targetpath = 'D:/SoftwareEvaluationNew/ninanjie/target_searchgui_out'
decoypath = 'D:/SoftwareEvaluationNew/ninanjie/deoy_searchgui_out'
output = 'D:/SoftwareEvaluationNew/ninanjie/percolator'

for filename in os.listdir(targetpath):
	if os.path.splitext(filename)[1] == '.xml':
		print('Begin dealing ' + filename)
		print('================================')
		os.system('tandem2pin.exe -o %s/%s.tsv %s/%s %s/%s'%(output, os.path.splitext(filename)[0], targetpath, filename, decoypath, filename))
