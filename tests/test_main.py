from unittest import TestCase
from context.json_data import *
from split.main import split
import copy


class Test(TestCase):
    def test_one_split_JSON_ARRAY_01(self):
        # do one split
        json_array = copy.deepcopy(JSON_ARRAY_01)
        json_array, episode_index = split(json_array=json_array,
                                          split_types=SPLIT_TYPE_DICT,
                                          initial_episode_index=0,
                                          max_iteration=1)
        self.assertEqual(1, episode_index)
        self.assertEqual(JSON_ARRAY_01_1st_split, json_array)
        del json_array
        del episode_index

    def test_up_to_two_splits_JSON_ARRAY_01(self):
        # do up to two splits
        json_array = copy.deepcopy(JSON_ARRAY_01)
        json_array, episode_index = split(json_array=json_array,
                                          split_types=SPLIT_TYPE_DICT,
                                          initial_episode_index=0,
                                          max_iteration=2)
        self.assertEqual(2, episode_index)
        self.assertEqual(JSON_ARRAY_01_2nd_split, json_array)
        del json_array
        del episode_index

    def test_max_split_JSON_ARRAY_01(self):
        # do as many splits as possible
        json_array = copy.deepcopy(JSON_ARRAY_01)
        json_array, episode_index = split(json_array=json_array,
                                          split_types=SPLIT_TYPE_DICT,
                                          initial_episode_index=0,
                                          max_iteration=2)
        self.assertEqual(2, episode_index)
        self.assertEqual(JSON_ARRAY_01_max_split, json_array)

    def test_one_split_add_split_JSON_ARRAY_01(self):
        # do one split, add split variables and timestamps to current episode and then do the second split
        json_array = copy.deepcopy(JSON_ARRAY_01)
        json_array, episode_index = split(json_array=json_array,
                                          split_types=SPLIT_TYPE_DICT,
                                          initial_episode_index=0,
                                          max_iteration=1)
        self.assertEqual(1, episode_index)
        self.assertEqual(JSON_ARRAY_01_1st_split, json_array)

        json_array[episode_index]['vaa10'] = 'ao1'
        json_array[episode_index]['vaa11splitDate'] = '2019-04-01T01-00-00.000Z'
        json_array[episode_index]['vaa14'] = 'ao1'
        json_array[episode_index]['vaa15splitDate'] = '2019-02-01T01-00-00.000Z'

        json_array, episode_index = split(json_array=json_array.copy(),
                                          split_types=SPLIT_TYPE_DICT,
                                          initial_episode_index=episode_index,
                                          max_iteration=1)

        self.assertEqual(2, episode_index)
        self.assertEqual(JSON_ARRAY_01_modifed_2nd_split, json_array)

        json_array[episode_index]['vaa12'] = 'ao2'
        json_array[episode_index]['vaa11splitDate'] = '2019-04-01T01-00-00.000Z'
        json_array[episode_index]['vaa14'] = 'ao1'
        json_array[episode_index]['vaa15splitDate'] = '2018-01-01T01-00-00.000Z'

        json_array, episode_index = split(json_array=json_array.copy(),
                                          split_types=SPLIT_TYPE_DICT,
                                          initial_episode_index=episode_index,
                                          max_iteration=1)

        self.assertEqual(3, episode_index)
        self.assertEqual(JSON_ARRAY_01_modifed_3rd_split, json_array)

        json_array, episode_index = split(json_array=json_array.copy(),
                                          split_types=SPLIT_TYPE_DICT,
                                          initial_episode_index=episode_index,
                                          max_iteration=0)

        self.assertEqual(-1, episode_index)
        self.assertEqual(JSON_ARRAY_01_modified_max_split, json_array)
