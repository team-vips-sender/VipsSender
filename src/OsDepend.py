import os
import platform
import Logger
from Defines import STANDARD_RETURN

def get_user_path():
    ret = STANDARD_RETURN.OK
    path = ''

    os_name = platform.system()
    if os_name == 'Windows':
        path = os.path.expanduser('~/AppData/Roaming')
    elif os_name == 'MacOS':
        path = os.path.expanduser('~').format(_dir)
    else:
        Logger.Logging('get_vipstarcoin_path : Unknown OS ({0})'.format(os_name))
        ret = STANDARD_RETURN.NOT_OK

    return ret, path

