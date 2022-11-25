from int_dict import IntDict
from time_it import timeit

idict = IntDict()


@timeit('')
def extend():
    global idict
    total_cnt = 1 * 10 ** 1

    import random
    r_list = random.sample(range(1, total_cnt + 1), total_cnt)
    r_list = {i: i * 10 for i in r_list}

    # Filling
    idict.extend(r_list)

    idict[99] = 990

    # idict._sort()


extend()
# print(idict)
print('len:', len(idict))

# Search
for s in [3, 30]:
    v = idict.get(s)
    print(f'idict: search for k={s}: index={v}')


@timeit('')
def save_load():
    # Saving and loading
    f_name = 'aaa.bin'
    idict.to_file(f_name)
    idict.clear()
    idict.from_file(f_name)


save_load()
# print(idict)

# Time tests
test_ses = 100


@timeit('')
def search():
    for i in range(test_ses):
        idict.get(300)


search()


def mem():
    # Size in memory
    from pympler import asizeof
    print('size in memory: ', asizeof.asizeof(idict))


mem()
