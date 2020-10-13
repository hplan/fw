#!/bin/bash

sudo apt-get install snmpd snmp snmp-mibs-downloader -y
sudo download-mibs


sudo cp /etc/snmp/snmpd.conf /etc/snmp/snmpd.conf.ori
sudo vim /etc/snmp/snmpd.conf

#1
# Change
#   agentAddress  udp:127.0.0.1:161
# to
#   #agentAddress  udp:127.0.0.1:161
#
# Change
#   agentAddress udp:161,udp6:[::1]:161 
# to
#   agentAddress udp:161

#2
# Change
#   view   systemonly  included   .1.3.6.1.2.1.1
# to
#   #view   systemonly  included   .1.3.6.1.2.1.1
#
# Change
#   view   systemonly  included   .1.3.6.1.2.1.25.1
# to
#   #view   systemonly  included   .1.3.6.1.2.1.25.1
#
# Add
#   view   systemonly  included   .1

#3
# Change 
#   rocommunity public  default    -V systemonly
# to
#   rocommunity hplan   default    -V systemonly
#
# Change
#   rocommunity6 public  default   -V systemonly
# to
#   rocommunity6 hplan   default   -V systemonly

