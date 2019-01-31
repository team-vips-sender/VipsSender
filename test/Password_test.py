import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..\src'))
import Logger
from Password import Password

try:
    p = Password()
    print(p.get_password(True))
except Exception as e:
    tb = sys.exc_info()[2]
    Logger.Logging("message:{0}".format(e.with_traceback(tb)))

