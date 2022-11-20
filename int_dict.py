"""
    Dictionary with low memory consumption
    Type of data: only unsigned integer, 4 bytes
"""

import array
import bisect
from typing import Optional, Generator
import datetime


class IntDict(object):
    def __init__(self):
        self._len_f_header: int = 8
        self._k: array.array = array.array('L')
        self._v: array.array = array.array('L')

    def __str__(self):
        return str({self._k[i]: self._v[i] for i in range(len(self._k))})

    def __len__(self):
        return len(self._k)

    def __getitem__(self, i: int):
        if i > len(self._k) - 1:
            raise IndexError
        else:
            return self._k[i]

    def clear(self) -> None:
        """
        Полная очистка словаря

        :return: None
        """

        self._k = array.array('L')
        self._v = array.array('L')

    def pop(self, i: int) -> int:
        """
        Возвращает значение и удаляет элемент с индексом i

        :param i: int
        :return: int - значение элемента с индексом i
        """
        self._v.pop(i)
        return self._k.pop(i)

    def keys(self) -> Generator:
        """
        Последовательность ключей словаря
        """
        for k in self._k:
            yield k

    def values(self) -> Generator:
        """
        Последовательность значений словаря
        """
        for v in self._v:
            yield v

    def items(self) -> Generator:
        """
        Последовательность пар ключ-значение
        """
        for i in range(len(self._k)):
            yield self._k[i], self._v[i]

    def get(self, k: int, default: Optional[int] = None) -> Optional[int]:
        """
        Возвращает элемент по его ключу

        :param k: - ключевое значение поиска
        :param default: int - значение по умолчанию
        :return: Optional[int] - результат поиска
        """

        indx = self.index(k)
        res = self._v[indx] if indx is not None else default

        return res

    def _sort(self) -> None:
        tmp = [(k, i) for i, k in enumerate(self._k)]
        tmp.sort(key=lambda x: x[0])

        self._k = array.array('L')
        self._v_new = array.array('L')
        for item in tmp:
            self._k.append(item[0])
            self._v_new.append(self._v[item[1]])
        self._v = self._v_new
        del self._v_new

    def _index(self, k: int, lo: int, hi: int) -> Optional[int]:
        """
        Поиск индекса элемента по его ключу внутри выделенного диапазона

        :param k: - ключ поиска
        :param lo: - начало диапазона поиска
        :param hi: - предел диапазона поиска
        :return: Optional[int] - найденное значение
        """

        if lo <= hi:
            indx: int = lo + len(self._k[lo:hi:1]) // 2
            if self._k[indx] == k:
                return indx
            elif k < self._k[indx]:
                return self._index(k, lo, indx-1)
            else:
                return self._index(k, indx+1, hi)

    def index(self, k) -> Optional[int]:
        """
        Поиск индекса элемента по его ключу

        :param k: - ключ поиска
        :return: Optional[int] - результат поиска
        """

        return self._index(k, 0, len(self._k) - 1)

    def append(self, k: int, v: int) -> None:
        """
        Добавить элемент в словарь

        :param k: - ключ
        :param v: - значение
        :return: None
        """

        i: int = bisect.bisect_left(self._k, k)
        if i < len(self._k) and self._k[i] == k:
            self._v[i] = v
        else:
            self._k.insert(i, k)
            self._v.insert(i, v)

    def extend(self, data: dict) -> None:
        """
        Слияние со словарем

        :param data: - внешний словарь
        :return: None
        """

        if data is not None and isinstance(data, dict):
            if len(data) < 10**3:
                for k in data.keys():
                    self.append(k, data[k])
                else:
                    self._k.extend([item for item in data.keys()])
                    self._v.extend([item for item in data.values()])
                    idict._sort()

    def to_file(self, f_name: str) -> None:
        """
        Запись данных в файл

        :param f_name: - имя файла
        :return: None
        """
        kb = self._k.tobytes()
        vb = self._v.tobytes()
        data: bytes = len(kb).to_bytes(self._len_f_header, 'big') + kb + vb
        with open(f_name, 'wb') as f:
            f.write(data)

    def from_file(self, f_name: str) -> None:
        """
        Загрузка данных из файла

        :param f_name: - имя файла
        :return: None
        """
        self.clear()

        with open(f_name, 'rb') as f:
            data = f.read()

        if len(data) > 0:
            l_data: int = int.from_bytes(data[:self._len_f_header], 'big')
            self._k.frombytes(data[self._len_f_header:l_data + self._len_f_header])
            self._v.frombytes(data[self._len_f_header + l_data:self._len_f_header + l_data*2])

            if len(self._k) != len(self._v):
                self.clear()
                raise AssertionError
        else:
            raise EOFError


if __name__ == '__main__':
    idict = IntDict()

    from time_it import timeit

    @timeit('')
    def extend():
        global idict
        total_cnt = 1 * 10**1

        import random
        r_list = random.sample(range(1, total_cnt+1), total_cnt)
        r_list = {i: i*10 for i in r_list}

        # Filling
        idict.extend(r_list)

        # idict._sort()
    extend()
    #print(idict)
    print('len=', len(idict))

    # Search
    s = 30
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
