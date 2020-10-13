#!/bin/bash
source /etc/profile
export ENG=true
export DEBUG=false
export REPO_SYNC_CODE=false
export CLEAN=false
export TARGET_BRANCH="C03_Master"
export CURRENT_BRANCH="git symbolic-ref --short HEAD"
export MAIL_TO="hz_gvc3212@grandstream.cn"
export MAIL_TO_DEBUG="hplan@grandstream.cn"
export MAIL_TITLE="GVC3212 git log"
export SH_PATH="$(cd "$(dirname "$0")";pwd)"
export PROJ_PATH="/media/gshz/4T_Disk/gvc3212"
export BUILD_CMD="./autoBuild.sh"
export LOG_FILE="/media/gshz/4T_Disk/hplan/BuildLog/gvc3212/`whoami`_gvc3212_10_"`date -d"today" +%y_%m_%d`"_build_Log"

Log_Raw="/tmp/logGVC3212Raw.html"
Log_Pretty="/tmp/logGVC3212Pretty.html"

print_help() {
echo "
    DailyBuild tool for GVC3212

    # -h: print this help document
    # -r: specify email addressee. default: hz_gvc3212@grandstream.cn
    # -s: build as secure boot. default: false
    # -c: clean build. default: not clean
    # -v: set version
    # -p: hw_c03 / hw_gvc3212. default: hw_gvc3212s
    # -u: update source code. default: not update
"
}

repo_sync() {
    source ${SH_PATH}/../env.sh
    # clear previous log
    cat /dev/null > ${Log_Raw}
    cat /dev/null > ${Log_Pretty}

    cd ${PROJ_PATH}

    while true
    do
        repo forall -c "git checkout . && git reset --hard \`git remote\`/\`${CURRENT_BRANCH}\` && git checkout ${TARGET_BRANCH} && git reset --hard m/master && git pull \`git remote\` ${TARGET_BRANCH}" | tee ${LOG_FILE}
        repo sync -c -j8 | tee ${LOG_FILE}

        if [[ $? -eq 0 ]]; then
            break
        fi
    done

    repo forall -c "git pull \`git remote\` ${TARGET_BRANCH} && git rebase m/master" | tee ${LOG_FILE}
    repo forall -p -c  git log  --graph  --name-status --since="24 hours ago" --pretty=format:"<span style='color:#00cc33'>%ci</span>  <span style='color:yellow'>%an %ae</span>%n<span style='color:#00cc33'>Log:</span>      <span style='color:yellow'> %B</span>%nFiles List:"  > ${Log_Raw}
}

mail() {
    if [[ $(stat -c %s ${Log_Raw}) -eq 0 ]]; then
        echo "There is no new commit, nothing to do" | tee ${LOG_FILE}
        return 1
    else
        echo "<html><body  style='background-color:#151515; font-size: 14pt; color: white'><div style='background-color:#151515;color: white'>" > ${Log_Pretty}
        sed -e 's/$/<br>/g' ${Log_Raw} >> ${Log_Pretty}
        echo "</div></body></html>" >> ${Log_Pretty}
        if ! ${DEBUG}; then
            sendemail -f hz_no_reply@grandstream.cn -t $1 -s smtp.grandstream.cn -o tls=no message-charset=utf-8 -xu hz_no_reply@grandstream.cn -xp S1pTestH2 -v -u ${MAIL_TITLE} < ${Log_Pretty}
        fi
        return 0
    fi
}

build() {
    source ${SH_PATH}/../env_java6.sh
    source ${PROJ_PATH}/jdks/env.sh

    source ${PROJ_PATH}/android/build/envsetup.sh
#    if ${ENG}; then
#        cd ${PROJ_PATH}/android && lunch gvc3212-eng
#    else
#        cd ${PROJ_PATH}/android && lunch gvc3212-user
#    fi
#
#    if ${CLEAN}; then
#        cd ${PROJ_PATH}/android && make clean
#    fi

    cd ${PROJ_PATH}/android/vendor/grandstream/build && ${BUILD_CMD} -r ${MAIL_TO} -p "gvc3212" | tee ${LOG_FILE}
}

entrance() {
    ## sync code
    if ${REPO_SYNC_CODE}; then
        repo_sync
        mail ${MAIL_TO}
    fi

    ## build code
    if [[ $? -eq 0 ]]; then
        build
    fi
}

while getopts "v:r:p:cshu" arg
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
           export CLEAN=true
           ;;

        u)
           export REPO_SYNC_CODE=true
           ;;

        p)
           if [[ ${OPTARG} == "hw_c03" ]]; then
               export BUILD_CMD="${BUILD_CMD} -k v1.1A"
           fi
           ;;

        ?)
           echo "unknown argument $OPTARG"
           exit 1
           ;;
    esac
done

if ${ENG}; then
    export LOG_FILE="${LOG_FILE}_eng"
else
    export LOG_FILE="${LOG_FILE}_usr"
fi

entrance
