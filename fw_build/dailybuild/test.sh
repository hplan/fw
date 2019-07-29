#!/bin/bash

#cmd=$(python ./dailybuild.py --kernel)
#echo ${cmd}
#`${cmd}`
#
#cmd=$(python ./dailybuild.py --kernel)
#`${cmd}`
export PROJECT_TOP=
export PROJECT_KERNEL_BUILD_CMD
export

function __help__() {
    echo "
    daily build tools

    # -h: print this help document
    # -r: specify email addressee. default: hz_gxv33xx@grandstream.cn
    # -s: user build.  default: eng
    # -c: clean build. default: not clean
    # -v: set version
    "
}

function __find_project_definition__() {
    echo "__find_project_definition__ ${1}"
}

function __build__() {
    echo "__build__"
}

while getopts "chg:" arg
do
    case ${arg} in
        h)
            __help__
            exit 0
            ;;
        g)
            __find_project_definition__ ${OPTARG}
            ;;
        c)
            echo "clean"
            ;;
        *)
        ;;
    esac
done

__build__
