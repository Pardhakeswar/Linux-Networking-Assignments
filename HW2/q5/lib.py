#!/usr/bin/python

#https://libvirt.org/docs/libvirt-appdev-guide-python/en-US/html/
#define imports
import sys
import time 
import libvirt
import operator
import movingavg

#Initialization 
virtual_machines=[]
initial_vcpu_time= []
final_vcpu_time= []
memory_stats =[]
cpu_usage = {}
memory_usage ={}
names_of_vm=[]

#establish connection with qemu
conn = libvirt.open('qemu:///system')

#get IDs of the VMs running 
vm_ids=conn.listDomainsID()

#access info from the user (threshold value, sort_type , sample_time for vcpu )
sort_type = raw_input("\nEnter value the sort type.\" CPU  or  MEM \" :  ")
if sort_type!="CPU" and sort_type!="MEM":
	print( "you have entered wrong input expected CPU OR MEM got {}",sort_type)
	exit(1)
thresh_value = raw_input("\nEnter the value for threshold CPU usage :")
thresh_value = float(thresh_value)
sample_time = raw_input("\nEnter the sample time to calculate the cpu usage :")
sample_time =float(sample_time)

#get objects of the VMs running
for id in vm_ids:
	virtual_machines.append(conn.lookupByID(id))

#exceptions for nil virtual machines


#Get V-CPU stats
for virtual_machine in virtual_machines:
	initial_vcpu_time.append(virtual_machine.getCPUStats(False)[0]['cpu_time'])

# introduce delay equal to smaple_time
time.sleep(sample_time)

for virtual_machine in virtual_machines:
	final_vcpu_time.append(virtual_machine.getCPUStats(False)[0]['cpu_time'])

for virtual_machine in virtual_machines:
	names_of_vm.append(virtual_machine.name()) 
#time stats 
timestamp = time.ctime(time.time())

#cpu usage = final -initial / sample_time
for iterator in range(len(virtual_machines)):
	cpu_usage[names_of_vm[iterator]]=float(final_vcpu_time[iterator]-initial_vcpu_time[iterator])/(sample_time*1000000000)

#get memory usage
for virtual_machine in virtual_machines:
	memory_stats.append(virtual_machine.memoryStats())

#print memory_stats[1]

for iterator in range(len(virtual_machines)):
 	 memory_usage[names_of_vm[iterator]]=float(memory_stats[iterator]['rss'])/float(memory_stats[iterator]['actual'])
#print cpu_usage

#sort the memory
memory_usage = sorted (memory_usage.items(), key =lambda x:x[1])
cpu_usage    = sorted (cpu_usage.items(), key = lambda x:x[1])

#generate alert for if the file usage crosses certain point
with open(  'alert.txt','a') as file:
	for items in cpu_usage:
		vm_name, vm_cpu_usage = items
#		print  vm_cpu_usage
		if vm_cpu_usage>thresh_value:
			file.write ("{0},{1},{2} \n".format(vm_name,timestamp,vm_cpu_usage))

if sort_type == "MEM":
        print ("List of VM sorted by Memory usage")
        print ("NAME of VM:  MEMORY USAGE")
        for iterator in range(len(memory_usage)):
                print  memory_usage[iterator]

if sort_type == "CPU":
	print ("List of VM sorted by CPU usage")
        print ("NAME of VM :  CPU USAGE")
        for iterator in range(len(cpu_usage)):
                print  cpu_usage[iterator]


conn.close()

