#!/bin/bash
source /etc/profile
export ENG=true
export DEBUG=false
export BUILD_KERNEL=false
export REPO_SYNC_CODE=false
export TARGET_BRANCH="Alpaca"
export CURRENT_BRANCH="git symbolic-ref --short HEAD"
export MAIL_TO="hz_gxv33xx@grandstream.cn"
export MAIL_TO_DEBUG="hplan@grandstream.cn"
export MAIL_TITLE="GXV3380 OEM D33 git log"
export SH_PATH="$(cd "$(dirname "$0")";pwd)"
export PROJ_PATH="/home/hplan/project/dailybuild/alpaca7"
export BUILD_CMD="./autoBuild.sh"
export version="54."`date -d"today" +%y.%m.%d`
export LOG_FILE="/home/hplan/BuildLog/d33/`whoami`_d33_54_"`date -d"today" +%y_%m_%d`"_build_Log"

Log_Raw="/tmp/logRaw_D33.html"
Log_Pretty="/tmp/logPretty_D33.html"

print_help() {
echo "
    dailybuild tool for GXV3380 OEM D33

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
    cd ${PROJ_PATH}/cht && git reset --hard `git remote`/`${CURRENT_BRANCH}` && git checkout D33 && git reset --hard `git remote`/D33 && git pull `git remote` D33
    repo forall -p -c  git log  --graph  --name-status --since="24 hours ago" --pretty=format:"<span style='color:#00cc33'>%ci</span>  <span style='color:yellow'>%an %ae</span>%n<span style='color:#00cc33'>Log:</span>      <span style='color:yellow'> %B</span>%nFiles List:"  > ${Log_Raw}
}

mail() {
    if [[ $(stat -c %s ${Log_Raw}) -eq 0 ]]; then
        echo "There is no new commit, nothing to do"  | tee ${LOG_FILE}
        return 1
    else
        echo "<html><body  style='background-color:#151515; font-size: 14pt; color: white'><div style='background-color:#151515;color: white'>" > ${Log_Pretty}
        sed -e 's/$/<br>/g' ${Log_Raw} >> ${Log_Pretty}
        echo "</div></body></html>" >> ${Log_Pretty}
        if ! ${DEBUG}; then
            sendemail -f hz_no_reply@grandstream.cn -t $1 -s smtp.grandstream.cn -o tls=no message-charset=utf-8 -xu hz_no_reply@grandstream.cn -xp S1pTestH2 -v -u "GXV3380 OEM D33 git log" < ${Log_Pretty}
        fi
        return 0
    fi
}

build() {
    source ${SH_PATH}/../env.sh
    source ${SH_PATH}/../openjdk-8-env

    cd ${PROJ_PATH}/android && source ${PROJ_PATH}/android/build/envsetup.sh
    if ${ENG}; then
        cd ${PROJ_PATH}/android && lunch cht_alpaca-eng
    else
        cd ${PROJ_PATH}/android && lunch cht_alpaca-user
    fi

    if ${BUILD_KERNEL}; then
        cd ${PROJ_PATH}/cht && git reset --hard `git remote`/`${CURRENT_BRANCH}` && git checkout D33 && git reset --hard `git remote`/D33 && git pull `git remote` D33
        cd ${PROJ_PATH}/android && extract-bsp
        cd ${PROJ_PATH}/cht && ./build.sh -c

        #if [[ ! -e ${PROJ_PATH}/android/out/target/product/cht_alpaca/boot.img ]]; then
        #    ## regenerate boot.img
        #    cd ${PROJ_PATH}/android && make bootimage -j16
        #    cd ${PROJ_PATH}/cht && ./build.sh -c
        #fi
        ## check again
        #if [[ ! -e ${PROJ_PATH}/android/out/target/product/cht_alpaca/boot.img ]]; then
        #    sendemail -f hz_no_reply@grandstream.cn -t $1 -s smtp.grandstream.cn -o tls=no message-charset=utf-8 -xu hz_no_reply@grandstream.cn -xp S1pTestH2 -v -u "GXV3380 eng build kernel failed."
        #    exit 1
        #fi
    fi

    cd ${PROJ_PATH}/android/vendor/grandstream/build && ${BUILD_CMD} -r ${MAIL_TO} -m 54 -v ${version}
}

entrance() {
    if ${REPO_SYNC_CODE}; then
        repo_sync
        mail ${MAIL_TO}
    fi
    if [[ $? -eq 0 ]]; then
        build
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
           export version=${OPTARG}
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

entrance
