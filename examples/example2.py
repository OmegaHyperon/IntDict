from int_dict import IntDict
import datetime
from pympler import asizeof

idict = IntDict()
d = dict()

total_cnt = 1000

# Filling
df = datetime.datetime.now()
for i in range(total_cnt):
    idict.append(i, i * 10)
print('idict filling time: ', (datetime.datetime.now() - df).total_seconds())
# print('idict=', idict)

df = datetime.datetime.now()
for i in range(total_cnt):
    d[i] = i
print('dict filling time ', (datetime.datetime.now() - df).total_seconds())

# Search
s = 30
v = idict.get(s)
print(f'search for k={s}, value={v}')

# Saving and loading
f_name = 'aaa.bin'
df = datetime.datetime.now()
idict.to_file(f_name)
print('saving time: ', (datetime.datetime.now() - df).total_seconds())
idict.clear()
df = datetime.datetime.now()
idict.from_file(f_name)
print('loading time: ', (datetime.datetime.now() - df).total_seconds())
# print('idict=', idict)

# Time tests
test_ses = 1000

df = datetime.datetime.now()
for i in range(test_ses):
    idict.get(3)
print('test time of idict: ', (datetime.datetime.now() - df).total_seconds())

df = datetime.datetime.now()
for i in range(test_ses):
    d.get(3)
print('test of dict: ', (datetime.datetime.now() - df).total_seconds())

# Size in memory
print('size in memory: ', asizeof.asizeof(idict), '/', asizeof.asizeof(d))
