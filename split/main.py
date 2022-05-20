from typing import List, Union, Tuple, Dict, Optional
from collections import defaultdict
import datetime
import pprint

from context.json_data import JSON_ARRAY_01 as JSON_ARRAY
from context.json_data import SPLIT_TYPE_VAR


def get_episode(json_array: List[dict], index: Union[int, str]) -> dict:
    if int(index) < 0:
        return {}
    return json_array[int(index)]


def get_json_property(episode: dict, prprty: str) -> Union[dict, list, str, None]:
    if prprty in episode.keys():
        return episode[prprty]
    else:
        return None


def remove_property(episode: dict, prprty: str) -> dict:
    if prprty in episode.keys():
        episode.pop(prprty)
    return episode


def add_or_replace_prprty(episode: dict, prprty: str, value: str) -> dict:
    episode[prprty] = value
    return episode


def valid_timestamp(ts_str: str) -> bool:
    assert as_datetime_timestamp(ts_str)
    return True


def timestamp_within_episode(ts_str: str, episode: dict) -> bool:
    if ts_str is None:
        return False
    ts_1 = as_datetime_timestamp(ts_str)

    ts_0 = as_datetime_timestamp(episode['startDate'])
    ts_n = as_datetime_timestamp(episode['endDate'])
    if ts_0 < ts_1 <= ts_n:
        return True
    else:
        return False


def create_split_stack(json_array: List[dict],
                       episode_index: int,
                       split_type_var_dict: dict) -> Tuple[List[dict], Dict[str, list]]:
    # create stack
    episode = get_episode(json_array, episode_index)

    split_dict = {}
    for split_type, value in split_type_var_dict.items():

        split_type_var = split_type_var_dict[split_type]["var"]
        split_type_reference_val = split_type_var_dict[split_type]["val"]
        split_type_var_value = get_json_property(episode, split_type_var)

        if split_type_var_value is None:
            continue

        if split_type_var_value == split_type_reference_val:
            split_type_timestamp_var = split_type_var_dict[split_type]['timestampvar']
            split_type_timestamp = get_json_property(episode, split_type_timestamp_var)
            if split_type_timestamp is None:
                continue

            if valid_timestamp(split_type_timestamp):
                if split_type_timestamp in split_dict.keys():
                    split_dict[split_type_timestamp].append(split_type)
                else:
                    split_dict[split_type_timestamp] = [split_type]

            # DEV
            # breakpoint()

            # clean up parent episode
            #  clean up split timestamp
            remove_property(episode, split_type_timestamp_var)
            #  clean up split var
            remove_property(episode, split_type_var)

            # DEV
            # breakpoint()

    return json_array, split_dict


def end_of_current_month(ts: datetime) -> datetime:
    return add_timedelta(ts, months=1, days=-1)


def end_of_previous_month(ts: datetime) -> datetime:
    return add_timedelta(ts, months=0, days=-1)


def split_episode(json_array: List[dict],
                  index: Union[int, str],
                  timestamp: str,
                  split_stack: dict) -> Tuple[List[dict], str, dict]:
    index = int(index)
    tmp_json_array = json_array.copy()
    assert valid_timestamp(timestamp)
    ts = as_datetime_timestamp(timestamp)

    parent_episode = tmp_json_array[index]
    max_episode_id = max([int(episode_json['id']) for episode_json in tmp_json_array if 'id' in episode_json.keys()])

    # child episode
    child_id = str(max_episode_id + 1)
    child_episode = parent_episode.copy()
    child_episode['startDate'] = as_zofar_datetime_str(ts)
    child_episode['id'] = child_id
    child_episode['parent'] = str(parent_episode['id'])
    child_episode['state'] = 'new'

    if child_episode['startDate'] in [ts for ts in split_stack.keys()]:
        child_episode['splitType'] = split_stack[child_episode['startDate']]
        split_stack.pop(child_episode['startDate'])
    child_episode['splitStack'] = split_stack
    if child_episode['splitStack'] == {}:
        child_episode.pop('splitStack')

    # parent episode
    parent_episode['endDate'] = as_zofar_datetime_str(end_of_previous_month(ts))
    parent_episode['child'] = child_id
    if 'splitStack' in parent_episode:
        parent_episode.pop('splitStack')

    tmp_json_array[index] = parent_episode
    tmp_json_array.append(child_episode)
    new_index = len(tmp_json_array) - 1

    return tmp_json_array, str(new_index), split_stack


