Question2:
The scripts will prompt for the Input IP in the format :x.x.x.x/24 format
Assuming the 4 correspdoning xml files exist in the same folder and are predefined
with the basic L2 ovs config.
1.ovs-net-nat.xml
2.ovs-net-l2.xml
3.ovs-net-routed.xml
4.ovs-net-other.xml 

In turn the script is using two bash scripts 
1.iptables-nat-config.sh for configuring the Ip tables for nat and routed mode
2.dns-config.sh for configuring the dns files.


=====================creation of VMs=========================
1.Script will prompt for input of the reference VM for copying teh xml file
It has to be in the format VM1 or VM2
2.Input the names of two Vm to get created 
3.The script is using xml_modify.sh for modfying the xml file and creating a new vm

with Virt build for installing the wireshark 
following error is being thrown 
/etc/fstab no such file or directory error
so commentng out the teh code in the script.  


 

