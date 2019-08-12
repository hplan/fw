#!/bin/bash
DEBUG=false
export ENG=true
export VERSION="0.0.0.0"
export BUILD_KERNEL=false
export MAIL_TO_DEBUG="hplan@grandstream.cn"
export MAIL_TO="hz_gxv33xx@grandstream.cn"
export SH_PATH="$(cd "$(dirname "$0")";pwd)"
PROJ_TOP=/home/hplan/project/alpaca7
export BUILD_CMD="./autoBuild.sh"

print_help() {
echo "
    release tool for GXV3380

    # -h: print this help document
    # -r: specify email addressee. default: hz_gxv33xx@grandstream.cn
    # -b: build kernel
    # -s: user build.  default: eng
    # -c: clean build. default: not clean
    # -v: set version
"
}

while getopts "v:r:csbh" arg
do
    case ${arg} in
        h)
           print_help
           exit 0
           ;;

        v)
           export BUILD_CMD="${BUILD_CMD} -v ${OPTARG}"
           ;;

        r)
           if ${DEBUG}; then
               export MAIL_TO=${MAIL_TO_DEBUG}
           else
               export MAIL_TO=${OPTARG}
           fi
           ;;

        s)
           export ENG=false
           export BUILD_CMD="${BUILD_CMD} -s"
           ;;

        c)
           export BUILD_CMD="${BUILD_CMD} -c"
           ;;

        b)
           export BUILD_KERNEL=true
           ;;

        ?)
           echo "unknown argument ${OPTARG}"
           exit 1
           ;;
    esac
done

if ${DEBUG}; then
   echo "under test, break;"
   exit 0
fi

build() {
    source ${SH_PATH}/../../env.sh
    source ${SH_PATH}/../../openjdk-8-env
    cd ${PROJ_TOP}/android && source ${PROJ_TOP}/android/build/envsetup.sh
    if ${ENG}; then
        cd ${PROJ_TOP}/android && lunch cht_alpaca-eng
    else
        cd ${PROJ_TOP}/android && lunch cht_alpaca-user
    fi

    if ${BUILD_KERNEL}; then
        cd ${PROJ_TOP}/cht && ./build.sh -c
    fi

    cd ${PROJ_TOP}/android/vendor/grandstream/build && ${PROJ_TOP} -r ${MAIL_TO}
}

build