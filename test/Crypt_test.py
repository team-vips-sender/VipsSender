import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..\src'))
import Logger
import Crypt

try:
    str = 'hogefuga'
    print('暗号化対象文字列：' + str)
    encrypt_result = Crypt.Encrypt(str)
    #encrypt_result[0]：暗号化した文字列
    #encrypt_result[1]：秘密鍵
    crypted_str = encrypt_result[0]
    key = encrypt_result[1]
    print('暗号化した文字列：',end='')
    print(crypted_str)
    decrypt_result = Crypt.Decrypt(crypted_str,key)
    print('復号した文字列：' + decrypt_result)
except Exception as e:
    tb = sys.exc_info()[2]
    Logger.Logging("message:{0}".format(e.with_traceback(tb)))
