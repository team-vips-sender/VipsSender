import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..\src'))
import Logger
from Amount import Amount

try:
    a = Amount()
    result = a.input()

    print('実行結果：',end='')
    print(result[0])
    print('金額：',end='')
    print(result[1])

except Exception as e:
    tb = sys.exc_info()[2]
    Logger.Logging("message:{0}".format(e.with_traceback(tb)))

