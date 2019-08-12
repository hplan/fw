#!/bin/bash


export mailTo="hz_gxv33xx@grandstream.cn"
#export mailTo="hplan@grandstream.cn"
export title="GXV3350 Auto Build version 1.0.0.1 user done"
sendemail -f hz_no_reply@grandstream.cn -t ${mailTo} -s smtp.grandstream.cn -o tls=no message-charset=utf-8 -xu hz_no_reply@grandstream.cn -xp S1pTestH2 -v -u "${title}" < ./message.txt
