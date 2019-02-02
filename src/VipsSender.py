import json
import sys
from Vips import Vips

args = sys.argv
send_info_str = args[1]

send_info = json.loads(send_info_str)

vips = Vips()
vips.send(send_info)
