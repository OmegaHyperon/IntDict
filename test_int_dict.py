import pytest
from int_dict import IntDict


class TestIntDict:
    @pytest.fixture(scope='session')
    def int_dict(self):
        return IntDict()

    def test_append(self, int_dict):
        int_dict.append(1, 10)
        int_dict.append(2, 200)

        assert len(int_dict) == 2
        assert int_dict.index(2) == 1
        assert int_dict[1] == 10

    def test_set(self, int_dict):
        assert list(int_dict.values())[1] == 200
        int_dict[2] = 20
        assert list(int_dict.values())[1] == 20

    def test_extend(self, int_dict):
        int_dict.extend({3: 30, 4: 40, 5: 50})
        assert len(int_dict) == 5
