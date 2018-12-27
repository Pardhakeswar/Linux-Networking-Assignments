import xml.etree.ElementTree as ET
import sys
from  shutil import copyfile

#tree =ET.parse('/etc/libvirt/qemu/duplicate_ip.xml')
#domain =tree.getroot()

class create_xml:
	def __init__(self):
		self =None
	def copy(self):
		copyfile("/var/lib/libvirt/images/"+sys.argv[1]+".img", "/var/lib/libvirt/images/"+sys.argv[2]+'.img')		

	def name(self,domain):
		name_ =domain.find('name')
		name_.text =sys.argv[2]

	def remove_uuid(self, domain):
		uuid =domain.find('uuid')
		domain.remove(uuid)
		
	def modify_source_file(self, domain):
		for child in domain.iter("source"):
			if 'file' in child.attrib:
				child.set('file','/var/lib/libvirt/images/'+sys.argv[2]+'.img')	


	def remove_exist_interf(self, domain):
		device =domain.find('devices')
		for interfaces in device.findall('interface'):
			device.remove(interfaces)

	def Add_network(self,domain,network):
		device =domain.find('devices')
		interf =ET.SubElement(device,'interface')
		interf.set('type','network')
		source =ET.SubElement(interf,'source')
		source.set('network', network)
		model =ET.SubElement(interf,'model')
		model.set('type','virtio')
		#adress =ET.SubElement(interf,'address')
		#adress.set('type','pci')
		#adress.set('domain','0x0000')
		#adress.set('bus','0x00')
		#adress.set('function','0x0')
		#adress.set('slot',slot)

if __name__ == "__main__":
	tree =ET.parse('/etc/libvirt/qemu/'+sys.argv[1]+'.xml')
	domain =tree.getroot()
	netlist =sys.argv[3].split(":")
	xml_file =create_xml()
	xml_file.copy()
	xml_file.name(domain)
	xml_file.remove_uuid(domain)
	xml_file.modify_source_file(domain)
	xml_file.remove_exist_interf(domain)
        for item in netlist:
		xml_file.Add_network(domain,item)

	tree.write('/etc/libvirt/qemu/'+sys.argv[2]+'.xml')
