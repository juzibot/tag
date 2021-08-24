import sys
import time

for i in range(10):
    print('\r{}'.format(i), end='')
    sys.stdout.flush()
    time.sleep(0.1)
# print()