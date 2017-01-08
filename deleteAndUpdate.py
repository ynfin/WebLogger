#!/usr/bin/env python

import os
import sys
from lxml import etree
import time
import stat
from datetime import datetime, timedelta
import shutil
import copy
from collections import namedtuple

_ntuple_diskusage = namedtuple('usage', 'total used free')

def disk_usage(path):
    """Return disk usage statistics about the given path.

    Returned valus is a named tuple with attributes 'total', 'used' and
    'free', which are the amount of total, used and free space, in bytes.
    """
    st = os.statvfs(path)
    free = st.f_bavail * st.f_frsize
    total = st.f_blocks * st.f_frsize
    used = (st.f_blocks - st.f_bfree) * st.f_frsize
    return _ntuple_diskusage(total, used, free)

class sidepanelitem:
	def __init__(self):
		self.nickname = ""
		self.address = ""
		self.dealmethod = ""

skynetFiles_lower = []
skynetFiles = []
logfile = '/var/www/logger/WebLogger/updateXmlLog.txt'
logstring = ""
loglist = []

searchdir = '/var/www/logger/WebLogger/logstorage'
pathtologfolder = '/var/www' #searchdir[0:searchdir.rfind('/')+1]
#print pathtologfolder

print disk_usage("/var/www/data/disk")

diskpath = "/var/www/data/disk"
statvfs = os.statvfs(diskpath)

availableBytes = statvfs.f_frsize * statvfs.f_bavail
totalBytes = statvfs.f_frsize * statvfs.f_blocks
spaceRatio = float(availableBytes) / float(totalBytes)

print availableBytes
print totalBytes
print spaceRatio

for path, subdirs, files in os.walk(searchdir):
	for name in files:
		if name.endswith(('.txt','.log','.autolog')):  
			skynetFiles_lower.append(name.lower())
			skynetFiles.append(os.path.join(path,name))
			#print "found: " + os.path.join(path,name)

skynetFiles.sort(key=lambda x: os.path.getmtime(x), reverse=True)

with open('/var/www/logger/WebLogger/addresslist.txt') as f:
	addresscontent = f.readlines()

sidepanel = []



for line in addresscontent:
	if line.startswith("10.47.89."):
		tempsidepanelitem = sidepanelitem()
		
		nickname = line.split(" ")[1]
		address = line.split(" ")[0]
		dealmethod = line.split(" ")[2].rstrip()
		
		tempsidepanelitem.nickname = nickname
		tempsidepanelitem.address = address
		tempsidepanelitem.dealmethod = dealmethod
		
		for filename in skynetFiles_lower:
			if address in filename:
				print filename + ' matches ',
				print nickname
				#sidepanel.append(address)
				sidepanel.append(copy.deepcopy(tempsidepanelitem))

seen = set()
finalList = []
for obj in sidepanel:
    if obj.address not in seen:
        finalList.append(obj)
        seen.add(obj.address)

#finalList = list(set(sidepanel))
finalList.sort()

# Write XML file for AJAX sidepanel
response = etree.Element("response")
info = etree.SubElement(response, "info")
panelfiles = etree.SubElement(response, "panelfiles")
serverfiles = etree.SubElement(response, "serverfiles")

spaceTotal = etree.SubElement(info,"spaceTotal")
spaceFree = etree.SubElement(info,"spaceFree")
spaceTotal.text = str(totalBytes)
spaceFree.text = str(availableBytes)

for item in finalList:
    panelfile = etree.SubElement(panelfiles, "panelfile")
    filename = etree.SubElement(panelfile, "filename")
    fileip = etree.SubElement(panelfile,"address")
    filedeal = etree.SubElement(panelfile,"deal")
    filename.text = str(item.nickname)
    fileip.text = str(item.address)
    filedeal.text = str(item.dealmethod)

for item in skynetFiles:
    serverfile = etree.SubElement(serverfiles, "serverfile")
    filename = etree.SubElement(serverfile, "serverfilename")
    filepath = etree.SubElement(serverfile, "serverfilepath")
    filedate = etree.SubElement(serverfile, "serverfiledate")
    filename.text = str(os.path.basename(item))
    filepath.text = str(item).replace(pathtologfolder,"")
    print str(item).replace(pathtologfolder,"../")
    filedate.text = str(time.ctime(os.path.getmtime(item)))
    logstring = logstring + "[ " + filedate.text + " ]\t"
    logstring = logstring + filename.text + "\n"


print(etree.tostring(response, pretty_print=True))

# Write the XML to the output file
with open('/var/www/logger/WebLogger/skynetcontent.xml', 'w') as output_file:
    output_file.write('<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>\n')
    output_file.write(etree.tostring(response, pretty_print = True))

print "xml written..."

with open(logfile, "w") as myfile:
    date = datetime.now().strftime("%I:%M %B %d, %Y")
    myfile.write(str(date)+"\n")
    myfile.write("-----------------------------------------------------\n")
    myfile.write(logstring)
