#!/bin/bash
source /etc/profile
export ENG=true
export DEBUG=false
export BUILD_KERNEL=false
export REPO_SYNC_CODE=false
export TARGET_BRANCH="Bat"
export CURRENT_BRANCH="git symbolic-ref --short HEAD"
export MAIL_TO="hz_gxv33xx@grandstream.cn"
export MAIL_TO_DEBUG="hplan@grandstream.cn"
export MAIL_TITLE="GXV3350 git log"
export SH_PATH="$(cd "$(dirname "$0")";pwd)"
export PROJ_PATH="/home/hplan/project/eagle"
export BUILD_CMD="./autoBuild.sh"
export LOG_FILE="/home/hplan/BuildLog/eagle/`whoami`_eagle_20_"`date -d"today" +%y_%m_%d`"_build_Log"

Log_Raw="/tmp/logEagleRaw.html"
Log_Pretty="/tmp/logEaglePretty.html"

print_help() {
echo "
    dailybuild tool for GXV3350

    # -h: print this help document
    # -r: specify email addressee. default: hz_gxv33xx@grandstream.cn
    # -s: user build.  default: eng
    # -c: clean build. default: not clean
    # -b: build kernel
    # -v: set version
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
        repo sync -c -j16 | tee ${LOG_FILE}

        if [[ $? -eq 0 ]]; then
            break
        fi
    done

    repo forall -c "git pull \`git remote\` ${TARGET_BRANCH} && git rebase m/master" | tee ${LOG_FILE}
    repo forall -p -c  git log  --graph  --name-status --since="24 hours ago" --pretty=format:"<span style='color:#00cc33'>%ci</span>  <span style='color:yellow'>%an %ae</span>%n<span style='color:#00cc33'>Log:</span>      <span style='color:yellow'> %B</span>%nFiles List:"  > ${Log_Raw}
}

mail() {
    if [[ $(stat -c %s ${Log_Raw}) -eq 0 ]]; then
        echo "There is no commit, nothing to do"
        return 1
    else
        echo "<html><body  style='background-color:#151515; font-size: 14pt; color: white'><div style='background-color:#151515;color: white'>" > ${Log_Pretty}
        sed -e 's/$/<br>/g' ${Log_Raw} >> ${Log_Pretty}
        echo "</div></body></html>" >> ${Log_Pretty}
        if ! ${DEBUG}; then
            export version="20."`date -d"today" +%y.%m.%d`
#            sendemail -f hz_no_reply@grandstream.cn -t $1 -s smtp.grandstream.cn -o tls=no message-charset=utf-8 -xu hz_no_reply@grandstream.cn -xp S1pTestH2 -v -u "GXV3350 ${version} git log" < ${Log_Pretty}
            sendemail -f hz_no_reply@grandstream.cn -t $1 -s smtp.grandstream.cn -o tls=no message-charset=utf-8 -xu hz_no_reply@grandstream.cn -xp S1pTestH2 -v -u "GXV3350 git log" < ${Log_Pretty}
        fi
        return 0
    fi
}

build() {
    source ${SH_PATH}/../env.sh
    source ${SH_PATH}/../openjdk-8-env

    cd ${PROJ_PATH}/android && source ${PROJ_PATH}/android/build/envsetup.sh
    if ${ENG}; then
        cd ${PROJ_PATH}/android && lunch full_eagle-eng
    else
        cd ${PROJ_PATH}/android && lunch full_eagle-user
    fi

    if ${BUILD_KERNEL}; then
        cd ${PROJ_PATH}/kernel-3.18 && ./buildkernel.sh -b | tee ${LOG_FILE}
        # check if there is boot.img
        if [[ ! -e ${PROJ_PATH}/android/out/target/product/eagle/boot.img ]]; then
            ## regenerate boot.img
            cd ${PROJ_PATH}/android && make bootimage -j16
            cd ${PROJ_PATH}/kernel-3.18 && ./buildkernel.sh -b | tee ${LOG_FILE}
        fi
        # check again
        if [[ ! -e ${PROJ_PATH}/android/out/target/product/eagle/boot.img ]]; then
            sendemail -f hz_no_reply@grandstream.cn -t $1 -s smtp.grandstream.cn -o tls=no message-charset=utf-8 -xu hz_no_reply@grandstream.cn -xp S1pTestH2 -v -u "GXV3350 build kernel failed."
            exit 1
        fi
    fi

    cd ${PROJ_PATH}/android/vendor/grandstream/build && ${BUILD_CMD} -d -r ${MAIL_TO} -g eagle | tee ${LOG_FILE}
}

entrance() {
    ## sync code
    if ${REPO_SYNC_CODE}; then
        repo_sync
        mail ${MAIL_TO}
    fi

    ## build code
    if [[ $? -eq 0 ]]; then
        build ${MAIL_TO}
    fi
}

while getopts "v:r:csbuh" arg
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

        b)
           export BUILD_KERNEL=true
           ;;

        c)
           export BUILD_CMD="${BUILD_CMD} -c"
           ;;

        u)
           export REPO_SYNC_CODE=true
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
