import client
import numpy as np


class TestMain:
    def test_extract_n_smallest_indices(self):
        four_smallest_indices = client.extract_n_smallest_indices([2, 3, 5, 1, 6, 10], 4)
        assert [3, 0, 1, 2] == list(four_smallest_indices)

    def test_extract_n_biggest_indices(self):
        four_smallest_indices = client.extract_n_biggest_indices([2, 3, 5, 1, 6, 10], 4, order="descending")
        assert [5,4,2,1] == list(four_smallest_indices)

    def test_get_values_from_lists_for_certain_indices(self):
        values = client.get_values_from_lists_for_certain_indices([0,5,1,3], [0,1,2,3,4,5,6,7], [3,2,1,5,100,10])
        assert values[0] == [0,5,1,3] and values[1] == [3,10,2,5]

    def test_transform_numpy_array_to_list(self):
        numpy_arrays = (np.array([1,1,2]) , np.array([1]))
        lists = client.transform_numpy_array_to_list(*numpy_arrays)
        assert type(lists[0]) == type([]) and type(lists[1]) == type([])