import os
import array
import bisect
from pympler import asizeof
from typing import Optional
import datetime


class IntDict(object):
    def __init__(self):
        self._k: array.array = array.array('L')
        self._v: array.array = array.array('L')

    def __str__(self):
        return str({self._k[i]: self._v[i] for i in range(len(self._k))})

    def __len__(self):
        return len(self._k)

    def __getitem__(self, k: int):
        if k > len(self._k):
            raise IndexError

        return self.get(k)

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

    def append(self, k: int, v: int) -> None:
        """
        Добавить элемент в словарь

        :param k: - ключ
        :param v: - значение
        :return:
        """

        i: int = bisect.bisect_left(self._k, k)
        if i < len(self._k) and self._k[i] == k:
            self._v[i] = v
        else:
            self._k.insert(i, k)
            self._v.insert(i, v)

    def keys(self) -> list:
        """
        Список ключей словаря

        :return: list
        """
        return list(self._k)

    def values(self) -> list:
        """
        Список значений словаря

        :return: list
        """

        return list(self._v)

    def items(self) -> list:
        return [(self._k[i], self._v[i]) for i in range(len(self._k))]

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

    def _index(self, k: int, lo: int, hi: int) -> Optional[int]:
        """
        Поиск индекса элемента по его ключу внутри выделенного диапазона

        :param k: - ключ поиска
        :param lo: - начало диапазона поиска
        :param hi: - предел диапазона поиска
        :return: - найденное значение
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

    def update(self, data: dict) -> None:
        """
        Слияние со словарем

        :param data: - внешний словарь
        :return: None
        """

        if data is not None and isinstance(data, dict):
            for k in data.keys():
                self.append(k, data[k])

    def to_file(self, f_name: str):
        kb = self._k.tobytes()
        vb = self._k.tobytes()
        data: bytes = len(kb).to_bytes(8, 'big') + kb + vb
        with open(f_name, 'wb') as f:
            f.write(data)

    def from_file(self, f_name: str):
        self.clear()

        with open(f_name, 'rb') as f:
            data = f.read()

        l_data: int = int.from_bytes(data[:8], 'big')
        k_data: bytes = data[8:l_data+8]
        v_data: bytes = data[8+l_data:8+l_data*2]
        self._k.frombytes(k_data)
        self._v.frombytes(v_data)


if __name__ == '__main__':
    idict = IntDict()
    d = dict()

    total_cnt = 40000000

    df = datetime.datetime.now()
    for i in range(total_cnt):
        idict.update({i: i*10})
    print('fill of idict: ', (datetime.datetime.now() - df).total_seconds())
    print('len=', len(idict), '; k, v:', len(idict._k), len(idict._v))

    df = datetime.datetime.now()
    for i in range(total_cnt):
        d[i] = i
    print('fill of d: ', (datetime.datetime.now() - df).total_seconds())
    print(idict[10])

    df = datetime.datetime.now()
    idict.to_file('aaa.bin')
    print('save: ', (datetime.datetime.now() - df).total_seconds())
    idict.clear()
    df = datetime.datetime.now()
    idict.from_file('aaa.bin')
    print('load: ', (datetime.datetime.now() - df).total_seconds())
    print(len(idict))

    test_ses = 1

    df = datetime.datetime.now()
    for i in range(test_ses):
        idict.get(300)
    print('time of idict: ', (datetime.datetime.now() - df).total_seconds())

    df = datetime.datetime.now()
    for i in range(test_ses):
        d.get(300)
    print('time of d: ', (datetime.datetime.now() - df).total_seconds())

    print('Size in memory: ', asizeof.asizeof(idict), asizeof.asizeof(d))


