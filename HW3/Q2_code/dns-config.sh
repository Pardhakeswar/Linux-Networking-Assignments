#!/bin/bash

interface_name=$1

ip_adress=$2
#echo $ip_adress
mod_ip=$(echo "$ip_adress" | cut -c-11)
echo interface = $interface_name >> /etc/dnsmasq.conf
echo dhcp-range =$interface_name, $mod_ip.2, $mod_ip.254 >> /etc/dnsmasq.conf
#echo dhcp-range = $interface_name, $mod_ip.2, $mod_ip.254 >> pacha
sudo systemctl restart dnsmasq
