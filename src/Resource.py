import sys
import os

def resource_path(filename):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(filename)

def get_vips_icon_path():
    return resource_path('resources/vipstarcoin.ico')
