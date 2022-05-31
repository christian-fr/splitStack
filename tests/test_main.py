import datetime
from unittest import TestCase
from context.json_data import *
from typing import Dict, List, Any
from split.main import split, add_timedelta, \
    get_flags, get_flags_array, \
    set_flags, set_flags_array, \
    remove_flags, remove_flags_array
import copy


class TestSplit(TestCase):
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
        json_array[episode_index]['vaa13splitDate'] = '2019-04-01T01-00-00.000Z'
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

    def test_one_split_with_flags_JSON_ARRAY_04(self):
        # do one split, add split variables and timestamps to current episode and then do the second split
        json_array = copy.deepcopy(JSON_ARRAY_04)
        json_array, episode_index = split(json_array=json_array,
                                          split_types=SPLIT_TYPE_DICT,
                                          initial_episode_index=0,
                                          max_iteration=1)
        self.assertEqual(2, episode_index)
        self.assertEqual(JSON_ARRAY_04_first_split, json_array)


class TestGetFlags(TestCase):
    # tests for episode dict
    def test_get_flags_false(self):
        episode_dict = copy.deepcopy(JSON_ARRAY_02[0])
        self.assertFalse(get_flags(episode_dict=episode_dict, flag_str="sHO"))

    def test_get_flags_true(self):
        episode_dict = copy.deepcopy(JSON_ARRAY_02[0])
        self.assertTrue(get_flags(episode_dict=episode_dict, flag_str="eHO"))

    def test_get_flags_false_unknown_flag(self):
        episode_dict = copy.deepcopy(JSON_ARRAY_02[0])
        self.assertFalse(get_flags(episode_dict=episode_dict, flag_str="anotherFlag"))

    # tests for json array
    def test_get_flags_array_false(self):
        json_array = copy.deepcopy(JSON_ARRAY_02)
        self.assertFalse(get_flags_array(json_array=json_array, index=0, flag_str="sHO"))

    def test_get_flags_array_true(self):
        json_array = copy.deepcopy(JSON_ARRAY_02)
        self.assertTrue(get_flags_array(json_array=json_array, index=0, flag_str="eHO"))

    def test_get_flags_array_false_unknown_flag(self):
        json_array = copy.deepcopy(JSON_ARRAY_02)
        self.assertFalse(get_flags_array(json_array=json_array, index=0, flag_str="anotherFlag"))


class TestSetFlags(TestCase):
    def check_and_set_and_check(self, episode_dict: Dict[str, Any], flag_str: str, set_before: bool) -> Dict[str, Any]:
        if set_before:
            self.assertTrue(get_flags(episode_dict=episode_dict, flag_str=flag_str))
        else:
            self.assertFalse(get_flags(episode_dict=episode_dict, flag_str=flag_str))
        episode_dict = set_flags(episode_dict=episode_dict, flag_str=flag_str)
        self.assertTrue(get_flags(episode_dict=episode_dict, flag_str=flag_str))
        return episode_dict

    def check_and_set_and_check_array(self, json_array: List[Dict[str, Any]],
                                      index: int,
                                      flag_str: str,
                                      set_before: bool) -> List[Dict[str, Any]]:
        json_array = copy.deepcopy(json_array)
        if set_before:
            self.assertTrue(get_flags_array(json_array=json_array, index=index, flag_str=flag_str))
        else:
            self.assertFalse(get_flags_array(json_array=json_array, index=index, flag_str=flag_str))
        json_array = set_flags_array(json_array=json_array, index=index, flag_str=flag_str)
        self.assertTrue(get_flags_array(json_array=json_array, index=index, flag_str=flag_str))
        return json_array

    def test_set_flags_not_set_before(self):
        episode_dict = copy.deepcopy(JSON_ARRAY_04[1])
        self.check_and_set_and_check(episode_dict=episode_dict, flag_str="sHO", set_before=False)

    def test_set_flags_set_before(self):
        episode_dict = copy.deepcopy(JSON_ARRAY_04[1])
        self.check_and_set_and_check(episode_dict=episode_dict, flag_str="eHO", set_before=True)

    # test array functions
    def test_set_flags_array_not_set_before_index0(self):
        json_array = copy.deepcopy(JSON_ARRAY_04)
        self.check_and_set_and_check_array(json_array=json_array, index=0, flag_str="anotherFlag", set_before=False)

    def test_set_flags_array_not_set_before_index1(self):
        json_array = copy.deepcopy(JSON_ARRAY_04)
        self.check_and_set_and_check_array(json_array=json_array, index=1, flag_str="sHO", set_before=False)

    def test_set_flags_array_set_before_index0(self):
        json_array = copy.deepcopy(JSON_ARRAY_04)
        self.check_and_set_and_check_array(json_array=json_array, index=0, flag_str="sHO", set_before=True)

    def test_set_flags_array_set_before_index1(self):
        json_array = copy.deepcopy(JSON_ARRAY_04)
        self.check_and_set_and_check_array(json_array=json_array, index=1, flag_str="eHO", set_before=True)


