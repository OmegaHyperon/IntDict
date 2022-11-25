"""
    Dictionary with low memory consumption
    Type of data: only unsigned integer, 4 bytes
"""

import array
import bisect
import traceback
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

    def __getitem__(self, key: int):
        i = self.index(key)
        if i is None:
            raise IndexError
        else:
            return self._v[i]

    def __setitem__(self, key: int, val: int):
        i = self.index(key)
        if i is None:
            self.append(key, val)
        else:
            self._v[i] = val

    def clear(self) -> None:
        """
        Full dictionary cleaning

        :return: None
        """

        self._k = array.array('L')
        self._v = array.array('L')

    def pop(self, i: int) -> int:
        """
        Returns a value and removes the element at index i

        :param i: int
        :return: int - значение элемента с индексом i
        """
        self._v.pop(i)
        return self._k.pop(i)

    def keys(self) -> Generator:
        """
        Sequence of dictionary keys
        """
        for k in self._k:
            yield k

    def values(self) -> Generator:
        """
        Sequence of dictionary values
        """
        for v in self._v:
            yield v

    def items(self) -> Generator:
        """
        Sequence of key-value pairs
        """
        for i in range(len(self._k)):
            yield self._k[i], self._v[i]

    def get(self, k: int, default: Optional[int] = None) -> Optional[int]:
        """
        Return an element by its key

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
        Finding the index of an element by its key within the selected range

        :param k: - key
        :param lo: - start from
        :param hi: - end of
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
        Searching the index of an element by its key

        :param k: - ключ поиска
        :return: Optional[int] - результат поиска
        """

        return self._index(k, 0, len(self._k) - 1)

    def append(self, k: int, v: int) -> bool:
        """
        Add an element

        :param k: - ключ
        :param v: - значение
        :return: bool - item was inserted
        """

        i: int = bisect.bisect_left(self._k, k)
        if i < len(self._k) and self._k[i] == k:
            self._v[i] = v
            res = False
        else:
            self._k.insert(i, k)
            self._v.insert(i, v)
            res = True

        return res

    def extend(self, data: dict) -> None:
        """
        Expand the storage with external list

        :param data: - внешний словарь {key: val}
        :return: None
        """

        if data is not None and isinstance(data, dict):
            if len(data) < 10**6:
                for item in data.items():
                    i = self.index(item[0])
                    if i is None:
                        self.append(item[0], item[1])
                    else:
                        self[i] = item[1]

    def to_file(self, f_name: str) -> None:
        """
        Save into the file

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
        Load from the file

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
    pass