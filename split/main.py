import copy
from typing import List, Union, Tuple, Dict, Any
import datetime
import math


def get_episode(json_array: List[dict], index: Union[int, str]) -> dict:
    """

    :param json_array:
    :param index:
    :return:
    """
    json_array = json_array.copy()
    if int(index) < 0 or int(index) > len(json_array) - 1:
        return {}
    return json_array[int(index)]


def get_json_property(episode: dict, json_property: str) -> Union[dict, list, str, None]:
    """

    :param episode:
    :param json_property:
    :return:
    """
    if json_property in episode.keys():
        return episode[json_property]
    else:
        return None


def get_flags(episode_dict: Dict[str, Any], flag_str: str) -> bool:
    # when current_episode already has a "flag" property/key
    if "flags" in episode_dict.keys():
        # when a "flag" key exists and its value is a list
        if isinstance(episode_dict["flags"], list):
            # when the flag is already set: return the unmodified json array
            if flag_str in episode_dict["flags"]:
                return True
    return False


def set_flags(episode_dict: Dict[str, Any], flag_str: str) -> Dict[str, Any]:
    episode_dict = copy.deepcopy(episode_dict)
    # when the flag is already set: return the unmodified episode_dict
    if get_flags(episode_dict=episode_dict, flag_str=flag_str):
        return episode_dict
    # when current_episode does not have "flag" property/key or it is malformed: initiate a new array with flag_str
    else:
        episode_dict["flags"] = [flag_str]
    return episode_dict


def remove_flags(episode_dict: Dict[str, Any], flag_str: str) -> Dict[str, Any]:
    episode_dict = copy.deepcopy(episode_dict)
    if get_flags(episode_dict=episode_dict, flag_str=flag_str):
        episode_dict["flags"].remove(flag_str)
    return episode_dict


def get_flags_array(json_array: List[Dict[str, Any]], index: int, flag_str: str) -> bool:
    current_episode = get_episode(json_array=json_array, index=index)
    return get_flags(episode_dict=current_episode, flag_str=flag_str)


def set_flags_array(json_array: List[Dict[str, Any]], index: int, flag_str: str) -> List[Dict[str, Any]]:
    json_array = copy.deepcopy(json_array)
    current_episode = get_episode(json_array=json_array, index=index)
    # when the flag is not yet set: set it in current_episode and return the modified json_array
    if not get_flags(episode_dict=current_episode, flag_str=flag_str):
        # set flag and update the episode
        json_array[index] = set_flags(episode_dict=current_episode, flag_str=flag_str)
    return json_array


def remove_flags_array(json_array: List[Dict[str, Any]], index: int, flag_str: str) -> List[Dict[str, Any]]:
    json_array = copy.deepcopy(json_array)
    current_episode = get_episode(json_array=json_array, index=index)
    # when the flag is set
    if get_flags(episode_dict=current_episode, flag_str=flag_str):
        # remove the flag_str from the array and update the episode
        json_array[index] = remove_flags(episode_dict=current_episode, flag_str=flag_str)
    return json_array


def max_id_in_json_array(json_array: List[Dict[str, Any]]) -> int:
    """

    :param json_array:
    :return:
    """
    id_list = []
    for episode in json_array:
        if 'id' in episode.keys():
            id_list.append(int(episode['id']))
    return max(id_list)


def remove_property(episode: dict, json_property: str) -> dict:
    """

    :param episode:
    :param json_property:
    :return:
    """
    if json_property in episode.keys():
        episode.pop(json_property)
    return episode


def add_or_replace_json_property(episode: dict, json_property: str, value: str) -> dict:
    """

    :param episode:
    :param json_property:
    :param value:
    :return:
    """
    episode[json_property] = value
    return episode


def valid_timestamp(ts_str: str) -> bool:
    assert as_datetime_timestamp(ts_str)
    return True


def timestamp_within_episode(ts_str: str, episode: dict) -> bool:
    """

    :param ts_str:
    :param episode:
    :return:
    """
    if ts_str is None:
        return False
    ts_1 = as_datetime_timestamp(ts_str)

    ts_0 = as_datetime_timestamp(episode['startDate'])
    ts_n = as_datetime_timestamp(episode['endDate'])
    if ts_0 < ts_1 <= ts_n:
        return True
    else:
        return False


