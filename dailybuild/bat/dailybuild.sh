#!/bin/bash
source /etc/profile
export ENG=true
export DEBUG=true
export BUILD_KERNEL=false
export BRANCH="Bat"
export MAIL_TO="hz_gxv33xx@grandstream.cn"
export MAIL_TO_DEBUG="hplan@grandstream.cn"
export MAIL_TITLE="GXV3370 git log"
export SH_PATH="$(cd "$(dirname "$0")";pwd)"
export PROJ_PATH="/media/gshz/newdisk/ahluo/Bat/"
export BUILD_CMD="./autoBuild.sh"

Log_Raw="/tmp/logRaw_Bat.html"
Log_Pretty="/tmp/logPretty_Bat.html"

print_help() {
echo "
    dailybuild tool for GXV3370

    # -h: print this help document
    # -r: specify email addressee. default: hz_gxv33xx@grandstream.cn
    # -s: user build.  default: eng
    # -c: clean build. default: not clean
    # -b: build kernel
    # -v: set version
"
}

repo_sync() {
    source ${SH_PATH}/../../env.sh
    # clear previous log
    cat /dev/null > ${Log_Raw}
    cat /dev/null > ${Log_Pretty}

    cd ${PROJ_PATH}
    repo forall -c "git reset && git checkout . && git checkout ${BRANCH}"
    repo sync

    repo forall -c "git pull `git remote` ${BRANCH} && git rebase m/master"
    repo forall -p -c  git log  --graph  --name-status --since="24 hours ago" --pretty=format:"<span style='color:#00cc33'>%ci</span>  <span style='color:yellow'>%an %ae</span>%n<span style='color:#00cc33'>Log:</span>      <span style='color:yellow'> %B</span>%nFiles List:"  > ${Log_Raw}
}

repo_sync_debug() {
    echo "source ${SH_PATH}/../../env.sh"
    echo "cat /dev/null > ${Log_Raw}"
    echo "cat /dev/null > ${Log_Pretty}"

    echo "cd ${PROJ_PATH}"
    echo "repo forall -c \"git reset && git checkout . && git checkout ${BRANCH}\""
    echo "repo sync"

    echo "repo forall -c \"git pull `git remote` ${BRANCH} && git rebase m/master\""
    echo "repo forall -p -c \"git log  --graph  --name-status --since=\"24 hours ago\" \
--pretty=format:\"<span style='color:#00cc33'>%ci</span> \
 <span style='color:yellow'>%an %ae</span>%n<span style='color:#00cc33'>Log:</span> \
     <span style='color:yellow'> %B</span>%nFiles List:\"  > ${Log_Raw}"
}

mail() {
    if [[ $(stat -c %s ${Log_Raw}) -eq 0 ]]; then
        echo "There is no commit, nothing to do"
        return 1
    else
        echo "\"<html><body  style='background-color:#151515; font-size: 14pt; color: white'><div style='background-color:#151515;color: white'>\" > ${Log_Pretty}"
        echo "sed -e 's/$/<br>/g' ${Log_Raw} >> ${Log_Pretty}"
        echo "</div></body></html>" >> ${Log_Pretty}
        sendemail -f hz_no_reply@grandstream.cn -t $1 -s smtp.grandstream.cn -o tls=no message-charset=utf-8 -xu hz_no_reply@grandstream.cn -xp S1pTestH2 -v -u "${MAIL_TITLE}" < ${Log_Pretty}
        return 0
    fi
}

build() {
    cd ${PROJ_PATH}/android && source ${PROJ_PATH}/android/build/envsetup.sh
    if ${ENG}; then
        lunch full_bat-eng
    else
        lunch full_bat-user
    fi

    if ${BUILD_KERNEL}; then
        cd ${PROJ_PATH}/kernel-3.18 && make clean && make distclean && ./buildkernel.sh -b
    fi

    cd ${PROJ_PATH}/android/vendor/grandstream/build && ${BUILD_CMD} -d -r ${MAIL_TO}
}

build_debug() {
    echo "cd ${PROJ_PATH}/android && source ${PROJ_PATH}/android/build/envsetup.sh"
    if ${ENG}; then
        echo "lunch full_bat-eng"
    else
        echo "lunch full_bat-user"
    fi

    if ${BUILD_KERNEL}; then
        echo "cd ${PROJ_PATH}/kernel-3.18 && make clean && make distclean && ./buildkernel.sh -b"
    fi

    echo "cd ${PROJ_PATH}/android/vendor/grandstream/build && ${BUILD_CMD} -d -r ${MAIL_TO}"
}

entrance() {
    if ${DEBUG}; then
        repo_sync_debug
    else
        repo_sync
    fi

    mail ${MAIL_TO}
    if [[ $? -eq 0 ]]; then
        if ${DEBUG}; then
            build_debug
        else
            build
        fi
    fi
}

while getopts "v:r:csh" arg
do
    case ${arg} in
        h)
           print_help
           exit 0
           ;;

        v)
           export VERSION=${OPTARG}
           export BUILD_CMD="${BUILD_CMD} -v ${VERSION}"
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
           export BUILD_CMD="${BUILD_CMD} -s -p"
           ;;

        b)
           export BUILD_KERNEL=true
           ;;

        c)
           export BUILD_CMD="${BUILD_CMD} -c"
           ;;

        ?)
           echo "unknown argument $OPTARG"
           exit 1
           ;;
    esac
done

entrance
