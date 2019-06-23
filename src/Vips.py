from Defines import STANDARD_RETURN, WALLET_LOCK_STATE
import Logger
import Message
from VipsWallet import VipsWallet
from Amount import Amount
from Confirm import Confirm
from Password import Password


class Vips:
    def __init__(self):
        self.vips_wallet = VipsWallet()
        self.confirm = Confirm()
        self.password = Password()
        self.amount = Amount()

    def send(self, send_info):
        ret = STANDARD_RETURN.NOT_OK
        result = self.__check_argment(send_info)
        error_message = '[Error]\n送金に失敗しました。'
        
        if result != STANDARD_RETURN.OK:
            Logger.Logging('Argument error : {0}'.format(send_info))
        
        else:
            result = self.vips_wallet.connect_test()
            if result == STANDARD_RETURN.OK:
                result = self.confirm.is_sending()
                if result == STANDARD_RETURN.OK:
                    result, send_info = self.__compensate_argument(send_info)
                    if result == STANDARD_RETURN.OK:
                        ret = self.__send_process(send_info)
            else:
                error_message += '\nウォレットが起動していないか、VIPSTARCOIN.confの設定が正しくない可能性があります。'
    
        if ret != STANDARD_RETURN.OK:
            Message.display(error_message)

        return ret
    
    def __send_process(self, send_info):
        ret = STANDARD_RETURN.NOT_OK
        password = ''
        
        result, wallet_lock_status = self.vips_wallet.get_lock_status()
        if result == STANDARD_RETURN.OK:
            if wallet_lock_status != WALLET_LOCK_STATE.UNLOCK:
                result, password = self.__wallet_unlock()
            if result == STANDARD_RETURN.OK:
                result = self.vips_wallet.send(send_info)

                lock_result = self.vips_wallet.lock(wallet_lock_status, password)
                if lock_result != STANDARD_RETURN.OK:
                    Message.display('[Warning]\nウォレットのロックが解除されました。\nロック状態を確認し、必要に応じてロックをかけてください。')

                if result == STANDARD_RETURN.OK:
                    ret = STANDARD_RETURN.OK
                    
        return ret
    
    def __wallet_unlock(self):
        ret = STANDARD_RETURN.NOT_OK
        result,password = self.password.get_password(False)
        if result == STANDARD_RETURN.NOT_OK:
            return ret, password
        result = self.vips_wallet.unlock(password)
        
        if result == STANDARD_RETURN.OK:
            ret = STANDARD_RETURN.OK
        elif result == STANDARD_RETURN.NOT_OK:
            while True:
                result,password = self.password.get_password(True)
                if result == STANDARD_RETURN.NOT_OK:
                    return ret, password
                result = self.vips_wallet.unlock(password)
                if result == STANDARD_RETURN.OK:
                    ret = STANDARD_RETURN.OK
                    break
                elif result == STANDARD_RETURN.FATAL_ERROR:
                    break
        else: # If result equals FATAL_ERROR
            pass
        
        return ret, password
    
    def __compensate_argument(self, send_info):
        ret = STANDARD_RETURN.OK
    
        addresses = self.__get_address_unspecified_amount(send_info)
        if addresses:
            result, amount = self.amount.input()
            
            if result == STANDARD_RETURN.NOT_OK:
                ret = STANDARD_RETURN.NOT_OK
            else:
                for address in addresses:
                    send_info[address] = amount
        
        return ret, send_info
    
    def __get_address_unspecified_amount(self, send_info):
        addresses = []
        for address, amount in send_info.items():
            if amount == '0':
                addresses.append(address)
        
        return addresses
    
    def __check_argment(self, send_info):
        # Todo: add check logic.
        return STANDARD_RETURN.OK
