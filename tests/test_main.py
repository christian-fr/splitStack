from unittest import TestCase
from context.json_data import JSON_ARRAY_01, JSON_ARRAY_01_1st_split, JSON_ARRAY_01_2nd_split, \
    JSON_ARRAY_02, JSON_ARRAY_02_1st_split, JSON_ARRAY_02_2nd_split, \
    JSON_ARRAY_03, JSON_ARRAY_03_1st_split, JSON_ARRAY_03_2nd_split, \
    JSON_ARRAY_04, JSON_ARRAY_04_1st_split, \
    JSON_ARRAY_05, JSON_ARRAY_05_1st_split, JSON_ARRAY_05_2nd_split, \
    SPLIT_TYPE_DICT
from split.main import create_split_stack_json_array, split_episode
from typing import List, Union
import sys

DEBUG = getattr(sys, 'gettrace', None)


class Test(TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass


class Test(TestCase):
    def test_split_episode(self):
        episode_index = 0
        while episode_index != -1:
            json_array = create_split_stack_json_array(json_array=JSON_ARRAY_01,
                                                       current_episode_index=episode_index,
                                                       split_type=SPLIT_TYPE_DICT)

            # noinspection DuplicatedCode
            main_json_array, episode_index = split_episode(json_array=json_array,
                                                           current_episode_index=episode_index)
            if episode_index == 1:
                main_json_array[episode_index]['vaa10'] = 'ao1'
                main_json_array[episode_index]['vaa11splitDate'] = '2019-04-01T01-00-00.000Z'
            if episode_index == 1:
                main_json_array[episode_index]['vaa14'] = 'ao1'
                main_json_array[episode_index]['vaa15splitDate'] = '2019-02-01T01-00-00.000Z'

            # ToDo: finish tests for new implementation
