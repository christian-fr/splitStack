from typing import List, Union, Tuple, Dict, Any
import datetime
import pprint


def get_episode(json_array: List[dict], index: Union[int, str]) -> dict:
    json_array = json_array.copy()
    if int(index) < 0 or int(index) > len(json_array) - 1:
        return {}
    return json_array[int(index)]


def get_json_property(episode: dict, json_property: str) -> Union[dict, list, str, None]:
    if json_property in episode.keys():
        return episode[json_property]
    else:
        return None


def max_id_in_json_array(json_array: List[Dict[str, Any]]) -> int:
    id_list = []
    for episode in json_array:
        if 'id' in episode.keys():
            id_list.append(int(episode['id']))
    return max(id_list)


def remove_property(episode: dict, json_property: str) -> dict:
    if json_property in episode.keys():
        episode.pop(json_property)
    return episode


def add_or_replace_json_property(episode: dict, json_property: str, value: str) -> dict:
    episode[json_property] = value
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


def end_of_current_month(ts: datetime) -> datetime:
    return add_timedelta(ts, months=1, days=-1)


def end_of_previous_month(ts: datetime) -> datetime:
    return add_timedelta(ts, months=0, days=-1)


def to_zofar_ts_str(timestamp_str: datetime) -> str:
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


def add_type_to_split_stack(split_stack_dict: dict, timestamp: str, split_type: str) -> Dict[str, List[str]]:
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
    if key not in input_dict:
        return False
    if input_dict[key] != value:
        return False
    return True


def create_split_stack_json_array(json_array: List[Dict[str, Any]],
                                  current_episode_index: int,
                                  split_types: dict) -> List[Dict[str, Any]]:
    json_array = json_array.copy()
    json_array[current_episode_index] = create_split_stack(split_types=split_types,
                                                           current_episode_dict=json_array[current_episode_index])
    return json_array


def create_split_stack(split_types: Dict[str, Dict[str, List[Dict[str, str]]]],
                       current_episode_dict: Dict[str, Any]) -> Dict[str, Any]:
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
    results = set()
    for index, episode in enumerate(json_array):
        if property_key in episode.keys():
            results.add(index)
    return list(results)


def clean_other_episodes_of_property(json_array: List[Dict[str, Any]],
                                     property_key: str,
                                     current_episode_index: int) -> List[Dict[str, Any]]:
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
    list_of_timestamps = list(split_stack.keys())
    list_of_timestamps.sort()
    return list_of_timestamps[0], split_stack[list_of_timestamps[0]]


def split_episode(json_array: List[Dict[str, Any]], current_episode_index: int) -> Tuple[List[Dict[str, Any]], int]:
    # delete all other "splitStack" properties from other episodes
    json_array = json_array.copy()
    json_array = clean_other_episodes_of_property(json_array, 'splitStack', current_episode_index)

    current_episode = json_array[current_episode_index].copy()

    if 'splitStack' not in current_episode.keys():
        return json_array, -1

    current_episode['state'] = 'done'

    split_timestamp = None
    split_data = None

    flag_timestamp_valid = False
    while len(current_episode['splitStack']) > 0 and not flag_timestamp_valid:
        split_timestamp, split_data = lowest_split_stack_entry(current_episode['splitStack'])
        if not valid_timestamp(split_timestamp) or not timestamp_within_episode(episode=current_episode,
                                                                                ts_str=split_timestamp):
            current_episode['splitStack'] = remove_property(current_episode['splitStack'], split_timestamp)
            split_timestamp = None
            split_data = None
        else:
            flag_timestamp_valid = True

    if split_timestamp is None or split_data is None:
        # in case of error:
        # cleanup episode and finish without split
        current_episode = remove_property(current_episode, 'splitStack')
        current_episode = remove_property(current_episode, 'currentSplit')
        json_array[current_episode_index] = current_episode.copy()
        return json_array, -1

    # create child episode, modify parent
    parent_episode = current_episode.copy()
    child_episode = current_episode.copy()

    parent_episode['endDate'] = to_zofar_ts_str(end_of_previous_month(as_datetime_timestamp(split_timestamp)))
    parent_episode = remove_property(parent_episode, 'splitStack')
    parent_episode = remove_property(parent_episode, 'currentSplit')

    child_episode['startDate'] = split_timestamp
    child_episode['currentSplit'] = split_data
    if split_timestamp in child_episode['splitStack']:
        child_episode['splitStack'].pop(split_timestamp)
    if child_episode['splitStack'] == {}:
        remove_property(child_episode, 'splitStack')
    child_episode['id'] = str(max_id_in_json_array(json_array) + 1)
    child_episode['parent'] = parent_episode['id']
    if 'children' not in parent_episode.keys():
        parent_episode['children'] = [child_episode['id']]
    else:
        if isinstance(parent_episode['children'], list):
            parent_episode['children'].append(child_episode['id'])
        else:
            parent_episode['children'] = [child_episode['id']]

    json_array[current_episode_index] = parent_episode
    json_array.append(child_episode)

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
