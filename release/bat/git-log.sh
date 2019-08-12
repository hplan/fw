#!/bin/bash

export VERSION="0.0.0.0"
export MAIL_TO="hz_gxv33xx@grandstream.cn"
export PROJ_TOP=/home/hplan/project/bat

Log_Raw="/tmp/logBatRaw.html"
Log_Pretty="/tmp/logBatPretty.html"

print_help() {
    echo "
    release tool for GXV3370
    
    # -h: print this help document
    # -r: specify email addressee. default: hz_gxv33xx@grandstream.cn
    # -t: previous tag name 
    # -v: set version
    "
}

while getopts "v:r:t:h" arg
do
    case ${arg} in
        h)
           print_help
           exit 0
           ;;

        v)
           export VERSION=$OPTARG
           ;;

        r)
           export MAIL_TO=$OPTARG
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

cat /dev/null > ${Log_Raw}
cat /dev/null > ${Log_Pretty}

cd ${PROJ_TOP} && repo forall -p -c git log --graph --name-status ...${TAG} --pretty=format:"<span style='color:#00cc33'>%ci</span>  <span style='color:yellow'>%an %ae</span>%n<span style='color:#00cc33'>Log:</span>      <span style='color:yellow'> %s </span>%nFiles List:"  > ${Log_Raw}

if [[ $(stat -c %s ${Log_Raw}) -eq 0 ]]; then
        echo "There is no commit, nothing to do."
else
        echo "<html> <body  style='background-color:#151515; font-size: 14pt; color: white'><div style='background-color:#151515; color: white'>" > ${Log_Pretty}
        sed -e 's/$/<br>/g' ${Log_Raw} >> ${Log_Pretty}
        echo "</div></body></html>" >> ${Log_Pretty}

        sendemail -f hz_no_reply@grandstream.cn -t ${MAIL_TO} -s smtp.grandstream.cn -o tls=no message-charset=utf-8 -xu hz_no_reply@grandstream.cn -xp S1pTestH2 -v -u "GXV3370 ${VERSION} git log" < ${Log_Pretty}
fi
