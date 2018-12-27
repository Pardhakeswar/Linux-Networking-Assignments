import subprocess
import os
import time
import sys

cont ={}

################################### defining the GRE VXLN,Bridge function ##########################

def display_output(cmd):
	ping = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	while True:
    		 out = ping.stderr.read(1)
		 if out == '' and ping.poll() != None:
        		break

    		 if out != '':
        		sys.stdout.write(out)
        		sys.stdout.flush()


def container_create(name_cs):
	
	print "conatiner %s created " %(name_cs)
	p = subprocess.check_output("sudo docker ps",shell =True)
        cont[name_cs] = " "
	
        if name_cs in p:
                cont[name_cs] ="present"
	
        if cont[name_cs] != "present":
                os.system("sudo docker run -itd --privileged --name=" + name_cs +" iserver")
                time.sleep(5)


def bridge_create(name_cs):

        print "bridge creation for %s" %(name_cs)

        br = subprocess.check_output(" brctl show",shell =True)
        br_name = name_cs+"-br"

        if br_name not in br :
                os.system(" brctl addbr "+ br_name)
                os.system(" ip link set dev "+br_name+" up")

        return br_name


def veth_create_with_ns(name_cs, ns_name, br_name, ip_):
	
	veth1 = name_cs+"-br"
        veth2 = "br-"+name_cs
	#print "before veth_creation"
        os.system("ip link add " + veth1 +" type veth peer name "+ veth2)
        print "veth created for con1 and br"
        pid1 = subprocess.check_output("sudo docker inspect -f '{{.State.Pid}}' "+name_cs, shell=True).strip()
        os.system("sudo ip link set "+veth1+" netns "+pid1)
        os.system("sudo ip link set "+veth2+" netns "+ns_name)
        os.system("sudo ip netns exec "+ns_name+" brctl addif " +br_name+ " "+ veth2)
        os.system("sudo ip netns exec "+ns_name+" ip link set dev "+ veth2 +" up")
        print " veth Added to container and bridge"
        ip = ip_
        os.system("sudo docker exec --privileged "+name_cs+" ip addr add "+ip+" dev "+veth1)
        os.system("sudo docker exec --privileged "+name_cs+" ip link set dev "+veth1+" up")


def veth_create_with_cont(ns_name, leaf_con, ip_ns, ip_leaf):
	
	veth1 = leaf_con+"-"+ns_name
	veth2 = ns_name+"-"+leaf_con
	os.system("ip link add " + veth1 +" type veth peer name "+ veth2)
	print "veth created for ns & leaf_con"
	pid1 = subprocess.check_output("sudo docker inspect -f '{{.State.Pid}}' "+leaf_con, shell=True).strip()
	os.system("sudo ip link set "+veth1+" netns "+pid1)
        os.system("sudo ip link set "+veth2+" netns "+ns_name)
	os.system("sudo docker exec -it --privileged "+leaf_con+ " ip addr add "+ip_leaf+" dev "+veth1)
	os.system("sudo docker exec -it --privileged "+leaf_con+ " ip link set dev "+veth1+" up")
	os.system("sudo ip netns exec "+ns_name+" ip addr add "+ip_ns+" dev "+veth2)
	os.system("sudo ip netns exec "+ns_name+" ip link set dev "+veth2+" up")

	return veth2

	
def namespace_bridge_create(name_cs):
	
	print "Namespace & bridge creation for %s" %(name_cs)
	ns = subprocess.check_output("ip netns list ",shell =True)
        ns_name = name_cs+"-ns"

	if ns_name not in ns:
                os.system("sudo ip netns add "+ ns_name)

                
        br = subprocess.check_output("sudo ip netns exec "+ns_name+" brctl show",shell =True)
        br_name = name_cs+"-bridge"
	 
        if br_name not in br:
                os.system("sudo ip netns exec "+ns_name+" brctl addbr "+ br_name)
                os.system("sudo ip netns exec "+ns_name+" ip link set dev "+br_name+" up")

	
	return ns_name,br_name	
	#print "namespace :%s & bridge :%s creted" %(ns_name) %(br_name)