class TestRemoveFlags(TestCase):
    def check_and_rm_and_check(self, episode_dict: Dict[str, Any], flag_str: str, set_before: bool) -> Dict[str, Any]:
        if set_before:
            self.assertTrue(get_flags(episode_dict=episode_dict, flag_str=flag_str))
        else:
            self.assertFalse(get_flags(episode_dict=episode_dict, flag_str=flag_str))
        episode_dict = remove_flags(episode_dict=episode_dict, flag_str=flag_str)
        self.assertFalse(get_flags(episode_dict=episode_dict, flag_str=flag_str))
        return episode_dict

    def check_and_rm_and_check_array(self, json_array: List[Dict[str, Any]],
                                     index: int,
                                     flag_str: str,
                                     set_before: bool) -> List[Dict[str, Any]]:
        json_array = copy.deepcopy(json_array)
        if set_before:
            self.assertTrue(get_flags_array(json_array=json_array, index=index, flag_str=flag_str))
        else:
            self.assertFalse(get_flags_array(json_array=json_array, index=index, flag_str=flag_str))
        json_array = remove_flags_array(json_array=json_array, index=index, flag_str=flag_str)
        self.assertFalse(get_flags_array(json_array=json_array, index=index, flag_str=flag_str))
        return json_array

    def test_remove_flags_not_set_before(self):
        episode_dict = copy.deepcopy(JSON_ARRAY_04[1])
        self.check_and_rm_and_check(episode_dict=episode_dict, flag_str="sHO", set_before=False)

    def test_remove_flags_set_before(self):
        episode_dict = copy.deepcopy(JSON_ARRAY_04[1])
        self.check_and_rm_and_check(episode_dict=episode_dict, flag_str="eHO", set_before=True)

    # test array functions
    def test_remove_flags_array_not_set_before_index0(self):
        json_array = copy.deepcopy(JSON_ARRAY_04)
        self.check_and_rm_and_check_array(json_array=json_array, index=0, flag_str="anotherFlag", set_before=False)

    def test_remove_flags_array_not_set_before_index1(self):
        json_array = copy.deepcopy(JSON_ARRAY_04)
        self.check_and_rm_and_check_array(json_array=json_array, index=1, flag_str="sHO", set_before=False)

    def test_remove_flags_array_set_before_index0(self):
        json_array = copy.deepcopy(JSON_ARRAY_04)
        self.check_and_rm_and_check_array(json_array=json_array, index=0, flag_str="sHO", set_before=True)

    def test_remove_flags_array_set_before_index1(self):
        json_array = copy.deepcopy(JSON_ARRAY_04)
        self.check_and_rm_and_check_array(json_array=json_array, index=1, flag_str="eHO", set_before=True)


class TestTimeDelta(TestCase):

    def test_add_timedelta_sub_add(self):
        ts = add_timedelta(datetime.datetime(year=2000, month=5, day=1), months=-1, days=1)
        self.assertEqual(datetime.datetime(2000, 4, 2), ts)

    def test_add_timedelta_sub_sub(self):
        ts = add_timedelta(datetime.datetime(year=2000, month=5, day=1), months=-4, days=-1)
        self.assertEqual(datetime.datetime(1999, 12, 31), ts)

    def test_add_timedelta_same_same(self):
        ts = add_timedelta(datetime.datetime(year=2000, month=5, day=1), months=0, days=0)
        self.assertEqual(datetime.datetime(2000, 5, 1), ts)

    def test_add_timedelta_sub_same(self):
        ts = add_timedelta(datetime.datetime(year=2000, month=5, day=1), months=-4, days=0)
        self.assertEqual(datetime.datetime(2000, 1, 1), ts)

    def test_add_timedelta_same_sub(self):
        ts = add_timedelta(datetime.datetime(year=2000, month=5, day=1), months=0, days=-1)
        self.assertEqual(datetime.datetime(2000, 4, 30), ts)

    def test_add_timedelta_add_same(self):
        ts = add_timedelta(datetime.datetime(year=2000, month=5, day=1), months=10, days=0)
        self.assertEqual(datetime.datetime(2001, 3, 1), ts)

    def test_add_timedelta_add_add(self):
        ts = add_timedelta(datetime.datetime(year=2000, month=5, day=1), months=33, days=365)
        self.assertEqual(datetime.datetime(2004, 2, 1), ts)

    def test_add_timedelta_sub_sub_a_lot(self):
        ts = add_timedelta(datetime.datetime(year=2000, month=5, day=1), months=-26, days=-366)
        self.assertEqual(datetime.datetime(1997, 8, 31), ts)

    def test_add_timedelta_add_add_a_lot(self):
        ts = add_timedelta(datetime.datetime(year=2000, month=5, day=1), months=26, days=366)
        self.assertEqual(datetime.datetime(2003, 7, 2), ts)


class TestCreateSplitStack(TestCase):
    def test_create_split_stack(self):
        self.fail()
