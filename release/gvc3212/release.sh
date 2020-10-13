#!/bin/bash
DEBUG=false
export ENG=true
export VERSION="0.0.0.0"
export BUILD_KERNEL=false
export MAIL_TO_DEBUG="hplan@grandstream.cn"
export MAIL_TO="hz_gvc3212@grandstream.cn"
export SH_PATH="$(cd "$(dirname "$0")";pwd)"
PROJ_TOP=/media/gshz/4T_Disk/gvc3212
export BUILD_CMD="./autoBuild.sh"

print_help() {
echo "
    release tool for GVC3212

    # -h: print this help document
    # -r: specify email addressee. default: hz_gvc3212@grandstream.cn
    # -s: build as secure boot. default: false
    # -c: clean build. default: not clean
    # -p: hw_c03 / hw_gvc3212. default: hw_gvc3212s
    # -v: set version
"
}

while getopts "v:r:p:csh" arg
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
           export BUILD_CMD="${BUILD_CMD} -s"
           ;;

        c)
           export BUILD_CMD="${BUILD_CMD} -c"
           ;;

        b)
           export BUILD_KERNEL=true
           ;;

        p)
           if [[ ${OPTARG} == "hw_c03" ]]; then
               export BUILD_CMD="${BUILD_CMD} -k v1.1A"
           fi
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
    source ${SH_PATH}/../env_java6.sh
    source ${PROJ_TOP}/jdks/env.sh

    cd ${PROJ_TOP}/android/vendor/grandstream/build && ${BUILD_CMD} -r ${MAIL_TO} -p "gvc3212"
}

build
