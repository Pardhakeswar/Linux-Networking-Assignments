#! usr/bin/python
import xml.etree.ElementTree as ET
import time 
from  lib import AquireData
class ReadXml: 

	def __init__(self, vm_name):
		self.path = str('/etc/libvirt/qemu/'+str(vm_name)+'.xml')
		self.tree = ET.parse(self.path)
		self.root = self.tree.getroot()

	def update(self):
		self.tree = ET.parse(self.path)
		self.root = self.tree.getroot()

	def getXmlString(self):
		
		with open(self.path, 'rw') as myfile:
			data=myfile.read()
		return data 

	def getAttributesFromString(self, string):
		attributes=[]
		for child in self.root.iter(str(string)):
			attributes.append(child.attrib)
		return attributes

	def writeXml(self,address):
		for  child in self.root.iter("mac"):
			child.attrib['address']=address
		        #self.tree.write(self.path)
			self.writeToXml()

	def writeToXml(self):
		self.tree.write(self.path)


	def deleteMacByAddress(self, address):
		for elem in self.root.iter("interface"):
			for child in elem.iter("mac"): 
				if child.attrib['address']==address:
					print elem.remove(child)
					print "removing ip"
		self.tree.write(self.path)

def reboot(domain_name,lib_data):
	vm_object = lib_data.getObjectFromName(domain_name)
        vm_object.shutdown()
        xmlfile=ReadXml(domain_name)
        xml=xmlfile.getXmlString()
	conn=lib_data.getConn()
	conn.defineXML(xml)
	time.sleep(25)
	if vm_object.isActive() !=True:
		vm_object.create()	

# ger the list of names 
lib_data =AquireData() 
domains_name = lib_data.listAllDomainsName()

#initialize variable for duplicate IP resolution 
interface_data=[]
interface_data = lib_data.getAllMacIds()
dup_ip=[]
temp =[]
temp.append(interface_data[0][2])

#check for duplicates 
for item in interface_data[1:]: 
	if item[2] in temp:
		dup_ip.append(item)
		print "duplicate found"
	else:
		temp.append(item[2]) 
if dup_ip != []: 
	print dup_ip 
else:
	print "no duplicate address found"
#to  delete XML mac tag
for item in dup_ip:
	vm_data=ReadXml(item[0])
 	vm_data.deleteMacByAddress(item[2])
	
# to prevent same VM from restarting again 
restart_list=[]
for item in dup_ip:
	if item[0] not in restart_list:
		reboot(item[0],lib_data)
		restart_list.append(item[0])
