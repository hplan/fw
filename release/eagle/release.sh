#!/bin/bash
export MAILADDR=hz_no_reply@grandstream.cn
export MAILPWD=S1pTestH2
export ISENG=1
export ISCLEAN=0
export VERSION="0.0.0.0"
export BUILD_KERNEL=0
#MAIL_LIST="hplan@grandstream.cn"
MAIL_LIST="hz_gxv33xx@grandstream.cn"
PROJ_TOP=/home/hplan/project/eagle
DEBUG=0

printHelp() {
    echo "
    release tool for GXV3350

    # -h: print this help document
    # -r: specify email addressee. default: hz_gxv33xx@grandstream.cn
    # -b: build kernel
    # -s: user build.  default: eng
    # -c: clean build. default: not clean
    # -v: set version
    "
}

while getopts "v:r:cshb" arg
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

        s)
           export ISENG=0
           ;;

        c)
           export ISCLEAN=1
           ;;

        b)
           export BUILD_KERNEL=1
           ;;

        ?)
           echo "unknown argument $OPTARG"
           exit 1
           ;;
    esac
done

if [ "$DEBUG" == "1" ]; then
   echo "under test, break;"
   exit 0
fi

# setup env
cd /home/hplan/genLog/bin/env && source env.sh
cd /home/hplan/genLog/bin/env && source openjdk-8-env 

# start build
cd ${PROJ_TOP}/android && source ./build/envsetup.sh
if [ "$ISENG" == "1" ];then
    lunch full_eagle-eng
else
    lunch full_eagle-user
fi

if [ ${BUILD_KERNEL} == 1 ]; then
    # build kernel
    cd ${PROJ_TOP}/kernel-3.18 && ./buildkernel.sh -b
fi

# build android
if [ "$ISENG" == "1" ]; then
    # -c: clean build
    # -g: specify target product
    # -r: specify email addressee
    #
    # eng build
    #
    if [ ${ISCLEAN} == 1 ]; then
        cd ${PROJ_TOP}/android/vendor/grandstream/build && ./autoBuild.sh -c -g eagle -r ${MAIL_LIST}
    else
	cd ${PROJ_TOP}/android/vendor/grandstream/build && ./autoBuild.sh -g eagle -r ${MAIL_LIST}
    fi
else
    # -c: clean build
    # -g: specify target product
    # -r: specify email addressee
    # -s: user build
    # -p: upload avs & gs_phone symbols
    # -d: copy to dailybuild
    #
    # user build
    #
    if [ ${ISCLEAN} == 1 ]; then
        cd ${PROJ_TOP}/android/vendor/grandstream/build && ./autoBuild.sh -c -g eagle -r ${MAIL_LIST} -s -v ${VERSION} 
    else
        cd ${PROJ_TOP}/android/vendor/grandstream/build && ./autoBuild.sh -g eagle -r ${MAIL_LIST} -s -v ${VERSION} 
    fi
fi
