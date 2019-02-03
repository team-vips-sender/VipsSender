import json
import sys
from Vips import Vips
import Logger


def __convert_send_info_to_dict(send_info_str):
    send_info = {}

    try:
        send_info = json.loads(send_info_str)
    except json.decoder.JSONDecodeError as e:
        Logger.Logging('VipsSender : Wrong argument format : {0}'.format(e))

    return send_info


if __name__ == '__main__':
    args = sys.argv
    
    if len(args) != 2:
        Logger.Logging('VipsSender : Wrong argument num : {0}'.format(len(args)))
    else:
        send_info = __convert_send_info_to_dict(args[1])
    
        if send_info:
            vips = Vips()
            vips.send(send_info)