def veth_create_container_bridge(name_cs, br_name, ip_cs):
	
	print "veth between conatiner & bridge"
	veth1 = name_cs+"-"+br_name
        veth2 = br_name+"-"+name_cs
        os.system("ip link add " + veth1 +" type veth peer name "+ veth2)
        print "veth created for con & bridge"
        pid = subprocess.check_output("sudo docker inspect -f '{{.State.Pid}}' "+name_cs, shell=True).strip()
	
	#veth addition to container
	os.system("sudo ip link set "+veth1+" netns "+pid)
	os.system("sudo docker exec -it --privileged "+name_cs+ " ip addr add "+ip_cs+" dev "+veth1)
        os.system("sudo docker exec -it --privileged "+name_cs+ " ip link set dev "+veth1+" up")

	#veth addition to bridge
	os.system("brctl addif "+br_name+" "+veth2)
	os.system("sudo ip link set dev "+veth2+" up")
	



#########################conatiners connected with bridges#####################

def bridge_connection(name_cs1, name_cs2):

        print name_cs1, name_cs2, " connected by bridge"

	container_create(name_cs1)
	container_create(name_cs2)
	
	ns_name,br_name = namespace_bridge_create(name_cs1)

	#veth_creation for cs1-br
	veth_create_with_ns(name_cs1, ns_name, br_name, "30.0.0.1/24")
	print "ipadress given to veth in con1"

	#veth_creation for cs2-br
	veth_create_with_ns(name_cs2, ns_name, br_name, "30.0.0.2/24")
	print "ipadress given to veth in con2"
	
	#displaying the ping output between con1 and con2
	cmd = "sudo docker exec --privileged %s ping -i 1 -c 5 30.0.0.2" % (name_cs1)
	display_output(cmd)	

	#veth creation for name sapce  & bridge
	#veth5 = ns_name+ "-lc1"
        #veth6 = "lc1-"+ns_name      
        #os.system("ip link add " + veth5 +" type veth peer name "+ veth6)
	

	
	
######################### conatiners with VXLAN connection  #################################### 

def vxlan_connection(name_cs1, name_cs2):
	
	print name_cs1, name_cs2, " connected by vxlan"
	
	#contanier creation
	container_create(name_cs1)
	container_create(name_cs2)
	
	#namespace & bridge creation
	ns1,br1 = namespace_bridge_create(name_cs1)
	ns2,br2 = namespace_bridge_create(name_cs2)

	#veth creation for ns1
	veth_create_with_ns(name_cs1, ns1, br1, "40.0.0.1/24")
        print "ipadress given to veth in con1"
	 
	#veth creation for ns2
	veth_create_with_ns(name_cs2, ns2, br2, "40.0.0.2/24")
        print "ipadress given to veth in con2"

	#veth creation between ls1 & ns1
	ns1_int = veth_create_with_cont(ns1, "lc1", "41.0.0.1/24", "41.0.0.2/24")
	
	#veth creation between ls2 & ns2
	ns2_int = veth_create_with_cont(ns2, "lc2", "43.0.0.1/24", "43.0.0.2/24")

	#vxlan interface creation in ns1
	os.system("sudo ip netns exec "+ns1+" ip link add name vxlan-"+ns1+" type vxlan id 40 dev "+ns1_int+" remote 43.0.0.1 dstport 5000")	
	os.system("sudo ip netns exec "+ns1+" ip link set dev vxlan-"+ns1+" up")
	os.system("sudo ip netns exec "+ns1+" brctl addif "+br1+ " vxlan-"+ns1)

	#vxlan interface creation in ns1
	os.system("sudo ip netns exec "+ns2+" ip link add name vxlan-"+ns2+" type vxlan id 40 dev "+ns2_int+" remote 41.0.0.1 dstport 5000")
        os.system("sudo ip netns exec "+ns2+" ip link set dev vxlan-"+ns2+" up")
        os.system("sudo ip netns exec "+ns2+" brctl addif "+br2+ " vxlan-"+ns2)	

	#adding the default route in ns1
	os.system("sudo ip netns exec "+ns1+" ip route add default via 41.0.0.2")
	
	os.system("sudo docker exec -it --privileged lc1 ip route add 43.0.0.0/24 via 26.0.0.1")
	os.system("sudo docker exec -it --privileged sc2 ip route add 43.0.0.0/24 via 28.0.0.2")
	os.system("sudo docker exec -it --privileged sc2 ip route add 41.0.0.0/24 via 26.0.0.2")
	os.system("sudo docker exec -it --privileged lc2 ip route add 41.0.0.0/24 via 28.0.0.1")
	
	#adding default route in ns2
	os.system("sudo ip netns exec "+ns2+" ip route add default via 43.0.0.2")

	cmd = "sudo docker exec --privileged %s ping -i 1 -c 5 40.0.0.2" % (name_cs1)
        display_output(cmd)