def end_of_current_month(ts: datetime) -> datetime:
    return add_timedelta(ts, months=1, days=-1)


def end_of_previous_month(ts: datetime) -> datetime:
    return add_timedelta(ts, months=0, days=-1)


def to_zofar_ts_str(timestamp_str: datetime) -> str:
    return timestamp_str.strftime(format='%Y-%m-%dT01-00-00.000Z')


def as_datetime_timestamp(date_str: str) -> datetime:
    return datetime.datetime.strptime(date_str, '%Y-%m-%dT01-00-00.000Z')


def add_timedelta(ts: datetime, months: int = 0, days: int = 0) -> datetime:
    """

    :param ts: input datetime object
    :param months: months delta (int)
    :param days: days delta (int)
    :return: new datetime object
    """
    new_year = ts.year
    # additional increment by 1 because we want to decrease it by 1 day (to get the end of the month) later
    months = ts.month + months

    if months > 12:
        new_year = new_year + math.floor(months / 12)
        new_months = months % 12

    elif months < 1:
        new_year = new_year + math.ceil(months / 12) - 1
        new_months = 12 - (months % 12)

    else:
        new_months = months

    return ts.replace(year=new_year, month=new_months) + datetime.timedelta(days=days)


def add_type_to_split_stack(split_stack_dict: dict, timestamp: str, split_type: str) -> Dict[str, List[str]]:
    """

    :param split_stack_dict:
    :param timestamp:
    :param split_type:
    :return:
    """
    if timestamp in split_stack_dict.keys():
        if not isinstance(split_stack_dict[timestamp], list):
            split_stack_dict[timestamp] = [split_type]
        else:
            if split_type not in split_stack_dict[timestamp]:
                split_stack_dict[timestamp].append(split_type)
    else:
        split_stack_dict[timestamp] = [split_type]
    return split_stack_dict


def check_if_key_value(input_dict: dict, key: str, value: Any) -> bool:
    """

    :param input_dict:
    :param key:
    :param value:
    :return:
    """
    if key not in input_dict:
        return False
    if input_dict[key] != value:
        return False
    return True


def create_split_stack_json_array(json_array: List[Dict[str, Any]],
                                  current_episode_index: int,
                                  split_types: dict) -> List[Dict[str, Any]]:
    """

    :param json_array:
    :param current_episode_index:
    :param split_types:
    :return:
    """
    json_array = json_array.copy()
    json_array[current_episode_index] = create_split_stack(split_types=split_types,
                                                           current_episode_dict=json_array[current_episode_index])
    return json_array


def create_split_stack(split_types: Dict[str, Dict[str, List[Dict[str, str]]]],
                       current_episode_dict: Dict[str, Any]) -> Dict[str, Any]:
    """

    :param split_types:
    :param current_episode_dict:
    :return:
    """
    # if "currentSplit" is in current episode, it is obsolete and will be removed
    remove_property(current_episode_dict, 'currentSplit')

    # get "splitStack" dict, if already present in current episode
    if 'splitStack' in current_episode_dict.keys():
        split_stack = current_episode_dict['splitStack']
    # otherwise: create an empty dict
    else:
        split_stack = {}

    # iterate over all split types in the dict
    #  e.g. {"SplitTypA": {"split_var": [{"splitvar01": "val0"}], "timestamp_var": "splitDate_var01"}}:
    #    split_type_str = "SplitTypA"
    #    split_data = {"split_var": [{"splitvar01": "val0"}], "timestamp_var": "splitDate_var01"}
    for split_type_str, split_data in split_types.items():
        timestamp_var = split_data['timestamp_var']
        if not isinstance(timestamp_var, str):
            continue

        for var_entry in split_data['split_var']:
            for var_name, var_reference_value in var_entry.items():
                if var_name is None or var_name == '':
                    continue
                if var_reference_value is None or var_name == '':
                    continue

                if check_if_key_value(current_episode_dict, key=var_name, value=var_reference_value):
                    if timestamp_var in current_episode_dict.keys():
                        split_timestamp = current_episode_dict[timestamp_var]
                        if valid_timestamp(split_timestamp):
                            split_stack = add_type_to_split_stack(split_stack, timestamp=split_timestamp,
                                                                  split_type=split_type_str)

                    # remove split variable from episode if it has been added to the split stack
                    current_episode_dict = remove_property(current_episode_dict, var_name)

        # remove all split timestamps from episode
        current_episode_dict = remove_property(current_episode_dict, timestamp_var)
    current_episode_dict['splitStack'] = split_stack

    if current_episode_dict['splitStack'] == {}:
        current_episode_dict = remove_property(current_episode_dict, 'splitStack')
    return current_episode_dict