def as_zofar_datetime_str(timestamp_str: datetime) -> str:
    return timestamp_str.strftime(format='%Y-%m-%dT01-00-00.000Z')


def as_datetime_timestamp(date_str: str) -> datetime:
    return datetime.datetime.strptime(date_str, '%Y-%m-%dT01-00-00.000Z')


def add_timedelta(ts: datetime, months: int = 0, days: int = 0) -> datetime:
    new_year = ts.year
    months_incr = months
    # additional increment by 1 because we want to decrease it by 1 day (to get the end of the month) later
    new_month = ts.month + months_incr

    if new_month > 12:
        new_year += 1
        new_month = new_month - 12

    return ts.replace(year=new_year, month=new_month) + datetime.timedelta(days=days)


def next_split(json_array: List[dict], episode_index: Union[int, str], split_stack_dict: dict) -> Tuple[
    List[dict], str, dict]:
    episode_index = int(episode_index)
    if episode_index == -1:
        breakpoint()

    if split_stack_dict == {}:
        return json_array, str(-1), {}

    def _prepare_timestamp(_split_stack_dict: dict) -> Tuple[Optional[str], Optional[List[str]]]:
        timestamp_list = list(split_stack_dict.keys())
        if timestamp_list != []:
            timestamp_list.sort()
            # get the first entry of the split_stack
            _timestamp = timestamp_list[0]
            return _timestamp, timestamp_list
        else:
            return None, None

    timestamp, sorted_timestamp_list = _prepare_timestamp(split_stack_dict)

    while not timestamp_within_episode(timestamp, get_episode(json_array, episode_index)):
        split_stack_dict.pop(timestamp)
        timestamp, sorted_timestamp_list = _prepare_timestamp(split_stack_dict)
        if timestamp is None:
            if 'splitStack' in get_episode(json_array, episode_index):
                if get_episode(json_array, episode_index)['splitStack'] == {}:
                    # json_array[episode_index] = json_array[episode_index].pop('splitStack')
                    json_array[episode_index].pop('splitStack')

            return json_array, str(-1), {}

    # split the episode at the current timestamp
    json_array, next_episode_index, split_stack_dict = split_episode(json_array, episode_index, timestamp,
                                                                     split_stack_dict)
    # pop the item after the split
    json_array[episode_index]['state'] = 'done'

    return json_array, next_episode_index, split_stack_dict


def main():
    pprint.pprint(JSON_ARRAY)
    episode_index = 0

    # Episode filled completely, end-page of module reached
    print('### Episode filled completely, end-page of module reached.')
    pprint.pprint(JSON_ARRAY)

    # we clicked on "Next"
    # before first split

    json_array, split_stack = create_split_stack(json_array=JSON_ARRAY,
                                                 episode_index=episode_index,
                                                 split_type_var_dict=SPLIT_TYPE_VAR)

    # first split
    resulting_json_array, episode_index, split_stack = next_split(json_array=json_array, episode_index=episode_index,
                                                                  split_stack_dict=split_stack)

    print('### we clicked on "Next", first split is done.')
    pprint.pprint(resulting_json_array)
    breakpoint()

    # second split
    if split_stack != {}:
        resulting_json_array, episode_index, split_stack = next_split(json_array=resulting_json_array,
                                                                      episode_index=episode_index,
                                                                      split_stack_dict=split_stack)

        print('### second split is done.')
        pprint.pprint(resulting_json_array)


if __name__ == '__main__':
    main()
