import json
import sys
from Vips import Vips
import Logger
import Message
from Defines import STANDARD_RETURN


def __convert_send_info_to_dict(send_info_str):
    send_info = {}

    try:
        send_info = json.loads(send_info_str)
    except json.decoder.JSONDecodeError as e:
        Logger.Logging('VipsSender : Wrong argument format : {0}'.format(send_info_str))

    return send_info


if __name__ == '__main__':
    args = sys.argv
    ret = STANDARD_RETURN.NOT_OK
    
    if len(args) < 2:
        Logger.Logging('VipsSender : Wrong argument num : {0}'.format(len(args)))
    else:
        arg_str = "".join(args[1:])
        send_info = __convert_send_info_to_dict("".join(arg_str.split()))
    
        if send_info:
            vips = Vips()
            vips.send(send_info)
            ret = STANDARD_RETURN.OK

    if ret != STANDARD_RETURN.OK:
        Message.display('[Error]\n送金に失敗しました。\nパラメータに異常があります。')

