#!/bin/bash

sudo apt-get install snmpd snmp snmp-mibs-downloader -y
sudo download-mibs


sudo cp /etc/snmp/snmpd.conf /etc/snmp/snmpd.conf.ori
sudo vim /etc/snmp/snmpd.conf

change 127.0.0.1 to 0.0.0.0
change public to hplan

