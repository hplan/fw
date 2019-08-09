#!/bin/bash

FILE=git-logs.txt


sed -i "/add daily/d" ${FILE}
sed -i "/update avs/d" ${FILE}

sed -i "/\[Bug/d" ${FILE}
sed -i "/Revert/d" ${FILE}

sed -i "/GVC/d" ${FILE}
sed -i "/gvc/d" ${FILE}

sed -i "/GSC/d" ${FILE}
sed -i "/gsc/d" ${FILE}
sed -i "/GAC/d" ${FILE}
sed -i "/gac/d" ${FILE}

sed -i "/WP/d" ${FILE}
sed -i "/wp820/d" ${FILE}

sed -i "/3350/d" ${FILE}
sed -i "/gxv3350/d" ${FILE}
sed -i "/GXV3350/d" ${FILE}


sed -i "/Update version/d" ${FILE}
sed -i "/nec/d" ${FILE}
sed -i "/NEC/d" ${FILE}
sed -i "/H60/d" ${FILE}
sed -i "/H51/d" ${FILE}
