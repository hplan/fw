#!/bin/bash

export VERSION="0.0.0.0"
MAIL_LIST="hz_gxv33xx@grandstream.cn"
PROJ_TOP=/home/hplan/project/eagle
DEBUG=0

printHelp() {
    echo "
    release tool for GXV3350
    
    # -h: print this help document
    # -r: specify email addressee. default: hz_gxv33xx@grandstream.cn
    # -t: previous tag name 
    # -v: set version
    "
}

while getopts "v:r:t:h" arg
do
    case $arg in
        h)
           printHelp
           exit 0
           ;;

        v)
           export VERSION=$OPTARG
           ;;

        r)
           export MAIL_LIST=$OPTARG
           ;;

        t)
           export TAG=$OPTARG
           ;;

        ?)
           echo "unknown argument $OPTARG"
           exit 1
           ;;
    esac
done

cat /dev/null > /tmp/logBat.html && cat /dev/null > /tmp/logBat2.html

cd $PROJ_TOP 

repo forall -p -c git log --graph --name-status ...${TAG} --pretty=format:"<span style='color:#00cc33'>%ci</span>  <span style='color:yellow'>%an %ae</span>%n<span style='color:#00cc33'>Log:</span>      <span style='color:yellow'> %s </span>%nFiles List:"  > /tmp/logBat.html

if [ $(stat -c %s /tmp/logBat.html ) -eq 0 ]; then
        echo "Empty file"
else
        echo "<html> <body  style='background-color:#151515; font-size: 14pt; color: white'><div style='background-color:#151515; color: white'>" > /tmp/logBat2.html
        sed -e 's/$/<br>/g'  /tmp/logBat.html >> /tmp/logBat2.html
        echo "</div></body></html>" >> /tmp/logBat2.html

        sendemail -f hz_no_reply@grandstream.cn -t $MAIL_LIST -s smtp.grandstream.cn -o tls=no message-charset=utf-8 -xu hz_no_reply@grandstream.cn -xp S1pTestH2 -v -u "GXV3350 ${VERSION} git log" < /tmp/logBat2.html
fi
