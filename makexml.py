import os
from lxml import etree
import logproc_pumpwall

""" go through each log and process it according to corresponding method """

searchdir = '/var/www/logger/WebLogger/logstorage'
mainlogfiles = []

for path, subdirs, files in os.walk(searchdir):
	for name in files:
		if name.endswith(('.txt','.log','.autolog')) and name.startswith("main_logfile"):  
			mainlogfiles.append(os.path.join(path,name))
			
for log in mainlogfiles:		
	if "89.180" in log:
		logproc_pumpwall.process(log)