def get_indices_of_episodes_with_property(json_array: List[Dict[str, Any]], property_key: str) -> List[int]:
    """

    :param json_array:
    :param property_key:
    :return:
    """
    results = set()
    for index, episode in enumerate(json_array):
        if property_key in episode.keys():
            results.add(index)
    return list(results)


def clean_other_episodes_of_property(json_array: List[Dict[str, Any]],
                                     property_key: str,
                                     current_episode_index: int) -> List[Dict[str, Any]]:
    """

    :param json_array:
    :param property_key:
    :param current_episode_index:
    :return:
    """
    json_array = json_array.copy()
    episode_index_list = get_indices_of_episodes_with_property(json_array, property_key)
    if current_episode_index in episode_index_list:
        episode_index_list.remove(current_episode_index)
    for index in episode_index_list:
        tmp_episode = json_array[index]
        if property_key in tmp_episode:
            tmp_episode = remove_property(tmp_episode, property_key)
        json_array[index] = tmp_episode
    return json_array


def lowest_split_stack_entry(split_stack: Dict[str, List[Dict[str, str]]]) -> Tuple[str, List[Dict[str, str]]]:
    """

    :param split_stack: input dictionary object: {"TIMESTAMP_t0: ["VAL1", "VAL2], "TIMESTAMP_t1": ["VAL3"]}
    :return: a tuple: the lowest key of dictionary, i.e. the lowest / earliest timestamp string and its value,
    i.e. a list of split_type strings
    """
    list_of_timestamps = list(split_stack.keys())
    list_of_timestamps.sort()
    return list_of_timestamps[0], split_stack[list_of_timestamps[0]]


