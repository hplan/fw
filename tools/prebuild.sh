#! /bin/bash
sudo apt-get install libswitch-perl -y
sudo apt-get install git gnupg flex bison gperf build-essential -y
sudo apt-get install zip curl libc6-dev -y
sudo apt-get install libncurses5-dev:i386 x11proto-core-dev -y
sudo apt-get install libx11-dev:i386 libreadline6-dev:i386 -y
sudo apt-get install libgl1-mesa-glx:i386 libgl1-mesa-dev -y
sudo apt-get install g++-multilib mingw32 tofrodos python-markdown -y
sudo apt-get install libxml2-utils xsltproc zlib1g-dev:i386 -y
sudo ln -s /usr/lib/i386-linux-gnu/mesa/libGL.so.1 /usr/lib/i386-linux-gnu/libGL.so -y
sudo apt-get install flex -y
sudo apt-get install bison -y
sudo apt-get install libglib2.0-0:i386 libpng12-0:i386 libfontconfig1:i386 libsm6:i386 libxrender1:i386 -y
sudo apt-get install email mailutils -y

git config --global alias.path '!echo $user "\033[32m `git branch | grep "*"` \033[0m   `pwd`"'
git config --global alias.since '!sh -c "git log ...$1"'
git config --global user.email hplan@grandstream.cn
git config --global user.name hplan
git config --global core.editor vim
git config --global i18n.commitencoding utf-8
git config --global i18n.logoutputencoding utf-8

