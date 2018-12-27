#!/usr/bin/python

#https://libvirt.org/docs/libvirt-appdev-guide-python/en-US/html/
#define imports
import sys
import time 
import libvirt
import operator

#Initialization 
virtual_machines=[]
initial_vcpu_time= []
final_vcpu_time= []
memory_stats =[]
cpu_usage = {}
memory_usage ={}
names_of_vm=[]
memory_usage2={}
mem_data_set =[]
cpu_data_set =[]
#establish connection with qemu
conn = libvirt.open('qemu:///system')

#get IDs of the VMs running 
vm_ids=conn.listDomainsID()

#access info from the user (threshold value, sort_type , sample_time for vcpu )
sort_type = raw_input("\nEnter value the sort type.\" CPU  or  MEM \" :  ")
if sort_type!="CPU" and sort_type!="MEM":
	print( "you have entered wrong input expected CPU OR MEM got {}",sort_type)
	exit(1)

sample_time = raw_input("\nEnter the sample time to calculate the cpu usage :")
sample_time =float(sample_time)
polling_time = raw_input("\nEnter the polling time  :")
window_size  = raw_input("\nEnter the window size  : ") 

#get objects of the VMs running
for id in vm_ids:
	virtual_machines.append(conn.lookupByID(id))

#exceptions for nil virtual machines

for g_iteration in range(window_size):
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

#sort the memory
	mem_data_set.append(list(memory_usage.values()))
	cpu_data_set.append(list(cpu_usage.values()))


# [i* 5 for i in my list ]

mem_data_set= [sum(x)/window_size for x in zip(*mem_data_set)]

print mem_data_set 

cpu_data_set= [sum(x)/window_size for x in zip(*cpu_data_set)]


print memory_usage 
for iterator in range(len(virtual_machines)):
	memory_usage[names_of_vm[iterator]]=mem_data_set[iterator]

print memory_usage

memory_usage = sorted (memory_usage.items(), key =lambda x:x[1])

cpu_usage    = sorted (cpu_usage.items(), key = lambda x:x[1])


#generate alert for if the file usage crosses certain point


if sort_type == "MEM":
        print ("List of VM sorted by Memory usage")
        print ("NAME of VM:  MEMORY USAGE")
        for iterator in range(len(memory_usage)):
                print  memory_usage[iterator]
	for iterator in range (len(memory_usage)):
		print memory_usage2[iterator]

if sort_type == "CPU":
	print ("List of VM sorted by CPU usage")
        print ("NAME of VM :  CPU USAGE")
        for iterator in range(len(cpu_usage)):
                print  cpu_usage[iterator]


conn.close()

   
