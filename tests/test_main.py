import datetime
from unittest import TestCase
from context.json_data import *
from split.main import split, add_timedelta
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

    def test_add_timedelta_sub_01(self):
        ts1 = add_timedelta(datetime.datetime(year=2000, month=5, day=1), months=-1, days=-1)
        self.assertEqual(datetime.datetime(2000, 3, 31), ts1)

    def test_add_timedelta_sub_02(self):
        ts2 = add_timedelta(datetime.datetime(year=2000, month=5, day=1), months=-4, days=-1)
        self.assertEqual(datetime.datetime(1999, 12, 31), ts2)

    def test_add_timedelta_sub_03(self):
        ts3 = add_timedelta(datetime.datetime(year=2000, month=5, day=1), months=-5, days=-1)
        self.assertEqual(datetime.datetime(1999, 11, 30), ts3)

    def test_add_timedelta_sub_04(self):
        ts4 = add_timedelta(datetime.datetime(year=2000, month=5, day=1), months=-1, days=0)
        self.assertEqual(datetime.datetime(2000, 4, 1), ts4)

    def test_add_timedelta_sub_05(self):

        ts5 = add_timedelta(datetime.datetime(year=2000, month=5, day=1), months=-4, days=0)
        self.assertEqual(datetime.datetime(2000, 1, 1), ts5)

    def test_add_timedelta_sub_06(self):
        ts6 = add_timedelta(datetime.datetime(year=2000, month=5, day=1), months=-5, days=0)
        self.assertEqual(datetime.datetime(1999, 12, 1), ts6)

    def test_add_timedelta_add_01(self):
        ts7 = add_timedelta(datetime.datetime(year=2000, month=5, day=1), months=10, days=0)
        self.assertEqual(datetime.datetime(2001, 3, 1), ts7)

    def test_add_timedelta_add_02(self):
        ts8 = add_timedelta(datetime.datetime(year=2000, month=5, day=1), months=33, days=365)
        self.assertEqual(datetime.datetime(2004, 2, 1), ts8)

    def test_add_timedelta_add_03(self):
        ts9 = add_timedelta(datetime.datetime(year=2000, month=5, day=1), months=-26, days=-366)
        ts10 = add_timedelta(ts9, months=26, days=366)
        self.assertEqual(datetime.datetime(1997, 8, 31), ts9)

