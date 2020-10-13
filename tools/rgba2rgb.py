#!/usr/bin/env python

from PIL import Image

if __name__ == '__main__':
    img = Image.open('/home/hplan/project/alpaca7/android/hardware/intel/kernelflinger/libkernelflinger/res/images/oem_82.png')
    print(img.mode)
    img = img.convert('RGB')
    img.save('/home/hplan/project/alpaca7/android/hardware/intel/kernelflinger/libkernelflinger/res/images/oem_82_2.png')
    print(img.mode)
