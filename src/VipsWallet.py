import Client
from Defines import STANDARD_RETURN, WALLET_LOCK_STATE
import Logger


class VipsWallet:
    def __init__(self):
        self.rpc = Client.RpcClient(ip='127.0.0.1')

    def connect_test(self):
        ret = STANDARD_RETURN.NOT_OK
        try:
            result = self.rpc.getinfo()
            ret = self.__check_error('VipsWallet-connect_test', result)
        except ConnectionError as e:
            Logger.Logging('VipsWallet-connect_test : ' + str(e))
        
        return ret

    def get_lock_status(self):
        ret = STANDARD_RETURN.OK
        lock_state = WALLET_LOCK_STATE.UNLOCK

        try:
            result = self.rpc.dumpprivkey('VBoonburnwwwwwwwwwwwwwwwwwwwsL3j5g')
            # If wallet locked, occur error code -13
            if result['code'] == -13:
                if 'staking only' in result['message']:
                    lock_state = WALLET_LOCK_STATE.STAKING_ONLY
                else:
                    lock_state = WALLET_LOCK_STATE.LOCK
            elif result['code'] == -4:
                pass
            else:
                ret = self.__check_error('VipsWalle t-get_locl_status', result)
        except ConnectionError as e:
            Logger.Logging('VipsWallet-get_lock_status : ' + str(e))
            ret = STANDARD_RETURN.NOT_OK

        return ret, lock_state

    def unlock(self, password):
        ret = STANDARD_RETURN.NOT_OK

        try:
            result = self.rpc.walletpassphrase(password, 9999999999, False)
            ret = self.__check_error('VipsWallet-unlock', result)
        except ConnectionError as e:
            Logger.Logging('VipsWallet-unlock : ' + str(e))
            ret = STANDARD_RETURN.FATAL_ERROR

        return ret

    def lock(self, lock_status, password):
        ret = STANDARD_RETURN.OK
        if lock_status != WALLET_LOCK_STATE.UNLOCK:
            try:
                result = self.rpc.walletlock()
                ret = self.__check_error('VipsWallet-lock', result)
                if ret == STANDARD_RETURN.OK and lock_status == WALLET_LOCK_STATE.STAKING_ONLY:
                    result = self.rpc.walletpassphrase(password, 9999999999, True)
                    ret = self.__check_error('VipsWallet-lock', result)
            except ConnectionError as e:
                Logger.Logging('VipsWallet-lock : ' + str(e))
                ret = STANDARD_RETURN.NOT_OK

        return ret

    def send(self, send_info):
        ret = self.__check_addresses(send_info.keys())

        if ret == STANDARD_RETURN.OK:
            ret, balance = self.__get_balance()

            if ret == STANDARD_RETURN.OK:
                total_amount = 0
                for amount in send_info.values():
                    total_amount += int(amount)
                if int(balance) < total_amount:
                    Logger.Logging('VipsWallet-send : ' + 'Total amount is over balance.')
                    ret = STANDARD_RETURN.NOT_OK

            if ret == STANDARD_RETURN.OK:
                try:
                    for address, amount in send_info.items():
                        result = self.rpc.sendtoaddress(address, amount)
                        ret = self.__check_error('VipsWallet-send', result)
                        if ret == STANDARD_RETURN.NOT_OK:
                            break
                except ConnectionError as e:
                    Logger.Logging('VipsWallet-send : ' + str(e))
                    ret = STANDARD_RETURN.NOT_OK

        return ret

    def __check_addresses(self, addresses):
        ret = STANDARD_RETURN.OK
    
        try:
            for address in addresses:
                result = self.rpc.validateaddress(address)
                if result['isvalid'] == False:
                    Logger.Logging('VipsWallet-check_address : Invalid address : {0}'.format(address))
                    ret = STANDARD_RETURN.NOT_OK
        except ConnectionError as e:
            Logger.Logging('VipsWallet-check_address : ' + str(e))
            ret = STANDARD_RETURN.NOT_OK

        return ret

    def __get_balance(self):
        try:
            result = self.rpc.getbalance()
            ret = self.__check_error('VipsWallet-get_balance', result)
        except ConnectionError as e:
            Logger.Logging('VipsWallet-get_balance : ' + str(e))

        return ret, result

    def __check_error(self, check_id, result):
        ret = STANDARD_RETURN.OK

        # If occurred error, result contain key 'code'
        if isinstance(result, dict):
            if 'code' in result:
                Logger.Logging('{0} : {1} : {2}'.format(check_id, str(result['code']), result['message']))
                ret = STANDARD_RETURN.NOT_OK

        return ret