#########################containers with GRE Connection#########################

def gre_connection(name_cs1, name_cs2):
	
	print name_cs1, name_cs2, " connected by GRE"

        #contanier creation
        container_create(name_cs1)
        container_create(name_cs2)

	#bridge creation
	br_cs1 = bridge_create(name_cs1)
	br_cs2 =bridge_create(name_cs2)
	
	#veth craetion and addition to containers
	veth_create_container_bridge(name_cs1, br_cs1, "100.0.0.1/24")
	veth_create_container_bridge(name_cs2, br_cs2, "101.0.0.1/24")

	#veth addition between leaf containers & bridges
	veth_create_container_bridge("lc1", br_cs1, "100.0.0.2/24")
	veth_create_container_bridge("lc2", br_cs2, "101.0.0.2/24")

	#default route addition in con1
	os.system("docker exec -it --privileged "+name_cs1+" ip route add 101.0.0.0/24 via 100.0.0.2")
	
	#default route addition in con2
	os.system("docker exec -it --privileged "+name_cs2+" ip route add 100.0.0.0/24 via 101.0.0.2")
	
	#gre creation and route addition in lc1
	os.system("sudo docker exec -it --privileged lc1 ip tunnel add gretun-"+name_cs1+" mode gre local 25.0.0.2 remote 27.0.0.2")
	os.system("sudo docker exec -it --privileged lc1 ip link set dev gretun-"+name_cs1+" up")
	os.system ("sudo docker exec -it --privileged lc1 ip route add 101.0.0.0/24 dev gretun-"+name_cs1)
	
	#gre interface and route addition in lc2
	os.system("sudo docker exec -it --privileged lc2 ip tunnel add gretun-"+name_cs2+" mode gre local 27.0.0.2 remote 25.0.0.2")
	os.system("sudo docker exec -it --privileged lc2 ip link set dev gretun-"+name_cs2+" up")
	os.system ("sudo docker exec -it --privileged lc2 ip route add 100.0.0.0/24 dev gretun-"+name_cs2)

	cmd = "sudo docker exec --privileged %s ping -i 1 -c 5 101.0.0.1" % (name_cs1)
        display_output(cmd)


#################################### containers with l3 connection ##########################




def l3_connection(name_cs1, name_cs2):
	
	print name_cs1, name_cs2, " connected by L3"

        #contanier creation
        container_create(name_cs1)
        container_create(name_cs2)

        #bridge creation
        br_cs1 = bridge_create(name_cs1)
        br_cs2 =bridge_create(name_cs2)

        #veth craetion and addition to containers
        veth_create_container_bridge(name_cs1, br_cs1, "110.0.0.1/24")
        veth_create_container_bridge(name_cs2, br_cs2, "111.0.0.1/24")

        #veth addition between leaf containers & bridges
        veth_create_container_bridge("lc1", br_cs1, "110.0.0.2/24")
        veth_create_container_bridge("lc2", br_cs2, "111.0.0.2/24")

	#default route addition in con1
        os.system("sudo docker exec -it --privileged "+name_cs1+" ip route add 111.0.0.0/24 via 110.0.0.2")

        #default route addition in con2
        os.system("sudo docker exec -it --privileged "+name_cs2+" ip route add 110.0.0.0/24 via 111.0.0.2")


	#route addition in lc1 &cs2 &lc2
	os.system("sudo docker exec -it --privileged lc1 ip route add 111.0.0.0/24 via 26.0.0.1")
	os.system("sudo docker exec -it --privileged sc2 ip route add 111.0.0.0/24 via 28.0.0.2")
	
	os.system("sudo docker exec -it --privileged lc2 ip route add 110.0.0.0/24 via 28.0.0.1")
	os.system("sudo docker exec -it --privileged sc2 ip route add 110.0.0.0/24 via 26.0.0.2")

	cmd = "sudo docker exec --privileged %s ping -i 1 -c 5 111.0.0.1" % (name_cs1)
        display_output(cmd)


	


###################################### main file ###################

file_name = input("Enter the input file path:")
#print str(file_name)
input_file =open(str(file_name),'r')

for line in input_file:
        name_cs1,name_cs2,net_device = line.strip('\n').split(',')

        if net_device == "Bridge":
                bridge_connection(name_cs1, name_cs2)
                
        elif net_device == "VXLAN":
                vxlan_connection(name_cs1, name_cs2)

        elif net_device == "GRE":
                gre_connection(name_cs1, name_cs2)

        else:
                l3_connection(name_cs1, name_cs2)


