import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..\src'))
import Vips


vips = Vips.Vips()

# test configuration
address1 = 'Vxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
address2 = 'Vyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy'

# test function
def __test_vips_send(send_info):
    print(str(send_info))
    print('Send vips ({0}) : '.format(str(send_info)), end="")
    print(vips.send(send_info))


# ----------------------------------------------
print('===== Normal sequence test =====')

__test_vips_send({address1: '10', address2: '1'})
__test_vips_send({address1: '0'})
__test_vips_send({address1: '0', address2: '1'})
__test_vips_send({address1: '0', address2: '0'})

