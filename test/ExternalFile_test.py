import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..\src'))
import ExternalFile
from Defines import STANDARD_RETURN


# test function
def test_save(external_file, key, data):
    print('Save to external file(key={0}, data={1})'.format(key, data), end="")
    external_file.save(key, data)
    
    # read back test
    result, read_back_data = external_file.get(key)
    if result == STANDARD_RETURN.OK:
        if data == read_back_data:
            print('\t\tRead back test : OK')
        else:
            print('\t\tRead back test : NG  ⇒  Expect data : {0}, Read back data : {1}'.format(data, read_back_data))
    else:
        print('\t\tRead back test : NG  ⇒  Read back result is fail')

def test_get(external_file, key):
    print('Get by external file(key={0}) : '.format(key), end="")
    result, data = external_file.get(key)
    print('result={0}, data={1}'.format(result, data))


# ----------------------------------------------
external_file = ExternalFile.ExternalFile('ExternalFile_test.ini')
test_get(external_file, 'a')
test_save(external_file, 'a', 'abc')
test_save(external_file, 'b', '123')
test_save(external_file, 'c', '日本語')

external_file = ExternalFile.ExternalFile('ExternalFile_test.ini')
test_get(external_file, 'a')
test_save(external_file, 'a', 'def')
test_save(external_file, 'b', '456')

