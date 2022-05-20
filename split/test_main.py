from unittest import TestCase
from context.json_data import JSON_ARRAY_01, JSON_ARRAY_01_1st_split, JSON_ARRAY_01_2nd_split, \
    JSON_ARRAY_02, JSON_ARRAY_02_1st_split, JSON_ARRAY_02_2nd_split, \
    JSON_ARRAY_03, JSON_ARRAY_03_1st_split, JSON_ARRAY_03_2nd_split, \
    JSON_ARRAY_04, JSON_ARRAY_04_1st_split, \
    JSON_ARRAY_05, JSON_ARRAY_05_1st_split, JSON_ARRAY_05_2nd_split, \
    SPLIT_TYPE_VAR
from split.main import next_split, create_split_stack
from typing import List, Union
import sys

DEBUG = getattr(sys, 'gettrace', None)


class Test(TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_next_split(self):
        def _run_split(_initial_json_array: List[dict],
                       _init_episode_index: Union[int, str],
                       _split_typ_var: dict,
                       _first_split_result: dict,
                       _first_split_episode_index: Union[int, str],
                       _second_split_result: dict,
                       _second_split_episode_index: Union[int, str]) -> None:
            json_array = JSON_ARRAY_01
            episode_index = 0
            split_type_var_dict = SPLIT_TYPE_VAR

            # prepare first split stack
            json_array, split_stack = create_split_stack(json_array=_initial_json_array,
                                                         episode_index=_init_episode_index,
                                                         split_type_var_dict=_split_typ_var,
                                                         previous_split_stack={})

            # first split
            json_array, episode_index, split_stack = next_split(json_array=json_array,
                                                                episode_index=episode_index,
                                                                split_stack_dict=split_stack, )

            if DEBUG(): print(f'  1st split {episode_index=}')
            self.assertEqual(int(_first_split_episode_index), int(episode_index))
            self.assertEqual(_first_split_result, json_array)

            if int(episode_index) == -1:
                self.assertEqual(_initial_json_array, json_array)
                return

            # prepare second split stack
            # json_array, split_stack = create_split_stack(json_array=_initial_json_array,
            #                                             episode_index=episode_index,
            #                                             split_type_var_dict=_split_typ_var,
            #                                             previous_split_stack=split_stack)

            # second split
            json_array, episode_index, split_stack = next_split(json_array=json_array,
                                                                episode_index=episode_index,
                                                                split_stack_dict=split_stack)

            if DEBUG(): print(f'  2nd split {episode_index=}')
            self.assertEqual(int(_second_split_episode_index), int(episode_index))
            self.assertEqual(_second_split_result, json_array)

        for i, options_tuple in enumerate(
                [
                    (JSON_ARRAY_01, 0, SPLIT_TYPE_VAR, JSON_ARRAY_01_1st_split, 1, JSON_ARRAY_01_2nd_split, 2),
                    (JSON_ARRAY_02, 0, SPLIT_TYPE_VAR, JSON_ARRAY_02_1st_split, 1, JSON_ARRAY_02_2nd_split, -1),
                    (JSON_ARRAY_03, 0, SPLIT_TYPE_VAR, JSON_ARRAY_03_1st_split, 1, JSON_ARRAY_03_2nd_split, -1),
                    (JSON_ARRAY_04, 0, SPLIT_TYPE_VAR, JSON_ARRAY_04_1st_split, -1, None, None)
                ]):
            if DEBUG(): print(f'Test with options tuple {i=}')
            json_arr, index, split_type_var, \
            first_split_result, first_split_episode_index, \
            second_split_result, second_split_episode_index = options_tuple
            _run_split(json_arr, index, split_type_var, first_split_result, first_split_episode_index,
                       second_split_result, second_split_episode_index)

