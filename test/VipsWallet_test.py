import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..\src'))
import VipsWallet


vw = VipsWallet.VipsWallet()

# test configuration
password = 'password'
address1 = 'Vxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
address2 = 'Vyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy'

# ----------------------------------------------
print('===== Normal sequence test =====')

print('Get current lock status : ', end="")
result, lock_state = vw.get_lock_status()
print('result={0} lock_state={1}'.format(result, lock_state))

print('Unlock wallet : ', end="")
print(vw.unlock(password))

print('Send to addresses : ', end="")
print(vw.send({address1: '10', address2: '10'}))

print('Back to original lock state : ', end="")
print(vw.lock(lock_state, password))

# ----------------------------------------------
print('===== Send too many amount =====')

print('Unlock wallet : ', end="")
print(vw.unlock(password))

print('Send to addresss : ', end="")
print(vw.send({address1: '10000000000'}))

print('Back to original lock state : ', end="")
print(vw.lock(lock_state, password))

# ----------------------------------------------
print('Unlock by wrong passphrase : ', end="")
print(vw.unlock(password + 'a'))

