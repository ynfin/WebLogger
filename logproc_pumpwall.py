import os
from lxml import etree

def process(pathToLog):
	logcontent = []
	
	timestamps = []
	
	pump1PsIn = []
	pump2PsIn = []
	pump3PsIn = []
	pump4PsIn = []
	
	pump1PsOut = []
	pump2PsOut = []
	pump3PsOut = []
	pump4PsOut = []
	
	pump1TrqLow = []
	pump2TrqLow = []
	pump3TrqLow = []
	pump4TrqLow = []
		
	pump1TrqHi = []
	pump2TrqHi = []
	pump3TrqHi = []
	pump4TrqHi = []
	
	# Write XML file for AJAX sidepanel
	logfileroot = etree.Element("logfileroot")
	
	with open(pathToLog) as f:
		logcontent = f.readlines()
		
		for line in logcontent:
				if "PS:" in line:
					pump1PsIn.append((line.split(',')[1].rstrip(),line[0:19]))
					pump2PsIn.append((line.split(',')[2].rstrip(),line[0:19]))
					pump3PsIn.append((line.split(',')[3].rstrip(),line[0:19]))
					pump4PsIn.append((line.split(',')[4].rstrip(),line[0:19]))
				
					pump1PsOut.append((line.split(',')[5].rstrip(),line[0:19]))
					pump2PsOut.append((line.split(',')[6].rstrip(),line[0:19]))
					pump3PsOut.append((line.split(',')[7].rstrip(),line[0:19]))
					pump4PsOut.append((line.split(',')[8].rstrip(),line[0:19]))
						
				if "TRQ" in line:
					pump1TrqLow.append((line.split(',')[1].rstrip(),line[0:19]))
					pump2TrqLow.append((line.split(',')[2].rstrip(),line[0:19]))
					pump3TrqLow.append((line.split(',')[3].rstrip(),line[0:19]))
					pump4TrqLow.append((line.split(',')[4].rstrip(),line[0:19]))
				
					pump1TrqHi.append((line.split(',')[5].rstrip(),line[0:19]))
					pump2TrqHi.append((line.split(',')[6].rstrip(),line[0:19]))
					pump3TrqHi.append((line.split(',')[7].rstrip(),line[0:19]))
					pump4TrqHi.append((line.split(',')[8].rstrip(),line[0:19]))
					
		print "pressure sample lines: " + str(len(pump1PsIn))
		print "torque sample lines: " + str(len(pump1TrqLow))

		if len(pump1PsIn) > len(pump1TrqLow):
			arraycount = len(pump1TrqLow)
		else:
			arraycount = len(pump1PsIn)

		for i in range(arraycount):
			logline = etree.SubElement(logfileroot, "logline")
			timestamp = etree.SubElement(logline, "timestamp")
			timestamp.text = pump1PsIn[i][1]
		
			pump1psin = etree.SubElement(logline, "Pump1PSIn")
			pump2psin = etree.SubElement(logline, "Pump2PSIn")
			pump3psin = etree.SubElement(logline, "Pump3PSIn")
			pump4psin = etree.SubElement(logline, "Pump4PSIn")	
			pump1psin.text = pump1PsIn[i][0]
			pump2psin.text = pump2PsIn[i][0]
			pump3psin.text = pump3PsIn[i][0]
			pump4psin.text = pump4PsIn[i][0]
			
			pump1psout = etree.SubElement(logline, "Pump1PsOut")
			pump2psout = etree.SubElement(logline, "Pump2PsOut")
			pump3psout = etree.SubElement(logline, "Pump3PsOut")
			pump4psout = etree.SubElement(logline, "Pump4PsOut")
			pump1psout.text = pump1PsOut[i][0]
			pump2psout.text = pump2PsOut[i][0]
			pump3psout.text = pump3PsOut[i][0]
			pump4psout.text = pump4PsOut[i][0]
			
			pump1trqlow = etree.SubElement(logline, "Pump1TourqueLow")
			pump2trqlow = etree.SubElement(logline, "Pump2TourqueLow")
			pump3trqlow = etree.SubElement(logline, "Pump3TourqueLow")
			pump4trqlow = etree.SubElement(logline, "Pump4TourqueLow")
			pump1trqlow.text = pump1TrqLow[i][0]
			pump2trqlow.text = pump2TrqLow[i][0]
			pump3trqlow.text = pump3TrqLow[i][0]
			pump4trqlow.text = pump4TrqLow[i][0]
			
			pump1trqhi = etree.SubElement(logline, "Pump1TourqueHigh")
			pump2trqhi = etree.SubElement(logline, "Pump2TourqueHigh")
			pump3trqhi = etree.SubElement(logline, "Pump3TourqueHigh")
			pump4trqhi = etree.SubElement(logline, "Pump4TourqueHigh")
			pump1trqhi.text = pump1TrqHi[i][0]
			pump2trqhi.text = pump2TrqHi[i][0]
			pump3trqhi.text = pump3TrqHi[i][0]
			pump4trqhi.text = pump4TrqHi[i][0]
		
	#print(etree.tostring(logfileroot, pretty_print=True))
	
	# Write the XML to the output file
	pathToOutputXml = pathToLog[:-8]+".xml"
	with open(pathToOutputXml, 'w') as output_file:
		output_file.write('<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>\n')
		output_file.write(etree.tostring(logfileroot, pretty_print = True))
	
	print "done! file written to: " + pathToOutputXml 