def split_episode(json_array: List[Dict[str, Any]], current_episode_index: int) -> Tuple[List[Dict[str, Any]], int]:
    """

    :param json_array:
    :param current_episode_index:
    :return:
    """
    # delete all other "splitStack" properties from other episodes
    json_array = json_array.copy()
    json_array = clean_other_episodes_of_property(json_array, 'splitStack', current_episode_index)

    # get the current episode from JSON array
    current_episode = json_array[current_episode_index].copy()

    # cancel if there is no prepared "splitStack" in current episode
    if 'splitStack' not in current_episode.keys():
        return json_array, -1

    # set "state" of current episode to "done"
    current_episode['state'] = 'done'

    split_timestamp = None
    split_data = None

    # iterate over timestamps in splitStack
    flag_timestamp_valid = False
    while len(current_episode['splitStack']) > 0 and not flag_timestamp_valid:
        split_timestamp, split_data = lowest_split_stack_entry(current_episode['splitStack'])
        # check whether split_timestamp is valid
        if valid_timestamp(split_timestamp) and timestamp_within_episode(episode=current_episode,
                                                                         ts_str=split_timestamp):
            flag_timestamp_valid = True
        # otherwise: remove entry from "splitStack"
        else:
            current_episode['splitStack'] = remove_property(current_episode['splitStack'], split_timestamp)
            split_timestamp = None
            split_data = None

    if split_timestamp is None or split_data is None:
        # in case of error:
        # cleanup episode and finish without split, return episode_index of -1
        current_episode = remove_property(current_episode, 'splitStack')
        current_episode = remove_property(current_episode, 'currentSplit')
        json_array[current_episode_index] = current_episode.copy()
        return json_array, -1

    # if there was no error and split_timestamp is valid and has split_data:
    # create child episode, modify parent
    parent_episode = current_episode.copy()
    child_episode = current_episode.copy()

    # PARENT EPISODE: set new "endDate"
    parent_episode['endDate'] = to_zofar_ts_str(end_of_previous_month(as_datetime_timestamp(split_timestamp)))
    # clean up parent episode: remove "splitStack" and "currentSplit"
    parent_episode = remove_property(parent_episode, 'splitStack')
    parent_episode = remove_property(parent_episode, 'currentSplit')

    # remove "eHO" from parent's "flags" (if present)
    parent_episode = remove_flags(episode_dict=parent_episode, flag_str='eHO')
    # remove "sHO" from child's "flags" (if present)
    child_episode = remove_flags(episode_dict=child_episode, flag_str='sHO')

    # CHILD EPISODE: set new "startDate"
    child_episode['startDate'] = split_timestamp
    # set "currentSplit"
    child_episode['currentSplit'] = split_data
    # remove the timestamp of the current split from child episode "splitStack"
    #  (as the info is preserved within "currentSplit")
    if split_timestamp in child_episode['splitStack']:
        child_episode['splitStack'].pop(split_timestamp)
    # remove "splitStack" property if it is empty
    if child_episode['splitStack'] == {}:
        remove_property(child_episode, 'splitStack')
    # set id of child
    child_episode['id'] = str(max_id_in_json_array(json_array) + 1)
    # link to parent via parent id
    child_episode['parent'] = parent_episode['id']

    # PARENT EPISODE link to child via child id
    #  (an array is used here, as it may be possible for an episode to have multiple children)
    # when the parent does not yet have "children"
    if 'children' not in parent_episode.keys():
        parent_episode['children'] = [child_episode['id']]
    # when there already is a "children" property:
    else:
        # check if it is an array
        if isinstance(parent_episode['children'], list):
            parent_episode['children'].append(child_episode['id'])
        # ... otherwise: replace it with a new array
        else:
            parent_episode['children'] = [child_episode['id']]

    # write parent episode to JSON array
    json_array[current_episode_index] = parent_episode
    # append child episode to the end of the JSON array
    json_array.append(child_episode)

    # determine new episode_index via length of JSON array
    new_episode_index = len(json_array) - 1
    return json_array, new_episode_index

    # Definition:
    # - Modul:
    #   - eine Sammlung von Pages, die aufeinander verweisen und innerhalb der Gesamtbefragung einen Subgraphen
    #     bilden;
    #   - ein Modul beinhaltet detaillierte Nachfragen zu einem bestimmten Episoden-Typ;
    #   - in einem Modul gibt es:
    #     - mind. eine Page, über die das Modul betreten wird;
    #     - mind. eine Page, über die das Modul verlassen wird;
    #     - ggf. Verzweigungen innerhalb des Moduls;
    #     - ggf. Pages, auf denen ->Splitkriterien abgefragt werden;
    #     - ggf. Pages, auf denen ->Splitvariablen abgefragt werden;
    #     - ggf. Pages, auf denen ->Zeitstempel für diese ->Splitvariablen (per Monthpicker) abgefragt werden;
    #     - auf den End-Pages eines Moduls werden ggf. ->Split-Stacks erstellt und
    #       Splits durchgeführt (siehe hierzu: ->Elter-Episode);
    #   - die Modul-Zugehörigkeit einer Page lässt sich durch die ersten n Buchstaben ihres Namens eindeutig erkennen;
    # - Teilmodul:
    #   - innerhalb eines Modul kann es Teilmodule geben;
    #   - diese Teilmodule werden unter bestimmten Bedingungen betreten und wieder verlassen;
    #   - die Teilmodul-Zugehörigkeit einer Page lässt sich durch die ersten n+1 Buchstaben ihres Namens
    #     eindeutig erkennen;
    # - Splitkriterium: ein oder mehrere Merkmale, die inhaltlich zusammenhängen und bei denen eine
    #    eventuelle Änderung mithilfer einer ->Splitvariablen abgefragt wird;
    # - Zeitstempel-Variable: Variable, die über einen Monthpicker erfasst wurde und einen Zeitstempel der Form
    #    "YYYY-MM-DDT01:00:00.000Z" aufweist, wobei
    #     "DD" -> {"01","28","29","30","31"}
    #     sein kann (erster bzw. letzter Tag des Monats);
    # - Splitvariable: eine oder mehre Variablen, deren Beantwortung mit einem bestimmten Wert
    #    die Änderung eines ->Split-Kriteriums markiert und die einen Split auslöst; je nach Kombination aus
    #    Variablenname und Variablenwert wird dem zugehörigen Zeitstempel ein bestimmter ->Split-Typ zugeordnet;
    # - Split-Typ: ein String, der eindeutig eine von ggf. mehreren möglichen Kombinationen von Variablennamen und
    #    Variablenwerten markiert, ihm wird beim Split eine ->Zeitstempel-Variable zugeordnet;
    #    die Split-Typen werden als Map/Dictionary im QML festgelegt zugeführt:
    #      {
    #      	"SplitTypA": {
    #  	    	          "split_var": [{
    #  	    		                   "splitvar01": "val0",
    #  	    		                   "splitvar02": "val1"
    #  	    	                       }],
    #  	    	         "timestamp_var": "date_var01"
    #  	                 },
    #      	"SplitTypB": {
    #  	    	         "split_var": [{
    #  	    		                  "splitvar03": "val0"
    #  	    	                      }],
    #  	    	         "timestamp_var": "date_var04"
    #  	                 },
    #       [...]
    #      }
    # - Split-Stack: eine Map/Dictionary, die aus key-value-Paaren besteht und einem ->Zeitstempel eine Liste von
    #    Split-Typen zuordnet; wenn eine Episode ->Split-Variablen mit Variablenwerten enthält, die sich einem
    #    ->Split-Typ zuordnen lassen; der Split-Stack wird auf Grundlage der ->Split-Variablen und der Variablenwerte
    #    für die aktuelle Episode erstellt; falls bereits ein JSON-Property/Key "splitStack" in der aktuellen Episode
    #    vorhanden ist, werden die Split-Stacks vereinigt;

    #    - wenn der Split-Stack leer ist ("{}"), wird die Property aus der Episode entfernt;
    #    - wenn das Property "currentSplit" noch in der Episode vorhanden ist, wird dieses ebenfalls entfernt.
    #    - wenn der Split-Stack für die aktuelle Episode erstellt wurde (ggf. auch schon während der Erstellung),
    #      - werden die ->Split-Variablen, die sich einem ->Split-Typ zuordnen ließen, aus der Episode entfernt;
    #      - werden alle Split-Zeistempel aus der Episode entfernt;
    #      - der Split-Stack liegt unmittelbar nach Erstellung als Property "splitStack" der aktuellen Episode vor;
    #
    #     => hier sollten wir eine "Sicherung" einbauen: falls bereits eine andere Episode existiert (gleich welchen
    #        Typs), die einen Split-Stack (also das Property "splitStack" oder "currentSplit") beinhaltet, werden
    #        diese Properties entfernt, sobald ein neuer Split-Stack erstellt und in der Elter-Episode abgespeichert
    #        wird;
    # - Elter-Episode: wenn für die aktuelle Episode ein Split-Stack erstellt werden konnte oder noch als JSON-Property
    #    vorliegt, wird die aktuelle Episode zu einer Elter-Episode;
    #    - der Status "state" der Elter-Episode wird auf "done" gesetzt;
    #    - der "splitStack" der Elter-Episode wird nach Keys sortiert, der niedrigste Key (->Zeitstempel) wird
    #      ausgewählt;
    #    - dieser niedrigste Key (frühester ->Zeitstempel) wird für die Datumsanpassung genutzt:
    #        parent_episode["endDate"] = earliest_timestamp - 1day
    #        child_episode["startDate"] = earliest_timestamp
    #       zudem wird, falls vorhanden, der "flag"-Eintrag "eHO" für die Elter-Episoe entfernt:
    #        remove_flag(parent_episode, "eHO")
    #       und, falls vorhanden, wird der "flag"-Eintrag "sHO" für die Kind-Episoe entfernt:
    #        remove_flag(parent_episode, "sHO")
    #       falls hierbei auffällt, dass der Zeitstempel nicht innerhalb der Episode liegt, wird der Eintrag des
    #       Split-Stacks entfernt und der nächste niedrigste Zeitstempel wird gesucht;
    #         ** Prüfung, ob ein Split-Zeitstempel innerhalb der Episode liegt **
    #         parent_episode["startDate"] < timestamp_split <=  parent_episode["endDate"
    #    - falls kein Zeitstempel gefunden werden konnte, wird die Episode normal beendet, es wird kein
    #      ->Split-Stack erstellt; es findet kein Split statt;
    #
    #    - falls ein niedrigster Zeitstempel gefunden werden konnte, der innerhalb der Episode liegt:
    #      - die gesamte Elter-Episode wird kopiert, die Kopie bekommt eine neue ID:
    #          child_episode["id"] = max([Liste aller Episoden-IDs aus dem JSON-Array]) +1;
    #      - die Elter-Episode bekommt ein property:
    #          parent_episode["child"] = [child_episode["id"]]
    #        falls das property schon existiert, wird die Liste ergänzt:
    #          parent_episode["child"].append(child_episode["id"])
    #      - die generierte ->Kind-Episode erhält ein property "parent":
    #         child_episode["parent"] = parent_episode["id"]
    #
    #      - der Value des gefundenen, niedrigsten Eintrags im "splitStack" (Liste von ->Split-Typen, z.B.:
    #            ["SplitTypA", "SplitTypB"]
    #          wird ins Property "currentSplit" der ->Kind-Episode kopiert;
    #      - der Eintrag mit dem zuvor gefunden niedrigstens Zeitstempel wird daraufhin aus dem Split-Stack der Kind-
    #        Episode entfernt:
    #         child_episode["splitStack"].pop(**timestamp_used_for_split**)
    #      - der "stackSplit" der Elter-Episode wird entfernt:
    #          parent_episode.pop("splitStack")
    #      - die Property "currentSplit" der Elter-Episode wird entfernt:
    #          parent_episode.pop("currentSplit")
    #      - (die genutzten Split-Variablen und Zeitstempel wurden bereits beim Erstellen des Split-Stacks entfernt;)
    #      - die generierte Episode wird ans JSON-Array angehängt:
    #          JSON_ARRAY.append(child_episode)
    #
    # - Kind-Episode:
    #    - nach erfolgtem Split und kompletter Bearbeitung der Elter-Episode (siehe oben) ist die Kind-Episode
    #      die einzige im JSON-Array, die die Properties "splitStack" und "currentSplit" enthält;
    #    - sie besitzt zudem noch keine -> Split-Variablen oder Zeitstempel-Variablen;
    #
    #  Navigation
    #    - in die Kind-Episode wird navigiert, indem über das Property "child" der noch aktiven Elter-Episode
    #      der Index der Kind-Episode bestimmt wird:
    #        child_episode_index = find_index_of_id(json_array=JSON_ARRAY, id=parent_episode["child"])
    #      (alternativ kann unmittelbar nach Hinzufügen der child_episode zum JSON-Array auch die Länge des Arrays
    #      bestimmt werden und der Wert um 1 verringert werden:
    #        child_episode_index = len(JSON_ARRAY) -1
    #    - falls kein Property "child" gefunden werden kann, wird die Episode normal beendet;
    #    - innerhalb des Moduls, für das ->Split-Typen definiert wurden,


def split(json_array: List[Dict[str, Dict[str, Any]]],
          initial_episode_index: int,
          split_types: Dict[str, Dict[str, Union[List[Dict[str, str]], str]]],
          max_iteration: int = 0):
    """

    :param json_array:
    :param initial_episode_index:
    :param split_types:
    :param max_iteration:
    :return:
    """
    json_array = json_array.copy()
    split_counter = 0
    current_episode_index = initial_episode_index

    while True:
        json_array = create_split_stack_json_array(split_types=split_types,
                                                   json_array=json_array,
                                                   current_episode_index=current_episode_index).copy()

        json_array, current_episode_index = split_episode(json_array=json_array,
                                                          current_episode_index=current_episode_index)

        json_array = json_array.copy()

        split_counter += 1
        # exit the loop if max_iteration is reached or if the split has ended by itself
        if (0 < max_iteration <= split_counter) or current_episode_index == -1:
            break

    return json_array, current_episode_index


def main():
    pass


if __name__ == '__main__':
    main()
