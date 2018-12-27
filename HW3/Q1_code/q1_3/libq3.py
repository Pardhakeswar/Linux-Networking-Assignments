#! usr/bin/python
import libvirt	
#from getXml import ReadXml  

class AquireData:
	def __init__(self):
		self.conn=libvirt.open('qemu:///system')
#		self.interface=interface.new() 
	def __init__(self, username,ip):
		self.conn =libvirt.open('qemu+ssh://{}@{}/system'.format(username,ip))
	
	def getConn(self):
		return self.conn
	
	def listAllDomainsId(self):
		return self.conn.listDomainsID()

	def listAllDomainsName(self):
		domains_id = self.listAllDomainsId()
		domains_name=[]
		for domain_id in domains_id:
			domains_name.append(self.getNameFromId(domain_id))
		return domains_name

	def getNameFromId(self,arg1):
		return self.conn.lookupByID(arg1).name()

	def getObjectFromName(self, name):
		return self.conn.lookupByName(name)

	def getInterfacesFromObject(self, object):
		interface=object.interfaceAddresses(libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT,0)
		return interface

	def getIpFromObject(self,object):
		interfaces= self.getInterfacesFromObject(object)
		name_of_vm = object.name()
		hash = []
		return_array = []
		for (name, val) in interfaces.iteritems():
    			if val['addrs'] and name!="lo":
				hash.append(name_of_vm)
				hash.append(name) 
        			for ipaddr in val['addrs']:
					 if ipaddr['type'] == libvirt.VIR_IP_ADDR_TYPE_IPV4:
               					 hash.append(ipaddr['addr'])
            				 if ipaddr['type'] == libvirt.VIR_IP_ADDR_TYPE_IPV6:
                				 hash.append(ipaddr['addr'])
				return_array.append(hash)
				hash=[]
		return return_array

	def getMacFromObject(self, object):
		interfaces= self.getInterfacesFromObject(object)
               # print interfaces
		name_of_vm = object.name()
                hash = []
                return_array = []
                for (name, val) in interfaces.iteritems():
                	if val['hwaddr'] and name!="lo":
				 hash.append(name_of_vm)
                          	 hash.append(name) 
                                 hash.append(val['hwaddr'])
                		 return_array.append(hash)
                                 hash=[]
                return return_array

	def getAllIp(self):
		single_vm_data=[]
		consolidated_data =[]
		domains_name= self.listAllDomainsName()
		for domain_name in domains_name:
        		domain_object = self.getObjectFromName(domain_name)
        		ips_addr= self.getIpFromObject(domain_object)
        		for item in ips_addr:
        			single_vm_data.append(item[0])
				single_vm_data.append(item[1])
				single_vm_data.append(item[2])
				consolidated_data.append(single_vm_data)
				single_vm_data =[]
		return consolidated_data


	def getAllMacIds(self):
		single_vm_data=[]
                consolidated_data =[]
                domains_name= self.listAllDomainsName()
                for domain_name in domains_name:
                        domain_object = self.getObjectFromName(domain_name)
                        ips_addr= self.getMacFromObject(domain_object)
                        for item in ips_addr:
                                single_vm_data.append(item[0])
                                single_vm_data.append(item[1])
                                single_vm_data.append(item[2])
                                consolidated_data.append(single_vm_data)
                                single_vm_data =[]
                return consolidated_data

"""	
#question 1 
username = raw_input("enter username")
ip =raw_input("enter IP address ")
lib_data=AquireData(username, ip)


domain_id= lib_data.listAllDomainsId()
#print (domain_id)
domains_name= lib_data.listAllDomainsName()
#print (domains_name)
#lib_data.shutdown("duplicate_ip")


print("====================================================================")
print ("Printing IP addresses of the VM")
print("====================================================================")

for domain_name in domains_name:
	domain_object = lib_data.getObjectFromName(domain_name)
	ips_addr= lib_data.getIpFromObject(domain_object)
	for item in ips_addr:
		print ("vm name :{:20s}  inf name :{:10s}  ip addr: {:10s}".format(item[0],item[1],item[2]))

print("====================================================================")
print("Printing MAC addresses ")
print("====================================================================")

for domain_name in domains_name:
	domain_object =lib_data.getObjectFromName(domain_name)
	mac_addr= lib_data.getMacFromObject(domain_object)
	for item in mac_addr:
		print ("vm name :{:20s}  inf name :{:10s} Mac addr: {:10s}".format(item[0], item [1],item[2]))


"""
