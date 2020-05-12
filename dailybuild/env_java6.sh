#!/bin/bash

export SHELL=/bin/bash
export PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
export JAVA_HOME=/opt/jdk1.6.0_37/
export CLASSPATH=.:${JAVA_HOME}/lib:${CLASSPATH}
export PATH=${JAVA_HOME}/bin:${PATH}
echo $PATH
